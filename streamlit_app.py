import streamlit as st
import plotly.graph_objects as go

def main():
    st.title("Alzheimer's Disease Persona Quantifier")
    
    # Sidebar for Persona Characteristics
    st.sidebar.header("Persona Characteristics")
    race = st.sidebar.selectbox("Race", ["White", "African American", "Hispanic", "Asian", "Other"])
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    family_history = st.sidebar.selectbox("Family History of Alzheimer's", ["Yes", "No"])
    study_partner = st.sidebar.selectbox("Type of Study Partner", ["Spousal", "Son/Daughter", "Non-Family"])

    # Recruitment Strategy Inputs
    col1, col2 = st.columns(2)
    with col2:
        st.header("Recruitment Strategy")
        recruitment_strategy = st.selectbox("Return Personal Results?", ["Do not return personal results", "Return personal results"])
        childcare_services = st.selectbox("Provide Childcare Services?", ["No", "Yes"])
        cultural_practices = st.selectbox("Recruitment Leverages Cultural Practices?", ["No", "Yes"])
        emphasize_generations = st.selectbox("Emphasize Impact on Future Generations?", ["No", "Yes"])

    # Initialize base scores
    race_score = {
        "White": 80,
        "African American": 40,
        "Hispanic": 50,
        "Asian": 50,
        "Other": 50
    }[race]

    gender_score = 65 if gender == "Male" else 45
    family_score = 80 if family_history == "Yes" else 20
    partner_score = {"Spousal": 85, "Son/Daughter": 60, "Non-Family": 40}[study_partner]

    # Bonus labels to display
    bonus_labels = []
    motivators = []

    # Apply family history return bonus
    if recruitment_strategy == "Return personal results" and family_history == "Yes":
        family_score += 20
        family_score = min(family_score, 100)
        bonus_labels.append("✅ Bonus Applied: Returning personal results boosted family history score.")

    # Childcare bonus
    if childcare_services == "Yes":
        if study_partner == "Spousal":
            partner_score += 2
        elif study_partner == "Son/Daughter":
            partner_score += 15
        else:
            partner_score += 8
    partner_score = min(partner_score, 100)

    # Apply recruitment bonuses to RACE SCORE
    if cultural_practices == "Yes":
        if race == "White":
            race_score += 2
        else:
            race_score += 8
        bonus_labels.append("✅ Bonus Applied: Cultural practices leveraged for recruitment.")
        motivators.append("🟢 Recruitment strategy aligns with cultural practices.")
    if emphasize_generations == "Yes":
        if family_history == "Yes" or race == "African American":
            race_score += 6
        else:
            race_score += 3
        bonus_labels.append("✅ Bonus Applied: Future generations impact emphasized.")
        motivators.append("🟢 Emphasizing legacy motivates participation.")
    race_score = min(race_score, 100)

    # Final score across the 4 axes
    total_score = (race_score + gender_score + family_score + partner_score) / 4

    # Radar Chart
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[race_score, gender_score, family_score, partner_score],
        theta=["Race", "Gender", "Family History", "Study Partner"],
        fill="toself",
        name="Risk Factors",
        line=dict(color="blue"),
        fillcolor="rgba(0, 100, 255, 0.3)"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Alzheimer's Risk Factors",
        height=500,
        width=600
    )

    # Display chart and score
    st.plotly_chart(fig)
    st.subheader(f"Total Score: {total_score:.1f}")

    for label in bonus_labels:
        st.success(label)

    # Scoring Explanation
    st.markdown("### Scoring System")
    st.write("""
    - **Race Base Score**: White (80), African American (40), Hispanic/Asian/Other (50)
    - **Race Bonuses**:
        - +2 if cultural practices used (White)
        - +8 if cultural practices used (Others)
        - +6 if African American or Family History = Yes and future generations emphasized
        - +3 otherwise
    - **Gender**: Male (65 pts), Female (45 pts)
    - **Family History**: Yes (80 pts), No (20 pts)
        - +20 pts if returning personal results
    - **Study Partner**: Spousal (85), Son/Daughter (60), Non-Family (40)
        - +2–15 pts if childcare provided
    - **Total Score** = Average of Race, Gender, Family, Study Partner
    """)
    st.warning("Note: This is a simplified example for educational purposes.")

    # Behavioral Motivators and Avoiders
    st.markdown("### Behavioral Motivators and Avoiders")

    for m in motivators:
        st.success(m)

    avoider_messages = []
    if study_partner == "Son/Daughter" and childcare_services == "No":
        avoider_messages.append("🔴 Commitments, such as family life, prevent study partner, thus patient, participation.")
    if race != "White":
        avoider_messages.append("🔴 Medical mistrust due to historical injustices may reduce willingness to participate.")

    if avoider_messages:
        st.error("\n".join(avoider_messages))

if __name__ == "__main__":
    main(
