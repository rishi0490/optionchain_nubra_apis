import os
from datetime import datetime

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="NIFTY LIVE OPTION CHAIN",
    page_icon="📈",
    layout="wide"
)

# ==========================================================
# AUTO REFRESH
# ==========================================================

st_autorefresh(
    interval=60000,
    key="refresh"
)

# ==========================================================
# FILES
# ==========================================================

OPTION_FILE = "output/NIFTY_OPTION_CHAIN.xlsx"
SIGNAL_FILE = "output/NIFTY_SIGNAL.xlsx"
HISTORY_FILE = "output/oi_history.csv"

# ==========================================================
# CHECK FILES
# ==========================================================

if not os.path.exists(OPTION_FILE):
    st.error("Option Chain file not found.")
    st.stop()

if not os.path.exists(SIGNAL_FILE):
    st.error("Signal file not found.")
    st.stop()

# ==========================================================
# LOAD DATA
# ==========================================================

option_df = pd.read_excel(OPTION_FILE)

signal_df = pd.read_excel(SIGNAL_FILE)

history_df = pd.DataFrame()

if os.path.exists(HISTORY_FILE):

    history_df = pd.read_csv(HISTORY_FILE)

# ==========================================================
# HEADER
# ==========================================================

st.title("📈 NIFTY OPTION CHAIN LIVE DASHBOARD")

c1, c2 = st.columns(2)

with c1:

    st.success(
        f"Last Updated : {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
    )

with c2:

    st.info("Refresh Every : 60 Seconds")

st.divider()

# ==========================================================
# SIGNAL COUNTS
# ==========================================================

bullish = len(
    signal_df[
        signal_df["Signal"].str.contains(
            "Bullish",
            na=False
        )
    ]
)

bearish = len(
    signal_df[
        signal_df["Signal"].str.contains(
            "Bearish",
            na=False
        )
    ]
)

range_bound = len(
    signal_df[
        signal_df["Signal"].str.contains(
            "Range",
            na=False
        )
    ]
)

short_cover = len(
    signal_df[
        signal_df["Signal"].str.contains(
            "Short",
            na=False
        )
    ]
)

# ==========================================================
# ATM
# ==========================================================

atm_row = option_df[
    option_df["ATM"] == "YES"
]

if len(atm_row):

    atm = atm_row.iloc[0]["Strike"]

else:

    atm = "NA"

# ==========================================================
# OI SUMMARY
# ==========================================================

total_call = signal_df["Call Change OI"].sum()

total_put = signal_df["Put Change OI"].sum()

difference = total_put - total_call

ratio = (
    total_put / abs(total_call)
    if total_call != 0
    else 0
)

if difference > 0:

    bias = "🟢 BULLISH"

elif difference < 0:

    bias = "🔴 BEARISH"

else:

    bias = "🟡 NEUTRAL"

# ==========================================================
# OI SUMMARY METRICS
# ==========================================================

st.subheader("📊 Overall OI Summary")

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    "Call Change OI",
    f"{total_call:,.0f}"
)

m2.metric(
    "Put Change OI",
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

m5.metric(
    "Bias",
    bias
)

st.divider()

# ==========================================================
# MARKET SUMMARY
# ==========================================================

st.subheader("📈 Market Summary")

s1, s2, s3, s4, s5 = st.columns(5)

s1.metric(
    "Bullish",
    bullish
)

s2.metric(
    "Bearish",
    bearish
)

s3.metric(
    "Range",
    range_bound
)

s4.metric(
    "Short Cover",
    short_cover
)

s5.metric(
    "ATM",
    atm
)

st.divider()

# ==========================================================
# LAST 10 OI DIFFERENCE
# ==========================================================

st.subheader("📜 Last 10 OI Difference History")

if len(history_df):

    display = history_df.iloc[::-1]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "History file not created yet."
    )

st.divider()

# ==========================================================
# OVERALL MARKET BIAS
# ==========================================================

if "BULLISH" in bias:

    st.success(
        f"Overall Market Bias : {bias}"
    )

elif "BEARISH" in bias:

    st.error(
        f"Overall Market Bias : {bias}"
    )

else:

    st.warning(
        f"Overall Market Bias : {bias}"
    )

st.divider()

# ==========================================================
# SUPPORT / RESISTANCE
# ==========================================================

st.subheader("🛡️ Support & Resistance")

top_put = option_df.nlargest(2, "Put Change OI")
top_call = option_df.nlargest(2, "Call Change OI")

c1, c2 = st.columns(2)

with c1:

    st.success("Support (Highest Put Change OI)")

    st.table(
        top_put[
            [
                "Strike",
                "Put Change OI"
            ]
        ]
    )

with c2:

    st.error("Resistance (Highest Call Change OI)")

    st.table(
        top_call[
            [
                "Strike",
                "Call Change OI"
            ]
        ]
    )

st.divider()

# ==========================================================
# TOP 5 CALL / PUT CHANGE OI
# ==========================================================

st.subheader("🔥 Top OI Build-up")

left, right = st.columns(2)

with left:

    st.markdown("### 📈 Top 5 Call Change OI")

    st.dataframe(

        option_df
        .sort_values(
            "Call Change OI",
            ascending=False
        )
        [
            [
                "Strike",
                "Call Change OI"
            ]
        ]
        .head(5),

        use_container_width=True,
        hide_index=True
    )

with right:

    st.markdown("### 📉 Top 5 Put Change OI")

    st.dataframe(

        option_df
        .sort_values(
            "Put Change OI",
            ascending=False
        )
        [
            [
                "Strike",
                "Put Change OI"
            ]
        ]
        .head(5),

        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================================
# OPTION CHAIN STYLE
# ==========================================================

st.subheader("📋 ATM ±8 Option Chain")


def highlight_option_chain(row):

    styles = [""] * len(row)

    if row["ATM"] == "YES":

        styles = [
            "background-color:#ffe599;font-weight:bold"
        ] * len(row)

    return styles


styled_option = option_df.style.apply(
    highlight_option_chain,
    axis=1
)

st.dataframe(

    styled_option,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# SIGNAL TABLE
# ==========================================================

st.subheader("📊 Strike Wise Signals")


def signal_style(row):

    signal = str(row["Signal"])

    if "Bullish" in signal:

        return [
            "background-color:#d9ead3"
        ] * len(row)

    elif "Bearish" in signal:

        return [
            "background-color:#f4cccc"
        ] * len(row)

    elif "Range" in signal:

        return [
            "background-color:#fff2cc"
        ] * len(row)

    elif "Short" in signal:

        return [
            "background-color:#cfe2f3"
        ] * len(row)

    return [""] * len(row)


styled_signal = signal_df.style.apply(
    signal_style,
    axis=1
)

st.dataframe(

    styled_signal,

    use_container_width=True,

    hide_index=True

)

st.divider()


# ==========================================================
# IMPORT
# ==========================================================

import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# CALL VS PUT CHANGE OI
# ==========================================================

st.subheader("📊 Call vs Put Change OI")

fig = px.bar(

    option_df,

    x="Strike",

    y=[
        "Call Change OI",
        "Put Change OI"
    ],

    barmode="group",

    title="Call Change OI vs Put Change OI"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# DIFFERENCE HISTORY
# ==========================================================

st.subheader("📈 Difference (P-C) Trend")

if len(history_df):

    fig = px.line(

        history_df,

        x="Time",

        y="Difference",

        markers=True,

        title="Last 10 Difference (P-C)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

else:

    st.warning("No history available.")

st.divider()

# ==========================================================
# PIE CHART
# ==========================================================

st.subheader("🥧 Signal Distribution")

pie_df = pd.DataFrame({

    "Signal":[

        "Bullish",

        "Bearish",

        "Range",

        "Short Cover"

    ],

    "Count":[

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

    hole=.45

)

st.plotly_chart(

    pie,

    use_container_width=True

)

st.divider()

# ==========================================================
# GAUGE
# ==========================================================

st.subheader("🎯 Overall Market Strength")

gauge_value = 50

if "BULLISH" in bias:

    gauge_value = 80

elif "BEARISH" in bias:

    gauge_value = 20

else:

    gauge_value = 50

gauge = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=gauge_value,

        title={

            "text":"Market Strength"

        },

        gauge={

            "axis":{

                "range":[0,100]

            },

            "steps":[

                {

                    "range":[0,35],

                    "color":"red"

                },

                {

                    "range":[35,65],

                    "color":"yellow"

                },

                {

                    "range":[65,100],

                    "color":"green"

                }

            ]

        }

    )

)

st.plotly_chart(

    gauge,

    use_container_width=True

)

st.divider()

# ==========================================================
# CALL VS PUT COMPARISON
# ==========================================================

st.subheader("📊 Total OI Comparison")

compare = pd.DataFrame({

    "Type":[

        "Call",

        "Put"

    ],

    "OI":[

        total_call,

        total_put

    ]

})

fig = px.bar(

    compare,

    x="Type",

    y="OI",

    text="OI",

    title="Overall Call vs Put Change OI"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ==========================================================
# LIVE MARKET COMMENTARY
# ==========================================================

st.subheader("📢 Live Commentary")

if difference > 0:

    st.success(f"""
### 🟢 Market Observation

• Put writers are stronger than Call writers.

• Difference (P-C) = **{difference:,.0f}**

• OI Ratio = **{ratio:.2f}**

• Overall Bias = **Bullish**

• ATM = **{atm}**
""")

elif difference < 0:

    st.error(f"""
### 🔴 Market Observation

• Call writers are stronger than Put writers.

• Difference (P-C) = **{difference:,.0f}**

• OI Ratio = **{ratio:.2f}**

• Overall Bias = **Bearish**

• ATM = **{atm}**
""")

else:

    st.warning("""
### 🟡 Market Observation

No clear directional bias.

Market is balanced.
""")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    f"""
Last Dashboard Refresh :
{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}

Dashboard refreshes automatically every 60 seconds.
"""
)
