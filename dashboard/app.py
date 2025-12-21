import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
from report_data import DataLoader

# --- Page Config ---
st.set_page_config(
    page_title="Revenue Ops Risk Report",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS STYLING ---
st.markdown(
    """
    <style>
        /* 1. FORCE Main App Background to Light Grey */
        .stApp {
            background-color: #f5f7f9;
        }

        /* 2. KPI CARD STYLING */
        .kpi-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #e0e0e0;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 120px;
            width: 100%;
            margin-bottom: 10px;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 4px;
        }
        .kpi-label {
            font-size: 0.8rem;
            font-weight: 600;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* 3. CHART CARD STYLING */
        /* Targets the st.container(border=True) */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 1px solid #eaeaea !important;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Force inner container elements to be white */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #ffffff !important;
        }

        /* 4. TYPOGRAPHY */
        h4 {
            margin-top: 0px !important;
            padding-top: 0px !important;
            font-size: 1.1rem;
            font-weight: 700;
            color: #34495e;
            margin-bottom: 15px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Path Setup ---
ROOT = Path(__file__).resolve().parent.parent
QUERIES = ROOT / "models" / "queries"


# --- Load Filter Options ---
@st.cache_data
def load_years():
    df = DataLoader(QUERIES / "year_options.sql").get_data()
    if not df.empty:
        return df["report_year"].tolist()
    return [2019, 2018, 2017]


years_list = load_years()

# --- Sidebar ---
st.sidebar.title("Report Settings")
selected_year = st.sidebar.selectbox("Select Fiscal Year", years_list, index=0)


# --- Data Loading ---
@st.cache_data(show_spinner=False)
def load_dashboard_data(year):
    daily = DataLoader(QUERIES / "daily_metrics.sql").get_data(year=year)
    hourly = DataLoader(QUERIES / "hourly_stats.sql").get_data(year=year)
    demos = DataLoader(QUERIES / "demographic_stats.sql").get_data(year=year)
    cats = DataLoader(QUERIES / "category_stats.sql").get_data(year=year)

    # Pre-processing
    if not hourly.empty:
        hourly["fraud_rate"] = hourly["fraud_cases"] / hourly["vol"]
    if not demos.empty:
        demos["fraud_rate"] = demos["fraud_cases"] / demos["vol"]
    if not cats.empty:
        cats["fraud_rate"] = cats["fraud_cases"] / cats["vol"]
        cats["fraud_loss"] = cats.get("fraud_loss", 0)

    return daily, hourly, demos, cats


daily_df, hourly_df, demo_df, cat_df = load_dashboard_data(selected_year)

if daily_df.empty:
    st.warning(f"No data found for {selected_year}.")
    st.stop()

# --- HEADER (Centered) ---
st.markdown(
    f"<h1 style='text-align: center;'>Revenue Ops: {selected_year} Strategic Risk Profile</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- KPI ROW (6 Columns) ---
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

vol_val = daily_df["vol"].sum()
vol_str = f"{vol_val / 1e6:.2f}M" if vol_val > 1e6 else f"{vol_val:,.0f}"

rev_val = daily_df["rev"].sum()
rev_str = f"${rev_val / 1e6:.2f}M" if rev_val > 1e6 else f"${rev_val:,.0f}"

avg_ticket = f"${rev_val / vol_val:.2f}"

loss_val = daily_df["fraud_loss"].sum()
loss_str = f"${loss_val / 1e6:.2f}M" if loss_val > 1e6 else f"${loss_val:,.0f}"

fraud_rate = daily_df["fraud_cases"].sum() / vol_val
fraud_rate_str = f"{fraud_rate:.2%}"


def render_kpi(col, value, label):
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )


render_kpi(kpi1, vol_str, "Annual Volume")
render_kpi(kpi2, f"{daily_df['vol'].mean():,.0f}", "Avg Daily Tx")
render_kpi(kpi3, rev_str, "Annual Revenue")
render_kpi(kpi4, avg_ticket, "Avg Ticket")
render_kpi(kpi5, fraud_rate_str, "Fraud Rate")
render_kpi(kpi6, loss_str, "Fraud Loss")

st.markdown("---")


# --- CHART HELPER ---
def render_chart_in_card(title, chart_obj):
    with st.container(border=True):
        st.markdown(f"#### {title}")

        # CHART CONFIGURATION
        final_chart = (
            chart_obj.properties(
                background="#ffffff",
                padding={"left": 20, "top": 20, "right": 50, "bottom": 20},
            )
            .configure_view(strokeWidth=0)
            .configure_axis(
                gridColor="#f0f0f0",
                labelColor="#555",
                titleColor="#555",
                titleFontWeight="bold",
            )
        )

        st.altair_chart(final_chart, width="stretch")


# --- DASHBOARD LAYOUT ---
col_left, col_right = st.columns(2)

with col_left:
    # --- Q1: Vampire Index ---
    base_q1 = alt.Chart(hourly_df).encode(
        x=alt.X("hour_of_day:O", title="Hour of Day"),
        tooltip=[
            "hour_of_day",
            alt.Tooltip("fraud_rate", format=".2%", title="Fraud Rate"),
        ],
    )

    line_q1 = base_q1.mark_line(color="#e74c3c", strokeWidth=3).encode(
        y=alt.Y("fraud_rate:Q", title="Fraud Rate (%)")
    )
    area_q1 = base_q1.mark_area(color="#e74c3c", opacity=0.1).encode(y="fraud_rate:Q")
    points_q1 = base_q1.mark_point(color="#e74c3c", fill="white", size=50).encode(
        y="fraud_rate:Q"
    )

    text_q1 = base_q1.mark_text(dy=-15, color="#c0392b", fontSize=10).encode(
        y="fraud_rate:Q", text=alt.Text("fraud_rate:Q", format=".2%")
    )

    chart_q1 = (line_q1 + area_q1 + points_q1 + text_q1).properties(height=320)
    render_chart_in_card("Q1. Risk Timing (Vampire Index)", chart_q1)

    # --- Q3: Victim Profile ---
    base_q3 = alt.Chart(demo_df).encode(
        x=alt.X(
            "age_group:N",
            sort=["Gen Z (<25)", "Millennial (25-40)", "Gen X (41-60)", "Senior (60+)"],
            title=None,
            axis=alt.Axis(labelAngle=-45),
        ),
        y=alt.Y("fraud_rate:Q", title="Fraud Rate (%)", scale=alt.Scale(padding=0.2)),
        tooltip=[
            "age_group",
            alt.Tooltip("fraud_rate", format=".2%", title="Fraud Rate"),
        ],
    )

    bar_q3 = base_q3.mark_bar(
        color="#3498db", cornerRadiusTopLeft=5, cornerRadiusTopRight=5
    ).encode()

    text_q3 = base_q3.mark_text(dy=-10, color="#2980b9", fontWeight="bold").encode(
        text=alt.Text("fraud_rate:Q", format=".2%")
    )

    chart_q3 = (bar_q3 + text_q3).properties(height=320)
    render_chart_in_card("Q3. Victim Profile (Fraud by Age)", chart_q3)

with col_right:
    # --- Q2: Volume Context ---
    base_q2 = alt.Chart(hourly_df).encode(
        x=alt.X("hour_of_day:O", title="Hour of Day"),
        tooltip=["hour_of_day", alt.Tooltip("vol", format=",", title="Volume")],
    )

    bar_q2 = base_q2.mark_bar(
        color="#95a5a6", opacity=0.6, cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(y=alt.Y("vol:Q", title="Transaction Volume", scale=alt.Scale(padding=0.2)))

    text_q2 = base_q2.mark_text(dy=-10, color="#7f8c8d", fontSize=9).encode(
        y="vol:Q", text=alt.Text("vol:Q", format=".2s")
    )

    chart_q2 = (bar_q2 + text_q2).properties(height=320)
    render_chart_in_card("Q2. Operational Rhythm (Volume)", chart_q2)

    # --- Q4: High Risk Segments ---
    top_risk_cats = cat_df.sort_values("fraud_rate", ascending=False).head(10)

    base_q4 = alt.Chart(top_risk_cats).encode(
        y=alt.Y(
            "merchant_category:N", sort="-x", title=None, axis=alt.Axis(labelLimit=400)
        ),
        x=alt.X("fraud_rate:Q", title="Fraud Rate (%)", scale=alt.Scale(padding=0.2)),
        tooltip=[
            "merchant_category",
            alt.Tooltip("fraud_rate", format=".2%", title="Fraud Rate"),
        ],
    )

    bar_q4 = base_q4.mark_bar(
        color="#e67e22", cornerRadiusBottomRight=3, cornerRadiusTopRight=3
    ).encode()

    text_q4 = base_q4.mark_text(
        dx=5, color="#d35400", align="left", fontWeight="bold"
    ).encode(text=alt.Text("fraud_rate:Q", format=".2%"))

    chart_q4 = (bar_q4 + text_q4).properties(height=320)
    render_chart_in_card("Q4. High-Risk Segments (Top 10)", chart_q4)

# --- DETAIL TABLE ---
st.markdown("---")
with st.expander("Detailed Performance Data", expanded=False):
    # Select specific columns and rename them
    display_df = cat_df[
        ["merchant_category", "vol", "rev", "fraud_cases", "fraud_loss", "fraud_rate"]
    ].rename(
        columns={
            "merchant_category": "Merchant Category",
            "vol": "Volume",
            "rev": "Revenue",
            "fraud_cases": "Fraud Cases",
            "fraud_loss": "Fraud Loss",
            "fraud_rate": "Fraud Rate",
        }
    )

    st.dataframe(
        display_df.sort_values("Fraud Rate", ascending=False).style.format(
            {
                "Volume": "{:,}",
                "Revenue": "${:,.0f}",  # No decimals
                "Fraud Cases": "{:,}",
                "Fraud Loss": "${:,.0f}",
                "Fraud Rate": "{:.2%}",
            }
        ),
        width="stretch",
    )
