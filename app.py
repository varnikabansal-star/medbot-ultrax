# MEDBOT Ultra-X (Restored & Enhanced Version)
# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import pyttsx3
import datetime
import random

# ------------------ SETUP ------------------
st.set_page_config(page_title="MEDBOT Ultra-X", layout="centered")
st.title("🤖 MEDBOT Ultra-X: AI Health Assistant")
st.markdown("An AI-based tool for basic symptom check, diagnosis & health tips.")

# Language toggle
lang = st.radio("Choose Language / झीओ भाषा चुनें:", ["English", "Hindi"])

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    engine.say(text)
    engine.runAndWait()

# ------------------ SYMPTOMS ------------------
all_symptoms = [
    "Fever", "Cough", "Headache", "Sore throat", "Fatigue", "Vomiting", "Diarrhea", "Shortness of breath",
    "Chest pain", "Runny nose", "Muscle pain", "Joint pain", "Rash", "Sneezing", "Loss of smell", "Loss of taste",
    "Stomach pain", "Dizziness", "Sweating", "Weight loss", "Nausea", "Chills", "Dry mouth", "Blurred vision"
]

# Symptom Input
st.subheader("Select your symptoms:")
selected_symptoms = st.multiselect("", all_symptoms, help="Select all the symptoms you're experiencing")

# ------------------ AI DIAGNOSIS ------------------
model = DecisionTreeClassifier()

# Dummy training data (for offline demo)
data = pd.DataFrame({
    "Fever": [1, 0, 1, 1, 0],
    "Cough": [1, 1, 0, 1, 0],
    "Headache": [0, 1, 1, 0, 1],
    "Fatigue": [1, 0, 1, 0, 0],
    "Diagnosis": ["Flu", "Cold", "Migraine", "COVID-19", "Healthy"]
})

X = data.drop("Diagnosis", axis=1)
y = data["Diagnosis"]
model.fit(X, y)

def diagnose(symptoms):
    input_data = {s: 1 if s in symptoms else 0 for s in X.columns}
    input_df = pd.DataFrame([input_data])
    return model.predict(input_df)[0]

if st.button("Diagnose Me"):
    if not selected_symptoms:
        st.warning("Please select at least one symptom.")
    else:
        result = diagnose(selected_symptoms)
        if lang == "English":
            st.success(f"Based on your symptoms, you may have: {result}")
            speak(f"Your diagnosis is {result}")
        else:
            translations = {"Flu": "जज़काम ", "Cold": "जकन ", "Migraine": "मायग्रेन ", "COVID-19": "कोविड-19", "Healthy": "स्वास्थ्य"}
            hindi_result = translations.get(result, result)
            st.success(f"आपकी जांच के आधार पर आपको {hindi_result} हो सकता है")
            speak(hindi_result)

# ------------------ HEALTH TIPS ------------------
st.subheader("💡 Health Tips")
tips = [
    "Stay hydrated.", "Get at least 8 hours of sleep.", "Wash your hands regularly.",
    "Eat fresh fruits and vegetables.", "Avoid self-medication.", "Exercise daily for 30 minutes."
]
st.info(random.choice(tips))

# ------------------ FEEDBACK ------------------
st.subheader("📝 Feedback")
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    rating = st.slider("Rate MEDBOT", 1, 5)
    comments = st.text_area("Comments")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Thank you for your feedback!")

# ------------------ GRAPH ------------------
st.subheader("📊 Symptom Frequency Chart")
if selected_symptoms:
    fig, ax = plt.subplots()
    counts = [random.randint(10, 100) for _ in selected_symptoms]
    ax.bar(selected_symptoms, counts, color='skyblue')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ------------------ HISTORY ------------------
st.subheader("📁 Diagnosis History")
if "history" not in st.session_state:
    st.session_state.history = []

if selected_symptoms:
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    st.session_state.history.append({"time": time_now, "symptoms": selected_symptoms})

if st.checkbox("Show My Past Checks"):
    for entry in reversed(st.session_state.history):
        st.write(f"🕒 {entry['time']} - Symptoms: {', '.join(entry['symptoms'])}")
