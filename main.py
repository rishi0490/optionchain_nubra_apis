# ============================================================
# main.py
# ============================================================

import os
import time
from datetime import datetime

import pandas as pd

from login import login
from option_chain import fetch_option_chain
from excel_writer import save_excel
from config import UPDATE_INTERVAL


def main():

    print("=" * 80)
    print("            NIFTY OPTION CHAIN LIVE MONITOR")
    print("=" * 80)

    # --------------------------------------------------------
    # Login only once
    # --------------------------------------------------------

    client = login()

    print("✅ Login successful.")

    while True:

        try:

            print("\n")
            print("=" * 80)

            current_time = datetime.now()

            print(
                f"🕒 Fetch Time : "
                f"{current_time.strftime('%d-%b-%Y %H:%M:%S')}"
            )

            print("=" * 80)

            print("📡 Fetching latest option chain...")

            # ------------------------------------------------
            # Fetch Option Chain
            # ------------------------------------------------

            option_chain = fetch_option_chain(client)

            # ------------------------------------------------
            # Save Excel
            # ------------------------------------------------

            overall_signal, signal_df = save_excel(option_chain)

            # ------------------------------------------------
            # Convert SDK Object
            # ------------------------------------------------

            if hasattr(option_chain, "model_dump"):

                data = option_chain.model_dump()

            else:

                data = option_chain.dict()

            chain = data["chain"]

            underlying = chain["current_price"] / 100

            atm = chain["at_the_money_strike"] / 100

            expiry = chain["expiry"]

            # ------------------------------------------------
            # OI SUMMARY
            # ------------------------------------------------

            total_call_change = signal_df[
                "Call Change OI"
            ].sum()

            total_put_change = signal_df[
                "Put Change OI"
            ].sum()

            difference = (
                total_put_change -
                total_call_change
            )

            if total_call_change != 0:

                oi_ratio = (
                    total_put_change /
                    abs(total_call_change)
                )

            else:

                oi_ratio = 0

            if difference > 0:

                oi_bias = "🟢 BULLISH"

            elif difference < 0:

                oi_bias = "🔴 BEARISH"

            else:

                oi_bias = "🟡 NEUTRAL"

            # ------------------------------------------------
            # TERMINAL OUTPUT
            # ------------------------------------------------

            print()

            print(f"📈 NIFTY LTP      : {underlying:.2f}")

            print(f"🎯 ATM Strike     : {atm:.0f}")

            print(f"📅 Expiry         : {expiry}")

            print()

            print("=" * 80)

            print("📊 OVERALL OI SUMMARY")

            print("=" * 80)

            print(
                f"Total Call Change OI : "
                f"{total_call_change:,.0f}"
            )

            print(
                f"Total Put Change OI  : "
                f"{total_put_change:,.0f}"
            )

            print(
                f"Difference (P-C)     : "
                f"{difference:,.0f}"
            )

            print(
                f"OI Ratio             : "
                f"{oi_ratio:.2f}"
            )

            print(
                f"Overall OI Bias      : "
                f"{oi_bias}"
            )

            print(
                f"Signal Generator     : "
                f"{overall_signal}"
            )

            print("=" * 80)


                        # ------------------------------------------------
            # SAVE LAST 10 OI HISTORY
            # ------------------------------------------------

            history_file = "output/oi_history.csv"

            history_row = pd.DataFrame([{
                "Time": current_time.strftime("%H:%M:%S"),
                "Difference": difference,
                "Call Change OI": total_call_change,
                "Put Change OI": total_put_change,
                "OI Ratio": round(oi_ratio, 2),
                "Bias": oi_bias
            }])

            if os.path.exists(history_file):

                history = pd.read_csv(history_file)

                history = pd.concat(
                    [history, history_row],
                    ignore_index=True
                )

            else:

                history = history_row

            # Keep only the latest 10 records
            history = history.tail(10)

            history.to_csv(
                history_file,
                index=False
            )

            # ------------------------------------------------
            # PRINT LAST 10 HISTORY
            # ------------------------------------------------

            print()
            print("=" * 80)
            print("📈 LAST 10 OI DIFFERENCE READINGS")
            print("=" * 80)

            print(
                history[
                    [
                        "Time",
                        "Difference",
                        "OI Ratio",
                        "Bias"
                    ]
                ].to_string(index=False)
            )

            # ------------------------------------------------
            # PRINT STRIKE SIGNALS
            # ------------------------------------------------

            print()
            print("=" * 80)
            print("📋 ATM ±8 STRIKE SIGNALS")
            print("=" * 80)

            print(signal_df.to_string(index=False))

            print()
            print("✅ Excel Updated Successfully")

        except KeyboardInterrupt:

            print("\nProgram stopped by user.")
            break

        except Exception as e:

            print(f"\n❌ ERROR : {e}")

        # ------------------------------------------------
        # COUNTDOWN
        # ------------------------------------------------

        print()

        for remaining in range(
            UPDATE_INTERVAL,
            0,
            -1
        ):

            print(
                f"\r⏳ Next Refresh In : {remaining:02d} sec",
                end="",
                flush=True
            )

            time.sleep(1)

        print("\n")


if __name__ == "__main__":
    main()
