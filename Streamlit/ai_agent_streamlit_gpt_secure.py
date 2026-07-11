import os
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import yfinance as yf

# ---------------- 1. STRATEGIC PORTAL CONFIG ----------------
st.set_page_config(page_title="FinMark | Corporate Simulation Suite", page_icon="📈", layout="wide")

# ---------------- 2. SECURE CREDENTIAL CHECK ----------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ Enterprise Security: OpenAI Key Validation Failed. Please verify Secrets Manager.")
    st.stop()

# ---------------- 3. DATA ENGINE ----------------
@st.cache_data
def load_my_uploaded_data():
    possible_local_paths = [
        "Streamlit/financial_behavior.csv",
        "Phase3_BehaviorSimulation/customers_hma_10000_india.csv",
        "Streamlit/customers_hma_10000_india.csv",
        "financial_behavior.csv", 
        "customers_hma_10000_india.csv"
    ]
    for path in possible_local_paths:
        if os.path.exists(path):
            try:
                my_df = pd.read_csv(path)
                my_df.columns = my_df.columns.str.strip().str.lower()
                return my_df
            except Exception:
                continue
    return None

df = load_my_uploaded_data()

# Auto-align column structures across your CSV files
if df is not None:
    if 'income' not in df.columns:
        df['income'] = np.random.normal(750000, 150000, len(df))
    if 'spending' not in df.columns:
        df['spending'] = np.random.normal(400000, 80000, len(df))
    if 'balance' not in df.columns:
        df['balance'] = df['account_balance'] if 'account_balance' in df.columns else np.random.normal(200000, 50000, len(df))
    if 'credit_score' not in df.columns:
        df['credit_score'] = np.random.randint(600, 850, len(df))
    if 'persona' not in df.columns:
        df['persona'] = np.random.choice(['saver', 'investor', 'risk-taker', 'spender'], len(df))
    if 'savings_rate' not in df.columns:
        df['savings_rate'] = np.random.uniform(0.10, 0.30, len(df))
else:
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

df['savings'] = df['income'] - df['spending']

# ---------------- 4. REAL-TIME MARKET BENCHMARK (YAHOO FINANCE) ----------------
@st.cache_data(ttl=3600)
def get_live_market_benchmarks():
    try:
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="1y")
        if len(hist) > 1:
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            annual_market_return = ((end_price - start_price) / start_price) * 100
        else:
            annual_market_return = 12.5
    except Exception:
        annual_market_return = 12.5
    return round(annual_market_return, 2)

live_benchmark_yield = get_live_market_benchmarks()

# ---------------- 5. CORPORATE DASHBOARD UI ----------------
st.title("🏛️ FinMark — Institutional Product Launch Simulator")
st.markdown("### **Enterprise Strategic Portal:** Quantifying Consumer Adoption and Capital Impact Against Real-Time Market Benchmarks")
st.markdown("---")

st.info(f"📈 Trailing 1-Year Live Market Benchmark (Nifty 50 Yield via Yahoo Finance API): **{live_benchmark_yield}%**")

st.subheader("📊 Target Population Parameters (Active Sample N=10,000)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Addressable Market (TAM)", f"{len(df):,} Profiles")
m2.metric("Aggregate Market Base Income", f"₹{df['income'].sum()/10000000:.2f} Cr")
m3.metric("Available Ecosystem Savings Pool", f"₹{df['savings'].sum()/10000000:.2f} Cr")
m4.metric("Mean System Credit Score", f"{int(df['credit_score'].mean())}")

st.markdown("---")

st.subheader("🚀 Financial Product Deployment Sandbox")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    product_type = st.selectbox("Product Vehicle Structure", ["High-Yield Systematic Investment Plan (SIP)", "Tier-1 Corporate Fixed Income Bond", "Equity Alpha Mutual Fund Tracker", "Liquid Cash Management Account"])
with col_p2:
    offered_interest = st.slider("Offered Dividend / Annual Return Rate (%)", min_value=4.0, max_value=20.0, value=11.0, step=0.5)
with col_p3:
    min_monthly_commitment = st.number_input("Minimum Threshold Monthly Commitment (₹)", min_value=500, max_value=25000, value=5000, step=500)

# --- SIMULATION ENGINE MATHEMATICS ---
market_spread = offered_interest - live_benchmark_yield

# 1. Base persona interest weights
persona_weights = {'saver': 35, 'investor': 45, 'risk-taker': 20, 'spender': 5}
df['persona_score'] = df['persona'].str.lower().map(persona_weights).fillna(15)
df['credit_booster'] = (df['credit_score'] - 300) / 550 * 20

# 2. Balanced market spread modifier
spread_bonus = np.clip(market_spread * 3, -20, 20) 

# 3. Calculate cumulative baseline interest score
df['total_interest_score'] = df['persona_score'] + df['credit_booster'] + spread_bonus

# 4. CALIBRATED ACCESSIBILITY FILTER
# Young professionals pool their monthly disposable capacity to gauge affordability
df['monthly_savings_est'] = (df['income'] / 12) * df['savings_rate']

df['reaction'] = np.select(
    [
        (df['total_interest_score'] >= 50) & (df['monthly_savings_est'] >= (min_monthly_commitment * 0.7)),
        (df['total_interest_score'] >= 35) & (df['monthly_savings_est'] >= (min_monthly_commitment * 0.4))
    ],
    [
        'Highly Interested (Immediate Buyer)', 
        'Moderately Interested (Marketing Target)'
    ],
    default='Not Interested (Churned / Insufficient Funds)'
)

reaction_counts = df['reaction'].value_counts()
highly_interested_count = reaction_counts.get('Highly Interested (Immediate Buyer)', 0)
projected_monthly_capital = highly_interested_count * min_monthly_commitment

# --- SIMULATION IMPACT REPORTING ---
st.markdown("### **Simulation Impact Report**")
c_metrics1, c_metrics2, c_metrics3 = st.columns(3)
with c_metrics1:
    st.metric("Projected Market Conversion Rate", f"{(highly_interested_count / len(df)) * 100:.2f}%")
with c_metrics2:
    st.metric("Immediate Account Acquisitions", f"{highly_interested_count:,} Clients")
with c_metrics3:
    st.metric("Projected Monthly AUM Capital Inflow", f"₹{projected_monthly_capital:,.0f}")

col_graph1, col_graph2 = st.columns([1, 2])
with col_graph1:
    st.write("#### Population Sentiment Vectors")
    st.dataframe(reaction_counts)
with col_graph2:
    st.write("#### Conversion Volume Distribution")
    st.bar_chart(reaction_counts)

st.write("#### 👥 Segment Analysis: Penetration Share by Consumer Persona Type")
pivot_table = pd.crosstab(df['persona'], df['reaction'], normalize='index') * 100
st.dataframe(pivot_table.style.format("{:.1f}%"))

# --- 6. ENTERPRISE AI STRATEGIST AGENT (GPT FOCUS) ---
st.markdown("---")
st.subheader("🧠 FinMark Corporate AI Strategist")
st.write("Instruct the corporate AI Agent to analyze the economic viability of this simulation.")

# Fixed duplicate element bug by adding unique key string
corporate_query = st.text_input(
    "Enterprise System Command:",
    placeholder="Analyze market response vectors for this configuration...",
    key="corporate_ai_input" 
)

if st.button("Generate Executive Strategy Assessment"):
    if corporate_query.strip() == "":
        st.warning("Please enter a question or instruction for the AI Agent.")
    else:
        with st.spinner("AI Agent aggregating cross-tabular segments..."):
            summary_context = f"""
            You are an institutional B2B Financial Strategy Consultant auditing a simulated product rollout.
            Simulation Variables:
            - Launched Product Type: {product_type}
            - Interest Offered: {offered_interest}%
            - Live Market Benchmark (Nifty): {live_benchmark_yield}%
            - Yield Spread vs Market: {market_spread}%
            - Calculated Conversion Rate: {(highly_interested_count / len(df)) * 100:.2f}%
            - Projected Monthly Capital Flow: ₹{projected_monthly_capital}
            - Audience Pool: 10,000 synthetic Indian Young Professionals modeled via CTGAN/HMA.
            """
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a strategic financial consultant. Provide executive analysis based on macroeconomic indicators and live market yield spreads in a crisp corporate style."},
                        {"role": "user", "content": f"{summary_context}\n\nTask: {corporate_query}"}
                    ],
                    temperature=0.4,
                    max_tokens=500
                )
                st.success("🏢 Corporate Strategy Matrix Output:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"⚠️ OpenAI System Connection Refused: {e}")

st.markdown("---")
st.caption("🤖 Powered by your private FinMark Synthetic Repositories and GPT reasoning.")
