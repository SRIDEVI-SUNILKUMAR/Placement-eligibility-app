#!/usr/bin/env python
# coding: utf-8
"""
Placement Eligibility Streamlit App with Login 
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# --------------------------------------------------
# 🎛️  Page configuration - MUST be first Streamlit command
# --------------------------------------------------
st.set_page_config(
    page_title="Placement Eligibility App",
    page_icon="🎓",
    layout="wide",
)

# --------------------------------------------------
# Simple user database (hardcoded for demo)
# --------------------------------------------------
USER_CREDENTIALS = {
    "sridevi": "password123",
    "sunil": "qwerty456",
    "admin": "adminpass"
}

# --------------------------------------------------
# Login function (only sets session_state)
# --------------------------------------------------
def login():
    st.title("🔐 Please Log In")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_btn = st.button("Login")

    if login_btn:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("✅ Login successful!")
            if st.button("Continue to app"):
                # On clicking this button, the app reruns,
                # and since logged_in=True, main_app() is called.
                pass
        else:
            st.error("❌ Invalid username or password")

# --------------------------------------------------
# Database connection (cached)
# --------------------------------------------------
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root', #enter your username
        password='Jaya7494@123', #enter your password
        database='placements'
    )

connection = get_connection()

# --------------------------------------------------
# Main app content function (run after login)
# --------------------------------------------------
def main_app():
    st.image(
        "https://vignan.ac.in/blog/images/march/placement1.png",
        caption="Vignan University Placement Drive",
        width=400  # smaller logo
    )

    st.title("🎓 Placement Eligibility App")
    st.write(f"Welcome, **{st.session_state['username']}**! Check your eligibility for placements based on your profile.")

    def get_filtered_students(
        min_problems: int,
        min_soft_skills: int,
        use_lang_filter: bool,
        selected_langs: list[str],
        use_score_filter: bool,
        min_latest_score: int,
        use_status_filter: bool,
        selected_statuses: list[str],
    ) -> pd.DataFrame:
        query = """
            SELECT s.Student_id,
                   s.Full_Name,
                   s.Email,
                   p.prog_lang,
                   p.latest_score,
                   p.prob_solved,
                   (ss.communication + ss.teamwork + ss.leadership + ss.critical_thinking) / 4 AS soft_skills_score,
                   pl.placement_status
            FROM students s
            JOIN programming   p  ON s.Student_id = p.Stud_id
            JOIN soft_skills   ss ON s.Student_id = ss.Stud_id
            JOIN placement     pl ON s.Student_id = pl.Stud_id
            WHERE p.prob_solved >= %s
              AND ((ss.communication + ss.teamwork + ss.leadership + ss.critical_thinking) / 4) >= %s
        """

        params: list = [min_problems, min_soft_skills]

        if use_lang_filter and selected_langs:
            placeholders = ",".join(["%s"] * len(selected_langs))
            query += f" AND p.prog_lang IN ({placeholders})"
            params.extend(selected_langs)

        if use_score_filter:
            query += " AND p.latest_score >= %s"
            params.append(min_latest_score)

        if use_status_filter and selected_statuses:
            placeholders = ",".join(["%s"] * len(selected_statuses))
            query += f" AND pl.placement_status IN ({placeholders})"
            params.extend(selected_statuses)

        return pd.read_sql(query, connection, params=params)

    # Put filters in sidebar
    st.sidebar.header("🎯 Eligibility & Filters")
    min_problems = st.sidebar.number_input("Minimum Problems Solved", min_value=0, value=50)
    min_soft_skills = st.sidebar.slider("Minimum Soft Skills Score (Avg)", 0, 100, 75)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 🧠 Optional Filters")

    use_lang_filter = st.sidebar.checkbox("Filter by Programming Language?")
    selected_langs: list[str] = []
    if use_lang_filter:
        lang_query = "SELECT DISTINCT prog_lang FROM programming"
        lang_options_df = pd.read_sql(lang_query, connection)
        lang_options = lang_options_df["prog_lang"].dropna().sort_values().tolist()
        selected_langs = st.sidebar.multiselect("Select Languages", lang_options, default=lang_options)

    use_score_filter = st.sidebar.checkbox("Filter by Latest Assessment Score?")
    min_latest_score = 0
    if use_score_filter:
        min_latest_score = st.sidebar.slider("Minimum Latest Assessment Score", 0, 100, 75)

    use_status_filter = st.sidebar.checkbox("Filter by Placement Status?")
    selected_statuses: list[str] = []
    if use_status_filter:
        status_query = "SELECT DISTINCT placement_status FROM placement"
        status_options_df = pd.read_sql(status_query, connection)
        status_options = status_options_df["placement_status"].dropna().sort_values().tolist()
        selected_statuses = st.sidebar.multiselect("Select Status", status_options, default=status_options)

    df = get_filtered_students(
        min_problems,
        min_soft_skills,
        use_lang_filter,
        selected_langs,
        use_score_filter,
        min_latest_score,
        use_status_filter,
        selected_statuses,
    )

    st.subheader("🎓 Eligible Students")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.success(f"✅ {len(df)} students match your criteria.")
    else:
        st.warning("⚠️ No students match your selected criteria.")

    if not df.empty:
        st.markdown("---")
        st.subheader("📈 Visual Insights")

        lang_counts = df["prog_lang"].value_counts().reset_index()
        lang_counts.columns = ["Language", "Count"]
        fig_lang = px.bar(
            lang_counts,
            x="Language",
            y="Count",
            title="👨‍💻 Students by Programming Language",
            text="Count",
            color="Language",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_lang.update_layout(xaxis_title="Language", yaxis_title="Student Count")
        st.plotly_chart(fig_lang, use_container_width=True)

        status_counts = df["placement_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Placement Status Distribution",
            hole=0.35,
        )
        st.plotly_chart(fig_status, use_container_width=True)

        st.markdown("### 🧠 Top 5 Students – Latest Assessment Score")
        top_latest = df.sort_values(by="latest_score", ascending=False).head(5)
        st.dataframe(
            top_latest[["Student_id", "Full_Name", "prog_lang", "latest_score"]],
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("### 🤝 Top 5 Students – Soft Skills Average")
        top_soft = df.sort_values(by="soft_skills_score", ascending=False).head(5)
        st.dataframe(
            top_soft[["Student_id", "Full_Name", "soft_skills_score"]],
            hide_index=True,
            use_container_width=True,
        )


# --------------------------------------------------
# Main script logic to control login flow
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    st.success(f"👋 Welcome, {st.session_state['username']}!")
    main_app()
else:
    login()
