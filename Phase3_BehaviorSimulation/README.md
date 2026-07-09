# 💼 Phase 3 — Financial Behavior Simulation Engine

## 🎯 Objective
This phase teaches the **synthetic customers** (generated in Phase 2) how to **manage money month by month** — modeling realistic financial behavior over time.

Instead of creating new customers, this step simulates **12 months of financial activity** for each one, resulting in a dynamic “financial life movie.”



## 🧠 Concept
Each customer earns income, spends, saves, invests, and (if applicable) repays loans.  
Their balance changes monthly, influenced by their **financial persona**.

This creates a **temporal behavioral dataset**, which can be used for:
- Financial trend analysis  
- Persona-based segmentation  
- Credit risk and savings simulations  
- Testing of AI financial advisors or recommendation engines  


## 👥 Personas Modeled
To add realism and diversity, four financial archetypes are assigned to customers:

| Persona | Behavioral Traits | Financial Pattern |
|----------|------------------|------------------|
| **Saver** | Cautious and disciplined | Saves 40–60% of income; steady balance growth |
| **Spender** | Impulsive and lifestyle-oriented | Spends 70–90% of income; minimal savings |
| **Investor** | Strategic and goal-driven | Invests 20–30% of income; moderate spending |
| **Risk-Taker** | Unpredictable and adventurous | Irregular spending/investment; volatile balance |

These personas are inspired by **behavioral finance** and **psychographic segmentation** principles, making the simulation behaviorally rich and lifelike.



## ⚙️ Script and Workflow

| File | Description |
|------|--------------|
| `financial_behavior_simulation.py` | Main script that simulates monthly financial data for each customer over 12 months. |
| `financial_behavior.csv` | Output dataset with month-by-month financial activity. |



## 🧮 Simulation Logic

For each customer:
1. Assign a **persona** (Saver, Spender, Investor, or Risk-Taker).
2. Simulate **12 months** of income inflows and outflows:
   - **Income:** salary or freelance income (±10% monthly variation)  
   - **Spending:** based on persona-driven ratio of income  
   - **Investments:** variable depending on persona  
   - **Loan repayment:** if `existing_loan_balance` > 0  
3. Update **balance** each month:  
   `balance = previous_balance + income - (spending + investment + loan_repayment)`  


## 📊 Output Columns

| Column | Description |
|---------|-------------|
| `customer_id` | Unique customer reference |
| `month` | Month number (1–12) |
| `persona` | Assigned financial behavior type |
| `income` | Monthly earnings |
| `spending` | Monthly expenses |
| `savings` | Income left after expenses and investments |
| `investments` | Investment made in that month |
| `loan_repayment` | Loan amount repaid that month |
| `balance` | Updated running balance |


## 📈 Example Output

| customer_id | month | persona | income | spending | savings | investments | loan_repayment | balance |
|--------------|--------|----------|---------|-----------|-----------|----------------|----------|
| 1 | 1 | Saver | 78,000 | 30,000 | 38,000 | 10,000 | 0 | 88,000 |
| 1 | 2 | Saver | 80,000 | 31,000 | 38,000 | 11,000 | 0 | 126,000 |
| 2 | 1 | Spender | 60,000 | 50,000 | 5,000 | 2,000 | 3,000 | 55,000 |
| 3 | 1 | Investor | 85,000 | 50,000 | 10,000 | 25,000 | 0 | 90,000 |



## 📦 Output Summary

- For **10,000 customers × 12 months** → `120,000 rows`
- Ready for:
  - Financial trend dashboards  
  - Persona-based analytics  
  - Predictive modeling (e.g., savings forecast, risk scoring)



## 🧩 Key Insights

- Different personas exhibit distinct monthly trajectories.
- **Savers** show consistent growth in balance.  
- **Spenders** display fluctuating or declining balances.  
- **Investors** show stable but slower liquidity due to investments.  
- **Risk-Takers** have volatile and unpredictable balance curves.


## 🧾 Requirements
Ensure the dependencies from `requirements.txt` are installed:

