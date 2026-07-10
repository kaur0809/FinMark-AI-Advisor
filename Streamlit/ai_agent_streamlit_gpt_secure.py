# ============================================
# FinMark – AI Financial Advisor (Secure 2-Page Streamlit App)
# ============================================

import os
import streamlit as st
import pandas as pd
import numpy as np
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

# ---------------- PAGE 1: LOGIN (BYPASS MODE) ----------------
def login_page():
    # 🎯 AUTOMATIC BYPASS: Force the app to log in immediately using the first record
    if "df" in globals() and not df.empty:
        # Grab the first actual customer ID from your sheet automatically
        fallback_id = int(df["customer_id"].iloc[0]) if "customer_id" in df.columns else int(df.iloc[0, 0])
        
        st.session_state.authenticated = True
        st.session_state.customer_id = fallback_id
        st.rerun()
    else:
        # Emergency backup if the data sheet fails to load entirely
        st.session_state.authenticated = True
        st.session_state.customer_id = 1001
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

# ---------------- PHASING ENGINE: NEW PRODUCT SIMULATION ----------------
st.markdown("---")
st.write("### 🚀 Market Simulation: New Product Launch Window")
st.write("Launch a new financial instrument into the market to test consumer adoption metrics across your 10,000 synthetic profiles.")

# 1. Product Variable Selection Panels
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    product_type = st.selectbox("Select Product Category", ["High-Yield SIP Mutual Fund", "Digital Gold Savings Locker", "Fixed Return Bond"])
with col_p2:
    offered_interest = st.slider("Offered Annual Return Percentage (%)", min_value=4.0, max_value=15.0, value=9.5, step=0.5)
with col_p3:
    min_monthly_commitment = st.number_input("Minimum Monthly Commitment (₹)", min_value=500, max_value=10000, value=2000)

# 2. Simulation Execution Engine
if st.button("Simulate Population Response"):
    if df is not None:
        with st.spinner("Processing structural affinity rules across population data..."):
            
            # Vectorized rule engine simulating real-world decision paths
            # Calculate a base interest score out of 100 for each synthetic profile
            
            # Map structural personas to numerical weights
            persona_weights = {'saver': 30, 'investor': 40, 'risk-taker': 15, 'spender': 5}
            df['persona_score'] = df['persona'].str.lower().map(persona_weights).fillna(15)
            
            # Credit score reliability booster
            df['credit_booster'] = (df['credit_score'] - 300) / 600 * 20
            
            # Financial capability filter (checks if their estimated monthly savings can afford the commitment)
            df['monthly_savings_est'] = (df['income'] / 12) * (df['savings_rate'] if 'savings_rate' in df.columns else 0.15)
            df['financial_capacity_score'] = np.where(df['monthly_savings_est'] >= min_monthly_commitment, 20, 0)
            
            # Product yield attraction factor
            yield_bonus = (offered_interest - 6.0) * 4 # More return = more interest
            
            # Total Cumulative Adoption Score Calculation
            df['total_interest_score'] = df['persona_score'] + df['credit_booster'] + df['financial_capacity_score'] + yield_bonus
            
            # Categorize consumer response vectors
            df['reaction'] = np.select(
                [df['total_interest_score'] >= 65, df['total_interest_score'] >= 40],
                ['Highly Interested (Likely Buyer)', 'Moderately Interested (Needs Marketing)'],
                default='Not Interested (No Action)'
            )
            
            # Compile aggregated data metrics
            reaction_counts = df['reaction'].value_counts()
            
            # 3. Render Visual Simulation Metrics Dashboard
            st.success("🎯 Simulation Processing Finalized!")
            
            col_r1, col_r2 = st.columns([1, 2])
            with col_r1:
                st.write("#### Market Adoption Breakdown")
                st.dataframe(reaction_counts)
            
            with col_r2:
                st.write("#### Sentiment Share Summary")
                # Streamlit automatically plots the categorical counts
                st.bar_chart(reaction_counts)
                
            # Cross-tabulate to show conversion rate by profile categories
            st.write("#### 👥 Adoption Patterns by Persona Type")
            pivot_table = pd.crosstab(df['persona'], df['reaction'], normalize='index') * 100
            st.dataframe(pivot_table.style.format("{:.1f}%"))
    else:
        st.error("No database pipeline detected to aggregate consumer metrics.")




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


