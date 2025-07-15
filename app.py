# MEDBOT Ultra-X (Advanced Streamlit Web App Version)
# Author: ChatGPT + Varnika

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import webbrowser

# Load dataset
data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv")

# Train model
X = data.drop('Outcome', axis=1)
y = data['Outcome']
model = DecisionTreeClassifier()
model.fit(X, y)

# Health tips
health_tips = {
    "COVID-19": "Isolate yourself and get tested. Wear a mask and consult a doctor.",
    "Flu": "Rest, drink plenty of fluids, and consider paracetamol for fever.",
    "Common Cold": "Use steam inhalation and warm fluids. Avoid cold drinks.",
    "Allergy": "Avoid allergens. You may take an antihistamine after medical consultation.",
    "Stomach Ache": "Avoid oily food, stay hydrated, and rest. Seek help if pain increases."
}

# Hindi Translations (simplified)
hindi_dict = {
    "Select symptoms": "लक्षण चुनें",
    "Diagnose Me": "जांच करें",
    "Your diagnosis is": "आपका निदान है",
    "Health Tip": "स्वास्थ्य सुझाव",
    "Feedback": "प्रतिक्रिया",
    "Submit": "जमा करें",
    "Language": "भाषा",
}

# UI starts here
st.set_page_config(page_title="MEDBOT Ultra-X", layout="centered")

st.title("🤖 MEDBOT Ultra-X")
st.markdown("An AI-powered medical assistant for quick symptom diagnosis and health support.")

# Language toggle
lang = st.radio("Language / भाषा", ["English", "Hindi"])
translate = lambda x: hindi_dict.get(x, x) if lang == "Hindi" else x

# Symptoms selection
symptom_list = ["Fever", "Cough", "Fatigue", "Body Ache", "Sore Throat", "Loss of Smell", "Runny Nose", "Diarrhea"]
st.markdown(f"### {translate('Select symptoms')}")
selected = st.multiselect("", symptom_list)

# Predict button
if st.button(translate("Diagnose Me")):
    if len(selected) == 0:
        st.warning("Please select at least one symptom.")
    else:
        # Fake logic for demo
        if "Fever" in selected and "Cough" in selected:
            result = "COVID-19"
        elif "Fatigue" in selected and "Body Ache" in selected:
            result = "Flu"
        elif "Runny Nose" in selected:
            result = "Common Cold"
        elif "Sore Throat" in selected:
            result = "Allergy"
        elif "Diarrhea" in selected:
            result = "Stomach Ache"
        else:
            result = "Unable to Diagnose"

        st.success(f"{translate('Your diagnosis is')}: {result}")

        if result in health_tips:
            st.info(f"💡 {translate('Health Tip')}: {health_tips[result]}")

# Health Stats Chart (for visuals)
st.markdown("### 📊 Symptom Trends (Dummy Data)")
chart_data = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Symptom Cases": np.random.randint(10, 50, 5)
})
chart = alt.Chart(chart_data).mark_bar().encode(
    x='Day',
    y='Symptom Cases',
    color=alt.Color('Symptom Cases', scale=alt.Scale(scheme='reds'))
)
st.altair_chart(chart, use_container_width=True)

# Feedback Form
st.markdown(f"### {translate('Feedback')}")
feedback = st.text_area("Share your experience with MEDBOT Ultra-X")
if st.button(translate("Submit")):
    st.success("✅ Thanks for your feedback!")

# Footer
st.markdown("---")
st.caption("© 2025 MEDBOT Ultra-X | Human-AI Collaboration Project")
