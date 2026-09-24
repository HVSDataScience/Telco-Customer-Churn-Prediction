import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon="📡",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title  { font-size: 2rem; font-weight: 700; color: #1f2328; }
    .section-hdr { font-size: 1.2rem; font-weight: 600; color: #3b82d4;
                   border-bottom: 2px solid #3b82d4; padding-bottom: 4px;
                   margin-bottom: 12px; }
    .metric-card { background: #f7f8fa; border: 1px solid #e5e7eb;
                   border-radius: 8px; padding: 16px; text-align: center; }
    .metric-val  { font-size: 1.6rem; font-weight: 700; color: #3b82d4; }
    .metric-lbl  { font-size: 0.85rem; color: #57606a; }
    .best-badge  { background: #dcfce7; color: #166534; border-radius: 4px;
                   padding: 2px 8px; font-size: 0.8rem; font-weight: 600; }
    .insight-box { background: #eff6ff; border-left: 4px solid #3b82d4;
                   padding: 12px 16px; border-radius: 0 6px 6px 0;
                   margin-bottom: 8px; font-size: 0.93rem; color: #1f2328; }
</style>
""", unsafe_allow_html=True)


# ── Data Loading & Modeling (cached) ─────────────────────────────────────────
@st.cache_data
def load_and_process():
    df = pd.read_csv('Telco-Customer-Churn.csv')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna(subset=['TotalCharges']).reset_index(drop=True)
    return df


@st.cache_resource
def train_models(df):
    # Keep customerID separately for display
    customer_ids = df['customerID'].values

    df_model = df.drop('customerID', axis=1).copy()
    df_model['Churn'] = (df_model['Churn'] == 'Yes').astype(int)

    le = LabelEncoder()
    for col in df_model.select_dtypes(include='object').columns:
        df_model[col] = le.fit_transform(df_model[col])

    X = df_model.drop('Churn', axis=1)
    y = df_model['Churn']

    # Use index to track customer IDs through the split
    idx = np.arange(len(X))
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, idx, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_s, y_train)
    y_pred_lr = lr.predict(X_test_s)
    y_prob_lr = lr.predict_proba(X_test_s)[:, 1]

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]

    def metrics(y_true, y_pred, y_prob):
        return {
            'Accuracy (%)': round(accuracy_score(y_true, y_pred) * 100, 2),
            'Precision (%)': round(precision_score(y_true, y_pred) * 100, 2),
            'Recall (%)': round(recall_score(y_true, y_pred) * 100, 2),
            'F1-Score (%)': round(f1_score(y_true, y_pred) * 100, 2),
            'ROC-AUC (%)': round(roc_auc_score(y_true, y_prob) * 100, 2),
        }

    results = {
        'Logistic Regression': metrics(y_test, y_pred_lr, y_prob_lr),
        'Random Forest': metrics(y_test, y_pred_rf, y_prob_rf),
    }

    # Build predictions dataframe with Customer ID
    preds_df = pd.DataFrame({
        'Customer ID': customer_ids[idx_test],
        'Actual_Churn': y_test.values,
        'Predicted_Churn': y_pred_lr,
        'Churn_Probability': y_prob_lr.round(4),
    })

    feat_imp = pd.Series(
        rf.feature_importances_, index=X.columns
    ).sort_values(ascending=False).head(10)

    return results, preds_df, feat_imp, y_test, y_pred_lr, y_pred_rf, y_prob_lr, y_prob_rf


df = load_and_process()
results, preds_df, feat_imp, y_test, y_pred_lr, y_pred_rf, y_prob_lr, y_prob_rf = train_models(df)

# ── Sidebar Navigation ────────────────────────────────────────────────────────
st.sidebar.markdown("## 📡 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dataset Summary", "Churn Analysis", "Visualizations",
     "Model Comparison", "Predictions", "Business Insights"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** Telco Customer Churn  \n**Records:** 7,032  \n**Features:** 20")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📡 Telco Customer Churn Prediction</div>', unsafe_allow_html=True)
st.markdown("Predict and understand customer churn using machine learning on the IBM Telco dataset.")
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Dataset Summary
# ══════════════════════════════════════════════════════════════════════════════
if page == "Dataset Summary":
    st.markdown('<div class="section-hdr">Dataset Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-val">7,032</div><div class="metric-lbl">Total Customers</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-val">20</div><div class="metric-lbl">Features</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-val">1,869</div><div class="metric-lbl">Churned Customers</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-val">26.58%</div><div class="metric-lbl">Overall Churn Rate</div></div>', unsafe_allow_html=True)

    st.markdown("### Raw Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown("### Statistical Summary")
    st.dataframe(df.describe().round(2), use_container_width=True)

    st.markdown("### Missing Values")
    mv = df.isnull().sum()
    mv = mv[mv > 0]
    if mv.empty:
        st.success("No missing values in the cleaned dataset.")
    else:
        st.dataframe(mv.rename("Missing Count"), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Churn Analysis
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Churn Analysis":
    st.markdown('<div class="section-hdr">Churn Analysis by Key Factors</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Contract Type")
        ct = df.groupby('Contract')['Churn'].apply(lambda x: round((x == 'Yes').mean() * 100, 2))
        st.dataframe(ct.rename("Churn Rate (%)"), use_container_width=True)

        st.markdown("#### Internet Service")
        ist = df.groupby('InternetService')['Churn'].apply(lambda x: round((x == 'Yes').mean() * 100, 2))
        st.dataframe(ist.rename("Churn Rate (%)"), use_container_width=True)

    with col2:
        st.markdown("#### Payment Method")
        pm = df.groupby('PaymentMethod')['Churn'].apply(lambda x: round((x == 'Yes').mean() * 100, 2))
        st.dataframe(pm.rename("Churn Rate (%)"), use_container_width=True)

        st.markdown("#### Tenure vs Monthly Charges")
        comp = pd.DataFrame({
            'Metric': ['Avg Tenure (months)', 'Avg Monthly Charges ($)'],
            'Churned': [17.98, 74.44],
            'Not Churned': [37.65, 61.31]
        })
        st.dataframe(comp.set_index('Metric'), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Visualizations
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Visualizations":
    st.markdown('<div class="section-hdr">Data Visualizations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Churn Distribution")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        churn_c = df['Churn'].value_counts()
        ax.bar(churn_c.index, churn_c.values, color=['#3b82d4', '#e05252'])
        for i, v in enumerate(churn_c.values):
            ax.text(i, v + 30, str(v), ha='center', fontsize=10)
        ax.set_ylabel("Count")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Churn Rate by Contract")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ct.plot(kind='bar', ax=ax, color='#3b82d4')
        ax.set_ylabel("Churn Rate (%)")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
        for i, v in enumerate(ct.values):
            ax.text(i, v + 0.5, f'{v}%', ha='center', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Tenure Distribution by Churn")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        df[df['Churn'] == 'No']['tenure'].plot(kind='hist', bins=30, ax=ax,
            alpha=0.7, color='#3b82d4', label='Not Churned')
        df[df['Churn'] == 'Yes']['tenure'].plot(kind='hist', bins=30, ax=ax,
            alpha=0.7, color='#e05252', label='Churned')
        ax.set_xlabel("Tenure (months)")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col4:
        st.markdown("#### Churn Rate by Payment Method")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        pm.plot(kind='bar', ax=ax, color='#7c5cd8')
        ax.set_ylabel("Churn Rate (%)")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
        for i, v in enumerate(pm.values):
            ax.text(i, v + 0.5, f'{v}%', ha='center', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("#### Top 10 Feature Importances (Random Forest)")
    fig, ax = plt.subplots(figsize=(8, 4))
    feat_imp.sort_values().plot(kind='barh', ax=ax, color='#3b82d4')
    ax.set_xlabel("Importance Score")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Model Comparison
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Model Comparison":
    st.markdown('<div class="section-hdr">Model Evaluation & Comparison</div>', unsafe_allow_html=True)

    results_df = pd.DataFrame(results).T
    st.markdown("#### Performance Metrics")

    cols = st.columns(len(results_df.columns))
    for i, metric in enumerate(results_df.columns):
        with cols[i]:
            lr_val = results['Logistic Regression'][metric]
            rf_val = results['Random Forest'][metric]
            st.metric(f"LR {metric}", f"{lr_val}%", f"{round(lr_val - rf_val, 2)}% vs RF")

    st.markdown("#### Full Comparison Table")
    st.dataframe(results_df, use_container_width=True)

    st.markdown('<span class="best-badge">✔ Best Model: Logistic Regression</span>', unsafe_allow_html=True)
    st.markdown("Logistic Regression outperforms Random Forest on Accuracy, Recall, F1-Score, and ROC-AUC — making it the preferred model for churn prediction.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ROC Curves")
        fig, ax = plt.subplots(figsize=(5, 4))
        for y_prob, label, color in [
            (y_prob_lr, f'LR (AUC={results["Logistic Regression"]["ROC-AUC (%)"]:.2f}%)', '#3b82d4'),
            (y_prob_rf, f'RF (AUC={results["Random Forest"]["ROC-AUC (%)"]:.2f}%)', '#7c5cd8')
        ]:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            ax.plot(fpr, tpr, label=label, linewidth=2, color=color)
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1)
        ax.set_xlabel("FPR"); ax.set_ylabel("TPR")
        ax.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Confusion Matrix — Logistic Regression")
        fig, ax = plt.subplots(figsize=(4, 3.5))
        cm = confusion_matrix(y_test, y_pred_lr)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['No Churn', 'Churn'],
                    yticklabels=['No Churn', 'Churn'])
        ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Predictions
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Predictions":
    st.markdown('<div class="section-hdr">Customer Churn Predictions (Test Set)</div>', unsafe_allow_html=True)

    disp_df = preds_df[['Customer ID', 'Actual_Churn', 'Predicted_Churn', 'Churn_Probability']].copy()
    disp_df['Risk Level'] = disp_df['Churn_Probability'].apply(
        lambda x: '🔴 High' if x > 0.7 else ('🟡 Medium' if x > 0.4 else '🟢 Low')
    )

    st.markdown(f"**Test set size:** 1,407 customers | **Churned (actual):** 374 | **Not Churned:** 1,033")

    col1, col2, col3 = st.columns(3)
    high_risk = preds_df[preds_df['Churn_Probability'] > 0.7]
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{len(high_risk)}</div><div class="metric-lbl">High-Risk Customers (≥70%)</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{int(high_risk["Actual_Churn"].sum())}</div><div class="metric-lbl">Actual Churners in High-Risk</div></div>', unsafe_allow_html=True)
    with col3:
        prec_hr = round(high_risk["Actual_Churn"].mean() * 100, 1) if len(high_risk) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-val">{prec_hr}%</div><div class="metric-lbl">Precision on High-Risk Group</div></div>', unsafe_allow_html=True)

    st.markdown("#### Prediction Results")
    risk_filter = st.selectbox("Filter by Risk Level", ["All", "🔴 High", "🟡 Medium", "🟢 Low"])
    if risk_filter != "All":
        st.dataframe(disp_df[disp_df['Risk Level'] == risk_filter].reset_index(drop=True).head(50), use_container_width=True)
    else:
        st.dataframe(disp_df.reset_index(drop=True).head(50), use_container_width=True)

    st.markdown("#### Churn Probability Distribution")
    fig, ax = plt.subplots(figsize=(8, 3))
    preds_df[preds_df['Actual_Churn'] == 0]['Churn_Probability'].plot(
        kind='hist', bins=40, ax=ax, alpha=0.7, color='#3b82d4', label='Not Churned')
    preds_df[preds_df['Actual_Churn'] == 1]['Churn_Probability'].plot(
        kind='hist', bins=40, ax=ax, alpha=0.7, color='#e05252', label='Churned')
    ax.set_xlabel("Churn Probability")
    ax.set_ylabel("Count")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6: Business Insights
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Business Insights":
    st.markdown('<div class="section-hdr">Key Findings & Business Recommendations</div>', unsafe_allow_html=True)

    st.markdown("### Key Findings")
    findings = [
        "Overall churn rate is <b>26.58%</b> — over 1 in 4 customers leaves.",
        "Month-to-month contract customers churn at <b>42.71%</b>, compared to only <b>2.85%</b> for two-year contracts.",
        "Fiber optic internet subscribers churn at <b>41.89%</b> — the highest among internet service types.",
        "Electronic check users have a <b>45.29%</b> churn rate — significantly higher than automatic payment methods (~16%).",
        "Customers with tenure under 12 months churn at <b>47.68%</b> — the highest-risk tenure group.",
        "Churned customers have average tenure of <b>17.98 months</b> vs <b>37.65 months</b> for retained customers.",
        "Churned customers pay <b>$74.44/month</b> on average vs <b>$61.31</b> for retained customers.",
        "Top predictors (Random Forest): TotalCharges (18.49%), MonthlyCharges (17.72%), tenure (15.91%), Contract (8.30%).",
    ]
    for f in findings:
        st.markdown(f'<div class="insight-box">🔍 {f}</div>', unsafe_allow_html=True)

    st.markdown("### Business Recommendations")
    recommendations = [
        ("<b>Promote Long-Term Contracts:</b>", "Offer discounts or loyalty rewards to encourage month-to-month customers to upgrade to annual or two-year plans."),
        ("<b>Investigate Fiber Optic Issues:</b>", "Address pricing and service quality concerns driving the 41.89% churn rate among fiber optic customers."),
        ("<b>Target Electronic Check Users:</b>", "Incentivize customers using electronic checks to switch to automatic payments, which correlate with lower churn."),
        ("<b>Early Tenure Retention Programs:</b>", "Customers with tenure under 12 months have a 47.68% churn rate — the highest of any tenure group. Implement proactive check-ins, onboarding support, and welcome offers in the first year."),
        ("<b>Deploy Churn Prediction Model:</b>", "Use Logistic Regression (ROC-AUC: 83.45%) to score all customers monthly and prioritize retention outreach for high-risk segments."),
        ("<b>Review High Monthly Charges:</b>", "Churned customers pay more on average. Offer tailored pricing plans to high-value customers showing churn signals."),
    ]
    for title, detail in recommendations:
        st.markdown(f'<div class="insight-box">💡 {title} {detail}</div>', unsafe_allow_html=True)

    st.markdown("### Model Summary")
    st.markdown("""
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Logistic Regression** ✔ | 79.39% | 62.43% | 56.42% | 59.27% | 83.45% |
| Random Forest | 78.32% | 61.77% | 48.40% | 54.27% | 81.13% |

**Logistic Regression** is selected as the best model — it delivers higher Recall and ROC-AUC, which are critical metrics for catching churners early.
""")
