import pandas as pd
from config import SIGNAL_FILE


def generate_signal(df):

    signals = []

    bullish = 0
    bearish = 0
    rangebound = 0
    shortcover = 0

    for _, row in df.iterrows():

        call_change = row["Call Change OI"]
        put_change = row["Put Change OI"]

        if call_change > 0 and put_change < 0:
            signal = "🔴 Bearish"
            bearish += 1

        elif call_change < 0 and put_change > 0:
            signal = "🟢 Bullish"
            bullish += 1

        elif call_change > 0 and put_change > 0:
            signal = "🟡 Range Bound"
            rangebound += 1

        else:
            signal = "🔵 Short Covering"
            shortcover += 1

        signals.append({
            "Strike": row["Strike"],
            "Call Change OI": call_change,
            "Put Change OI": put_change,
            "Signal": signal
        })

    signal_df = pd.DataFrame(signals)

    with pd.ExcelWriter(SIGNAL_FILE, engine="openpyxl") as writer:
        signal_df.to_excel(writer, sheet_name="Signals", index=False)

    # Overall market signal
    if bullish > bearish:
        overall = "🟢 BULLISH"

    elif bearish > bullish:
        overall = "🔴 BEARISH"

    else:
        overall = "🟡 NEUTRAL"

    return overall, signal_df
