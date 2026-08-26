import streamlit as st
import pandas as pd
import io
from pages.model_utils import load_artifacts, predict_churn

SAMPLE_CSV = """tenure_months,monthly_charges,total_charges,num_products,support_calls,payment_delays,contract_type,internet_service,online_security,tech_support,paperless_billing,gender,senior_citizen,partner,dependents
6,89.5,537.0,1,7,3,Month-to-month,Fiber optic,No,No,Yes,Female,0,No,No
36,55.0,1980.0,3,1,0,One year,DSL,Yes,Yes,No,Male,0,Yes,Yes
2,105.0,210.0,1,8,4,Month-to-month,Fiber optic,No,No,Yes,Male,1,No,No
48,45.0,2160.0,4,0,0,Two year,DSL,Yes,Yes,No,Female,0,Yes,Yes
14,72.0,1008.0,2,3,1,Month-to-month,Fiber optic,No,Yes,Yes,Male,0,No,No
"""

def show():
    st.markdown("# 📦 Batch Customer Scoring")
    st.markdown("Upload a CSV file with multiple customers to score them all at once.")
    st.divider()

    artifacts = load_artifacts()
    if artifacts is None:
        st.error("⚠️ Model not found. Run `python models/train_model.py` first.")
        return

    col1, col2 = st.columns([2,1])
    with col1:
        uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    with col2:
        st.markdown("**Download sample CSV:**")
        st.download_button(
            "⬇️ Sample CSV Template",
            data=SAMPLE_CSV,
            file_name="sample_customers.csv",
            mime="text/csv",
        )

    df_source = None
    if uploaded:
        df_source = pd.read_csv(uploaded)
        st.success(f"✅ Loaded {len(df_source)} customers")
    else:
        if st.button("📋 Use Sample Data (5 customers)"):
            df_source = pd.read_csv(io.StringIO(SAMPLE_CSV))

    if df_source is not None:
        required = ['tenure_months','monthly_charges','total_charges','num_products',
                    'support_calls','payment_delays','contract_type','internet_service',
                    'online_security','tech_support','paperless_billing','gender',
                    'senior_citizen','partner','dependents']
        missing = [c for c in required if c not in df_source.columns]
        if missing:
            st.error(f"Missing columns: {missing}")
            return

        with st.spinner("Scoring customers…"):
            probas = []
            for _, row in df_source.iterrows():
                p = predict_churn(artifacts, row.to_dict())
                probas.append(round(p * 100, 1))

        df_out = df_source.copy()
        df_out['churn_probability_%'] = probas
        df_out['risk_level'] = df_out['churn_probability_%'].apply(
            lambda x: "🚨 High" if x > 60 else "⚠️ Medium" if x > 35 else "✅ Low"
        )
        df_out = df_out.sort_values('churn_probability_%', ascending=False)

        st.divider()
        st.markdown("### 📊 Scoring Results")

        # summary
        high   = (df_out['churn_probability_%'] > 60).sum()
        medium = ((df_out['churn_probability_%'] > 35) & (df_out['churn_probability_%'] <= 60)).sum()
        low    = (df_out['churn_probability_%'] <= 35).sum()
        c1,c2,c3 = st.columns(3)
        c1.metric("🚨 High Risk",   high,   delta=f"{high/len(df_out)*100:.0f}% of total")
        c2.metric("⚠️ Medium Risk", medium, delta=f"{medium/len(df_out)*100:.0f}% of total")
        c3.metric("✅ Low Risk",    low,    delta=f"{low/len(df_out)*100:.0f}% of total")

        st.dataframe(
            df_out[['churn_probability_%','risk_level','tenure_months','monthly_charges','contract_type']],
            use_container_width=True,
            height=300,
        )

        csv_out = df_out.to_csv(index=False)
        st.download_button(
            "⬇️ Download Scored Results",
            data=csv_out,
            file_name="churn_predictions.csv",
            mime="text/csv",
        )
