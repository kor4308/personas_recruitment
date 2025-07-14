import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --- Constants ---
SCHIZOPHRENIA_TARGET = {
    "Gender": {"Female": 40.0, "Male": 60.0},
    "Race": {
        "Hispanic": 15.0,
        "White, NH": 30.0,
        "Black, NH": 25.0,
        "Asian, NH": 10.0,
        "AIAN, NH": 10.0,
        "NHPI, NH": 5.0,
        "Other": 5.0
    }
}

US_CENSUS = {
    "Gender": {"Female": 50.5, "Male": 49.5},
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

US_65PLUS = {
    "Gender": {"Female": 50.9, "Male": 49.1},
    "Race": {
        "Hispanic": 8.8,
        "White, NH": 76.6,
        "Black, NH": 9.2,
        "Asian, NH": 4.5,
        "AIAN, NH": 0.7,
        "NHPI, NH": 0.1,
        "Other": 3.4
    }
}

ALZHEIMERS_TARGET = {
    "Gender": {"Female": 64.0, "Male": 36.0},
    "Race": {
        "Hispanic": 21.2,
        "White, NH": 51.7,
        "Black, NH": 19.2,
        "Asian, NH": 5.9,
        "AIAN, NH": 0.8,
        "NHPI, NH": 0.3,
        "Other": 0.9
    }
}

BIPOLAR_TARGET = {
    "Gender": {"Female": 51.0, "Male": 49.0},
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

# --- Title ---
st.title("🎯 US vs Target Demographic Comparator")

# --- Dropdowns ---
therapeutic_area = st.selectbox("Select Therapeutic Area", ["Neuro", "Other"])
disease = st.selectbox("Select Disease", ["Alzheimer's", "Bipolar Disorder", "Schizophrenia", "Other"])

age_group = None
if disease == "Alzheimer's":
    age_group = st.selectbox("Select Age Inclusion Criteria", ["18+", "65+"])
    st.caption("Population estimates reflect U.S. population in selected age group.")

# --- Column Layout ---
col1, col2, col3 = st.columns([1, 1, 1])

# --- Determine Target ---
if disease == "Alzheimer's":
    target = ALZHEIMERS_TARGET
elif disease == "Bipolar Disorder":
    target = BIPOLAR_TARGET
elif disease == "Schizophrenia":
    target = SCHIZOPHRENIA_TARGET
else:
    target = US_CENSUS

# --- Functions ---
def adjustable_input(label, default):
    return st.number_input(label, min_value=0.0, max_value=100.0, value=float(default), step=0.1, key=f"input_{label}")

# --- Gender Section ---
if disease == "Alzheimer's" and age_group:
    if age_group == "65+":
        US_TOTAL_POP = 55792501
        current_us = US_65PLUS
    else:
        US_TOTAL_POP = 342_000_000
        current_us = US_CENSUS
else:
    US_TOTAL_POP = 342_000_000
    current_us = US_CENSUS

# --- Disease Prevalence ---
DISEASE_PREVALENCE = {
    "Alzheimer's": {
        "overall": 0.103,
        "Gender": {"Female": 0.12, "Male": 0.086},
        "Race": {
            "White, NH": 0.08,
            "Black, NH": 0.14,
            "Hispanic": 0.11,
            "Asian, NH": 0.06,
            "AIAN, NH": 0.07,
            "NHPI, NH": 0.07,
            "Other": 0.07
        },
        "screen_fail": {"Female": 0.3, "Male": 0.2, "White, NH": 0.2, "Black, NH": 0.4, "Hispanic": 0.35, "Asian, NH": 0.3, "AIAN, NH": 0.3, "NHPI, NH": 0.3, "Other": 0.3}
    },
    "Schizophrenia": {
        "overall": 0.01,
        "Gender": {"Female": 0.008, "Male": 0.012},
        "Race": {
            "White, NH": 0.007,
            "Black, NH": 0.015,
            "Hispanic": 0.012,
            "Asian, NH": 0.008,
            "AIAN, NH": 0.009,
            "NHPI, NH": 0.009,
            "Other": 0.01
        },
        "screen_fail": {"Female": 0.25, "Male": 0.2, "White, NH": 0.2, "Black, NH": 0.25, "Hispanic": 0.25, "Asian, NH": 0.25, "AIAN, NH": 0.25, "NHPI, NH": 0.25, "Other": 0.25}
    },
    "Bipolar Disorder": {
        "overall": 0.03,
        "Gender": {"Female": 0.032, "Male": 0.028},
        "Race": {
            "White, NH": 0.028,
            "Black, NH": 0.032,
            "Hispanic": 0.03,
            "Asian, NH": 0.025,
            "AIAN, NH": 0.03,
            "NHPI, NH": 0.03,
            "Other": 0.03
        },
        "screen_fail": {"Female": 0.25, "Male": 0.25, "White, NH": 0.25, "Black, NH": 0.25, "Hispanic": 0.25, "Asian, NH": 0.25, "AIAN, NH": 0.25, "NHPI, NH": 0.25, "Other": 0.25}
    }
}

# --- Display Gender Census and Target ---
st.subheader("Gender Comparison")
with col1:
    st.markdown("**US Census Gender Demographics**")
    st.caption(f"Total Population: {US_TOTAL_POP:,}")
    for key, value in current_us["Gender"].items():
        st.text(f"{key}: {value}%")

with col2:
    total_enroll_gender = st.markdown(f"**Gender targets for {disease}**")
    total_enroll_gender = st.number_input("Total Enrollment Target", min_value=100, max_value=1000000, value=1000, step=100, key="total_enroll_target")
    st.caption("These demographic targets are not validated.")
    gender_target = {}
    total_gender = 0
    for key, value in target["Gender"].items():
        col_gender, col_fail = st.columns([3, 2])
        with col_gender:
            val = adjustable_input(f"{key} (%)", value)
        with col_fail:
            fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=1.0, value=DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25), step=0.01, key=f"sf_gender_{key}")
        gender_target[key] = val
        DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val
        total_gender += val
    st.markdown(f"**Total: {total_gender:.1f}%**")

with col3:
    st.markdown("**Estimated Quantity Needed to Screen to Reach Target**")
    st.caption("To reach target enrollment numbers, each group's screening estimate is shown below")
    for key, val in gender_target.items():
        prevalence = DISEASE_PREVALENCE[disease]["Gender"].get(key, DISEASE_PREVALENCE[disease]["overall"])
        fail_rate = DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25)
        est_target_n = (val / 100) * US_TOTAL_POP * prevalence * (1 + fail_rate)
        st.markdown(f"**{key}**: {int(est_target_n):,} to screen")
        percentage = (est_target_n / US_TOTAL_POP) * 100
        st.caption(f"To reach target enrollment numbers, approximately {percentage:.1f}% of eligible {key} individuals must be screened.")
    percentage = (est_target_n / US_TOTAL_POP) * 100
    st.caption(f"To reach target enrollment numbers, approximately {percentage:.1f}% of eligible {key} individuals must be screened.")

# --- Race Comparison Section ---
st.subheader("Race Comparison")
with col1:
    st.markdown("**US Census Race Demographics**")
    for key, value in current_us["Race"].items():
        st.text(f"{key}: {value}%")

with col2:
    st.markdown(f"**Race targets for {disease}**")
    st.caption("These demographic targets are not validated.")
    race_target = {}
    total_race = 0
    for key, value in target["Race"].items():
        col_race, col_fail = st.columns([3, 2])
        with col_race:
            val = adjustable_input(f"{key} (%)", value)
        with col_fail:
            fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=1.0, value=DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25), step=0.01, key=f"sf_race_{key}")
        race_target[key] = val
        DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val
        total_race += val
    st.markdown(f"**Total: {total_race:.1f}%**")

with col3:
    st.markdown("**Estimated Quantity Needed to Screen to Reach Target**")
    st.caption("To reach target enrollment numbers, each group's screening estimate is shown below")
    for key, val in race_target.items():
        prevalence = DISEASE_PREVALENCE[disease]["Race"].get(key, DISEASE_PREVALENCE[disease]["overall"])
        fail_rate = DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25)
        est_target_n = (val / 100) * US_TOTAL_POP * prevalence * (1 + fail_rate)
        st.markdown(f"**{key}**: {int(est_target_n):,} to screen")
