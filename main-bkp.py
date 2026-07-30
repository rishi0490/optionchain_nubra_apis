# main.py

import time
from datetime import datetime

from login import login
from option_chain import fetch_option_chain
from excel_writer import save_excel
from config import UPDATE_INTERVAL


def main():

    print("=" * 80)
    print("                 NIFTY OPTION CHAIN LIVE MONITOR")
    print("=" * 80)

    # Login only once
    client = login()

    while True:

        try:

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("\n" + "=" * 80)
            print(f"🕒 Fetch Time : {current_time}")
            print("=" * 80)

            print("📡 Fetching latest option chain...")

            option_chain = fetch_option_chain(client)

            # Save Excel and generate signals
            overall_signal, signal_df = save_excel(option_chain)

            # SDK object -> dict
            if hasattr(option_chain, "model_dump"):
                data = option_chain.model_dump()
            else:
                data = option_chain.dict()

            chain = data["chain"]

            underlying = chain["current_price"] / 100
            atm = chain["at_the_money_strike"] / 100
            expiry = chain["expiry"]

            # --------------------------------------------------
            # OVERALL OI SUMMARY
            # --------------------------------------------------

            total_call_change = signal_df["Call Change OI"].sum()
            total_put_change = signal_df["Put Change OI"].sum()

            difference = total_put_change - total_call_change

            if total_call_change != 0:
                oi_ratio = total_put_change / abs(total_call_change)
            else:
                oi_ratio = 0

            if difference > 0:
                oi_bias = "🟢 BULLISH"

            elif difference < 0:
                oi_bias = "🔴 BEARISH"

            else:
                oi_bias = "🟡 NEUTRAL"

            # --------------------------------------------------
            # HEADER
            # --------------------------------------------------

            print(f"\n📈 NIFTY LTP      : {underlying:.2f}")
            print(f"🎯 ATM Strike     : {atm:.0f}")
            print(f"📅 Expiry         : {expiry}")
            print(f"📊 Signal Logic   : {overall_signal}")

            # --------------------------------------------------
            # OI SUMMARY
            # --------------------------------------------------

            print("\n" + "=" * 80)
            print("📊 OVERALL OI SUMMARY (ATM ±8 STRIKES)")
            print("=" * 80)

            print(f"Total Call Change OI : {total_call_change:,.0f}")
            print(f"Total Put Change OI  : {total_put_change:,.0f}")
            print(f"Difference (P-C)     : {difference:,.0f}")
            print(f"OI Ratio             : {oi_ratio:.2f}")
            print(f"Overall OI Bias      : {oi_bias}")

            print("=" * 80)

            # --------------------------------------------------
            # SIGNAL TABLE
            # --------------------------------------------------

            print("\n📋 ATM ±8 STRIKE SIGNALS")
            print("-" * 80)

            print(signal_df.to_string(index=False))

            print("-" * 80)

            print("\n✅ Option Chain Excel Updated")
            print("✅ Signal Excel Updated")

        except KeyboardInterrupt:

            print("\nProgram stopped by user.")
            break

        except Exception as e:

            print(f"\n❌ ERROR : {e}")

        # --------------------------------------------------
        # COUNTDOWN
        # --------------------------------------------------

        print("\nWaiting for next refresh...")

        for remaining in range(UPDATE_INTERVAL, 0, -1):

            print(
                f"\r⏳ Next refresh in {remaining:02d} seconds...",
                end="",
                flush=True
            )

            time.sleep(1)

        print("\n")


if __name__ == "__main__":
    main()
