# 🌆 Phase 2 — Synthetic Expansion using SDV (CTGAN + HMA Synthesizer)

## 🎯 Objective
This phase expands the seed datasets from Phase 1 using **Synthetic Data Vault (SDV)** — an AI-based synthetic data generation framework.

The goal is to:
- Train **CTGAN** on single-table data (`customers.csv`)  
- Train **HMA Synthesizer** on multi-table data (`customers + transactions + campaigns`)  
- Generate **10,000+ synthetic customers** with consistent financial behavior  
- Validate the quality and realism of the synthetic data  



## 🧠 Models Used

| Model | Type | Description |
|--------|------|-------------|
| **CTGAN** | Single-table | Deep-learning GAN that models tabular data. Learns column distributions and relationships. |
| **HMA Synthesizer** | Multi-table | Hierarchical model that preserves relationships between tables (e.g., customer ↔ transactions ↔ campaigns). |


## ⚙️ Scripts and Files

| File | Description |
|------|-------------|
| `ctgan_full.py` | Trains the CTGAN model on `customers.csv` and generates synthetic customers (`customers_ctgan_10000.csv`). |
| `hma_full.py` | Trains HMA Synthesizer using all Phase 1 tables (`customers`, `transactions`, `campaign_events`) to produce linked synthetic datasets. |


## 🧮 Outputs Generated

| Output File | Description |
|--------------|-------------|
| `customers_ctgan_10000.csv` | 10,000 synthetic customer profiles (single-table). |
| `customers_hma_10000.csv` | Multi-table synthetic customers with linked data. |
| `transactions_hma_10000.csv` | Synthetic transaction activity generated via HMA Synthesizer. |
| `campaigns_hma_10000.csv` | Synthetic marketing campaign responses. |
| `income_distribution.png`, `credit_score_distribution.png`, `account_balance_distribution.png` | Distribution comparison plots. |
| `income_vs_credit_scatter.png` | Scatter plot comparing income–credit score correlation. |



## 📊 Evaluation Results

### **CTGAN (Single-Table Evaluation)**
| Metric | Score |
|--------|--------|
| Column Shapes | 87.5% |
| Column Pair Trends | 88.9% |
| **Overall Quality Score** | **0.882** |

### **HMA Synthesizer (Multi-Table Evaluation)**
| Metric | Score |
|--------|--------|
| Column Shapes | 89.2% |
| Column Pair Trends | 92.3% |
| Cardinality | 93.3% |
| Intertable Trends | 79.9% |
| **Overall Multi-Table Score** | **0.882** |

✅ These results show strong synthetic data realism and structure preservation across both models.


## 🧩 Key Insights
- CTGAN captured customer-level patterns well (income, credit_score, balances).  
- HMA maintained logical multi-table consistency (customers ↔ transactions ↔ campaigns).  
- Slight reduction in correlations (expected in synthetic generation).  
- Synthetic data can safely replace real data for analytics and simulation.  


## 📦 Requirements
Ensure all dependencies from `requirements.txt` are installed:
