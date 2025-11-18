"""
app.py - Streamlit demo for Dumroo AI Developer Assignment
Run: streamlit run app.py
"""
import streamlit as st
from ai_query import load_data, parse_query_and_filter
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dumroo AI Demo", layout="wide")

st.title("Dumroo.ai — Admin Natural Language Query Demo")
st.markdown("Type a simple English question and the demo will return filtered results (with role-based scoping).")

# Sidebar: admin scope
st.sidebar.header("Admin scope (role-based access)")
grades_input = st.sidebar.text_input("Allowed grades (comma separated)", value="8")
regions_input = st.sidebar.text_input("Allowed regions (comma separated)", value="North")

def parse_list(s, cast=str):
    return [cast(x.strip()) for x in s.split(",") if x.strip()]

admin_scope = {
    "grades": parse_list(grades_input, int) if grades_input else [],
    "regions": parse_list(regions_input, str) if regions_input else []
}

data = load_data("students.csv")

st.sidebar.markdown("**Example admin scope**: grades=[8], regions=['North']")

query = st.text_input("Enter your question", value="Which students haven't submitted their homework yet?")
if st.button("Run Query"):
    result, explanation = parse_query_and_filter(query, data, admin_scope=admin_scope, as_of_date=datetime(2025,11,18).date())
    st.subheader(explanation)
    if result.empty:
        st.info("No results found.")
    else:
        st.dataframe(result.reset_index(drop=True))
        # show simple summary stats for performance queries
        if "performance" in query.lower():
            st.markdown("**Summary stats:**")
            st.write(result[["quiz_score"]].describe())
