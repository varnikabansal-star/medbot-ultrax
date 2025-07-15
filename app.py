import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pyttsx3
from datetime import datetime
import matplotlib.pyplot as plt
import time
import webbrowser
import random
from fpdf import FPDF
import plotly.express as px

# Text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Page setup
st.set_page_config(page_title="🧠 MEDBOT Ultra-X", page_icon="🧬", layout="wide")

# Sidebar: user info
st.sidebar.title("👩‍⚕️ MEDBOT Ultra-X")
lang = st.sidebar.radio("🌐 Language:", ["English", "Hindi"])
theme = st.sidebar.radio("🌓 Theme:", ["Light", "Dark"])
username = st.sidebar.text_input("Your Name:", value="Guest")
st.sidebar.markdown(f"**🕒 Logged in at:** {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

# Translations
translations = {
    'fever': 'बुखार', 'cough': 'खांसी', 'headache': 'सिरदर्द', 'sore_throat': 'गले में खराश',
    'fatigue': 'थकान', 'nausea': 'मतली', 'chills': 'सर्दी लगना', 'vomiting': 'उल्टी',
    'runny_nose': 'बहती नाक', 'body_ache': 'शरीर में दर्द', 'sneezing': 'छींक आना',
    'loss_of_smell': 'गंध की हानि', 'loss_of_taste': 'स्वाद की हानि', 'diarrhea': 'दस्त',
    'eye_pain': 'आंख में दर्द', 'dizziness': 'चक्कर', 'chest_pain': 'सीने में दर्द',
    'shortness_of_breath': 'सांस फूलना', 'rash': 'चकत्ते', 'joint_pain': 'जोड़ों का दर्द',
    'dry_throat': 'सूखा गला', 'muscle_pain': 'मांसपेशियों में दर्द', 'anxiety': 'चिंता',
    'high_blood_pressure': 'उच्च रक्तचाप', 'low_blood_pressure': 'कम रक्तचाप'
}

def trans(s):
    return translations.get(s, s) if lang == "Hindi" else s.replace('_', ' ').capitalize()

user_diagnosis = ""

# Tabs
tabs = st.tabs([
    "🩺 Diagnosis", "💊 Remedies", "📚 Tips", "📈 BMI", "📍 Hospitals", "⏰ Reminder", "📘 Diseases",
    "📄 PDF Report", "📊 Weekly Tracker", "🧠 Chatbot", "🧪 Nutrition Info"
])

# ----- SYMPTOM CHECKER -----
with tabs[0]:
    st.title("🩺 Symptom Checker")
    symptoms = list(translations.keys())
    data = pd.DataFrame({s: [int(i % 2 == j % 2) for i in range(6)] for j, s in enumerate(symptoms)})
    data['disease'] = ['Flu', 'Cold', 'Migraine', 'Food Poisoning', 'Sinus Infection', 'COVID-19']

    X = data[symptoms]
    y = data['disease']
    model = DecisionTreeClassifier()
    model.fit(X, y)

    cols = st.columns(3)
    input_symptoms = {s: cols[i % 3].checkbox(trans(s)) for i, s in enumerate(symptoms)}

    if st.button("🔍 Diagnose"):
        user_input = [[int(input_symptoms[s]) for s in symptoms]]
        prediction = model.predict(user_input)[0]
        user_diagnosis = prediction
        st.success(f"🧾 You may have: {prediction}")
        speak(f"{username}, you may have {prediction}")

# ----- REMEDIES -----
with tabs[1]:
    st.title("💊 Home Remedies")
    choice = st.selectbox("Choose a problem:", ["Cold", "Cough", "Fever", "Headache"])
    st.info({
        "Cold": "Steam, ginger tea, vitamin C-rich fruits.",
        "Cough": "Honey with warm water, tulsi.",
        "Fever": "Paracetamol, sponge bath.",
        "Headache": "Hydration, sleep, mint balm."
    }[choice])

# ----- HEALTH TIPS -----
with tabs[2]:
    st.title("📚 Health Tips")
    for t in ["Sleep well", "Stay hydrated", "Limit screen time", "Walk daily", "Wash hands"]:
        st.markdown(f"✅ {t}")

# ----- BMI -----
with tabs[3]:
    st.title("📈 BMI Calculator")
    h = st.number_input("Height (cm):", 100, 250)
    w = st.number_input("Weight (kg):", 30, 200)
    if st.button("Calculate"):
        bmi = w / ((h/100)**2)
        st.success(f"BMI: {bmi:.2f}")

# ----- HOSPITALS -----
with tabs[4]:
    st.title("📍 Nearby Hospitals")
    if st.button("🔎 Search Google Maps"):
        webbrowser.open("https://www.google.com/maps/search/hospitals+near+me")

# ----- REMINDER -----
with tabs[5]:
    st.title("⏰ Medicine Reminder")
    med = st.text_input("Medicine Name")
    sec = st.slider("Remind in (sec):", 5, 60)
    if st.button("Start Reminder"):
        st.info(f"⏱️ {med} in {sec} sec")
        time.sleep(sec)
        st.warning(f"Take: {med}")
        speak(f"Take medicine: {med}")

# ----- DISEASE EXPLORER -----
with tabs[6]:
    st.title("📘 Disease Info")
    d = st.selectbox("Select Disease:", ["Cold", "Flu", "Migraine"])
    st.markdown(f"### About {d}\n- Symptoms: ...\n- Treatment: ...\n- Prevention: ...")

# ----- PDF REPORT -----
with tabs[7]:
    st.title("📄 Generate PDF Report")
    if st.button("Create PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="MEDBOT Ultra-X Report", ln=1, align='C')
        pdf.cell(200, 10, txt=f"User: {username}", ln=2)
        pdf.cell(200, 10, txt=f"Diagnosis: {user_diagnosis or 'Not diagnosed'}", ln=3)
        pdf.output("medbot_report.pdf")
        st.success("PDF saved as medbot_report.pdf")

# ----- WEEKLY TRACKER -----
with tabs[8]:
    st.title("📊 Weekly Tracker")
    df = pd.DataFrame({
        'Day': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        'Mood (1-10)': [random.randint(4, 10) for _ in range(7)],
        'Water Intake (L)':[round(random.uniform(1.5, 3.5), 2) for _ in range(7)]
    })
    st.plotly_chart(px.bar(df, x="Day", y=["Mood (1-10)", "Water Intake (L)"], barmode='group'))

# ----- AI CHATBOT -----
with tabs[9]:
    st.title("🧠 Ask MEDBOT")
    question = st.text_input("Ask a health question:")
    if st.button("Answer"):
        st.success(f"🤖 Based on '{question}', please consult a physician for confirmation.")

# ----- NUTRITION INFO -----
with tabs[10]:
    st.title("🧪 Nutrition Explorer")
    food = st.selectbox("Select food item:", ["Apple", "Banana", "Milk", "Egg"])
    st.markdown({
        "Apple": "52 kcal, 0.3g protein, 14g carbs",
        "Banana": "96 kcal, 1.3g protein, 27g carbs",
        "Milk": "42 kcal (per 100ml), 3.4g protein",
        "Egg": "77 kcal, 6g protein, 5g fat"
    }[food])

# Footer
st.markdown("---")
st.markdown("Made with 💖 by Team Varnika | Vasudha 2025–26")
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
from fpdf import FPDF

# Title
st.set_page_config(page_title="MEDBOT Ultra-X", layout="wide")
st.title("🤖 MEDBOT Ultra-X: AI Symptom Checker & Health Assistant")

st.markdown("---")

# Symptom List (You can expand this easily)
symptoms = [
    "Fever", "Cough", "Cold", "Fatigue", "Headache", "Body Pain", "Nausea", 
    "Vomiting", "Diarrhea", "Sore Throat", "Shortness of Breath", "Chest Pain",
    "Loss of Smell", "Loss of Taste", "Skin Rash", "Sneezing"
]

# Disease database (very basic sample, can be expanded)
disease_data = {
    "Fever": ["Flu", "COVID-19", "Malaria"],
    "Cough": ["Flu", "COVID-19", "Bronchitis"],
    "Cold": ["Common Cold", "Allergy"],
    "Headache": ["Migraine", "Sinusitis"],
    "Fatigue": ["Anemia", "Thyroid Issues"],
    "Nausea": ["Food Poisoning", "Gastritis"],
    "Chest Pain": ["Heart Attack", "Anxiety"]
}

# Symptom input
st.subheader("🩺 Select Your Symptoms")
selected_symptoms = st.multiselect("Choose all symptoms you're experiencing:", symptoms)

# Button to Diagnose
if st.button("🔍 Diagnose"):
    if not selected_symptoms:
        st.warning("Please select at least one symptom.")
    else:
        matched_diseases = []
        for symptom in selected_symptoms:
            matched_diseases.extend(disease_data.get(symptom, []))

        # Count and rank diseases
        disease_count = pd.Series(matched_diseases).value_counts()
        top_diseases = disease_count.head(3)

        st.success("✅ Possible Conditions Based on Your Symptoms:")
        for i, (disease, count) in enumerate(top_diseases.items(), 1):
            st.markdown(f"**{i}. {disease}** (matched {count} symptom{'s' if count > 1 else ''})")

        # Pie Chart
        fig = px.pie(values=top_diseases.values, names=top_diseases.index, title="Prediction Distribution")
        st.plotly_chart(fig)

        # Download PDF Report
        def create_pdf(symptoms, predictions):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="MEDBOT Ultra-X Health Report", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Symptoms Selected:", ln=True)
            for s in symptoms:
                pdf.cell(200, 8, txt=f"- {s}", ln=True)
            pdf.ln(5)
            pdf.cell(200, 10, txt="Top Predictions:", ln=True)
            for i, (disease, score) in enumerate(predictions.items(), 1):
                pdf.cell(200, 8, txt=f"{i}. {disease} (matched {score} symptoms)", ln=True)
            return pdf

        pdf = create_pdf(selected_symptoms, top_diseases)
        pdf.output("medbot_report.pdf")
        with open("medbot_report.pdf", "rb") as f:
            st.download_button("📄 Download PDF Report", f, file_name="medbot_report.pdf")

# About Section
st.markdown("---")
with st.expander("📘 About MEDBOT Ultra-X"):
    st.write("""
    MEDBOT Ultra-X is a powerful AI-powered health assistant designed for educational use.
    It analyzes user-selected symptoms to suggest possible conditions based on basic matching algorithms.
    The app demonstrates how humans and AI can collaborate in early disease detection and healthcare education.
    """)

# Footer
st.markdown("🔬 Developed as a Vasudha Project on Human-AI Collaboration | © 2025 Team MEDBOT Ultra-X")
