import pandas as pd

from config import EXCEL_FILE
from signal_generator import generate_signal


def save_excel(option_chain):

    if hasattr(option_chain, "model_dump"):
        data = option_chain.model_dump()
    else:
        data = option_chain.dict()

    chain = data["chain"]

    ce = chain["ce"]
    pe = chain["pe"]

    atm = chain["at_the_money_strike"]

    STRIKE_INTERVAL = 5000      # 50 points × 100
    STRIKES_AROUND = 8

    lower = atm - (STRIKE_INTERVAL * STRIKES_AROUND)
    upper = atm + (STRIKE_INTERVAL * STRIKES_AROUND)

    rows = []

    for ce_row, pe_row in zip(ce, pe):

        strike = ce_row["strike_price"]

        if lower <= strike <= upper:

            ce_oi = ce_row.get("open_interest") or 0
            ce_prev = ce_row.get("previous_open_interest") or 0

            pe_oi = pe_row.get("open_interest") or 0
            pe_prev = pe_row.get("previous_open_interest") or 0

            rows.append({
                "Strike": strike / 100,
                "Call Change OI": ce_oi - ce_prev,
                "Put Change OI": pe_oi - pe_prev,
                "Call OI": ce_oi,
                "Put OI": pe_oi,
                "ATM": "YES" if strike == atm else ""
            })

    df = pd.DataFrame(rows)

    # Save Option Chain Excel
    df.to_excel(
        EXCEL_FILE,
        index=False
    )

    # Generate Signal Excel
    overall_signal, signal_df = generate_signal(df)

    print("✅ Option Chain Updated")

    return overall_signal, signal_df
