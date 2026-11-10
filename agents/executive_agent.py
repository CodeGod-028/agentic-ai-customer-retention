"""
Executive Agent

Master Orchestrator

Workflow

Customer
    ↓
Explainability Agent
    ↓
Retention Agent
    ↓
Marketing Agent
    ↓
Knowledge Agent (Gemini + RAG)
    ↓
Executive Recommendation
"""

import pandas as pd

from agents.explainability_agent import ExplainabilityAgent
from agents.retention_agent import RetentionAgent
from agents.marketing_agent import MarketingAgent
from agents.knowledge_agent import KnowledgeAgent


class ExecutiveAgent:

    def __init__(self):

        self.explainability_agent = ExplainabilityAgent()

        self.retention_agent = RetentionAgent()

        self.marketing_agent = MarketingAgent()

        self.knowledge_agent = KnowledgeAgent()

        self.customer_df = pd.read_csv(
            "data/customer_segments.csv"
        )

    def run(
        self,
        customer_id
    ):

        print("Running Explainability Agent...")

        explanation = (
            self.explainability_agent
            .generate_explanation(
                customer_id
            )
        )

        risk_level = explanation["risk_level"]

        segment = explanation["segment"]

        print("Running Retention Agent...")

        retention_strategy = (
            self.retention_agent
            .generate_retention_strategy(
                risk_level=risk_level,
                segment=segment
            )
        )

        print("Running Marketing Agent...")

        campaign = (
            self.marketing_agent
            .generate_campaign(
                customer_id=customer_id,
                segment=segment,
                offer=retention_strategy["offer"],
                channel=retention_strategy["channel"],
                priority=retention_strategy["priority"]
            )
        )

        question = f"""
Customer Segment: {segment}

Risk Level: {risk_level}

Recommended Offer:
{retention_strategy['offer']}

Provide executive retention insights.
"""

        print("Running Knowledge Agent...")

        try:

            knowledge = (
                self.knowledge_agent.ask(
                    question
                )
            )

        except Exception as ex:

            print(
                f"Knowledge Agent Error: {str(ex)}"
            )

            knowledge = {
                "answer":
                """
Executive Insight

Knowledge service is currently unavailable.

Based on predictive analytics,
customer segmentation,
and retention strategy analysis,
the recommended offer should be
executed through the proposed channel.

Customer monitoring is recommended
for the next 30 days.
                """,

                "sources": []
            }

        executive_summary = (
            self.build_summary(
                explanation,
                retention_strategy
            )
        )

        return {

            "customer_id": customer_id,

            "explanation": explanation,

            "retention_strategy":
                retention_strategy,

            "campaign": campaign,

            "knowledge": knowledge,

            "executive_summary":
                executive_summary
        }

    def build_summary(

        self,

        explanation,

        strategy

    ):

        return f"""
Customer ID:
{explanation['customer_id']}

Risk Level:
{explanation['risk_level']}

Segment:
{explanation['segment']}

Churn Probability:
{explanation['churn_probability']}

Recommended Offer:
{strategy['offer']}

Preferred Channel:
{strategy['channel']}

Priority:
{strategy['priority']}

Expected Retention Lift:
{strategy['expected_lift']}
"""


if __name__ == "__main__":

    df = pd.read_csv(
        "data/customer_segments.csv"
    )

    customer_id = (
        df.iloc[0]["customerID"]
    )

    agent = ExecutiveAgent()

    result = agent.run(
        customer_id
    )

    print("\n")
    print("=" * 70)
    print("EXECUTIVE AGENT RESULT")
    print("=" * 70)

    print(
        result["executive_summary"]
    )

    print("\n")
    print("KNOWLEDGE INSIGHT")
    print("-" * 70)

    print(
        result["knowledge"]["answer"]
    )

    print("\n")
    print("RETENTION STRATEGY")
    print("-" * 70)

    print(
        result["retention_strategy"]
    )