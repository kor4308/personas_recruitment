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
    age_group = st.selectbox("Select Age Inclusion Criteria", ["60+", "70+", "80+"])
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
# Constants
if disease == "Alzheimer's" and age_group:
    if age_group == "60+":
        US_TOTAL_POP = 75000000
    elif age_group == "70+":
        US_TOTAL_POP = 45000000
    elif age_group == "80+":
        US_TOTAL_POP = 20000000
else:
    US_TOTAL_POP = 342_000_000

# Disease Prevalence Estimates
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
st.subheader("Gender Comparison")
with col1:
    if disease == "Alzheimer's" and age_group:
        st.markdown(f"**🧓 US Census (2023), Population {age_group}**")
    else:
        st.markdown("**US Census (2023) Population Estimate**")
    gender_census = US_CENSUS["Gender"]
    for key, value in gender_census.items():
        st.text(f"{key}: {value}%")

with col2:
    st.markdown(f"**Gender targets for {disease}**")
    st.caption("These demographic targets are not validated.")
    
    gender_target = {}
    total_gender = 0
    for key, value in target["Gender"].items():
        col_gender, col_fail = st.columns([3, 2])
        with col_gender:
            val = adjustable_input(f"{key} (%)", value)
        with col_fail:
            fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=1.0, value=DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25), step=0.01, key=f"sf_race_{key}")
        gender_target[key] = val
        DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val
        total_gender += val
            fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=1.0, value=DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25), step=0.01, key=f"sf_race_{key}")
    race_target[key] = val
    DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val
    st.markdown(f"**Total: {total_gender:.1f}%**")

    st.markdown(f"**Demographic targets for {disease}**")
st.caption("These demographic targets are not validated.")
race_target = {}
    for key, value in target["Race"].items():
    col_race, col_fail = st.columns([3, 2])
    with col_race:
        val = adjustable_input(f"{key} (%)", value)
    with col_fail:
        fail_val = st.number_input("Screen Fail %", min_value=0.0, max_value=1.0, value=DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25), step=0.01, key=f"sf_race_{key}")
    race_target[key] = val
    DISEASE_PREVALENCE[disease]["screen_fail"][key] = fail_val

with col3:
    st.markdown("**📊 Estimated Quantity needed to screen to reach target**")
    estimated_screens = []
    for key in gender_target:
        pct = gender_target[key] / 100
        prev = DISEASE_PREVALENCE[disease]["Gender"].get(key, DISEASE_PREVALENCE[disease]["overall"])
        fail = DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25)
        census_pct = US_CENSUS["Gender"].get(key, 0)
        total_group_pop = US_TOTAL_POP * census_pct / 100
        needed_enroll = US_TOTAL_POP * pct * prev
        estimated_screen = needed_enroll * (1 + fail)
        screen_ratio = estimated_screen / total_group_pop if total_group_pop else 0
        estimated_screens.append((key, estimated_screen, screen_ratio))

    
    for key in race_target:
        pct = race_target[key] / 100
        prev = DISEASE_PREVALENCE[disease]["Race"].get(key, DISEASE_PREVALENCE[disease]["overall"])
        fail = DISEASE_PREVALENCE[disease]["screen_fail"].get(key, 0.25)
        census_pct = US_CENSUS["Race"].get(key, 0)
        total_group_pop = US_TOTAL_POP * census_pct / 100
        needed_enroll = US_TOTAL_POP * pct * prev
        estimated_screen = needed_enroll * (1 + fail)
        screen_ratio = estimated_screen / total_group_pop if total_group_pop else 0
        estimated_screens.append((key, estimated_screen, screen_ratio))

    estimated_screens_sorted = sorted(estimated_screens, key=lambda x: -x[2])
    for key, estimate, ratio in estimated_screens_sorted:
        st.markdown(f"<span style='color:green'>{key}: {int(estimate):,} people to screen</span>", unsafe_allow_html=True)
        st.caption(f"To reach target enrollment numbers, approximately {ratio:.1%} of eligible {key} individuals must be screened.")

# --- Recruitment Motivators Section ---
st.markdown("---")
st.header("General Recruitment Motivators")
if disease == "Alzheimer's":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<span style='color:green'>●</span> **Recruitment Motivators**", unsafe_allow_html=True)
        st.markdown("<span style='color:green'>●</span> Trusted voices (HCP referral and Research Centers)<br><span style='color:green'>●</span> Altruism<br><span style='color:green'>●</span> Education & Disease Awareness<br><span style='color:green'>●</span> Personal Benefit (especially among early-stage AD)", unsafe_allow_html=True)
    with col2:
        st.markdown("<span style='color:red'>●</span> **Recruitment Barriers & Solutions**", unsafe_allow_html=True)
        st.markdown("<span style='color:red'>●</span> Study Partner Barriers → Provide logistical and emotional support to study partners<br><span style='color:red'>●</span> Procedure/Investigational Burden → Shift to blood-based biomarkers and hybrid visit flexibility<br><span style='color:red'>●</span> Disease Stigma → Normalize participation through storytelling and community leaders<br><span style='color:red'>●</span> Population Considerations → Address cultural/linguistic accessibility and trusted communication", unsafe_allow_html=True)
elif disease == "Bipolar Disorder":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<span style='color:green'>●</span> **Recruitment Motivators**", unsafe_allow_html=True)
        st.markdown("<span style='color:green'>●</span> Access to mental health care<br><span style='color:green'>●</span> Hope for improved personal outcomes<br><span style='color:green'>●</span> Financial compensation<br><span style='color:green'>●</span> Peer influence or community-based encouragement", unsafe_allow_html=True)
    with col2:
        st.markdown("<span style='color:red'>●</span> **Recruitment Barriers & Solutions**", unsafe_allow_html=True)
        st.markdown("<span style='color:red'>●</span> Stigma → Partner with mental health advocacy orgs to reduce fear and misinformation<br><span style='color:red'>●</span> Medication concerns → Clearly explain risks and benefits during informed consent<br><span style='color:red'>●</span> Time & Life disruption → Offer flexible scheduling, virtual participation<br><span style='color:red'>●</span> Trust in research → Use transparency and patient testimonials", unsafe_allow_html=True)
        st.caption("Note: These are not informed recommendations specific to bipolar disorder, but general possibilities.")

# --- Strategy Recommendations ---
# Calculate gender_diffs and race_diffs_pos for strategy sorting
    gender_diffs = []
    for key in gender_target:
        target_val = gender_target[key]
        census_val = US_CENSUS["Gender"].get(key, 0)
        diff = target_val - census_val
        if diff > 0:
            gender_diffs.append((key, diff))

    race_diffs_pos = []
    for key in race_target:
        target_val = race_target[key]
        census_val = US_CENSUS["Race"].get(key, 0)
        diff = target_val - census_val
        if diff > 0:
            race_diffs_pos.append((key, diff))
st.markdown("---")
st.header(f"Strategy Recommendations For {disease}")
st.caption("🔻 Ordered by largest to smallest gap")
if disease == "Alzheimer's":
    combined_diffs = gender_diffs + race_diffs_pos
    combined_diffs_sorted = sorted(combined_diffs, key=lambda x: -x[1])

    for key, diff in combined_diffs_sorted:
        # Match estimated ratio from earlier section
        ratio_text = next((f"To reach target enrollment numbers, approximately {ratio:.1%} of eligible {key} individuals must be screened." for k, _, ratio in estimated_screens_sorted if k == key), None)

        if key == "Female":
            st.markdown("**Female:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Connect with research registries and women’s health organizations.")
            st.markdown("- Provide resources and scheduling flexibility for women in caregiving roles.")

        elif key == "Male":
            st.markdown("**Male:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Address stigma and increase awareness around cognitive screening.")

        elif key == "Black, NH":
            st.markdown("**Black, NH:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Avoid or reassess the need use of CDR screening and logical memory scoring to improve inclusivity.")
            st.markdown("- Offer resources to support nonspousal study partners (hybrid visits, productive workshops).")

        elif key == "Hispanic":
            st.markdown("**Hispanic:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Avoid or reassess the need for MMSE and logical memory scoring as these can be barriers.")
            st.markdown("- Provide culturally sensitive materials and Spanish-speaking resources.")
            st.markdown("- Combat stigma through education and myth-busting outreach.")

        elif key == "Asian, NH":
            st.markdown("**Asian, NH:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Emphasize how Alzheimer's differs from normal aging to improve detection and participation.")

        elif key == "AIAN, NH":
            st.markdown("**AIAN, NH:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Use community-based events to build trust.")
            st.markdown("- Offer transportation support and involve tribal health leaders.")

        elif key == "NHPI, NH":
            st.markdown("**NHPI, NH:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Incorporate family-based and holistic outreach models.")
            st.markdown("- Highlight research as a tool for long-term community wellness.")

        elif key == "Other":
            st.markdown("**Other:**")
            if ratio_text: st.caption(ratio_text)
            st.markdown("- Apply personalized outreach through local community and faith groups.")
            st.markdown("- Translate materials and provide multilingual staff if needed.")

        elif key == "White, NH":
            st.markdown("**White, NH:**")
            if ratio_text:
                st.caption(ratio_text)
            st.markdown("- Collaborate with primary care and memory clinics in suburban and rural areas.")
            

