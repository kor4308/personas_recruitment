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

# COL 1
with col1.expander("US Demographics and Disease Epidemiology"):
    st.markdown("### 2023 US Census")
    st.caption("Information in this section is from the 2023 US Census.")
    st.subheader("Gender")
    if disease == "Alzheimer's" and age_group:
        current_us = US_65PLUS if age_group == "65+" else US_CENSUS
        US_TOTAL_POP = 55792501 if age_group == "65+" else 342_000_000
    else:
        current_us = US_CENSUS
        US_TOTAL_POP = 342_000_000
    for k, v in current_us["Gender"].items():
        total = int((v / 100) * US_TOTAL_POP)
        st.markdown(f"{k}: {v}%")
        st.caption(f"There are ~{total:,} {k} in the United States")
    st.subheader("Race")
    for k, v in current_us["Race"].items():
        total = int((v / 100) * US_TOTAL_POP)
        st.markdown(f"{k}: {v}%")
        st.caption(f"There are ~{total:,} {k} in the United States")
    st.markdown("---")
    st.subheader(f"Disease Epidemiology in {disease} (Estimated)")
    if disease == "Alzheimer's":
        st.caption("Information provided is from the 2023 Alzheimer's Report (Alzheimer's Association Journal). AIAN and NHPI races were not accounted for in this report, thus they are from the internet.")
    elif disease in ["Schizophrenia", "Bipolar Disorder"]:
        st.caption("These numbers are from the internet.")
    total_disease_pop = DISEASE_TOTALS.get(f"Alzheimer's_{age_group}" if disease == "Alzheimer's" else disease, US_TOTAL_POP)
    st.markdown("**Gender:**")
    for k, v in (ALZHEIMERS_TARGET if disease == "Alzheimer's" else BIPOLAR_TARGET if disease == "Bipolar Disorder" else SCHIZOPHRENIA_TARGET)["Gender"].items():
        total = int((v / 100) * total_disease_pop)
        st.markdown(f"{k}: {v}%")
        st.caption(f"There are ~{total:,} {k} patients with {disease} in the United States")
    st.markdown("**Race:**")
    for k, v in (ALZHEIMERS_TARGET if disease == "Alzheimer's" else BIPOLAR_TARGET if disease == "Bipolar Disorder" else SCHIZOPHRENIA_TARGET)["Race"].items():
        total = int((v / 100) * total_disease_pop)
        st.markdown(f"{k}: {v}%")
        st.caption(f"There are ~{total:,} {k} patients with {disease} in the United States")

# COL 2
with col2.expander("Target Enrollment Inputs"):
    st.markdown("Inputs coming soon...")

# COL 3
with col3.expander("Estimated Quantity Needed to Screen"):
    st.markdown("Estimates coming soon...")

# GENERAL RECRUITMENT STRATEGIES
st.markdown("---")
st.subheader(f"General Motivators and Barriers for {disease}")
st.caption("These motivators and barriers can be explored through Patient dossiers.")
cols = st.columns(2)
with cols[0]:
    st.markdown("### ✅ Motivators")
    st.markdown("- Trusted Voices")
    st.markdown("- Altruism")
    st.markdown("- Education & Disease Awareness")
    st.markdown("- Personal Benefit")
with cols[1]:
    st.markdown("### ⛔ Barriers")
    st.markdown("- Study Partner Requirement")
    st.markdown("- Procedure/Investigational Burden")
    st.markdown("- Disease Stigma")
    st.markdown("- Specific Population Injustices")

# RECRUITMENT STRATEGIES FOR FOCUS POPULATIONS
st.markdown("---")
st.subheader(f"📣 Recruitment Strategies for Focus Populations with {disease}")
st.caption("⬇️ List is in order from greatest % population needed to screen; thus greatest need to focus")
st.markdown("Strategies coming soon...")
