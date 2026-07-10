import os
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FinMark AI Advisor", page_icon="💬", layout="wide")

# ---------------- LOAD OPENAI API KEY ----------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ Missing or invalid OpenAI API key in .streamlit/secrets.toml.")
    st.stop()

# ---------------- LOAD DATA ----------------
data_path = "https://raw.githubusercontent.com/30Anushka/FinMark-AI-Agent-Project/main/Streamlit/financial_behavior.csv"
try:
    df = pd.read_csv(data_path)
    # Ensure columns have a reliable format
    df.columns = df.columns.str.strip().str.lower()
except Exception as e:
    st.error("❌ Could not load dynamic financial_behavior.csv sheet. Falling back to local mode.")
    # Quick mock structure creation to keep the engine from failing
    df = pd.DataFrame({
        'customer_id': [1001, 1002], 'income': [850000, 950000], 
        'spending': [400000, 450000], 'savings': [450000, 500000], 
        'balance': [120000, 300000], 'credit_score': [720, 680],
        'persona': ['investor', 'saver'], 'savings_rate': [0.20, 0.25]
    })

# ---------------- SESSION STATE SETUP ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

# ---------------- PAGE 1: LOGIN (BYPASS MODE) ----------------
def login_page():
    if df is not None and not df.empty:
        # Match 'customer_id' regardless of case conversions
        id_col = 'customer_id' if 'customer_id' in df.columns else df.columns[0]
        fallback_id = int(df[id_col].iloc[0])
        
        st.session_state.authenticated = True
        st.session_state.customer_id = fallback_id
        st.sidebar.success("⚡ Developer Authentication Bypass Applied")
        st.rerun()
    else:
        st.session_state.authenticated = True
        st.session_state.customer_id = 1001
        st.rerun()

# ---------------- GPT ADVISOR FUNCTION ----------------
def ask_gpt(user_query, profile):
    prompt = f"""
    You are an Indian AI financial advisor helping users make smart personal finance decisions.

    Customer Financial Profile:
    - Average Monthly Income: ₹{profile['income']:,.0f}
    - Average Monthly Spending: ₹{profile['spending']:,.0f}
    - Average Monthly Savings: ₹{profile['savings']:,.0f}
    - Average Account Balance: ₹{profile['balance']:,.0f}

    Provide a short, data-backed, and easy-to-understand answer in plain English using Indian currency (₹).

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

# ---------------- PAGE 2: ADVISOR & SIMULATOR CONTROL PANEL ----------------
def advisor_page():
    # Safely extract customer rows
    id_col = 'customer_id' if 'customer_id' in df.columns else df.columns[0]
    cust = df[df[id_col] == st.session_state.customer_id]
    
    if cust.empty:
        cust = df.iloc[[0]]

    st.title("💬 FinMark — Your AI Financial Advisor")
    st.markdown("Welcome! Ask any question about your income, spending, or savings, and get real insights instantly.")

    # Customer summary metrics display
    st.subheader("📊 Your Financial Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Income", f"₹{float(cust['income'].mean()):,.0f}")
    col2.metric("Avg Spending", f"₹{float(cust['spending'].mean()):,.0f}")
    col3.metric("Avg Savings", f"₹{float(cust['savings'].mean()):,.0f}")
    col4.metric("Avg Balance", f"₹{float(cust['balance'].mean()):,.0f}")

    # Chat section
    st.markdown("---")
    user_query = st.text_input("💭 Ask your question (e.g., 'Can I afford a ₹5 lakh car loan?')")

    if st.button("Ask AI"):
        if user_query.strip() == "":
            st.warning("Please enter a question before asking.")
        else:
            profile = {
                "income": float(cust["income"].mean()),
                "spending": float(cust["spending"].mean()),
                "savings": float(cust["savings"].mean()),
                "balance": float(cust["balance"].mean())
            }
            with st.spinner("💡 Thinking..."):
                reply = ask_gpt(user_query, profile)
                st.success(reply)

    # 🚀 MARKET SIMULATION SECTION (Encapsulated safely inside the active page router)
    st.markdown("---")
    st.write("### 🚀 Market Simulation: New Product Launch Window")
    st.write("Launch a new financial instrument into the market to test consumer adoption metrics across synthetic profiles.")

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        product_type = st.selectbox("Select Product Category", ["High-Yield SIP Mutual Fund", "Digital Gold Savings Locker", "Fixed Return Bond"])
    with col_p2:
        offered_interest = st.slider("Offered Annual Return Percentage (%)", min_value=4.0, max_value=15.0, value=9.5, step=0.5)
    with col_p3:
        min_monthly_commitment = st.number_input("Minimum Monthly Commitment (₹)", min_value=500, max_value=10000, value=2000)

    if st.button("Simulate Population Response"):
        with st.spinner("Processing structural affinity rules across population data..."):
            # Ensure critical columns exist before processing vector mathematics
            if 'persona' not in df.columns:
                df['persona'] = 'investor'
            if 'credit_score' not in df.columns:
                df['credit_score'] = 700
            if 'savings_rate' not in df.columns:
                df['savings_rate'] = 0.20

            persona_weights = {'saver': 30, 'investor': 40, 'risk-taker': 15, 'spender': 5}
            df['persona_score'] = df['persona'].str.lower().map(persona_weights).fillna(15)
            df['credit_booster'] = (df['credit_score'] - 300) / 600 * 20
            df['monthly_savings_est'] = (df['income'] / 12) * df['savings_rate']
            df['financial_capacity_score'] = np.where(df['monthly_savings_est'] >= min_monthly_commitment, 20, 0)
            
            yield_bonus = (offered_interest - 6.0) * 4
            df['total_interest_score'] = df['persona_score'] + df['credit_booster'] + df['financial_capacity_score'] + yield_bonus
            
            df['reaction'] = np.select(
                [df['total_interest_score'] >= 65, df['total_interest_score'] >= 40],
                ['Highly Interested (Likely Buyer)', 'Moderately Interested (Needs Marketing)'],
                default='Not Interested (No Action)'
            )
            
            reaction_counts = df['reaction'].value_counts()
            
            st.success("🎯 Simulation Processing Finalized!")
            col_r1, col_r2 = st.columns([1, 2])
            with col_r1:
                st.write("#### Market Adoption Breakdown")
                st.dataframe(reaction_counts)
            with col_r2:
                st.write("#### Sentiment Share Summary")
                st.bar_chart(reaction_counts)
                
            st.write("#### 👥 Adoption Patterns by Persona Type")
            pivot_table = pd.crosstab(df['persona'], df['reaction'], normalize='index') * 100
            st.dataframe(pivot_table.style.format("{:.1f}%"))

    # Sidebar Logout controls
    if st.sidebar.button("🔒 Reset System Application"):
        st.session_state.authenticated = False
        st.session_state.customer_id = None
        st.rerun()

# ---------------- MAIN ROUTER ----------------
if not st.session_state.authenticated:
    login_page()
else:
    advisor_page()

st.markdown("---")
st.caption("🤖 Powered by FinMark Synthetic Data (Phase 5) and GPT reasoning.")
