import os
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI

# ---------------- STRATEGIC PORTAL CONFIG ----------------
st.set_page_config(page_title="FinMark | Corporate Simulation Suite", page_icon="📈", layout="wide")

# ---------------- SECURE CREDENTIAL CHECK ----------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ Enterprise Security: OpenAI Key Validation Failed.")
    st.stop()

# ---------------- CORPORATE SYNTHETIC DATA ENGINE ----------------
data_path = "https://raw.githubusercontent.com/30Anushka/FinMark-AI-Agent-Project/main/Streamlit/financial_behavior.csv"
try:
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip().str.lower()
except Exception:
    # Fail-safe high-fidelity matrix mirroring your 10,000 synthetic parameters
    np.random.seed(42)
    n_records = 10000
    df = pd.DataFrame({
        'customer_id': np.arange(1001, 1001 + n_records),
        'income': np.random.normal(750000, 150000, n_records),
        'spending': np.random.normal(400000, 80000, n_records),
        'balance': np.random.normal(200000, 50000, n_records),
        'credit_score': np.random.randint(400, 850, n_records),
        'persona': np.random.choice(['saver', 'investor', 'risk-taker', 'spender'], n_records, p=[0.3, 0.4, 0.15, 0.15]),
        'savings_rate': np.random.uniform(0.05, 0.35, n_records)
    })

# Clean data fields
df['savings'] = df['income'] - df['spending']

# ---------------- CORPORATE EXECUTIVE DASHBOARD ----------------
st.title("🏛️ FinMark — Institutional Product Launch Simulator")
st.markdown("### **Enterprise Portal:** Quantifying Consumer Reaction & Adoption Metrics Across Synthetic Indian Demographics")
st.markdown("---")

# --- SECTION 1: MACRO ENVIRONMENT METRICS ---
st.subheader("📊 Target Synthetic Population Parameters (N=10,000)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Addressable Market (TAM)", "10,000 Nodes")
m2.metric("Aggregate Market Base Income", f"₹{df['income'].sum()/10000000:.2f} Cr")
m3.metric("Available Ecosystem Savings Pool", f"₹{df['savings'].sum()/10000000:.2f} Cr")
m4.metric("Mean Credit Risk Vector (Score)", f"{int(df['credit_score'].mean())}")

st.markdown("---")

# --- SECTION 2: PRODUCT DEPLOYMENT ENGINE ---
st.subheader("🚀 Financial Product Deployment Sandbox")
st.write("Configure the parameters of your new financial asset to evaluate macro adoption vectors and capital migration.")

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    product_type = st.selectbox("Product Vehicle Structure", ["High-Yield Systematic Investment Plan (SIP)", "Tier-1 Corporate Fixed Income Bond", "Equity Alpha Mutual Fund Tracker"])
with col_p2:
    offered_interest = st.slider("Offered Dividend / Annual Return Rate (%)", min_value=4.0, max_value=16.0, value=9.5, step=0.5)
with col_p3:
    min_monthly_commitment = st.number_input("Minimum Threshold Monthly Commitment (₹)", min_value=500, max_value=15000, value=2500, step=500)

# --- RUNNING DATA COMPARISONS ---
persona_weights = {'saver': 35, 'investor': 45, 'risk-taker': 20, 'spender': 5}
df['persona_score'] = df['persona'].str.lower().map(persona_weights).fillna(15)
df['credit_booster'] = (df['credit_score'] - 300) / 550 * 20
df['monthly_savings_est'] = (df['income'] / 12) * df['savings_rate']
df['financial_capacity_score'] = np.where(df['monthly_savings_est'] >= min_monthly_commitment, 20, 0)
yield_bonus = (offered_interest - 6.5) * 4

df['total_interest_score'] = df['persona_score'] + df['credit_booster'] + df['financial_capacity_score'] + yield_bonus
df['reaction'] = np.select(
    [df['total_interest_score'] >= 68, df['total_interest_score'] >= 45],
    ['Highly Interested (Immediate Buyer)', 'Moderately Interested (Marketing Target)'],
    default='Not Interested (Churned)'
)

reaction_counts = df['reaction'].value_counts()
highly_interested_count = reaction_counts.get('Highly Interested (Immediate Buyer)', 0)
projected_monthly_capital = highly_interested_count * min_monthly_commitment

# --- SECTION 3: SIMULATION IMPACT DASHBOARD ---
st.markdown("### **Simulation Impact Report**")

c_metrics1, c_metrics2, c_metrics3 = st.columns(3)
with c_metrics1:
    st.metric("Projected Conversion Rate", f"{(highly_interested_count / len(df)) * 100:.2f}%")
with c_metrics2:
    st.metric("Immediate Client Acquisition", f"{highly_interested_count:,} Accounts")
with c_metrics3:
    st.metric("Projected Monthly Capital Inflow (AUM)", f"₹{projected_monthly_capital:,.0f}")

col_graph1, col_graph2 = st.columns([1, 2])
with col_graph1:
    st.write("#### Population Sentiment Vectors")
    st.dataframe(reaction_counts)
with col_graph2:
    st.write("#### Conversion Volume Distribution")
    st.bar_chart(reaction_counts)

# Cross-tabulation framework
st.write("#### 👥 Segment Analysis: Penetration Share by Consumer Persona Type")
pivot_table = pd.crosstab(df['persona'], df['reaction'], normalize='index') * 100
st.dataframe(pivot_table.style.format("{:.1f}%"))

# --- SECTION 4: ENTERPRISE AI AUDIT AGENT (GPT FOCUS) ---
st.markdown("---")
st.subheader("🧠 FinMark Corporate AI Strategist")
st.write("Query the AI Agent to run structural business interpretation models against the simulation graph metrics above.")

corporate_query = st.text_input(
    "Enterprise System Command:",
    placeholder=f"Analyze market response vectors if we deploy a {product_type} offering {offered_interest}% returns to savers."
)

if st.button("Generate Executive Strategy Assessment"):
    if corporate_query:
        with st.spinner("AI Agent aggregating cross-tabular segments..."):
            
            summary_context = f"""
            You are a B2B Financial Strategy Consultant auditing a simulated market launch.
            Simulation Variables:
            - Product: {product_type}
            - Interest Offered: {offered_interest}%
            - Capital Commitment: ₹{min_monthly_commitment}/month
            - Conversion Rate: {(highly_interested_count / len(df)) * 100:.2f}%
            - Projected Monthly Inflow: ₹{projected_monthly_capital}
            - Demographics: 10,000 synthetic Indian Young Professionals modeled via CTGAN/HMA.
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a strategic financial consultant. Provide executive analysis based on macroeconomic indicators, pricing efficiency, and demographic volume insights in a crisp corporate style."},
                        {"role": "user", "content": f"{summary_context}\n\nTask: {corporate_query}"}
                    ],
                    temperature=0.4
                )
                st.success("🏢 Corporate Strategy Matrix Output:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"API Vector Error: {e}")
