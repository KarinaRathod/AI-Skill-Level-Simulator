import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Skill Level Simulator", layout="wide")
st.title("🎮 AI Skill Level Simulator")
st.caption("Understand how skills evolve from beginner to expert")

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# INPUT
# -----------------------------
skill = st.text_input("🎯 Enter a skill (e.g., Coding, Public Speaking)")

# -----------------------------
# GENERATE SIMULATION
# -----------------------------
if st.button("🚀 Simulate Skill Levels"):

    if not skill.strip():
        st.warning("⚠️ Please enter a skill")
        st.stop()

    with st.spinner("🧠 Simulating skill progression..."):

        prompt = f"""
        Simulate skill progression for: {skill}

        Provide 3 levels:

        1. Beginner:
        - Mindset
        - Common mistakes
        - What to focus on

        2. Intermediate:
        - Mindset
        - Challenges
        - What improves

        3. Advanced:
        - Expert thinking
        - Optimization strategies
        - Key insights

        Also include:
        - How to move from Beginner → Advanced
        """

        response = model.generate_content(prompt)
        result = response.text

        st.subheader("📊 Skill Simulation")
        st.write(result)

        st.session_state.history.append(result)

# -----------------------------
# SELF LEVEL DETECTION
# -----------------------------
st.subheader("🧠 Find Your Level")

description = st.text_area("Describe your current ability")

if st.button("🔍 Analyze My Level"):
    if description.strip():
        prompt = f"""
        Based on this description, determine skill level:

        {description}

        Output:
        - Level (Beginner/Intermediate/Advanced)
        - Reason
        - Next steps to improve
        """

        response = model.generate_content(prompt)
        st.write(response.text)

# -----------------------------
# HISTORY
# -----------------------------
if st.session_state.history:
    st.subheader("💾 Past Simulations")

    for item in st.session_state.history[-5:]:
        st.info(item)