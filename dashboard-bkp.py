import os
from datetime import datetime

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NIFTY LIVE OPTION CHAIN",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# AUTO REFRESH
# ============================================================

refresh_count = st_autorefresh(
    interval=60000,
    key="refresh"
)

# ============================================================
# FILE PATHS
# ============================================================

OPTION_FILE = "output/NIFTY_OPTION_CHAIN.xlsx"
SIGNAL_FILE = "output/NIFTY_SIGNAL.xlsx"

# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(OPTION_FILE):
    st.error("Option Chain Excel not found.")
    st.stop()

if not os.path.exists(SIGNAL_FILE):
    st.error("Signal Excel not found.")
    st.stop()

# ============================================================
# READ DATA
# ============================================================

option_df = pd.read_excel(OPTION_FILE)
signal_df = pd.read_excel(SIGNAL_FILE)

# ============================================================
# HEADER
# ============================================================

st.title("📈 NIFTY OPTION CHAIN LIVE DASHBOARD")

c1, c2 = st.columns(2)

with c1:
    st.success(
        f"Last Updated : {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
    )

with c2:
    st.info(
        f"Auto Refresh Count : {refresh_count}"
    )

st.divider()

# ============================================================
# SIGNAL COUNTS
# ============================================================

bullish = len(
    signal_df[
        signal_df["Signal"].str.contains("Bullish", na=False)
    ]
)

bearish = len(
    signal_df[
        signal_df["Signal"].str.contains("Bearish", na=False)
    ]
)

range_bound = len(
    signal_df[
        signal_df["Signal"].str.contains("Range", na=False)
    ]
)

short_cover = len(
    signal_df[
        signal_df["Signal"].str.contains("Short", na=False)
    ]
)

# ============================================================
# OI SUMMARY
# ============================================================

total_call = signal_df["Call Change OI"].sum()

total_put = signal_df["Put Change OI"].sum()

difference = total_put - total_call

ratio = (
    total_put / abs(total_call)
    if total_call != 0
    else 0
)

if difference > 0:
    overall_bias = "🟢 BULLISH"

elif difference < 0:
    overall_bias = "🔴 BEARISH"

else:
    overall_bias = "🟡 NEUTRAL"

# ============================================================
# ATM
# ============================================================

atm_row = option_df[
    option_df["ATM"] == "YES"
]

if len(atm_row):

    atm_strike = atm_row.iloc[0]["Strike"]

else:

    atm_strike = "NA"

# ============================================================
# METRICS
# ============================================================

st.subheader("📊 LIVE OI SUMMARY")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Total Call Change OI",
    f"{total_call:,.0f}"
)

m2.metric(
    "Total Put Change OI",
    f"{total_put:,.0f}"
)

m3.metric(
    "Difference",
    f"{difference:,.0f}"
)

m4.metric(
    "OI Ratio",
    f"{ratio:.2f}"
)

st.divider()

# ============================================================
# SIGNAL SUMMARY
# ============================================================

st.subheader("📈 MARKET SUMMARY")

a1, a2, a3, a4, a5 = st.columns(5)

a1.metric(
    "Bullish",
    bullish
)

a2.metric(
    "Bearish",
    bearish
)

a3.metric(
    "Range Bound",
    range_bound
)

a4.metric(
    "Short Cover",
    short_cover
)

a5.metric(
    "ATM Strike",
    atm_strike
)

st.divider()

# ============================================================
# OVERALL BIAS
# ============================================================

if "BULLISH" in overall_bias:

    st.success(
        f"Overall Market Bias : {overall_bias}"
    )

elif "BEARISH" in overall_bias:

    st.error(
        f"Overall Market Bias : {overall_bias}"
    )

else:

    st.warning(
        f"Overall Market Bias : {overall_bias}"
    )

st.divider()

# ============================================================
# TOP CALL / PUT CHANGE OI
# ============================================================

st.subheader("🔥 Top OI Build-up")

left, right = st.columns(2)

with left:

    st.markdown("### 📈 Top 5 Call Change OI")

    top_call = option_df.sort_values(
        "Call Change OI",
        ascending=False
    )[["Strike", "Call Change OI"]].head(5)

    st.dataframe(
        top_call,
        use_container_width=True,
        hide_index=True
    )

with right:

    st.markdown("### 📉 Top 5 Put Change OI")

    top_put = option_df.sort_values(
        "Put Change OI",
        ascending=False
    )[["Strike", "Put Change OI"]].head(5)

    st.dataframe(
        top_put,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ============================================================
# OPTION CHAIN
# ============================================================

st.subheader("📋 ATM ±8 Option Chain")

def highlight_atm(row):

    if row["ATM"] == "YES":
        return [
            "background-color:#ffe066;font-weight:bold"
        ] * len(row)

    return [""] * len(row)

styled_option = option_df.style.apply(
    highlight_atm,
    axis=1
)

st.dataframe(
    styled_option,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# SIGNAL TABLE
# ============================================================

st.subheader("📊 Strike Wise Signals")

def signal_color(row):

    signal = row["Signal"]

    if "Bullish" in signal:

        return [
            "background-color:#d4edda"
        ] * len(row)

    elif "Bearish" in signal:

        return [
            "background-color:#f8d7da"
        ] * len(row)

    elif "Range" in signal:

        return [
            "background-color:#fff3cd"
        ] * len(row)

    else:

        return [
            "background-color:#d1ecf1"
        ] * len(row)

styled_signal = signal_df.style.apply(
    signal_color,
    axis=1
)

st.dataframe(
    styled_signal,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================================
# BAR CHART
# ============================================================

import plotly.express as px

st.subheader("📈 Call vs Put Change OI")

bar_fig = px.bar(

    option_df,

    x="Strike",

    y=[
        "Call Change OI",
        "Put Change OI"
    ],

    barmode="group",

    title="Call vs Put Change OI"
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

st.divider()

# ============================================================
# PIE CHART
# ============================================================

st.subheader("📊 Signal Distribution")

pie_df = pd.DataFrame({

    "Signal": [

        "Bullish",

        "Bearish",

        "Range",

        "Short Cover"

    ],

    "Count": [

        bullish,

        bearish,

        range_bound,

        short_cover

    ]

})

pie = px.pie(

    pie_df,

    names="Signal",

    values="Count",

    hole=0.45

)

st.plotly_chart(

    pie,

    use_container_width=True

)

st.divider()

# ============================================================
# FOOTER
# ============================================================

st.success(
    "Dashboard refreshes automatically every 60 seconds."
    )
