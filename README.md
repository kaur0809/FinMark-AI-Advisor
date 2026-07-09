FinMark AI Agent — Synthetic Financial Simulation
This project builds an AI-driven synthetic financial ecosystem using Faker and SDV (CTGAN + HMA).
It simulates customer profiles, transactions, marketing responses, and monthly financial behavior, enabling safe and realistic experimentation for fintech product and marketing strategy design.

🧱 Phase 1 — Seed Data Generation
Tools: Faker, Pandas

Generated ~2000 young professional customer profiles.
Added behavioral data: transactions and campaign responses.
Outputs:

customers.csv, transactions.csv, campaign_events.csv
🌆 Phase 2 — Synthetic Expansion (SDV: CTGAN + HMA)
Tools: SDV (CTGANSynthesizer, HMASynthesizer), Matplotlib

Expanded customers → 10,000 synthetic profiles.
Preserved multi-table relationships using HMA Synthesizer.
Validated data realism via SDV quality scores and KS tests.
Outputs:

customers_ctgan_10000.csv
customers_hma_10000.csv
transactions_hma_10000.csv
campaigns_hma_10000.csv
Evaluation Results:

Single-table CTGAN Quality Score: 0.882
Multi-table HMA Quality Score: 0.881
Distributions realistic; minor correlation drift observed.
💼 Phase 3 — Financial Behavior Simulation
Goal: Simulate monthly money behavior for each synthetic customer.
Logic: Each customer assigned a persona →

Saver (high savings, low risk)
Spender (low savings, high consumption)
Investor (moderate spending, consistent investing)
Risk-Taker (volatile behavior)
Output:

financial_behavior.csv (12 months × customers)
Columns: customer_id, month, persona, income, spending, savings, investments, loan_repayment, balance
📊 Example Visuals
Persona	Behavior
Saver	Balance grows steadily each month
Spender	High fluctuations, lower ending balance
Investor	Moderate growth + investment activity
Risk-Taker	Irregular spikes and dips
⚙️ Tools & Libraries
Python 3.10+
faker, pandas, numpy, sdv, matplotlib, scipy
📈 Key Insights
Synthetic data realism achieved (SDV quality ≥ 0.88)
Behavior engine creates realistic financial diversity
System fully privacy-safe — no real data used
