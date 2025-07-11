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

# --- Recruitment Motivators Section ---
st.header("General Recruitment Motivators")
if disease == "Alzheimer's":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Recruitment Motivators**")
        st.markdown("- Trusted voices (HCP referral and Research Centers)\n- Altruism\n- Education & Disease Awareness\n- Personal Benefit (especially among early-stage AD)")
    with col2:
        st.markdown("**Recruitment Barriers & Solutions**")
        st.markdown("- Study Partner Barriers → Provide logistical and emotional support to study partners\n- Procedure/Investigational Burden → Shift to blood-based biomarkers and hybrid visit flexibility\n- Disease Stigma → Normalize participation through storytelling and community leaders\n- Population Considerations → Address cultural/linguistic accessibility and trusted communication")

elif disease == "Bipolar Disorder":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Recruitment Motivators**")
        st.markdown("- Access to mental health care\n- Hope for improved personal outcomes\n- Financial compensation\n- Peer influence or community-based encouragement")
    with col2:
        st.markdown("**Recruitment Barriers & Solutions**")
        st.markdown("- Stigma → Partner with mental health advocacy orgs to reduce fear and misinformation\n- Medication concerns → Clearly explain risks and benefits during informed consent\n- Time & Life disruption → Offer flexible scheduling, virtual participation\n- Trust in research → Use transparency and patient testimonials")
        st.caption("Note: These are not informed recommendations specific to bipolar disorder, but general possibilities.")

st.header("Specific Persona Recruitment")

if disease == "Alzheimer's":
    st.subheader("Gender-Based Personas")
    st.markdown("**Female:** Motivators include personal/family risk awareness, early diagnosis interest, caregiver experience. Barriers include time burden, emotional toll, fear of diagnosis.")
    st.markdown("**Male:** Motivators include cognitive performance awareness and desire to contribute to science. Barriers include stigma, denial, and lower routine healthcare engagement.")

    st.subheader("Race-Based Personas")
    st.markdown("**Hispanic:** Motivators include family-centered decision-making and religious community support. Barriers include language, immigration fears, and healthcare mistrust.")
    st.markdown("**Black, NH:** Motivators include access to care and community advocacy. Barriers include historic mistrust, underrepresentation, and lack of culturally competent materials.")
    st.markdown("**White, NH:** Motivators include high healthcare literacy and research familiarity. Barriers include perceived low personal benefit or time conflicts.")
    st.markdown("**Asian, NH:** Motivators include familial influence and scientific trust. Barriers include stigma, lack of outreach, and limited culturally relevant materials.")
    st.markdown("**AIAN, NH:** Motivators include access to care and intergenerational health. Barriers include geographic isolation, cultural barriers, and systemic distrust.")
    st.markdown("**NHPI, NH:** Motivators include community wellness values. Barriers include limited inclusion in research design and lack of disaggregated data.")
    st.markdown("**Other:** Motivators and barriers may vary. Personalized community engagement is key.")

elif disease == "Bipolar Disorder":
    st.subheader("Gender-Based Personas")
    st.markdown("**Female:** Motivators include access to psychiatric care and mood stabilization. Barriers include childcare needs and stigma.")
    st.markdown("**Male:** Motivators include improving daily functioning and independence. Barriers include lower mental health service use and stigma.")

    st.subheader("Race-Based Personas")
    st.markdown("**Hispanic:** Motivators include family support and bilingual resources. Barriers include stigma, immigration fears, and access.")
    st.markdown("**Black, NH:** Motivators include culturally aligned providers. Barriers include misdiagnosis, distrust, and systemic inequities.")
    st.markdown("**White, NH:** Motivators include treatment history familiarity. Barriers include privacy concerns and time burden.")
    st.markdown("**Asian, NH:** Motivators include improving family relationships. Barriers include stigma and lack of culturally matched care.")
    st.markdown("**AIAN, NH:** Motivators include community support. Barriers include limited access and traditional beliefs.")
    st.markdown("**NHPI, NH:** Motivators include inclusion in holistic care. Barriers include underrepresentation in mental health literature.")
    st.markdown("**Other:** Personalized strategies necessary. Cultural nuances may be overlooked.")
    st.caption("Note: These personas are illustrative and not validated for clinical use.")

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
st.subheader("Race Comparison")
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

    st.markdown("**Other populations**")
    race_diffs_neg = [(key, race_target[key] - race_census[key]) for key in race_census if race_target[key] - race_census[key] < 0]
    for key, diff in sorted(race_diffs_neg, key=lambda x: diff):
        st.markdown(f"<span style='color:red'>{key}: {diff:+.1f}%</span>", unsafe_allow_html=True)
