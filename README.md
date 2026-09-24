# Telco Customer Churn Prediction

A machine learning project to predict customer churn for a telecommunications company using the IBM Telco Customer Churn dataset.

---

## Problem Statement

A telecom company faces a churn rate of 26.58%, meaning more than one in four customers leaves. Without a proactive early-warning system, the company cannot intervene before losing customers. The objective is to build a binary classification model that accurately predicts whether a customer will churn based on their demographics, account details, and subscribed services.

---

## Objective

Identify customers likely to churn and uncover actionable patterns to improve customer retention using data analysis and machine learning.

---

## Dataset

- **Name:** IBM Telco Customer Churn
- **Source:** Originally published by IBM as a sample dataset; publicly available on [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Records:** 7,032 (after cleaning)
- **Features:** 20 customer attributes + 1 target (Churn)
- **Target Variable:** `Churn` — whether a customer left the company (Yes/No)

**Key Features:**
| Feature | Description |
|---|---|
| `tenure` | Number of months the customer has been with the company |
| `Contract` | Type of contract (Month-to-month, One year, Two year) |
| `MonthlyCharges` | Monthly amount charged to the customer |
| `TotalCharges` | Total charges over the customer's lifetime |
| `InternetService` | Type of internet service (DSL, Fiber optic, No) |
| `PaymentMethod` | Payment method used |

---

## Technologies

| Category | Tools |
|---|---|
| Language | Python 3.9+ |
| Data Processing | pandas, numpy |
| Visualization | matplotlib, seaborn |
| Machine Learning | scikit-learn |
| Frontend | Streamlit |
| Notebook | Jupyter Notebook |
| Report | python-docx |

---

## Project Workflow

```
1. Load Dataset
       ↓
2. Data Cleaning (fix TotalCharges, drop 11 NaN rows, verify no duplicates)
       ↓
3. Exploratory Data Analysis (churn by contract, internet, payment, tenure, charges)
       ↓
4. Feature Engineering (label encoding, standard scaling)
       ↓
5. Train-Test Split (80% train / 20% test, stratified)
       ↓
6. Model Training (Logistic Regression, Random Forest)
       ↓
7. Model Evaluation (Accuracy, Precision, Recall, F1, ROC-AUC)
       ↓
8. Model Selection (Logistic Regression — best overall metrics)
       ↓
9. Predictions & Business Recommendations
```

---

## Project Structure

```
Telco-Customer-Churn/
│
├── Telco-Customer-Churn.csv                    # Raw dataset
├── HarshSingh_CustomerChurnPrediction.ipynb    # Jupyter Notebook (full analysis)
├── app.py                                      # Streamlit web application
├── requirements.txt                            # Python dependencies
├── README.md                                   # Project documentation
└── HarshSingh_ProjectReport.docx              # Professional project report
```

---

## Setup Instructions

### 1. Clone or download the project

```bash
git clone <repository-url>
cd Telco-Customer-Churn
```

### 2. (Optional) Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

### Jupyter Notebook

```bash
jupyter notebook HarshSingh_CustomerChurnPrediction.ipynb
```

Run all cells from top to bottom. The notebook covers:
- Data loading and cleaning
- Exploratory data analysis with charts
- Feature engineering and model training
- Model evaluation and comparison
- Predictions and business recommendations

### Streamlit Application

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501` and includes six pages:
- **Dataset Summary** — data preview, statistics, missing value check
- **Churn Analysis** — churn rates by contract, internet, payment method
- **Visualizations** — interactive charts
- **Model Comparison** — metrics, ROC curves, confusion matrix
- **Predictions** — test set predictions with risk levels
- **Business Insights** — key findings and recommendations

---

## Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Logistic Regression** ✔ | **79.39%** | **62.43%** | **56.42%** | **59.27%** | **83.45%** |
| Random Forest | 78.32% | 61.77% | 48.40% | 54.27% | 81.13% |

**Selected Model: Logistic Regression** — achieved higher scores than Random Forest across all five evaluated metrics (Accuracy, Precision, Recall, F1-Score, and ROC-AUC).

### Key Findings

- Overall churn rate: **26.58%**
- Month-to-month contract customers churn at **42.71%** vs **2.85%** for two-year contracts
- Fiber optic users churn at **41.89%** — highest among internet service types
- Electronic check customers churn at **45.29%** — far above automatic payment users (~16%)
- Customers with tenure under 12 months churn at **47.68%** — the highest-risk tenure group
- Churned customers average **17.98 months** tenure vs **37.65 months** for retained customers

### Top Business Recommendations

1. Incentivize long-term contracts to reduce month-to-month churn
2. Investigate and improve Fiber optic service quality
3. Encourage automatic payment methods over electronic checks
4. Implement early-tenure retention programs (customers < 12 months tenure: 47.68% churn)
5. Deploy the churn model to proactively identify at-risk customers
6. Review pricing for high monthly charge customers showing churn signals

---

## Conclusion

Logistic Regression (ROC-AUC: 83.45%) achieved the best performance on the test set. The analysis shows that contract type, internet service, payment method, and tenure are important factors associated with churn in this dataset. Applying model predictions alongside the identified patterns may help the telecom company prioritise retention efforts and support improvements in customer lifetime value.

---

*Dataset originally published by IBM; publicly available via Kaggle.*
