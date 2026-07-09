## 🎯 Objective
The goal of this phase is to build a **machine learning model** that predicts whether a customer is likely to **default on their loan or payments**.  
This phase transforms the synthetic financial datasets created earlier into a **predictive intelligence system** that classifies customers as:

> 🟩 **No** → Customer is not likely to default  
> 🟥 **Yes** → Customer is likely to default  



## 🧩 Input Dataset
The model uses the **Phase 2 HMA Synthetic Dataset** as input:

| Dataset | Description |
|----------|-------------|
| `customers_hma_10000_india.csv` | Synthetic customer profiles including income, savings, loan balance, and credit score generated using HMA Synthesizer. |



## ⚙️ Script Overview

| File | Description |
|------|--------------|
| `default_prediction.py` | Main script that generates a default flag (`Yes`/`No`), trains a predictive model, and evaluates results. |



## 🧠 Model Design

1. **Default Flag Generation**  
   A probabilistic `default` column is added based on financial health indicators:
   - Low credit score  
   - Low income  
   - Low savings rate  
   - High loan balance  

   Example logic:
   ```python
   if credit_score < 600 → +25% chance of default
   if income < ₹5L → +15%
   if savings_rate < 0.2 → +10%
   if existing_loan_balance > ₹3L → +20%
