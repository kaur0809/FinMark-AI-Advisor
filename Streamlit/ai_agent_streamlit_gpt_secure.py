# ============================================
# FinMark – AI Financial Advisor (Secure 2-Page Streamlit App)
# ============================================

import os
import streamlit as st
import pandas as pd
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FinMark AI Advisor", page_icon="💬", layout="wide")

# ---------------- LOAD OPENAI API KEY ----------------
# Streamlit Cloud automatically loads from .streamlit/secrets.toml
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ Missing or invalid OpenAI API key in .streamlit/secrets.toml.")
    st.stop()

# ---------------- LOAD DATA ----------------
data_path = "https://raw.githubusercontent.com/30Anushka/FinMark-AI-Agent-Project/main/Streamlit/financial_behavior.csv"
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("❌ Could not find financial_behavior.csv. Please check your project structure.")
    st.stop()

# ---------------- SESSION STATE SETUP ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

# ---------------- PAGE 1: LOGIN ----------------
def login_page():
    st.title("🔐 FinMark – Secure Login")
    st.markdown("Please enter your **Customer ID** to access your personal AI financial advisor.")

    customer_id = st.text_input("Enter your Customer ID")

    if st.button("Login"):
        if customer_id.strip() == "":
            st.warning("⚠️ Please enter a valid Customer ID.")
        elif not customer_id.isdigit():
            st.warning("⚠️ Customer ID must be numeric.")
        elif int(customer_id) not in df["customer_id"].values:
            st.error("❌ Customer ID not found in our system.")
        else:
            st.session_state.authenticated = True
            st.session_state.customer_id = int(customer_id)
            st.success("✅ Login successful! Redirecting...")
            st.rerun()

# ---------------- GPT ADVISOR FUNCTION ----------------
def ask_gpt(user_query, profile):
    """Send context + query to GPT and return personalized financial advice."""
    prompt = f"""
    You are an Indian AI financial advisor helping users make smart personal finance decisions.

    Customer Financial Profile:
    - Average Monthly Income: ₹{profile['income']:,.0f}
    - Average Monthly Spending: ₹{profile['spending']:,.0f}
    - Average Monthly Savings: ₹{profile['savings']:,.0f}
    - Average Account Balance: ₹{profile['balance']:,.0f}

    Provide a short, data-backed, and easy-to-understand answer in plain English
    using Indian currency (₹) and local financial context.

    User Question: "{user_query}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful Indian financial advisor AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ GPT API Error: {e}"

# ---------------- PAGE 2: ADVISOR ----------------
def advisor_page():
    cust = df[df["customer_id"] == st.session_state.customer_id]

    st.title("💬 FinMark — Your AI Financial Advisor")
    st.markdown("Welcome! Ask any question about your income, spending, or savings, and get real insights instantly.")

    # Customer summary
    st.subheader("📊 Your Financial Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Income", f"₹{cust['income'].mean():,.0f}")
    col2.metric("Avg Spending", f"₹{cust['spending'].mean():,.0f}")
    col3.metric("Avg Savings", f"₹{cust['savings'].mean():,.0f}")
    col4.metric("Avg Balance", f"₹{cust['balance'].mean():,.0f}")

    # Chat section
    st.markdown("---")
    user_query = st.text_input("💭 Ask your question (e.g., 'Can I afford a ₹5 lakh car loan?')")

    if st.button("Ask AI"):
        if user_query.strip() == "":
            st.warning("Please enter a question before asking.")
        else:
            profile = {
                "income": cust["income"].mean(),
                "spending": cust["spending"].mean(),
                "savings": cust["savings"].mean(),
                "balance": cust["balance"].mean()
            }
            with st.spinner("💡 Thinking..."):
                reply = ask_gpt(user_query, profile)
                st.success(reply)

    if st.button("🔒 Logout"):
        st.session_state.authenticated = False
        st.session_state.customer_id = None
        st.experimental_rerun()

# ---------------- MAIN ROUTER ----------------
if not st.session_state.authenticated:
    login_page()
else:
    advisor_page()

st.markdown("---")

st.caption("🤖 Powered by FinMark Synthetic Data (Phase 5) and GPT reasoning.")


