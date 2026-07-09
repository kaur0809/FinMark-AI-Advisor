# 🧱 Phase 1 — Seed Data Generation with Faker

## 🎯 Objective
The objective of this phase is to **build the base (seed) dataset** of young professional customers using the **Faker** library.  
This dataset serves as the foundation for all subsequent synthetic modeling and behavioral simulations.

The focus is to generate **realistic but fully synthetic** customer attributes, financial variables, and initial behavioral tables in a privacy-safe way.



## 🧩 Datasets Created

| Dataset | Description | Approx. Rows |
|----------|--------------|--------------|
| `customers.csv` | Core profile of young professionals aged 23–40 with income, credit, and balance data. | ~2 000 |
| `transactions.csv` | Monthly and lifestyle transactions (rent, groceries, travel, entertainment, etc.). | ~50 000 |
| `campaign_events.csv` | Simulated marketing interactions (opened, clicked, converted, ignored). | ~8 000 |



## 🧠 Data Schema — `customers.csv`

| Column | Description |
|---------|-------------|
| `customer_id` | Unique customer identifier |
| `age` | Age (23–40 yrs) |
| `gender` | Male / Female / Non-binary |
| `city` | City of residence (e.g., Mumbai, Bengaluru, Delhi) |
| `job_role` | Profession (e.g., Software Engineer, Consultant, Banker) |
| `employment_type` | Salaried / Contract / Freelance |
| `income` | Annual income (₹ 3 L – ₹ 20 L) |
| `credit_score` | Ranges 300–850 based on payment reliability |
| `savings_rate` | Fraction (0–1) of income saved monthly |
| `existing_loan_balance` | Outstanding loan amount (if any) |
| `account_balance` | Current account balance (₹) |
| `joined_date` | Date when the customer became active |


## ⚙️ Script Used

| File | Description |
|------|--------------|
| `faker_seed.py` | Python script that uses Faker (with Indian locale `en_IN`) to generate all three tables and save them as CSVs. |

datetime
