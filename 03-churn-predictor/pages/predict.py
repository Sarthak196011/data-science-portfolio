import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pages.model_utils import load_artifacts, predict_churn

def show():
    st.markdown("# 🎯 What-If Scenario Simulator")
    st.markdown("Adjust the customer metrics below. The machine learning model will predict the churn risk dynamically in real-time.")
    st.divider()

    artifacts = load_artifacts()
    if artifacts is None:
        st.error("⚠️ Model not found. Run `models/train_model.py` first to train the model.")
        return

    # ── Input container (What-If Controls) ────────────────────────────────────
    st.markdown("### 📋 Live Customer Profile Inputs")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**Account Parameters**")
        tenure       = st.slider("Tenure (months)", 1, 72, 12)
        contract     = st.selectbox("Contract Type", ["Month-to-month","One year","Two year"])
        payment_del  = st.slider("Payment Delays (months)", 0, 5, 0)

    with c2:
        st.markdown("**Financials**")
        monthly_chg  = st.slider("Monthly Charges ($)", 20.0, 120.0, 65.0, 0.5)
        total_chg    = st.number_input("Total Charges ($)", 100.0, 8000.0, float(monthly_chg * tenure))
        num_products = st.slider("Number of Connected Products", 1, 4, 2)

    with c3:
        st.markdown("**Technical Services**")
        internet     = st.selectbox("Internet Service Type", ["DSL","Fiber optic","No"])
        online_sec   = st.selectbox("Online Security Feature", ["Yes","No"])
        tech_support = st.selectbox("Tech Support Subscription", ["Yes","No"])

    st.markdown("**Demographics & Support Activity**")
    dc1, dc2, dc3, dc4, dc5 = st.columns(5)
    gender     = dc1.selectbox("Gender", ["Male","Female"])
    senior     = dc2.selectbox("Senior Citizen Status", [0, 1], format_func=lambda x: "Yes" if x else "No")
    partner    = dc3.selectbox("Has Partner", ["Yes","No"])
    dependents = dc4.selectbox("Has Dependents", ["Yes","No"])
    paperless  = dc5.selectbox("Paperless Billing", ["Yes","No"])
    support_calls = st.slider("Support Calls (last 12 months)", 0, 10, 2)

    # ── Dynamic Prediction Calculation ────────────────────────────────────────
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
    st.markdown("## 📊 Real-Time Risk Analysis")

    # ── Gauge chart ───────────────────────────────────────────────────────
    col_g, col_r = st.columns([1, 1])
    with col_g:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct,
            title={'text': "Dynamic Churn Probability", 'font': {'size': 18, 'color': '#0f172a'}},
            number={'suffix': "%", 'font': {'color': '#0f172a', 'size': 44}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': 'gray'},
                'bar': {'color': '#ef4444' if pct > 60 else '#f59e0b' if pct > 35 else '#10b981'},
                'bgcolor': 'rgba(15,23,42,0.05)',
                'bordercolor': 'rgba(15,23,42,0.1)',
                'steps': [
                    {'range': [0, 35],  'color': 'rgba(16,185,129,0.08)'},
                    {'range': [35, 60], 'color': 'rgba(245,158,11,0.08)'},
                    {'range': [60, 100],'color': 'rgba(239,68,68,0.08)'},
                ],
            }
        ))
        fig.update_layout(
            height=260,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0f172a'},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        if pct > 60:
            st.markdown(f"""
            <div class='churn-high'>
              <h3>🚨 HIGH CHURN RISK</h3>
              <p style='font-size:1.8rem;font-weight:800;color:#991b1b;margin: 5px 0;'>{pct:.1f}% probability</p>
              <p>Critical churn threshold breached. Retention actions should be initiated immediately.</p>
            </div>""", unsafe_allow_html=True)
        elif pct > 35:
            st.markdown(f"""
            <div style='background:#fef3c7;border:1px solid #fde68a;border-radius:10px;padding:16px;color:#92400e'>
              <h3>⚠️ MODERATE CHURN RISK</h3>
              <p style='font-size:1.8rem;font-weight:800;color:#b45309;margin: 5px 0;'>{pct:.1f}% probability</p>
              <p>Warning signals detected. Proactive customer success check-in recommended.</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='churn-low'>
              <h3>✅ LOW CHURN RISK</h3>
              <p style='font-size:1.8rem;font-weight:800;color:#166534;margin: 5px 0;'>{pct:.1f}% probability</p>
              <p>Healthy customer signals. Standard operational lifecycle communication applicable.</p>
            </div>""", unsafe_allow_html=True)

    # ── SHAP-style feature importance (approximate) ────────────────────────
    st.divider()
    col_l, col_rec = st.columns([1.2, 1])

    with col_l:
        st.markdown("### 🧠 Why This Prediction? (Feature Contributions)")
        model = artifacts['model']
        importance = model.feature_importances_
        feat_names = artifacts['feature_cols']
        top_idx    = np.argsort(importance)[::-1][:6]

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
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.01)',
            font={'color': '#0f172a'},
            margin=dict(l=10, r=40, t=10, b=10),
            xaxis_title="Importance Score",
            height=280,
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_rec:
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

        # ── AI Retention Email Generator ──────────────────────────────────────────
        st.divider()
        st.markdown("### ✉️ AI Retention Email Draft")
        
        openai_key = st.session_state.get("openai_key", "")
        
        if st.button("✉️ Draft Retention Email with AI", use_container_width=True):
            with st.spinner("Writing email..."):
                if openai_key:
                    try:
                        import openai
                        client = openai.OpenAI(api_key=openai_key)
                        prompt = (
                            f"Write a highly professional, polite customer retention email. "
                            f"Customer profile details: Contract type: {contract}, Monthly charges: ${monthly_chg:.2f}, "
                            f"Tenure: {tenure} months, Support calls: {support_calls}. "
                            f"Targeted retention offer: {recs[0] if recs else 'Standard check-in'}. "
                            f"Keep it concise, friendly, and structured. Return ONLY the email subject and body."
                        )
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role":"user","content":prompt}],
                            max_tokens=350, temperature=0.3
                        )
                        email_content = resp.choices[0].message.content
                        st.text_area("AI Drafted Email", email_content, height=220)
                    except Exception as e:
                        st.error(f"Failed to generate email via OpenAI: {str(e)}")
                else:
                    # Professional custom mock email draft based on values
                    offer_desc = recs[0] if recs else "Standard satisfaction check-in"
                    mock_email = (
                        f"Subject: A Special Offer for Your Account — ChurnShield AI\n\n"
                        f"Dear Valued Customer,\n\n"
                        f"Thank you for being a customer with us for the last {tenure} months. We value your business "
                        f"and want to ensure you are receiving the best possible service.\n\n"
                        f"We noticed that you are currently on a {contract} plan. To show our appreciation, "
                        f"we would love to offer you the following upgrade: {offer_desc}.\n\n"
                        f"If you have any questions or would like to apply this offer, please reply directly to this email "
                        f"or connect with our customer success team.\n\n"
                        f"Best regards,\n"
                        f"Customer Success Team\n"
                        f"ChurnShield AI"
                    )
                    st.text_area("AI Drafted Email (Demo Mode)", mock_email, height=220)
