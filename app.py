import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import time
from gemini_chat import get_gemini_response

API_URL = "http://127.0.0.1:5000"

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Smart India Water & Energy Reuse", layout="wide")
st.sidebar.title("🌍 Smart India Reuse Dashboard")

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

    st.markdown("""
    ### 🌿 Overview
    This platform predicts and analyzes **water and energy reuse efficiency** for major Indian cities.  
    It combines **Machine Learning**, **Gemini AI**, and **data visualization** to help build sustainable cities.
    """)

    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913463.png", width=150)
    st.markdown("---")
    st.markdown("#### 🧠 Powered by:")
    col1, col2, col3 = st.columns(3)
    col1.info("🤖 **Gemini AI** – Insight Generation")
    col2.success("📊 **Streamlit + Plotly** – Visualization")
    col3.warning("⚙️ **Flask + ML** – Prediction Engine")

# =========================================================
# 📊 CITY PREDICTION PAGE (Enhanced)
# =========================================================
elif menu == "📊 City Prediction":
    st.title("📊 Predict Reuse Efficiency by City")

    res = requests.get(f"{API_URL}/cities")
    if res.status_code == 200:
        cities_df = pd.DataFrame(res.json())
        city_list = cities_df["city"].tolist()
    else:
        st.error("❌ Failed to fetch city data from backend.")
        city_list = []

    selected_city = st.selectbox("🏙️ Select a City", city_list)

    if selected_city:
        city_data = requests.get(f"{API_URL}/city_data/{selected_city}").json()

        if "error" not in city_data:
            st.subheader(f"📍 Data for {selected_city}")
            st.dataframe(pd.DataFrame([city_data]))

            if st.button("🚀 Predict Efficiency"):
                st.info("📥 Step 1: City data received successfully.")
                time.sleep(0.7)

                progress_bar = st.progress(0)
                status_placeholder = st.empty()

                # Step 2
                status_placeholder.warning("⚙️ Step 2: Processing data...")
                for i in range(0, 25):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)

                # Step 3
                status_placeholder.info("🤖 Step 3: Running AI model...")
                for i in range(25, 60):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)

                # Send payload to backend
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

                        # Step 4
                        status_placeholder.info("🧠 Step 4: Generating Gemini AI Insights...")
                        for i in range(60, 90):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)

                        # Step 5
                        status_placeholder.success("✅ Step 5: Prediction complete!")
                        for i in range(90, 100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        time.sleep(0.5)
                        progress_bar.empty()

                        # Display prediction result
                        reuse_eff = result["reuse_efficiency"]
                        st.success(f"🌿 **Predicted Reuse Efficiency:** {reuse_eff:.2f}%")

                        # Efficiency level feedback
                        if reuse_eff > 75:
                            st.success("🌟 Excellent! This city is performing very efficiently.")
                        elif reuse_eff > 50:
                            st.warning("⚙️ Moderate efficiency — room for improvement.")
                        else:
                            st.error("🚨 Low reuse efficiency — needs immediate attention.")

                        # AI Insight
                        st.info("🧩 **Gemini AI Suggestions:**")
                        st.write(result["ai_insight"])

                        # Visualization
                        df_pie = pd.DataFrame({
                            "Category": ["Reused Water", "Reused Energy"],
                            "Value": [city_data["reused_water"], city_data["reused_energy"]]
                        })
                        fig_pie = px.pie(df_pie, names="Category", values="Value",
                                         title=f"♻️ Resource Reuse Distribution - {selected_city}",
                                         color_discrete_sequence=px.colors.sequential.Blues)
                        st.plotly_chart(fig_pie, use_container_width=True)

                        # Simulated trend chart
                        st.markdown("#### 📈 Yearly Reuse Trend")
                        trend_years = ["2020", "2021", "2022", "2023", "2024"]
                        trend_values = np.random.randint(40, 100, len(trend_years))
                        df_trend = pd.DataFrame({"Year": trend_years, "Reuse %": trend_values})
                        st.line_chart(df_trend.set_index("Year"))

                        # Download report
                        st.markdown("---")
                        st.download_button(
                            "📥 Download City Report",
                            data=pd.DataFrame([city_data]).to_csv(index=False).encode("utf-8"),
                            file_name=f"{selected_city}_reuse_report.csv",
                            mime="text/csv"
                        )

                    else:
                        status_placeholder.error("❌ Server error while predicting.")
                except Exception as e:
                    st.error(f"⚠️ Error during prediction: {e}")

# =========================================================
# 📈 CITY DASHBOARD
# =========================================================
elif menu == "📈 City Dashboard":
    st.title("🏙️ Indian Cities Reuse Efficiency Dashboard")

    res = requests.get(f"{API_URL}/cities")
    if res.status_code == 200:
        df = pd.DataFrame(res.json())

        st.markdown("### 🏆 City Rankings by Reuse Efficiency")
        st.dataframe(df.sort_values("reuse_efficiency", ascending=False).reset_index(drop=True))

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
    else:
        st.error("❌ Unable to load dashboard data.")

# =========================================================
# 🤖 GEMINI CHAT
# =========================================================
elif menu == "🤖 Gemini AI":
    st.title("🤖 Gemini Sustainability Chatbot")
    st.write("Ask Gemini about sustainability, resource management, or AI solutions.")
    user_q = st.text_area("💬 Ask your question:")
    if st.button("Ask Gemini"):
        with st.spinner("Gemini is thinking..."):
            reply = get_gemini_response(user_q)
        st.info(f"**Gemini:** {reply}")

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
    - 🧠 AI: Gemini 2.0 Flash  
    - ⚙️ Backend: Flask + ML  
    - 🎨 Frontend: Streamlit + Plotly  
    - 🌐 Data: Live (via internet)  

    ### 💡 Objective
    Empower Indian cities to reuse water and energy efficiently using AI-driven predictions, insights, and data visualization.

    ### 🚀 Features
    - Dynamic prediction via ML  
    - Gemini AI suggestions  
    - Real-time dashboards  
    - Downloadable reports  
    - City performance ranking
    """)
