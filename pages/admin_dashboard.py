# pages/admin_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_utils import get_connection

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.header("📊 Admin Dashboard")

# Fetch bookings data
try:
    conn = get_connection()
    query = "SELECT student_name, date, time, counsellor FROM bookings"
    bookings_df = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    st.error(f"Database error: {e}")
    bookings_df = pd.DataFrame()

# Show analytics
if not bookings_df.empty:
    # Convert date if not already datetime
    if not pd.api.types.is_datetime64_any_dtype(bookings_df["date"]):
        bookings_df["date"] = pd.to_datetime(bookings_df["date"], errors="coerce")

    # --- Histogram by Date and Counsellor ---
    fig_hist = px.histogram(
        bookings_df,
        x="date",
        color="counsellor",
        barmode="group",
        title="Bookings by Date and Counsellor"
    )
    fig_hist.update_layout(xaxis_title="Date", yaxis_title="Number of Bookings")
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- Calendar/Timeline View ---
    bookings_df["start"] = bookings_df["date"]
    bookings_df["end"] = bookings_df["date"] + pd.Timedelta(hours=1)

    fig_calendar = px.timeline(
        bookings_df,
        x_start="start",
        x_end="end",
        y="counsellor",
        color="counsellor",
        title="Appointments Calendar View"
    )
    fig_calendar.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_calendar, use_container_width=True)

    # Show raw table
    with st.expander("📋 View Raw Data"):
        st.dataframe(bookings_df)

else:
    st.info("No bookings yet.")
