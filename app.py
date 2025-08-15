import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import fetch_registrations  # Import API function

# --------------------------
# Utility function
# --------------------------
def add_yoy_qoq(df):
    df = df.copy()
    full_years = df.groupby("year")["quarter"].nunique()
    full_years = full_years[full_years == 4].index
    yearly_totals = (
        df[df["year"].isin(full_years)]
        .groupby("year")["total_registrations"]
        .sum()
        .reset_index()
    )

    yearly_totals["prev_year_count"] = yearly_totals["total_registrations"].shift(1)
    yearly_totals["YOY_%"] = (
        (yearly_totals["total_registrations"] - yearly_totals["prev_year_count"])
        / yearly_totals["prev_year_count"]
    ) * 100
    avg_yoy = yearly_totals["YOY_%"].mean()

    df["prev_quarter_count"] = df["total_registrations"].shift(1)
    df["QOQ_%"] = (
        (df["total_registrations"] - df["prev_quarter_count"])
        / df["prev_quarter_count"]
    ) * 100
    avg_qoq = df["QOQ_%"].mean()

    return df, yearly_totals, avg_yoy, avg_qoq


# --------------------------
# Page 1: Filters
# --------------------------
def page_filters():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Automobile Analysis Dashboard</h1>", unsafe_allow_html=True)

    manufacturers_df = pd.read_csv("manufacturers_data.csv")
    manufacturer_list = ["All Manufacturers"] + sorted(manufacturers_df["name"].unique().tolist())

    category = st.selectbox("Select Vehicle Category", ["All Categories", "2W", "3W", "4W"], index=0)
    manufacturer = st.selectbox("Select Manufacturer", manufacturer_list, index=0)

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("Start Year", min_value=2010, max_value=2025, value=2015)
        start_quarter = st.selectbox("Start Quarter", [1, 2, 3, 4], index=1)
    with col2:
        end_year = st.number_input("End Year", min_value=2010, max_value=2025, value=2025)
        end_quarter = st.selectbox("End Quarter", [1, 2, 3, 4], index=0)

    if st.button("Submit"):
        # Call backend API and store JSON response
        response_json = fetch_registrations(
            category, manufacturer, start_year, start_quarter, end_year, end_quarter
        )

        # Save inputs and response in session state
        st.session_state["category"] = category
        st.session_state["manufacturer"] = manufacturer
        st.session_state["start_year"] = start_year
        st.session_state["start_quarter"] = start_quarter
        st.session_state["end_year"] = end_year
        st.session_state["end_quarter"] = end_quarter
        st.session_state["api_response"] = response_json

        st.session_state["page"] = "results"


# --------------------------
# Page 2: Results
# --------------------------
def page_results(api_response):
    st.set_page_config(layout="wide")

    subtitle = (
        f"{st.session_state['category']} {st.session_state['manufacturer']} "
        f"from Q{st.session_state['start_quarter']} {st.session_state['start_year']} "
        f"to Q{st.session_state['end_quarter']} {st.session_state['end_year']}"
    )

    st.markdown("<h1 style='text-align: center;'>Results for:</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{subtitle}</h3>", unsafe_allow_html=True)

    # Convert JSON response to DataFrame
    if "data" in api_response:
        df = pd.DataFrame(api_response["data"])
        # Rename column for consistency with add_yoy_qoq()
        df = df.rename(columns={"registration_count": "total_registrations"})
    else:
        st.error(api_response.get("error", "No data returned from API"))
        return

    df, yearly_totals, avg_yoy, avg_qoq = add_yoy_qoq(df)

    col_spacer1, col_center, col_spacer2 = st.columns([4, 2, 4])
    with col_center:
        st.metric("Average YOY %", f"{avg_yoy:.2f}%")
    col_spacer1, col_center, col_spacer2 = st.columns([4, 2, 4])
    with col_center:
        st.metric("Average QOQ %", f"{avg_qoq:.2f}%")

    st.markdown("<h3 style='text-align: center;'>Registrations by Year (Full Years Only)</h3>", unsafe_allow_html=True)
    fig1 = px.line(yearly_totals, x="year", y="total_registrations", markers=True,
                   labels={"total_registrations": "Total Registrations", "year": "Year"})
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<h3 style='text-align: center;'>Registrations by Quarter (Sequential)</h3>", unsafe_allow_html=True)
    df["quarter_label"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)
    fig2 = px.line(df, x="quarter_label", y="total_registrations", markers=True,
                   labels={"total_registrations": "Total Registrations", "quarter_label": "Quarter"})
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<h3 style='text-align: center;'>YOY Table (Full Years)</h3>", unsafe_allow_html=True)
    st.dataframe(yearly_totals)
    st.markdown("<h3 style='text-align: center;'>QOQ Table</h3>", unsafe_allow_html=True)
    st.dataframe(df)

    if st.button("Back"):
        st.session_state["page"] = "filters"


# --------------------------
# Main App
# --------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "filters"

if st.session_state["page"] == "filters":
    page_filters()
elif st.session_state["page"] == "results":
    page_results(st.session_state.get("api_response", {}))
