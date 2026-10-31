"""A simple monthly savings goal calculator."""

import pandas as pd
import streamlit as st

from sectors import SectorsError, get_company_overview

st.set_page_config(page_title="Investment Goal Calculator", layout="centered")


def format_rupiah(amount):
    """Format a number as Indonesian rupiah with dots between thousands."""
    return f"Rp {amount:,.0f}".replace(",", ".")


@st.cache_data(ttl=300)
def load_company_overview(ticker):
    return get_company_overview(ticker)


display_mode = st.radio("Mode tampilan", ["Terang", "Gelap"], horizontal=True)
if display_mode == "Gelap":
    background_color = "#111827"
    text_color = "#F9FAFB"
    input_color = "#1F2937"
    border_color = "#374151"
    metric_color = "#1F2937"
else:
    background_color = "#FFFFFF"
    text_color = "#111827"
    input_color = "#FFFFFF"
    border_color = "#D1D5DB"
    metric_color = "#F3F4F6"

st.markdown(
    f"""
    <style>
        .stApp,
        [data-testid="stAppViewContainer"] {{
            background-color: {background_color};
            color: {text_color};
        }}
        [data-testid="stHeader"] {{
            background-color: {background_color};
        }}
        .stApp, .stApp p, .stApp h1, .stApp h2, .stApp label,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stMetricLabel"],
        .stApp [data-testid="stMetricValue"],
        .stApp [data-testid="stCaptionContainer"] {{
            color: {text_color};
        }}
        .stApp input,
        .stApp [data-baseweb="input"] {{
            background-color: {input_color};
            color: {text_color};
            border-color: {border_color};
        }}
        .stApp [data-testid="stMetric"] {{
            background-color: {metric_color};
            border-radius: 0.5rem;
            padding: 1rem;
        }}
        .stApp [data-testid="stVegaLiteChart"] {{
            background-color: {background_color};
        }}
        .stApp [data-testid="stVegaLiteChart"] svg text {{
            fill: {text_color};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Investment Goal Calculator")
st.write("See how your monthly saving could grow over time.")

ticker = st.text_input("IDX ticker", value="BBCA").strip().upper()
company = None

try:
    company = load_company_overview(ticker)
except SectorsError as error:
    st.warning(str(error))

if company:
    st.header(company.get("company_name") or ticker)
    st.write(f"**Sector:** {company.get('sector') or 'Not available'}")
    st.write(f"**Sub-sector:** {company.get('sub_sector') or 'Not available'}")
    closing_price = company.get("last_close_price")
    if isinstance(closing_price, (int, float)) and closing_price > 0:
        st.write(f"**Last close:** {format_rupiah(closing_price)}")
    else:
        st.warning("The last close price is unavailable, so lot information cannot be calculated.")

monthly_saving = st.number_input(
    "Monthly saving (Rp)",
    min_value=0,
    value=500_000,
    step=100_000,
)
years = st.number_input(
    "Number of years",
    min_value=1,
    max_value=50,
    value=10,
    step=1,
)
annual_return_percent = st.number_input(
    "Expected yearly return (%)",
    min_value=-100.0,
    max_value=100.0,
    value=8.0,
    step=0.5,
)

monthly_return = (1 + annual_return_percent / 100) ** (1 / 12) - 1
balance = 0.0
yearly_totals = []

for year in range(1, years + 1):
    for _ in range(12):
        balance *= 1 + monthly_return
        balance += monthly_saving
    yearly_totals.append({"Year": year, "Total": balance})

st.subheader("Estimated amount after your chosen period")
st.metric("Final amount", format_rupiah(balance))

if company and isinstance(closing_price, (int, float)) and closing_price > 0:
    lot_cost = closing_price * 100
    lots = int(monthly_saving // lot_cost)
    leftover = monthly_saving - lots * lot_cost
    st.write(
        f"Your monthly saving buys **{lots} lots** of this stock, "
        f"with **{format_rupiah(leftover)}** left over."
    )

st.subheader("Growth year by year")
st.line_chart(pd.DataFrame(yearly_totals).set_index("Year"))
st.caption(
    "Monthly saving is added at the end of each month. The yearly return is "
    "converted to an equivalent monthly rate. This estimate is not investment advice."
)

if company:
    with st.expander("Raw company data"):
        st.json(company)
