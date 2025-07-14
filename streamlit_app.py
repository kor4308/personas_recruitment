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
        "screen_fail": {k: 0.6 for k in ["Female", "Male", "White, NH", "Black, NH", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
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
st.title("\U0001F3AF US vs Target Demographic Comparator")
therapeutic_area = st.selectbox("Select Therapeutic Area", ["Neuro", "Other"])
disease = st.selectbox("Select Disease", ["Alzheimer's", "Bipolar Disorder", "Schizophrenia", "Other"])
age_group = None
if disease == "Alzheimer's":
    age_group = st.selectbox("Select Age Inclusion Criteria", ["18+", "65+"])
    st.caption("Population estimates reflect U.S. population in selected age group.")

if disease == "Alzheimer's":
    target = ALZHEIMERS_TARGET
elif disease == "Bipolar Disorder":
    target = BIPOLAR_TARGET
elif disease == "Schizophrenia":
    target = SCHIZOPHRENIA_TARGET
else:
    target = US_CENSUS

if disease == "Alzheimer's" and age_group == "65+":
    US_TOTAL_POP = 55792501
    current_us = US_65PLUS
    total_disease_pop = disease_totals["Alzheimer's_65+"]
elif disease == "Alzheimer's":
    US_TOTAL_POP = 342_000_000
    current_us = US_CENSUS
    total_disease_pop = disease_totals["Alzheimer's_18+"]
else:
    US_TOTAL_POP = 342_000_000
    current_us = US_CENSUS
    total_disease_pop = disease_totals.get(disease, US_TOTAL_POP)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("**Demographics Overview**")
    st.caption(f"Total US Population: {US_TOTAL_POP:,} | Total with {disease}: {total_disease_pop:,}")

    col_us, col_dis = st.columns(2)
    with col_us:
        st.markdown("**2023 US Census Population - Gender**")
        st.caption("Numbers directly from US Census (2023)")
        for key, value in current_us["Gender"].items():
            st.text(f"{key}: {value}%")
            count = int((value / 100) * US_TOTAL_POP)
            st.caption(f"~{count:,} individuals")

        
        st.markdown("**2023 US Census Population - Race**")
        
        for key, value in current_us["Race"].items():
            st.text(f"{key}: {value}%")
            count = int((value / 100) * US_TOTAL_POP)
            st.caption(f"~{count:,} individuals")

    with col_dis:
        st.markdown(f"**{disease} Disease Population - Gender**")
        st.caption("Numbers from Alzheimer's Association (2023)")
        for key, value in target["Gender"].items():
            st.text(f"{key}: {value}%")
            count = int((value / 100) * total_disease_pop)
            st.caption(f"~{count:,} with {disease}" + (" *Not included in report, this is an estimate from internet*" if key in ["AIAN, NH", "NHPI, NH"] else ""))
st.markdown("<br><br><br>", unsafe_allow_html=True)

        st.markdown(f"**{disease} Disease Population - Race**")
        for key, value in target["Race"].items():
            st.text(f"{key}: {value}%")
            count = int((value / 100) * total_disease_pop)
            st.caption(f"~{count:,} with {disease}" + (" *Not included in Alzheimer's Association report, this is an estimate from internet*" if key in ["AIAN, NH", "NHPI, NH", "Other"] else ""))
st.markdown("<br><br><br>", unsafe_allow_html=True)

with col2:
    st.markdown(f"**Target Enrollment by Gender for {disease}**")
    total_enroll = st.number_input("Total Enrollment Target", min_value=100, max_value=1000000, value=1000, step=100)
    demo_target = {}
    total_demo = 0
    import random
    for category in ["Gender", "Race"]:
        for key, value in target[category].items():
            col_demo, col_fail = st.columns([3, 2])
            with col_demo:
                val = st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"demo_input_{key}")
            with col_fail:
                if key == "Female":
                    fail_val = 60.0
                elif key == "Male":
                    fail_val = 30.0
                elif key == "White, NH":
                    fail_val = 20.0
                elif key == "Hispanic":
                    fail_val = 65.0
                elif key == "Black, NH":
                    fail_val = 60.0
                elif key == "Asian, NH":
                    fail_val = 60.0
                else:
                    fail_val = float(random.randint(41, 65))
                fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=100.0, value=fail_val, step=1.0, key=f"sf_demo_{key}")
            demo_target[key] = val
            DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val / 100.0
            total_demo += val
    st.markdown(f"**Total: {total_demo:.1f}%**")
st.markdown(f"**Target Enrollment by Race for {disease}**")
    total_enroll = st.number_input("Total Enrollment Target", min_value=100, max_value=1000000, value=1000, step=100)
    demo_target = {}
    total_demo = 0
    for category in ["Gender", "Race"]:
        for key, value in target[category].items():
            col_demo, col_fail = st.columns([3, 2])
            with col_demo:
                val = st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"demo_input_{key}")
            with col_fail:
                default_fail = DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25) * 100
                fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=100.0, value=default_fail, step=1.0, key=f"sf_demo_{key}")
            demo_target[key] = val
            DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val / 100.0
            total_demo += val
    st.markdown(f"**Total: {total_demo:.1f}%**")

with col3:
    st.markdown("**Estimated Quantity Needed to Screen to Reach Target**")
    demo_estimates = []
    for key, val in demo_target.items():
        prevalence = DISEASE_PREVALENCE[disease].get("Gender", {}).get(key,
                     DISEASE_PREVALENCE[disease].get("Race", {}).get(key, DISEASE_PREVALENCE[disease]["overall"]))
        fail_rate = DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.5)
        eligible_with_condition = total_disease_pop * prevalence
        needed_in_trial = (val / 100) * total_enroll
        to_screen = needed_in_trial * (1 + fail_rate)
        screen_percent = (to_screen / eligible_with_condition) * 100 if eligible_with_condition > 0 else 0
        demo_estimates.append((key, to_screen, screen_percent))
    for key, to_screen, screen_percent in sorted(demo_estimates, key=lambda x: -x[2]):
        st.markdown(f"{key}: {int(to_screen):,} ({screen_percent:.3f}%) to screen")
        st.caption(f"To reach target enrollment numbers, approximately {screen_percent:.3f}% of eligible {key} individuals must be screened.")
