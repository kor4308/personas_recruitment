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
            "Black, NH": 0.35,
            "Hispanic": 0.28,
            "Asian, NH": 0.50,
            "AIAN, NH": 0.50,
            "NHPI, NH": 0.50,
            "Other": 0.50
        },
        "screen_fail": {}
    },
    "Schizophrenia": {
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "Black, NH", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
    },
    "Bipolar Disorder": {
        "screen_fail": {k: 0.5 for k in ["Female", "Male", "White, NH", "Black, NH", "Hispanic", "Asian, NH", "AIAN, NH", "NHPI, NH", "Other"]}
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

with col1.expander("US Demographics and Disease Epidemiology"):
    st.subheader("2023 US Census")
    st.caption("Information in this section is from the 2023 US Census.")
    st.markdown(f"**Total U.S. Population:** {US_TOTAL_POP:,}")
    g_col, r_col = st.columns(2)
    with g_col:
        st.subheader("Gender")
        for k, v in current_us["Gender"].items():
            count = int((v / 100) * US_TOTAL_POP)
            st.markdown(f"{k}: {v}%")
            st.caption(f"There are ~{count:,} {k} individuals in the United States")
    with r_col:
        st.subheader("Race")
        for k, v in current_us["Race"].items():
            count = int((v / 100) * US_TOTAL_POP)
            st.markdown(f"{k}: {v}%")
            st.caption(f"There are ~{count:,} {k} individuals in the United States")

    if disease in ["Alzheimer's", "Bipolar Disorder", "Schizophrenia"]:
        st.markdown("---")
        st.subheader(f"Disease Epidemiology in {disease} (Estimated)")
        if disease == "Alzheimer's":
            st.caption("Information provided is from the 2023 Alzheimer's Report (Alzheimer's Association Journal). AIAN and NHPI races were not accounted for in this report, thus they are from the internet.")
        else:
            st.caption("These numbers are from the internet.")
        disease_total = DISEASE_TOTALS.get(pop_key)
        if disease_total:
            st.markdown(f"**Total population with {disease}: {disease_total:,}**")
        g_col2, r_col2 = st.columns(2)
        with g_col2:
            st.subheader("Gender")
            for k, v in target["Gender"].items():
                count = int((v / 100) * disease_total)
                st.markdown(f"{k}: {v}%")
                st.caption(f"There are ~{count:,} {k} patients with {disease} in the United States")
        with r_col2:
            st.subheader("Race")
            for k, v in target["Race"].items():
                count = int((v / 100) * disease_total)
                st.markdown(f"{k}: {v}%")
                st.caption(f"There are ~{count:,} {k} patients with {disease} in the United States")
            

with col2.expander("Target Enrollment Inputs"):
    total_enroll = st.number_input("Total Enrollment Target", min_value=100, max_value=1000000, value=1000, step=100, key="total_enroll")

    st.markdown("**Gender Target % and Screen Success**")
    for key, value in target["Gender"].items():
        cols = st.columns([2, 2])
        with cols[0]:
            st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"gender_{key}")
        with cols[1]:
            default_success = DISEASE_PREVALENCE[disease].get("screen_success", {}).get(key, 0.5) * 100
            st.number_input("Screen Success %", min_value=0.0, max_value=100.0, value=default_success, step=1.0, key=f"sf_gender_{key}")

    st.markdown("**Race Target % and Screen Success**")
    for key, value in target["Race"].items():
        cols = st.columns([2, 2])
        with cols[0]:
            st.number_input(f"{key} (%)", min_value=0.0, max_value=100.0, value=value, step=0.1, key=f"race_{key}")
        with cols[1]:
            default_success = 100 - DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.5) * 100
            st.number_input("Screen Success %", min_value=0.0, max_value=100.0, value=default_success, step=1.0, key=f"sf_race_{key}")

with col3.expander("Estimated Quantity Needed to Screen"):
    st.markdown("**Estimated Quantity Needed to Screen - Gender**")
    st.caption("⬇️ List is in order from greatest % population needed to screen")
    total_enroll = st.session_state.get("total_enroll", 1000)

    gender_data = []
    for key in target["Gender"]:
        pct = st.session_state.get(f"gender_{key}", target["Gender"][key])
        target_n = total_enroll * (pct / 100)
        screen_success_rate = st.session_state.get(f"sf_gender_{key}", 100) / 100
        screened_needed = math.ceil(target_n / screen_success_rate) if screen_success_rate > 0 else 0
        eligible_pop = int((target["Gender"].get(key, 100) / 100) * total_disease_pop)
        screen_percent = (screened_needed / eligible_pop) * 100 if eligible_pop > 0 else 0
        gender_data.append((key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop))

    gender_data.sort(key=lambda x: -x[2])
    for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in gender_data:
        st.markdown(f"{key}: {screened_needed:,} ({screen_percent:.3f}%)")
        st.caption(f"Approximately {screen_percent:.3f}% of {key} {disease} population must be screened to enroll target")

    st.markdown("**Estimated Quantity Needed to Screen - Race**")
    st.caption("⬇️ List is in order from greatest % population needed to screen")
    race_data = []
    for key in target["Race"]:
        pct = st.session_state.get(f"race_{key}", target["Race"][key])
        target_n = total_enroll * (pct / 100)
        screen_success_rate = st.session_state.get(f"sf_race_{key}", 100) / 100
        screened_needed = math.ceil(target_n / screen_success_rate) if screen_success_rate > 0 else 0
        eligible_pop = int((target["Race"].get(key, 0) / 100) * total_disease_pop)
        screen_percent = (screened_needed / eligible_pop) * 100 if eligible_pop > 0 else 0
        race_data.append((key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop))

    race_data.sort(key=lambda x: -x[2])
    for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in race_data:
        st.markdown(f"{key}: {screened_needed:,} ({screen_percent:.3f}%)")
        st.caption(f"Approximately {screen_percent:.3f}% of {key} {disease} population must be screened to enroll target")

    if st.toggle("Show Calculation Steps"):
        st.markdown("### Calculation Breakdown")
        for category, data in [("Gender", gender_data), ("Race", race_data)]:
            st.markdown(f"**{category} Calculations**")
            for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in data:
                st.text(f"{key}: Target = {target_n:.1f}, Screen Success Rate = {screen_success_rate:.2f}, Eligible Pop = {eligible_pop}, Screened Needed = {screened_needed}, Percent = {screen_percent:.3f}%")


# --- General Recruitment Strategies Section ---
st.markdown("---")
st.header(f"General Motivators and Barriers for {disease}")
st.caption("These motivators and barriers can be explored through Patient dossiers.")
if disease != "Alzheimer's":
    st.caption("Each group below includes an estimate of the % of the {disease} population that must be screened to meet enrollment targets.")

if disease == "Alzheimer's":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Motivators")
        st.markdown("- Trusted Voices")
        st.markdown("- Altruism")
        st.markdown("- Education & Disease Awareness")
        st.markdown("- Personal Benefit")

    with col2:
        st.subheader("⛔ Barriers")
        st.markdown("- Study Partner Requirement")
        st.markdown("- Procedure/Investigational Burden")
        st.markdown("- Disease Stigma")
        st.markdown("- Specific Population Injustices")

# --- Recruitment Strategies for Subgroups ---

st.markdown("---")
st.subheader(f"📣 Recruitment Strategies for Focus Populations with {disease}")
st.caption("⬇️ List is in order from greatest % population needed to screen; thus greatest need to focus")
recruitment_strategies = {
    "Female": [
        "Connect with women's health networks and caregiving support groups",
        "Partner with research registries",
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
    ],
    "Asian, NH": [
        "Partner with Asian community health coalitions or clinics",
        "Promote awareness that dementia is not a normal part of aging"
    ]
}

combined_data = gender_data + race_data
seen = set()
sorted_groups = []
for group, _, screen_percent, *_ in sorted(combined_data, key=lambda x: -x[2]):
    if group not in seen:
        seen.add(group)
        sorted_groups.append(group)

for group in sorted_groups:
    if group in recruitment_strategies:
        match = next((x for x in (gender_data + race_data) if x[0] == group), None)
        if match:
            _, _, screen_percent, *_ = match
            st.markdown(f"**{group}**")
            st.caption(f"Approximately {screen_percent:.3f}% of {group} {disease} population must be screened to enroll target")
        for strat in recruitment_strategies[group]:
            st.markdown(f"- {strat}")
        st.markdown("---")
