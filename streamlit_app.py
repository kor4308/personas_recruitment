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
st.title("US vs Target Demographic Comparator")

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

# --- Expandable Sections for All Columns ---
with col1.expander("US Demographics and Disease Epidemiology"):
    st.markdown(f"**Total U.S. Population:** {US_TOTAL_POP:,}")
    st.subheader("Gender")
    for k, v in current_us["Gender"].items():
        st.markdown(f"{k}: {v}%")
    st.subheader("Race")
    for k, v in current_us["Race"].items():
        st.markdown(f"{k}: {v}%")
    if disease in target:
        st.markdown(f"---")
        st.subheader(f"Disease Epidemiology in {disease} (Estimated)")
        st.markdown("**Gender:**")
        for k, v in target["Gender"].items():
            st.markdown(f"{k}: {v}%")
        st.markdown("**Race:**")
        for k, v in target["Race"].items():
            st.markdown(f"{k}: {v}%")

# --- Recruitment Strategy Section (Now Standalone Below Columns) ---
st.markdown("---")
st.header("Recruitment Strategies for Focus Populations")
recruitment_strategies = {
    "Female": [
        "Connect with women's health networks and caregiving support groups",
        "Partner with community-based organizations that focus on elder care",
        "Provide flexible study visit schedules or caregiver support"
    ],
    "Male": [
        "Target outreach through male-dominated environments such as sporting events",
        "Promote messaging around benefitting future generations",
        "Address stigma around mental health and participation"
    ],
    "Black, NH": [
        "Engage trusted faith-based and civic leaders",
        "Highlight historical medical distrust and steps taken to ensure ethical practices",
        "Avoid or reassess the need for MMSE and logical memory scoring inclusion criteria as these can be inequitable barriers."
    ],
    "Hispanic": [
        "Use Spanish-language materials and bilingual coordinators",
        "Partner with local Hispanic/Latino organizations and clinics",
        "Avoid or reassess the need for MMSE and logical memory scoring as these can be barriers."
    ],
    "White, NH": [
        "Collaborate with primary care and memory clinics in suburban and rural areas"
    ],
    "AIAN, NH": [
        "Partner with tribal health clinics and IHS facilities",
        "Provide culturally competent staff and materials",
        "Ensure trials accommodate rural residence or travel support"
    ],
    "NHPI, NH": [
        "Engage local community leaders and churches",
        "Incorporate family-centered decision-making",
        "Use Pacific Islander liaisons for outreach"
    ]
}

for group, strategies in recruitment_strategies.items():
    st.markdown(f"**{group}**")
    for strat in strategies:
        st.markdown(f"- {strat}")
    st.markdown("---")
