"""
Executive Report Agent

Purpose
-------
Generate DOCX Executive Reports
from Executive Agent output.
"""

from datetime import datetime
from pathlib import Path

from docx import Document


class ExecutiveReportAgent:

    def __init__(self):

        Path("reports").mkdir(
            exist_ok=True
        )

    def generate_report(
        self,
        executive_result
    ):

        customer_id = (
            executive_result["customer_id"]
        )

        document = Document()

        document.add_heading(
            "Customer Retention Executive Report",
            level=0
        )

        document.add_paragraph(
            f"Generated: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

        # --------------------------------
        # Executive Summary
        # --------------------------------

        document.add_heading(
            "1. Executive Summary",
            level=1
        )

        document.add_paragraph(
            executive_result[
                "executive_summary"
            ]
        )

        # --------------------------------
        # Risk Analysis
        # --------------------------------

        explanation = (
            executive_result[
                "explanation"
            ]
        )

        document.add_heading(
            "2. Customer Risk Analysis",
            level=1
        )

        document.add_paragraph(
            f"Customer ID: "
            f"{explanation['customer_id']}"
        )

        document.add_paragraph(
            f"Risk Level: "
            f"{explanation['risk_level']}"
        )

        document.add_paragraph(
            f"Customer Segment: "
            f"{explanation['segment']}"
        )

        document.add_paragraph(
            f"Churn Probability: "
            f"{explanation['churn_probability']}"
        )

        # --------------------------------
        # SHAP Drivers
        # --------------------------------

        document.add_heading(
            "3. SHAP Churn Drivers",
            level=1
        )

        drivers = (
            explanation[
                "top_drivers"
            ]
        )

        for driver in drivers:

            document.add_paragraph(
                f"{driver['Feature']} : "
                f"{round(driver['Impact'],4)}",
                style="List Bullet"
            )

        # --------------------------------
        # Retention
        # --------------------------------

        strategy = (
            executive_result[
                "retention_strategy"
            ]
        )

        document.add_heading(
            "4. Retention Strategy",
            level=1
        )

        document.add_paragraph(
            f"Offer: {strategy['offer']}"
        )

        document.add_paragraph(
            f"Channel: {strategy['channel']}"
        )

        document.add_paragraph(
            f"Priority: {strategy['priority']}"
        )

        document.add_paragraph(
            f"Expected Lift: "
            f"{strategy['expected_lift']}"
        )

        document.add_paragraph(
            strategy["justification"]
        )

        # --------------------------------
        # Marketing Campaign
        # --------------------------------

        campaign = (
            executive_result[
                "campaign"
            ]
        )

        document.add_heading(
            "5. Marketing Campaign",
            level=1
        )

        document.add_paragraph(
            campaign["subject"]
        )

        document.add_paragraph(
            campaign["campaign_text"]
        )

        # --------------------------------
        # Knowledge Insights
        # --------------------------------

        document.add_heading(
            "6. Knowledge Insights",
            level=1
        )

        document.add_paragraph(
            executive_result[
                "knowledge"
            ]["answer"]
        )

        # --------------------------------
        # Final Recommendation
        # --------------------------------

        document.add_heading(
            "7. Final Executive Recommendation",
            level=1
        )

        document.add_paragraph(
            executive_result[
                "executive_summary"
            ]
        )

        filename = (
            f"reports/"
            f"Retention_Report_"
            f"{customer_id}.docx"
        )

        document.save(filename)

        return filename