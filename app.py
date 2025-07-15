import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import altair as alt

# Load data (mock data for demo)
data = pd.DataFrame({
    'fever': [1, 0, 1, 1, 0],
    'cough': [1, 1, 1, 0, 0],
    'headache': [0, 1, 1, 1, 0],
    'fatigue': [1, 1, 0, 1, 1],
    'nausea': [0, 0, 1, 1, 1],
    'disease': ['Flu', 'Cold', 'COVID-19', 'Malaria', 'Food Poisoning']
})

X = data.drop('disease', axis=1)
y = data['disease']
model = DecisionTreeClassifier()
model.fit(X, y)

# Language toggle
lang = st.sidebar.radio("Language / भाषा:", ["English", "हिंदी"])

# Title
if lang == "English":
    st.title("🧠 MEDBOT Ultra-X - Smart Symptom Checker")
else:
    st.title("🧠 MEDBOT Ultra-X - चुक्ग जांच जांच चेकर")

# Symptom input
symptoms = ['fever', 'cough', 'headache', 'fatigue', 'nausea']
selected_symptoms = st.multiselect("Select your symptoms:", symptoms)

# Diagnosis button
if st.button("Diagnose Me"):
    input_data = [1 if symptom in selected_symptoms else 0 for symptom in symptoms]
    prediction = model.predict([input_data])[0]

    if lang == "English":
        st.success(f"Based on your symptoms, you may have: {prediction}")
    else:
        st.success(f"आपके औचिन की आधार पर, आपको यह जब हो सकता है: {prediction}")

    # Show graph
    chart_data = pd.DataFrame({"Symptoms": symptoms, "Present": input_data})
    chart = alt.Chart(chart_data).mark_bar().encode(
        x='Symptoms', y='Present', color=alt.condition(
            alt.datum.Present > 0, alt.value('orange'), alt.value('lightgray')
        )
    )
    st.altair_chart(chart, use_container_width=True)

# Health Tips
st.markdown("---")
if lang == "English":
    st.header("🩺 General Health Tips")
    st.write("""
    - Stay hydrated
    - Eat a balanced diet
    - Get enough sleep
    - Exercise regularly
    - Avoid stress
    """)
else:
    st.header("🩺 सामान्यिक चिकित्सा")
    st.write("""
    - पानी पीजें
    - संतुलित आहार खाएं
    - पूरी नींद लीजिए
    - नियमित अभ्यास करें
    - चिंता का क्याल रखें
    """)

# Feedback Form
st.markdown("---")
if lang == "English":
    st.subheader("💬 Feedback")
    feedback = st.text_area("What do you think about MEDBOT Ultra-X?")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
else:
    st.subheader("💬 प्रतिक्रिया")
    feedback = st.text_area("MEDBOT Ultra-X के बारे में अपकी क्या राय है?")
    if st.button("जमा करें"):
        st.success("अपका धन्यवाद की लिए धन्यवाद!")
