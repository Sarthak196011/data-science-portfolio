import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pages.model_utils import load_artifacts, predict_churn

def show():
    st.markdown("# 🎯 Single Customer Prediction")
    st.markdown("Fill in the customer details below to get an instant churn probability score with AI explanation.")
    st.divider()

    artifacts = load_artifacts()
    if artifacts is None:
        st.error("⚠️ Model not found. Run `python models/train_model.py` first to train the model.")
        return

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("predict_form"):
        st.markdown("### 📋 Customer Profile")
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**Account Info**")
            tenure       = st.slider("Tenure (months)", 1, 72, 12)
            contract     = st.selectbox("Contract Type", ["Month-to-month","One year","Two year"])
            payment_del  = st.slider("Payment Delays", 0, 5, 0)

        with c2:
            st.markdown("**Charges**")
            monthly_chg  = st.slider("Monthly Charges ($)", 20.0, 120.0, 65.0, 0.5)
            total_chg    = st.number_input("Total Charges ($)", 100.0, 8000.0, float(monthly_chg * tenure))
            num_products = st.slider("Number of Products", 1, 4, 2)

        with c3:
            st.markdown("**Services**")
            internet     = st.selectbox("Internet Service", ["DSL","Fiber optic","No"])
            online_sec   = st.selectbox("Online Security", ["Yes","No"])
            tech_support = st.selectbox("Tech Support", ["Yes","No"])

        st.markdown("**Demographics**")
        dc1, dc2, dc3, dc4, dc5 = st.columns(5)
        gender     = dc1.selectbox("Gender", ["Male","Female"])
        senior     = dc2.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x else "No")
        partner    = dc3.selectbox("Partner", ["Yes","No"])
        dependents = dc4.selectbox("Dependents", ["Yes","No"])
        paperless  = dc5.selectbox("Paperless Billing", ["Yes","No"])
        support_calls = st.slider("Support Calls (last year)", 0, 10, 2)

        submitted = st.form_submit_button("🔮 Predict Churn Risk", use_container_width=True)

    if submitted:
        input_dict = {
            'tenure_months': tenure,
            'monthly_charges': monthly_chg,
            'total_charges': total_chg,
            'num_products': num_products,
            'support_calls': support_calls,
            'payment_delays': payment_del,
            'contract_type': contract,
            'internet_service': internet,
            'online_security': online_sec,
            'tech_support': tech_support,
            'paperless_billing': paperless,
            'gender': gender,
            'senior_citizen': senior,
            'partner': partner,
            'dependents': dependents,
        }

        proba = predict_churn(artifacts, input_dict)
        pct   = proba * 100

        st.divider()
        st.markdown("## 📊 Prediction Result")

        # ── Gauge chart ───────────────────────────────────────────────────────
        col_g, col_r = st.columns([1, 1])
        with col_g:
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                title={'text': "Churn Probability", 'font': {'size': 20, 'color': 'white'}},
                number={'suffix': "%", 'font': {'color': 'white', 'size': 48}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': 'gray'},
                    'bar': {'color': '#ef4444' if pct > 60 else '#f59e0b' if pct > 35 else '#10b981'},
                    'bgcolor': 'rgba(255,255,255,0.05)',
                    'bordercolor': 'rgba(255,255,255,0.1)',
                    'steps': [
                        {'range': [0, 35],  'color': 'rgba(16,185,129,0.1)'},
                        {'range': [35, 60], 'color': 'rgba(245,158,11,0.1)'},
                        {'range': [60, 100],'color': 'rgba(239,68,68,0.1)'},
                    ],
                    'threshold': {'line': {'color': 'white', 'width': 3}, 'value': 50}
                }
            ))
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if pct > 60:
                st.markdown(f"""
                <div class='churn-high'>
                  <h3>🚨 HIGH CHURN RISK</h3>
                  <p style='font-size:1.5rem;font-weight:800;color:#ef4444'>{pct:.1f}% probability</p>
                  <p>Immediate action recommended. Consider a retention offer.</p>
                </div>""", unsafe_allow_html=True)
            elif pct > 35:
                st.markdown(f"""
                <div style='background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.4);border-radius:10px;padding:16px'>
                  <h3>⚠️ MEDIUM CHURN RISK</h3>
                  <p style='font-size:1.5rem;font-weight:800;color:#f59e0b'>{pct:.1f}% probability</p>
                  <p>Monitor this customer. Proactive outreach advised.</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='churn-low'>
                  <h3>✅ LOW CHURN RISK</h3>
                  <p style='font-size:1.5rem;font-weight:800;color:#10b981'>{pct:.1f}% probability</p>
                  <p>Customer appears satisfied. Standard engagement recommended.</p>
                </div>""", unsafe_allow_html=True)

        # ── SHAP-style feature importance (approximate) ────────────────────────
        st.divider()
        st.markdown("### 🧠 Why This Prediction? (Feature Contributions)")

        model = artifacts['model']
        importance = model.feature_importances_
        feat_names = artifacts['feature_cols']
        top_idx    = np.argsort(importance)[::-1][:8]

        vals  = importance[top_idx]
        names = [feat_names[i].replace('_',' ').title() for i in top_idx]

        colors = ['#ef4444' if v > 0.08 else '#f59e0b' if v > 0.04 else '#10b981' for v in vals]

        fig2 = go.Figure(go.Bar(
            x=vals[::-1], y=names[::-1],
            orientation='h',
            marker_color=colors[::-1],
            text=[f"{v:.3f}" for v in vals[::-1]],
            textposition='outside',
        ))
        fig2.update_layout(
            title="Top Feature Importances (XGBoost)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.02)',
            font={'color': 'white'},
            xaxis_title="Importance Score",
            height=350,
        )
        st.plotly_chart(fig2, use_container_width=True)

        # ── Recommendations ───────────────────────────────────────────────────
        st.markdown("### 💡 Retention Recommendations")
        recs = []
        if contract == "Month-to-month":   recs.append("📋 Offer a discounted annual contract upgrade")
        if monthly_chg > 80:               recs.append("💰 Consider a loyalty pricing discount (10-15%)")
        if tenure < 12:                    recs.append("🎁 New customer bonus: free month or service upgrade")
        if support_calls > 5:              recs.append("🤝 Assign a dedicated account manager")
        if online_sec == "No":             recs.append("🔒 Offer free Online Security add-on for 3 months")
        if not recs:                       recs.append("✅ Customer profile looks healthy — standard engagement")
        for r in recs:
            st.markdown(f"- {r}")
