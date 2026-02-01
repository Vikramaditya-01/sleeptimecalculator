import streamlit as st
from datetime import datetime, timedelta


# --------- LOGIC (same as your working calculator) ---------

def parse_time(time_str):
    time_str = time_str.strip().upper()

    if len(time_str) < 2 or time_str[-1] not in ("A", "P"):
        raise ValueError("Use format like 9A, 9.5A, 10.25P")

    meridian = time_str[-1]
    time_part = time_str[:-1]

    if "." in time_part:
        hour_str, minute_str = time_part.split(".")
        hour = int(hour_str)

        if len(minute_str) == 1:
            minute_str = "0" + minute_str

        minute = int(minute_str)
    else:
        hour = int(time_part)
        minute = 0

    if minute >= 60:
        raise ValueError("Minutes must be less than 60")

    if meridian == "P" and hour != 12:
        hour += 12
    if meridian == "A" and hour == 12:
        hour = 0

    return datetime(2000, 1, 1, hour, minute)


def calculate_sleep(sleep_time, wake_time):
    sleep = parse_time(sleep_time)
    wake = parse_time(wake_time)

    if wake <= sleep:
        wake += timedelta(days=1)

    duration = wake - sleep
    total_minutes = duration.seconds // 60

    return total_minutes // 60, total_minutes % 60


# --------- STREAMLIT UI ---------

st.set_page_config(page_title="Sleep Time Calculator", page_icon="😴", layout="centered")

st.title("😴 Sleep Time Calculator")
st.write("Calculate **hours slept** accurately (supports late nights & AM/PM).")

st.markdown("**Supported formats:** `9A`, `11P`, `9.9A`, `10.2P`, `11.25P`")

sleep_time = st.text_input("🛌 Sleep Time", placeholder="e.g. 11P, 9.9A")
wake_time = st.text_input("⏰ Wake Time", placeholder="e.g. 9.25A, 10A")

if st.button("Calculate Sleep"):
    if not sleep_time or not wake_time:
        st.warning("Please enter both sleep and wake time.")
    else:
        try:
            hours, minutes = calculate_sleep(sleep_time, wake_time)
            st.success(f"✅ **Hours slept:** {hours} hours {minutes} minutes")
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("---")
st.caption("Built for habit tracking • Accurate across midnight • Minimal & clean")