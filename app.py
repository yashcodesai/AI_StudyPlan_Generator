import streamlit as st

# Set custom page config
st.set_page_config(
    page_title="Edubot - AI Study Plan Generator",
    page_icon="🤖",
    layout="wide"
)

# App Title
st.markdown("<h1 style='text-align: center;'>🤖 Edubot - Your AI Study Planner</h1>", unsafe_allow_html=True)
import pandas as pd
from study_planner import generate_plan

# Set page layout
st.set_page_config(layout="centered")

# 🎯 Subject Icons Dictionary
subject_icons = {
    "DSA": "🧠",
    "DBMS": "🗃️",
    "OS": "🖥️",
    "CN": "🌐",
    "ML": "🤖",
    "AI": "🧠",
    "Maths": "📐"
}

# 🌟 App Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📚 AI-Powered Study Plan Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Plan your study time smartly with AI!</h4>", unsafe_allow_html=True)
st.markdown("---")

# Load data
try:
    df = pd.read_csv("data/topics_difficulty.csv")
except Exception as e:
    st.error(f"⚠️ Failed to load topic data: {e}")
    st.stop()

# 📘 Subject Selector
subjects = st.multiselect("📘 Select Subjects", options=df["Subject"].unique())
st.caption("You can select one or more subjects to generate your study plan.")

# ⏱ Input Hours & Days
col1, col2 = st.columns(2)
with col1:
    daily_hours = st.number_input("🕒 How many hours can you study daily?", min_value=1, max_value=24, value=4)
with col2:
    total_days = st.number_input("📅 In how many days do you want to complete your syllabus?", min_value=1, max_value=180, value=30)

st.markdown("---")

# 🚀 Generate Plan Button
if st.button("🚀 Generate My Study Plan"):
    if not subjects:
        st.warning("⚠️ Please select at least one subject.")
    else:
        try:
            plan = generate_plan(subjects, daily_hours, total_days)

            if plan.empty:
                st.warning("😕 No plan could be generated.")
            else:
                st.success("✅ Study plan generated successfully!")
                
                st.markdown("### 📑 Your Personalized Study Plan")

                # Add subject icons
                plan["Subject"] = plan["Subject"].apply(lambda s: f"{subject_icons.get(s, '')} {s}")

                # Calculate total study time for progress bars
                total_hours = plan["Hours"].sum()
                plan["Progress"] = plan["Hours"] / total_hours

                for _, row in plan.iterrows():
                    st.markdown(f"**{row['Subject']} - {row['Topic']}**")
                    st.markdown(f"🕓 Estimated: `{row['Hours']} hours`")
                    st.progress(row["Progress"])
                    st.markdown("---")
                # 📋 Day-wise Table Summary
                    st.markdown("## 📋 Study Plan Table (Day-wise)")
                    st.dataframe(plan, use_container_width=True)
                

                # Download CSV
                csv = plan.drop(columns=["Progress"]).to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Plan as CSV", csv, "study_plan.csv", "text/csv", key='csv-download')

        except Exception as e:
            st.error(f"❌ Error: {e}")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:13px;'>Made with ❤️ by Yash Saxena</p>", unsafe_allow_html=True)