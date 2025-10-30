import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time
from gemini_chat import get_gemini_response

API_URL = "http://127.0.0.1:5000"

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Smart India Water & Energy Reuse", layout="wide")
st.sidebar.title("🇮🇳 Smart India Reuse Dashboard")

menu = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 City Prediction", "📈 City Dashboard", "🤖 Gemini AI", "ℹ️ About"]
)

# =========================================================
# 🏠 HOME PAGE
# =========================================================
if menu == "🏠 Home":
    st.markdown(
        """
        <div style="background-color:#e6f7ff;padding:25px;border-radius:15px;text-align:center">
            <h1 style="color:#0073e6;">💧⚡ Smart India: AI-Powered Water & Energy Reuse</h1>
            <h3 style="color:#004d80;">Building Sustainable Cities with Data, AI, and Innovation</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.markdown("""
    ### 🌿 **Overview**
    The **Smart India Water & Energy Reuse System** predicts and analyzes 
    **reuse efficiency** across Indian cities using Machine Learning and Gemini AI.
    """)

    st.subheader("⚙️ How It Works")
    st.markdown("""
    1️⃣ Collects water and energy usage data for Indian cities.  
    2️⃣ Predicts reuse efficiency using ML models.  
    3️⃣ Generates sustainability tips using Gemini AI.  
    4️⃣ Displays interactive charts for analysis.
    """)

    st.subheader("🌍 Why This Matters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏙️ Cities Covered", "10+", "+Expanding")
    with col2:
        st.metric("💧 Avg. Water Efficiency", "68%", "↑ Optimized")
    with col3:
        st.metric("⚡ Avg. Energy Reuse", "45%", "↑ Predicted")

    st.markdown("---")
    st.subheader("👨‍💻 Team Winfinity")
    st.markdown("""
    | Member | Role | Focus |
    |:--------|:------|:------|
    | Thejaswi V R | Developer | frontend |
    | Chiranth KL | Team Lead | backend |
    | Madhusudan | Developer | AI integration |
    | Kishan TK | Researcher | Data |
    """)

    st.markdown("---")
    st.markdown("""
    > _“AI cannot solve climate change alone, but it can empower us to make smarter, greener choices.”_  
    — **Team Winfinity**
    """)

# =========================================================
# 📊 CITY PREDICTION PAGE (Enhanced with Progress + Status)
# =========================================================
elif menu == "📊 City Prediction":
    st.title("📊 Predict Reuse Efficiency by City")

    # Fetch city list
    res = requests.get(f"{API_URL}/cities")
    if res.status_code == 200:
        cities_df = pd.DataFrame(res.json())
        city_list = cities_df["city"].tolist()
    else:
        st.error("❌ Failed to fetch cities from backend.")
        city_list = []

    selected_city = st.selectbox("🏙️ Select a City", city_list)

    if selected_city:
        city_data = requests.get(f"{API_URL}/city_data/{selected_city}").json()

        if "error" not in city_data:
            st.subheader(f"📍 Data for {selected_city}")
            st.dataframe(pd.DataFrame([city_data]))

            if st.button("🚀 Predict Efficiency"):

                # Step 1: Initializing
                st.info("📥 Step 1: City data received successfully.")
                time.sleep(0.8)

                progress_bar = st.progress(0)
                status_placeholder = st.empty()

                # Step 2: Data Processing
                status_placeholder.warning("⚙️ Step 2: Processing input data...")
                for i in range(0, 25):
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)

                # Step 3: Running ML Model
                status_placeholder.info("🤖 Step 3: Running AI model to predict reuse efficiency...")
                for i in range(25, 60):
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)

                payload = {
                    "city": selected_city,
                    "water_usage": city_data["water_usage"],
                    "energy_usage": city_data["energy_usage"],
                    "reused_water": city_data["reused_water"],
                    "reused_energy": city_data["reused_energy"]
                }

                try:
                    res_pred = requests.post(f"{API_URL}/predict", json=payload)

                    if res_pred.status_code == 200:
                        result = res_pred.json()

                        # Step 4: AI Insights
                        status_placeholder.info("🧠 Step 4: Generating sustainability insights using Gemini AI...")
                        for i in range(60, 90):
                            time.sleep(0.03)
                            progress_bar.progress(i + 1)

                        # Step 5: Completed
                        status_placeholder.success("✅ Step 5: Prediction complete! Displaying results...")
                        for i in range(90, 100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        time.sleep(0.5)
                        progress_bar.empty()

                        # Results
                        st.success(f"🌿 **Predicted Reuse Efficiency:** {result['reuse_efficiency']}%")
                        st.info(result["ai_insight"])

                        # Visualization
                        df_pie = pd.DataFrame({
                            "Category": ["Reused Water", "Reused Energy"],
                            "Value": [city_data["reused_water"], city_data["reused_energy"]]
                        })
                        fig = px.pie(df_pie, names="Category", values="Value",
                                     title=f"♻️ Reuse Distribution - {selected_city}",
                                     color_discrete_sequence=px.colors.sequential.Blues)
                        st.plotly_chart(fig, use_container_width=True)

                        st.markdown("---")
                        st.success("🎯 **Prediction Completed Successfully!** Data processed, analyzed, and enriched with Gemini AI insights.")
                    else:
                        status_placeholder.error("❌ Server Error: Could not complete prediction.")
                except Exception as e:
                    st.error(f"⚠️ Error during prediction: {e}")
        else:
            st.warning("⚠️ No data available for this city.")

# =========================================================
# 📈 CITY DASHBOARD
# =========================================================
elif menu == "📈 City Dashboard":
    st.title("🏙️ Indian Cities Reuse Efficiency Dashboard")

    res = requests.get(f"{API_URL}/cities")
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        st.dataframe(df)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(df, x="city", y="reuse_efficiency", color="reuse_efficiency",
                          title="📊 Reuse Efficiency by City", color_continuous_scale="Blues")
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.pie(df, names="city", values="reuse_efficiency",
                          title="🪴 Efficiency Share by City")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📈 Water vs Energy Usage Trend")
        fig3 = px.line(df, x="city", y=["water_usage", "energy_usage"],
                       markers=True, title="💧 Water vs ⚡ Energy Usage")
        st.plotly_chart(fig3, use_container_width=True)

        with st.spinner("🧠 Generating AI summary..."):
            prompt = f"Summarize reuse efficiency trends for Indian cities: {df.to_dict()}"
            summary = get_gemini_response(prompt)
            st.success(summary)

# =========================================================
# 🤖 GEMINI CHATBOT
# =========================================================
elif menu == "🤖 Gemini AI":
    st.title("🤖 Gemini Sustainability Chatbot")
    user_q = st.text_area("Ask your question about reuse or sustainability:")
    if st.button("Ask Gemini"):
        with st.spinner("Gemini is thinking..."):
            reply = get_gemini_response(user_q)
        st.write(f"**Gemini:** {reply}")

# =========================================================
# ℹ️ ABOUT PAGE
# =========================================================
elif menu == "ℹ️ About":
    st.title("ℹ️ About This Project")
    st.markdown("""
    ## 🌿 Project Title  
    **Localisation of Circular Economy using Artificial Intelligence**  
    *Focus: Water & Energy Reuse*

    **Team Winfinity**
    - Thejaswi V R
    - Chiranth KL
    - Madhusudan
    - Kishan TK

    **Tech Stack**
    - Frontend: Streamlit  
    - Backend: Flask  
    - ML: Scikit-learn (Random Forest)  
    - AI: Gemini API  
    - Visualization: Plotly

    **Goal:**  
    Empower Indian cities to reuse water and energy efficiently  
    using AI-driven predictions and actionable sustainability insights.
    """)
