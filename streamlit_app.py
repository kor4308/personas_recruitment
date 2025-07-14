import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --- Constants ---
SCHIZOPHRENIA_TARGET = {
    "Gender": {"Female": 40.0, "Male": 60.0},
    "Race": {
        "Hispanic": 15.0, "White, NH": 30.0, "Black, NH": 25.0,
        "Asian, NH": 10.0, "AIAN, NH": 10.0, "NHPI, NH": 5.0, "Other": 5.0
    }
}

US_CENSUS = {
    "Gender": {"Female": 50.5, "Male": 49.5},
    "Race": {
        "Hispanic": 17.6, "White, NH": 61.1, "Black, NH": 12.3,
        "Asian, NH": 6.3, "AIAN, NH": 0.7, "NHPI, NH": 0.2, "Other": 1.8
    }
}

US_65PLUS = {
    "Gender": {"Female": 50.9, "Male": 49.1},
    "Race": {
        "Hispanic": 8.8, "White, NH": 76.6, "Black, NH": 9.2,
        "Asian, NH": 4.5, "AIAN, NH": 0.7, "NHPI, NH": 0.1, "Other": 3.4
    }
}

ALZHEIMERS_TARGET = {
    "Gender": {"Female": 64.0, "Male": 36.0},
    "Race": {
        "Hispanic": 21.2, "White, NH": 51.7, "Black, NH": 19.2,
        "Asian, NH": 5.9, "AIAN, NH": 0.8, "NHPI, NH": 0.3, "Other": 0.9
    }
}

BIPOLAR_TARGET = {
    "Gender": {"Female": 51.0, "Male": 49.0},
    "Race": {
        "Hispanic": 18.5, "White, NH": 53.0, "Black, NH": 16.0,
        "Asian, NH": 7.0, "AIAN, NH": 1.0, "NHPI, NH": 0.5, "Other": 4.0
    }
}

disease_totals = {
    "Alzheimer's_18+": 7100000,
    "Alzheimer's_65+": 6900000,
    "Schizophrenia": 3200000,
    "Bipolar Disorder": 3100000
}

# --- Disease Prevalence ---
DISEASE_PREVALENCE = {
    "Alzheimer's": {
        "overall": 0.103,
        "Gender": {"Female": 0.12, "Male": 0.086},
        "Race": {
            "White, NH": 0.08, "Black, NH": 0.14, "Hispanic": 0.11,
            "Asian, NH": 0.06, "AIAN, NH": 0.07, "NHPI, NH": 0.07, "Other": 0.07
        },
        "screen_fail": {
            "Female": 0.7, "Male": 0.3, "White, NH": 0.2,
            "Black, NH": 0.6, "Hispanic": 0.65, "Asian, NH": 0.6,
            "AIAN, NH": 0.45, "NHPI, NH": 0.65, "Other": 0.56
        }
    },
    "Schizophrenia": {
        "overall": 0.01,
        "Gender": {"Female": 0.008, "Male": 0.012},
        "Race": {
            "White, NH": 0.007, "Black, NH": 0.015, "Hispanic": 0.012,
            "Asian, NH": 0.008, "AIAN, NH": 0.009, "NHPI, NH": 0.009, "Other": 0.01
        },
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "Black, NH", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    },
    "Bipolar Disorder": {
        "overall": 0.03,
        "Gender": {"Female": 0.032, "Male": 0.028},
        "Race": {
            "White, NH": 0.028, "Black, NH": 0.032, "Hispanic": 0.03,
            "Asian, NH": 0.025, "AIAN, NH": 0.03, "NHPI, NH": 0.03, "Other": 0.03
        },
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "Black, NH", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    }
}

# --- Final Column Update ---
col1, col2, col3 = st.columns(3)
# ... [unchanged code for col1 and col2] ...

with col3:
    st.markdown("**Estimated Quantity Needed to Screen - Gender**")
    st.caption("⬆️ Order is in order of greatest needed recruitment focus for each eligible population")
    for key, value in target["Gender"].items():
        target_n = total_enroll * (value / 100)
        fail_rate = 1 - (st.session_state.get(f"sf_gender_{key}", 100) / 100)
        screened_needed = target_n / (1 - fail_rate)
        eligible_disease_pop = total_disease_pop * (value / 100)
        screen_percent = (screened_needed / eligible_disease_pop) * 100 if eligible_disease_pop > 0 else 0
        st.markdown(f"{key}: {int(screened_needed):,} (**{screen_percent:.3f}%**)\n")
        st.caption(f"To reach target enrollment numbers, approximately **{screen_percent:.3f}%** of eligible {key} {disease} patients must be screened.")

    st.markdown("**Estimated Quantity Needed to Screen - Race**")
    st.caption("⬆️ Order is in order of greatest needed recruitment focus for each eligible population")
    for key, value in target["Race"].items():
        target_n = total_enroll * (value / 100)
        fail_rate = 1 - st.session_state.get(f"sf_race_{key}", 100) / 100
        screened_needed = target_n / (1 - fail_rate)
        eligible_disease_pop = total_disease_pop * (value / 100)
        screen_percent = (screened_needed / eligible_disease_pop) * 100 if eligible_disease_pop > 0 else 0
        st.markdown(f"{key}: {int(screened_needed):,} (**{screen_percent:.3f}%**)\n")
        st.caption(f"To reach target enrollment numbers, approximately **{screen_percent:.3f}%** of eligible {key} individuals must be screened.")
