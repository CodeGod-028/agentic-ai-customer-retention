import pandas as pd


def load_customer_data():

    return pd.read_csv(
        "data/customer_segments.csv"
    )


def calculate_kpis(df):

    total_customers = len(df)

    high_risk = len(
        df[df["RiskLevel"] == "High"]
    )

    medium_risk = len(
        df[df["RiskLevel"] == "Medium"]
    )

    low_risk = len(
        df[df["RiskLevel"] == "Low"]
    )

    revenue_at_risk = round(
        df[
            df["RiskLevel"] == "High"
        ]["MonthlyCharges"].sum(),
        2
    )

    return {

        "total_customers":
            total_customers,

        "high_risk":
            high_risk,

        "medium_risk":
            medium_risk,

        "low_risk":
            low_risk,

        "revenue_at_risk":
            revenue_at_risk
    }