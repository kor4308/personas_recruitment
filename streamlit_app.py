import streamlit as st
import pandas as pd
import math

st.set_page_config(layout="wide")

# --- Constants ---
SCHIZOPHRENIA_TARGET = {
    "Gender": {"Female": 40.0, "Male": 60.0},
    "Race": {
        "Hispanic": 15.0,
        "White, NH": 30.0,
        "African American": 25.0,
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
        "African American": 12.3,
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
        "African American": 9.2,
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
        "African American": 19.2,
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
        "African American": 16.0,
        "Asian, NH": 7.0,
        "AIAN, NH": 1.0,
        "NHPI, NH": 0.5,
        "Other": 4.0
    }
}

DISEASE_TOTALS = {
    "Alzheimer's_18+": 7100000,
    "Alzheimer's_65+": 6900000,
    "Schizophrenia": 3200000,
    "Bipolar Disorder": 3100000
}

DISEASE_PREVALENCE = {
    "Alzheimer's": {
        "screen_success": {
            "Female": 0.3,
            "Male": 0.7,
            "White, NH": 0.75,
            "African American": 0.35,
            "Hispanic": 0.28,
            "Asian, NH": 0.50,
            "AIAN, NH": 0.50,
            "NHPI, NH": 0.50,
            "Other": 0.50
        },
        "screen_fail": {}
    },
    "Schizophrenia": {
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "African American", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    },
    "Bipolar Disorder": {
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "African American", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    }
}

st.title("US vs Target Demographic Comparator")

therapeutic_area = st.selectbox("Select Therapeutic Area", ["Neuro", "Other"])
disease = st.selectbox("Select Disease", ["Alzheimer's", "Bipolar Disorder", "Schizophrenia", "Other"])

age_group = None
if disease == "Alzheimer's":
    age_group = st.selectbox("Select Age Inclusion Criteria", ["18+", "65+"])
    st.caption("Population estimates reflect U.S. population in selected age group.")

col1, col2, col3 = st.columns([1, 1, 1])

if disease == "Alzheimer's":
    target = ALZHEIMERS_TARGET
elif disease == "Bipolar Disorder":
    target = BIPOLAR_TARGET
elif disease == "Schizophrenia":
    target = SCHIZOPHRENIA_TARGET
else:
    target = US_CENSUS

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

if disease == "Alzheimer's":
    pop_key = f"Alzheimer's_{age_group}"
else:
    pop_key = disease

total_disease_pop = DISEASE_TOTALS.get(pop_key, US_TOTAL_POP)

with col2.expander("Target Enrollment Inputs"):
    total_enroll = st.number_input("Total Enrollment Target", min_value=100, max_value=1000000, value=1000, step=100, key="total_enroll")

    st.markdown("**Gender Target % and Screen Success**")
    for key, value in target["Gender"].items():
        cols = st.columns([2, 2])
        with cols[0]:
            st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"gender_{key}")
            updated_pct = st.session_state.get(f"gender_{key}", value)
            target_n = int(total_enroll * (updated_pct / 100))
            st.caption(f"Targeting {target_n:,} {key} participants")
            target_n = int(total_enroll * (pct / 100))
            st.caption(f"Targeting {target_n:,} {key} participants")
        with cols[1]:
            default_success = DISEASE_PREVALENCE[disease].get("screen_success", {}).get(key, 0.5) * 100
            st.number_input("Screen Success %", min_value=0.0, max_value=100.0, value=default_success, step=1.0, key=f"sf_gender_{key}")

    st.markdown("**Race Target % and Screen Success**")
    for key, value in target["Race"].items():
        cols = st.columns([2, 2])
        with cols[0]:
            pct = st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"race_{key}")
            target_n = int(total_enroll * (pct / 100))
            st.caption(f"Targeting {target_n:,} {key} participants")
        with cols[1]:
            default_success = DISEASE_PREVALENCE[disease].get("screen_success", {}).get(key, 0.5) * 100
            st.number_input("Screen Success %", min_value=0.0, max_value=100.0, value=default_success, step=1.0, key=f"sf_race_{key}")
