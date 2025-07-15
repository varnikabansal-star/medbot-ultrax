import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pydeck as pdk

# Language toggle
lang = st.sidebar.radio("Language / भाषा", ["English", "हिन्दी"])

# Title
st.title("🩺 MEDBOT Ultra-X")

# Define UI labels
labels = {
    "English": {
        "select_symptoms": "Select your symptoms:",
        "predict": "Predict Disease",
        "feedback": "Your Feedback:",
        "submit": "Submit",
        "tips": "Health Tips",
        "result": "Predicted Disease:",
        "thank_you": "Thank you for your feedback!",
    },
    "हिन्दी": {
        "select_symptoms": "अपने लक्षण चुनें:",
        "predict": "रोग की भविष्यवाणी करें",
        "feedback": "आपकी प्रतिक्रिया:",
        "submit": "जमा करें",
        "tips": "स्वास्थ्य सुझाव",
        "result": "अनुमानित रोग:",
        "thank_you": "आपकी प्रतिक्रिया के लिए धन्यवाद!",
    }
}[lang]

# Symptoms and Diseases
symptom_list = [
    "Fever", "Cough", "Headache", "Sore Throat", "Fatigue", "Vomiting", "Diarrhea",
    "Rash", "Joint Pain", "Shortness of Breath", "Chest Pain", "Sneezing", "Runny Nose"
]
disease_list = ["Common Cold", "Flu", "COVID-19", "Food Poisoning", "Allergy"]

# Dummy training data
data = pd.DataFrame([
    [1,1,0,1,1,0,0,0,0,1,0,1,1, 2],
    [1,1,1,1,1,0,0,0,0,0,0,1,1, 1],
    [1,1,1,1,1,1,1,0,0,1,1,1,1, 2],
    [0,0,0,0,1,1,1,0,0,0,0,0,0, 3],
    [0,0,0,0,0,0,0,1,1,0,0,1,1, 4],
    [0,1,1,1,0,0,0,0,0,0,0,1,1, 0],
], columns=symptom_list + ["disease"])

X = data[symptom_list]
y = data["disease"]

model = DecisionTreeClassifier()
model.fit(X, y)

# User input
selected_symptoms = st.multiselect(labels["select_symptoms"], symptom_list)

# Voice input script
st.markdown("""
<script>
function recordSpeech() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.toLowerCase();
        const inputs = document.querySelectorAll('input[type="checkbox"]');
        inputs.forEach(input => {
            if (transcript.includes(input.nextSibling.innerText.toLowerCase())) {
                input.click();
            }
        });
    };
    recognition.start();
}
</script>
<button onclick="recordSpeech()">🎙️ Speak Symptoms</button>
""", unsafe_allow_html=True)

# Predict Button
if st.button(labels["predict"]):
    input_data = [1 if sym in selected_symptoms else 0 for sym in symptom_list]
    pred = model.predict([input_data])[0]
    st.success(f"{labels['result']} {disease_list[pred]}")

    st.subheader(labels["tips"])
    tips = {
        "Common Cold": "Drink warm fluids and rest well.",
        "Flu": "Take antiviral meds if prescribed and hydrate.",
        "COVID-19": "Isolate and monitor oxygen levels.",
        "Food Poisoning": "Avoid solid food, stay hydrated.",
        "Allergy": "Avoid allergens and take antihistamines."
    }
    st.info(tips[disease_list[pred]])

    # Bar chart of symptoms
    st.subheader("🩻 Symptom Chart")
    chart_data = pd.DataFrame({
        "Symptoms": symptom_list,
        "Selected": input_data
    })
    st.bar_chart(chart_data.set_index("Symptoms"))

# Feedback
st.subheader("📩 Feedback")
feedback = st.text_area(labels["feedback"])
if st.button(labels["submit"]):
    st.success(labels["thank_you"])
