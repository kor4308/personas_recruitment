import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --- Constants ---
US_CENSUS = {
    "Gender": {"Female": 51.0, "Male": 49.0},
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
        "Other": 1.9
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
disease = st.selectbox("Select Disease", ["Alzheimer's", "Bipolar Disorder", "Other"])

# --- Column Layout ---
col1, col2, col3 = st.columns([1, 1, 1])

# --- Determine Target ---
if disease == "Alzheimer's":
    target = ALZHEIMERS_TARGET
elif disease == "Bipolar Disorder":
    target = BIPOLAR_TARGET
else:
    target = US_CENSUS

# --- Functions ---
def adjustable_input(label, default):
    return st.number_input(label, min_value=0.0, max_value=100.0, value=float(default), step=0.1, key=f"input_{label}")

# --- Gender Section ---
st.subheader("Gender Comparison")
with col1:
    st.markdown("**Proportion of US (2023), Age 18+**")
    gender_census = US_CENSUS["Gender"]
    for key, value in gender_census.items():
        st.text(f"{key}: {value}%")

with col2:
    st.markdown(f"**Gender targets for {disease}**")
    gender_target = {}
    total_gender = 0
    for key, value in target["Gender"].items():
        val = adjustable_input(key, value)
        gender_target[key] = val
        total_gender += val
    st.markdown(f"**Total: {total_gender:.1f}%**")

with col3:
    st.markdown("**⬆️ Populations needing increased recruitment focus**")
    gender_diffs = [(key, gender_target[key] - gender_census[key]) for key in gender_census if gender_target[key] - gender_census[key] > 0]
    for key, diff in sorted(gender_diffs, key=lambda x: -x[1]):
        st.markdown(f"<span style='color:green'>{key}: {diff:+.1f}%</span>", unsafe_allow_html=True)

# --- Race Section ---
with col1:
    st.markdown("**Proportion of US (2023), Age 18+**")
    race_census = US_CENSUS["Race"]
    for key, value in race_census.items():
        st.text(f"{key}: {value}%")

with col2:
    st.markdown(f"**Demographic targets for {disease}**")
    race_target = {}
    total_race = 0
    for key, value in target["Race"].items():
        val = adjustable_input(key, value)
        race_target[key] = val
        total_race += val
    st.markdown(f"**Total: {total_race:.1f}%**")

with col3:
    st.markdown("**⬆️ Populations needing increased recruitment focus**")
    race_diffs_pos = [(key, race_target[key] - race_census[key]) for key in race_census if race_target[key] - race_census[key] > 0]
    for key, diff in sorted(race_diffs_pos, key=lambda x: -x[1]):
        st.markdown(f"<span style='color:green'>{key}: {diff:+.1f}%</span>", unsafe_allow_html=True)

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
st.markdown("---")
st.header(f"Strategy Recommendations For {disease}")
st.caption("🔻 Ordered by largest to smallest gap")
if disease == "Alzheimer's":
    combined_diffs = gender_diffs + race_diffs_pos
    combined_diffs_sorted = sorted(combined_diffs, key=lambda x: -x[1])

    for key, diff in combined_diffs_sorted:
        if key == "Female":
            st.markdown("**Female:**")
            st.markdown("- Connect with research registries and women’s health organizations.")
            st.markdown("- Provide resources and scheduling flexibility for women in caregiving roles.")
        elif key == "Male":
            st.markdown("**Male:**")
            st.markdown("- Address stigma and increase awareness around cognitive screening.")
        elif key == "Black, NH":
            st.markdown("**Black, NH:**")
            st.markdown("- Avoid or reassess the need use of CDR screening and logical memory scoring to improve inclusivity.")
            st.markdown("- Offer resources to support nonspousal study partners (hybrid visits, productive workshops).")
        elif key == "Hispanic":
            st.markdown("**Hispanic:**")
            st.markdown("- Avoid or reassess the need for MMSE and logical memory scoring as these can be barriers.") MMSE and logical memory scoring as these can be barriers.")
            st.markdown("- Provide culturally sensitive materials and Spanish-speaking resources.")
            st.markdown("- Combat stigma through education and myth-busting outreach.")
        elif key == "Asian, NH":
            st.markdown("**Asian, NH:**")
            st.markdown("- Emphasize how Alzheimer's differs from normal aging to improve detection and participation.")
        elif key == "AIAN, NH":
            st.markdown("**AIAN, NH:**")
            st.markdown("- Use community-based events to build trust.")
            st.markdown("- Offer transportation support and involve tribal health leaders.")
        elif key == "NHPI, NH":
            st.markdown("**NHPI, NH:**")
            st.markdown("- Incorporate family-based and holistic outreach models.")
            st.markdown("- Highlight research as a tool for long-term community wellness.")
        elif key == "Other":
            st.markdown("**Other:**")
            st.markdown("- Apply personalized outreach through local community and faith groups.")
            st.markdown("- Translate materials and provide multilingual staff if needed.")
