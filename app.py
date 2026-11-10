import streamlit as st
import plotly.express as px
from agents.executive_agent import ExecutiveAgent

@st.cache_resource
def get_executive_agent():

    return ExecutiveAgent()

@st.cache_resource
def get_knowledge_agent():

    return KnowledgeAgent()

st.set_page_config(
    page_title="Agentic AI Customer Retention Platform",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 Agentic AI Customer Retention Platform"
)

tabs = st.tabs([
    "📊 Executive Dashboard",
    "🤖 AI Decision Center",
    "📚 Knowledge Assistant",
    "🎯 Campaign Simulator"
])

dashboard_tab = tabs[0]
decision_tab = tabs[1]
knowledge_tab = tabs[2]
simulator_tab = tabs[3]


from utils.dashboard_utils import (
    load_customer_data,
    calculate_kpis
)

with dashboard_tab:

    st.header("Executive Dashboard")

    df = load_customer_data()

    kpis = calculate_kpis(df)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Customers",
        kpis["total_customers"]
    )

    col2.metric(
        "High Risk",
        kpis["high_risk"]
    )

    col3.metric(
        "Medium Risk",
        kpis["medium_risk"]
    )

    col4.metric(
        "Low Risk",
        kpis["low_risk"]
    )

    col5.metric(
        "Revenue At Risk",
        f"${kpis['revenue_at_risk']:,.0f}"
    )

    col_left, col_right = st.columns(2)

    with col_left:

        risk_counts = (
            df["RiskLevel"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "RiskLevel",
            "Count"
        ]

        fig = px.pie(
            risk_counts,
            names="RiskLevel",
            values="Count",
            title="Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
    with col_right:

        segment_counts = (
            df["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = [
            "Segment",
            "Customers"
        ]

        fig = px.bar(
            segment_counts,
            x="Segment",
            y="Customers",
            title="Customer Segment Distribution",
            color="Customers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )    
    
    col_left, col_right = st.columns(2)
    with col_left:

        fig = px.histogram(
            df,
            x="ChurnProbability",
            nbins=20,
            title="Churn Probability Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )   
    
    with col_right:

        revenue = (
            df.groupby("Segment")
            ["MonthlyCharges"]
            .sum()
            .reset_index()
        )

        fig = px.treemap(
            revenue,
            path=["Segment"],
            values="MonthlyCharges",
            title="Revenue at Risk by Segment"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
    st.subheader(
        "Top High-Risk Customers"
    )

    top_customers = (
        df.sort_values(
            "ChurnProbability",
            ascending=False
        )
        [
            [
                "customerID",
                "Segment",
                "RiskLevel",
                "ChurnProbability",
                "MonthlyCharges"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        top_customers,
        use_container_width=True
    )    
        
with decision_tab:

    st.header(
        "🤖 AI Decision Center"
    )

    if "analysis_result" not in st.session_state:

        st.session_state.analysis_result = None

    customer_ids = (
        df["customerID"]
        .tolist()
    )

    selected_customer = st.selectbox(
        "Select Customer",
        customer_ids
    )

    if st.button(
        "🚀 Run Executive Agent"
    ):

        with st.status(
            "Running Executive Agent...",
            expanded=True
        ) as status:

            status.write(
                "✅ Explainability Agent"
            )

            status.write(
                "✅ Retention Agent"
            )

            status.write(
                "✅ Marketing Agent"
            )

            status.write(
                "✅ Knowledge Agent"
            )

            agent = get_executive_agent()

            st.session_state.analysis_result = (
                agent.run(
                    selected_customer
                )
            )

            status.update(
                label="Analysis Complete",
                state="complete"
            )

    if st.session_state.analysis_result:

        result = (
            st.session_state.analysis_result
        )

        st.subheader(
            "Executive Summary"
        )

        st.info(
            result["executive_summary"]
        )

        explanation = (
            result["explanation"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Risk Level",
            explanation["risk_level"]
        )

        col2.metric(
            "Segment",
            explanation["segment"]
        )

        col3.metric(
            "Churn Probability",
            f"{explanation['churn_probability']:.2%}"
        )

        st.subheader(
            "Top Churn Drivers"
        )

        import pandas as pd

        driver_df = pd.DataFrame(
            explanation["top_drivers"]
        )

        st.dataframe(
            driver_df,
            use_container_width=True
        )

        strategy = (
            result["retention_strategy"]
        )

        st.subheader(
            "Retention Strategy"
        )

        st.success(
            f"""
Offer: {strategy['offer']}

Channel: {strategy['channel']}

Priority: {strategy['priority']}

Expected Lift:
{strategy['expected_lift']}
"""
        )

        st.subheader(
            "Marketing Campaign"
        )

        with st.expander(
            "View Campaign"
        ):

            st.write(
                result["campaign"][
                    "campaign_text"
                ]
            )

        st.subheader(
            "Knowledge Insights"
        )

        st.warning(
            result["knowledge"]["answer"]
        )

    
from agents.knowledge_agent import (
    KnowledgeAgent
)
with knowledge_tab:

    st.header(
        "📚 Knowledge Assistant"
    )

    st.markdown(
        """
Ask questions about:

• Retention Policies

• Customer Segments

• Historical Campaigns

• Approved Offers

• Customer Retention Strategy
"""
    )

    if "knowledge_response" not in st.session_state:

        st.session_state.knowledge_response = None

    question = st.text_area(
        "Ask a business question",
        height=120,
        placeholder=
        "What retention strategy works best for loyal customers?"
    )

    if st.button(
        "🔍 Ask Knowledge Assistant"
    ):

        with st.spinner(
            "Searching knowledge base..."
        ):

            agent = get_knowledge_agent()

            response = agent.ask(
                question
            )

            st.session_state.knowledge_response = (
                response
            )

    if st.session_state.knowledge_response:

        response = (
            st.session_state
            .knowledge_response
        )

        st.subheader(
            "AI Answer"
        )

        st.info(
            response["answer"]
        )

        st.subheader(
            "Retrieved Sources"
        )

        for idx, source in enumerate(
            response["sources"],
            start=1
        ):

            with st.expander(
                f"Source {idx}"
            ):

                st.write(
                    source
                )


with simulator_tab:

    st.header(
        "🎯 Campaign Simulator"
    )

    segment = st.selectbox(
        "Customer Segment",
        [
            "Champions",
            "Loyal Customers",
            "At Risk",
            "Price Sensitive",
            "New Customers"
        ]
    )

    offer = st.selectbox(
        "Retention Offer",
        [
            "20% Cashback",
            "15% Discount Upgrade",
            "Reward Point Bonus",
            "Premium Loyalty Reward",
            "VIP Benefits Package"
        ]
    )

    if st.button(
        "Run Campaign Simulation"
    ):
        campaign_data = {

            "Champions": {
                "response_rate": 72,
                "retention_lift": 18,
                "channel":
                    "Relationship Manager"
            },

            "Loyal Customers": {
                "response_rate": 65,
                "retention_lift": 14,
                "channel":
                    "Email"
            },

            "At Risk": {
                "response_rate": 58,
                "retention_lift": 21,
                "channel":
                    "Phone Call + Email"
            },

            "Price Sensitive": {
                "response_rate": 61,
                "retention_lift": 16,
                "channel":
                    "Email + SMS"
            },

            "New Customers": {
                "response_rate": 55,
                "retention_lift": 12,
                "channel":
                    "App Notification"
            }
        }
        
        result = (
            campaign_data[
                segment
            ]
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Response Rate",
            f"{result['response_rate']}%"
        )

        c2.metric(
            "Retention Lift",
            f"{result['retention_lift']}%"
        )

        c3.metric(
            "Recommended Channel",
            result["channel"]
        )
        
        import pandas as pd
        import plotly.express as px

        sim_df = pd.DataFrame({

            "Metric": [
                "Response Rate",
                "Retention Lift"
            ],

            "Value": [
                result["response_rate"],
                result["retention_lift"]
            ]
        })

        fig = px.bar(
            sim_df,
            x="Metric",
            y="Value",
            color="Metric",
            title="Campaign Outcome Projection"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        st.subheader(
            "Campaign Recommendation"
        )

        st.info(
            f"""
Segment:
{segment}

Offer:
{offer}

Recommended Channel:
{result['channel']}

Expected Response Rate:
{result['response_rate']}%

Expected Retention Lift:
{result['retention_lift']}%

This campaign is expected to
increase engagement and reduce
customer churn within the target
segment.
"""
        )
