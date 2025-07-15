# MEDBOT Ultra-X Final Version
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from fpdf import FPDF
import datetime

# --- CONFIG ---
st.set_page_config(page_title="MEDBOT Ultra-X", layout="centered")

# --- DARK/LIGHT MODE ---
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        header { background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

# --- LANGUAGE TOGGLE ---
lang = st.sidebar.radio("🌐 Language / भाषा:", ["English", "Hindi"])
translate = lambda e, h: h if lang == "Hindi" else e

# --- SYMPTOMS ---
symptoms = ["Fever", "Cough", "Fatigue", "Nausea", "Shortness of breath", "Sore throat", "Loss of taste", "Muscle pain"]
selected_symptoms = st.multiselect(translate("Select Symptoms", "लक्षण चुनें"), symptoms)

# --- DIAGNOSIS MODEL ---
mlb = MultiLabelBinarizer()
X_train = mlb.fit_transform([
    ["Fever", "Cough"],
    ["Fatigue", "Nausea"],
    ["Sore throat", "Cough"],
    ["Loss of taste", "Fever"],
    ["Shortness of breath", "Muscle pain"]
])
y_train = ["Flu", "Food Poisoning", "Cold", "COVID-19", "Asthma"]
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# --- UI HEADER ---
st.title("🤖 MEDBOT Ultra-X")
st.caption(translate("Your AI-powered medical assistant.", "आपका एआई-सक्षम चिकित्सा सहायक।"))

# --- DIAGNOSIS ---
if st.button(translate("🔍 Diagnose Me", "🔍 जांच करें")):
    if selected_symptoms:
        input_data = mlb.transform([selected_symptoms])
        result = model.predict(input_data)[0]
        st.success(translate(f"Possible Condition: {result}", f"संभावित रोग: {result}"))

        # Health Tips
        tips = {
            "Flu": "Drink warm fluids and rest well.",
            "Food Poisoning": "Stay hydrated, eat bland food.",
            "Cold": "Steam inhalation and rest recommended.",
            "COVID-19": "Isolate and consult a physician.",
            "Asthma": "Avoid allergens, use inhaler as prescribed."
        }
        st.info(translate("💡 Health Tip:", "💡 स्वास्थ्य सुझाव:") + " " + tips.get(result, "Consult a doctor."))

        # Home Remedies
        home = {
            "Flu": "Tulsi tea, ginger and honey mix.",
            "Cold": "Steam, turmeric milk.",
            "Food Poisoning": "ORS, jeera water.",
            "Asthma": "Steam, avoid cold items."
        }
        if result in home:
            st.warning(translate("🏡 Home Remedy:", "🏡 घरेलू उपाय:") + " " + home[result])
    else:
        st.error(translate("Please select at least one symptom.", "कृपया कम से कम एक लक्षण चुनें।"))

# --- NUTRITION EXPLORER ---
st.markdown("---")
st.header("🥗 " + translate("Nutrition Explorer", "पोषण जानकारी"))
food = st.selectbox(translate("Choose a food item:", "भोजन चुनें:"), ["Milk", "Egg", "Banana"])
nutrition = {
    "Milk": {"Calories": 42, "Protein": 3.4, "Calcium": 125},
    "Egg": {"Calories": 78, "Protein": 6, "Cholesterol": 186},
    "Banana": {"Calories": 89, "Potassium": 358, "Fiber": 2.6},
}
if food:
    df = pd.DataFrame([nutrition[food]])
    st.table(df)

# --- MOOD & WATER TRACKER ---
st.markdown("---")
st.header("📈 " + translate("Mood & Water Tracker", "मूड और पानी ट्रैकर"))
mood = st.slider(translate("Your Mood Today", "आज का मूड"), 0, 10, 5)
water = st.slider(translate("Glasses of Water", "पानी के गिलास"), 0, 15, 8)
chart_df = pd.DataFrame({"Metric": ["Mood", "Water"], "Score": [mood, water]})
st.plotly_chart(px.bar(chart_df, x="Metric", y="Score", color="Metric", title="Mood & Water Levels"))

# --- PDF GENERATION ---
def generate_pdf(diagnosis):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="MEDBOT Ultra-X Diagnosis Report", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=2, align="L")
    pdf.cell(200, 10, txt=f"Diagnosis: {diagnosis}", ln=3, align="L")
    pdf.output("medbot_report.pdf")
    st.success("📄 PDF Report Saved as medbot_report.pdf")

if selected_symptoms:
    if st.button("📄 Generate PDF Report"):
        result = model.predict(mlb.transform([selected_symptoms]))[0]
        generate_pdf(result)

# --- FEEDBACK ---
st.markdown("---")
st.header("💬 " + translate("Feedback Form", "प्रतिक्रिया फ़ॉर्म"))
name = st.text_input(translate("Your Name", "आपका नाम"))
message = st.text_area(translate("Your Feedback", "आपकी प्रतिक्रिया"))
if st.button(translate("Submit", "जमा करें")):
    st.success(translate("Thank you for your feedback!", "आपकी प्रतिक्रिया के लिए धन्यवाद!"))

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 MEDBOT Ultra-X | Human-AI Collaboration | Built with ❤️")
