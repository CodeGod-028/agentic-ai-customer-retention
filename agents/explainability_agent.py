"""
Explainability Agent

Responsibilities
----------------
1. Customer Risk Analysis
2. SHAP Explainability
3. Top Driver Detection
4. Executive Insights
"""

import joblib
import shap
import pandas as pd


class ExplainabilityAgent:

    def __init__(self):

        self.model = joblib.load(
            "models/churn_model.pkl"
        )

        self.preprocessor = joblib.load(
            "models/preprocessor.pkl"
        )

        self.df = pd.read_csv(
            "data/customer_segments.csv"
        )

        self.explainer = shap.TreeExplainer(
            self.model
        )

    def get_customer_record(
        self,
        customer_id
    ):

        customer = self.df[
            self.df["customerID"] == customer_id
        ]

        if customer.empty:

            raise ValueError(
                f"Customer {customer_id} not found"
            )

        return customer

    def prepare_features(
        self,
        customer
    ):

        X = customer.drop(
            columns=[
                "customerID",
                "Churn",
                "Cluster",
                "Segment",
                "RiskLevel",
                "ChurnProbability"
            ],
            errors="ignore"
        )

        X_processed = (
            self.preprocessor.transform(X)
        )

        return X_processed

    def get_shap_values(
        self,
        customer_id
    ):

        customer = self.get_customer_record(
            customer_id
        )

        X_processed = (
            self.prepare_features(customer)
        )

        shap_values = (
            self.explainer.shap_values(
                X_processed
            )
        )

        feature_names = (
            self.preprocessor
            .get_feature_names_out()
        )

        shap_df = pd.DataFrame({
            "Feature": feature_names,
            "Impact": shap_values[0]
        })

        shap_df["AbsImpact"] = (
            shap_df["Impact"]
            .abs()
        )

        shap_df = (
            shap_df
            .sort_values(
                "AbsImpact",
                ascending=False
            )
        )

        return shap_df

    def get_top_drivers(
        self,
        customer_id,
        top_n=10
    ):

        shap_df = self.get_shap_values(
            customer_id
        )

        return (
            shap_df
            .head(top_n)
            [
                [
                    "Feature",
                    "Impact"
                ]
            ]
        )

    def generate_explanation(
        self,
        customer_id
    ):

        customer = (
            self.get_customer_record(
                customer_id
            )
            .iloc[0]
        )

        top_drivers = (
            self.get_top_drivers(
                customer_id,
                top_n=5
            )
        )

        explanation = {

            "customer_id":
                customer["customerID"],

            "risk_level":
                customer["RiskLevel"],

            "segment":
                customer["Segment"],

            "churn_probability":
                float(
                    round(
                        customer["ChurnProbability"],
                        4
                    )
                ),

            "top_drivers":
                top_drivers.to_dict(
                    orient="records"
                )
        }

        return explanation


if __name__ == "__main__":

    df = pd.read_csv(
        "data/customer_segments.csv"
    )

    customer_id = (
        df.iloc[0]["customerID"]
    )

    agent = ExplainabilityAgent()

    result = (
        agent.generate_explanation(
            customer_id
        )
    )

    print("\n")
    print("=" * 70)
    print("EXPLAINABILITY RESULT")
    print("=" * 70)

    print(result)