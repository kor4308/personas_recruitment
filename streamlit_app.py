import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --- Constants ---
US_CENSUS = {
    "Gender": {"Female": 51, "Male": 49},
    "Race": {
        "Hispanic": 17.6,
        "White, NH": 61.1,
        "Black, NH": 12.3,
        "Asian, NH": 6.3,
        "AIAN, NH": 0.7,
        "NHPI, NH": 0.2,
        "Other": 1.8
    }
}

ALZHEIMERS_TARGET = {
    "Gender": {"Female": 64, "Male": 36},
    "Race": {
        "Hispanic": 21.2,
        "White, NH": 51.7,
        "Black, NH": 19.2,
        "Asian, NH": 5.9,
        "AIAN, NH": 0.8,
        "NHPI, NH": 0.3,
        "Other": 1.9
    }
}

BIPOLAR_TARGET = {
    "Gender": {"Female": 51, "Male": 49},
    "Race": {
        "Hispanic": 18.5,
        "White, NH": 53.0,
        "Black, NH": 16.0,
        "Asian, NH": 7.0,
        "AIAN, NH": 1.0,
        "NHPI, NH": 0.5,
        "Other": 4.0
    }
}

# --- Sidebar Selections ---
st.title("🎯 US vs Target Demographic Comparator")
col1, col2, col3 = st.columns([1, 1, 1])

therapeutic_area = st.selectbox("Select Therapeutic Area", ["Neuro", "Other"])
disease = st.selectbox("Select Disease", ["Alzheimer's", "Bipolar Disorder", "Other"])

# --- Determine Target ---
if disease == "Alzheimer's":
    target = ALZHEIMERS_TARGET
elif disease == "Bipolar Disorder":
    target = BIPOLAR_TARGET
else:
    target = US_CENSUS

# --- Functions ---
def adjustable_input(label, default):
    return st.number_input(label, min_value=0.0, max_value=100.0, value=default, step=0.1, key=label)

# --- Gender Section ---
st.subheader("Gender Comparison")
with col1:
    st.markdown("**Proportion of US (2023), Age 18+**")
    gender_census = US_CENSUS["Gender"]
    for key, value in gender_census.items():
        st.text(f"{key}: {value}%")

with col2:
    st.markdown(f"**Target: {disease}**")
    gender_target = {}
    total_gender = 0
    for key, value in target["Gender"].items():
        val = adjustable_input(key, value)
        gender_target[key] = val
        total_gender += val
    st.markdown(f"**Total: {total_gender:.1f}%**")

with col3:
    st.markdown("**Difference**")
    for key in gender_census:
        diff = gender_target[key] - gender_census[key]
        st.text(f"{key}: {diff:+.1f}%")

# --- Race Section ---
st.subheader("Race Comparison")
with col1:
    st.markdown("**Proportion of US (2023), Age 18+**")
    race_census = US_CENSUS["Race"]
    for key, value in race_census.items():
        st.text(f"{key}: {value}%")

with col2:
    st.markdown(f"**Target: {disease}**")
    race_target = {}
    total_race = 0
    for key, value in target["Race"].items():
        val = adjustable_input(key, value)
        race_target[key] = val
        total_race += val
    st.markdown(f"**Total: {total_race:.1f}%**")

with col3:
    st.markdown("**Difference**")
    for key in race_census:
        diff = race_target[key] - race_census[key]
        st.text(f"{key}: {diff:+.1f}%")
