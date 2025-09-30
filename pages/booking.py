# pages/booking.py
import streamlit as st
from utils.db_utils import get_connection, initialize_db

initialize_db()  # Make sure tables exist

st.title("📅 Book a Counsellor")
st.write("Please fill out the form below to book your appointment.")

student_name = st.text_input("Your Name")
date = st.date_input("Select Date")
time = st.time_input("Select Time")
counsellor = st.selectbox("Choose Counsellor", ["Dr. Smith", "Dr. Lee", "Dr. Patel"])

if st.button("Book Appointment"):
    if not student_name:
        st.warning("⚠️ Please enter your name before booking.")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (student_name, date, time, counsellor) VALUES (?, ?, ?, ?)",
            (student_name, str(date), str(time), counsellor)
        )
        conn.commit()
        conn.close()
        st.success("✅ Your appointment has been booked!")
