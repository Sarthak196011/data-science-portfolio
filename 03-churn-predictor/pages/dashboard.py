import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def show():
    st.markdown("# 📊 Analytics Dashboard")
    st.markdown("Explore model performance, customer segments, and churn drivers.")
    st.divider()

    pred_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'test_predictions.csv')
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'telecom_churn.csv')

    if not os.path.exists(pred_path):
        st.warning("Run `python models/train_model.py` to generate predictions for the dashboard.")
        return

    df_pred = pd.read_csv(pred_path)
    df_full = pd.read_csv(data_path)

    # ── KPI Row ───────────────────────────────────────────────────────────────
    from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
    acc  = accuracy_score(df_pred['churn'], df_pred['predicted'])
    auc  = roc_auc_score(df_pred['churn'], df_pred['churn_proba'])
    prec = precision_score(df_pred['churn'], df_pred['predicted'])
    rec  = recall_score(df_pred['churn'], df_pred['predicted'])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Accuracy",  f"{acc*100:.1f}%")
    c2.metric("AUC-ROC",   f"{auc:.3f}")
    c3.metric("Precision", f"{prec*100:.1f}%")
    c4.metric("Recall",    f"{rec*100:.1f}%")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📈 Model Performance","👥 Customer Segments","🔍 Churn Drivers"])

    # ── Tab 1: Model Performance ──────────────────────────────────────────────
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # ROC Curve
            from sklearn.metrics import roc_curve
            fpr, tpr, _ = roc_curve(df_pred['churn'], df_pred['churn_proba'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f'ROC (AUC={auc:.3f})',
                                     line=dict(color='#00d4ff', width=2)))
            fig.add_trace(go.Scatter(x=[0,1], y=[0,1], name='Random',
                                     line=dict(color='gray', dash='dash')))
            fig.update_layout(title="ROC Curve", xaxis_title="FPR", yaxis_title="TPR",
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                              font=dict(color='white'), height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Confusion matrix
            from sklearn.metrics import confusion_matrix
            cm = confusion_matrix(df_pred['churn'], df_pred['predicted'])
            fig2 = px.imshow(cm, text_auto=True,
                             labels=dict(x="Predicted", y="Actual", color="Count"),
                             x=['Retained','Churned'], y=['Retained','Churned'],
                             color_continuous_scale='Blues')
            fig2.update_layout(title="Confusion Matrix",
                               paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # Probability distribution
        fig3 = px.histogram(df_pred, x='churn_proba', color=df_pred['churn'].map({0:'Retained',1:'Churned'}),
                            nbins=40, barmode='overlay', opacity=0.7,
                            color_discrete_map={'Retained':'#10b981','Churned':'#ef4444'},
                            title="Churn Probability Distribution")
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                           font=dict(color='white'), height=300)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 2: Customer Segments ───────────────────────────────────────────────
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            churn_by_contract = df_full.groupby('contract_type')['churn'].mean().reset_index()
            fig = px.bar(churn_by_contract, x='contract_type', y='churn',
                         title="Churn Rate by Contract Type",
                         color='churn', color_continuous_scale='RdYlGn_r')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                              font=dict(color='white'), height=320)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            churn_by_internet = df_full.groupby('internet_service')['churn'].mean().reset_index()
            fig = px.pie(churn_by_internet, names='internet_service', values='churn',
                         title="Churn Distribution by Internet Service",
                         color_discrete_sequence=['#00d4ff','#8b5cf6','#10b981'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=320)
            st.plotly_chart(fig, use_container_width=True)

        fig = px.box(df_full, x='churn', y='monthly_charges',
                     color=df_full['churn'].map({0:'Retained',1:'Churned'}),
                     title="Monthly Charges vs Churn",
                     color_discrete_map={'Retained':'#10b981','Churned':'#ef4444'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                          font=dict(color='white'), height=320)
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 3: Churn Drivers ──────────────────────────────────────────────────
    with tab3:
        fig = px.scatter(df_full.sample(500), x='tenure_months', y='monthly_charges',
                         color=df_full.sample(500)['churn'].map({0:'Retained',1:'Churned'}),
                         size='support_calls', opacity=0.7,
                         title="Tenure vs Monthly Charges (sized by Support Calls)",
                         color_discrete_map={'Retained':'#10b981','Churned':'#ef4444'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                          font=dict(color='white'), height=400)
        st.plotly_chart(fig, use_container_width=True)

        corr_cols = ['tenure_months','monthly_charges','support_calls','payment_delays','num_products','churn']
        corr = df_full[corr_cols].corr()
        fig2 = px.imshow(corr, text_auto='.2f', title="Feature Correlation Heatmap",
                         color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400)
        st.plotly_chart(fig2, use_container_width=True)
