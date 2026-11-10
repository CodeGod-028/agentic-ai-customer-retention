"""
segmentation.py

Purpose
-------
1. Customer Segmentation
2. KMeans Clustering
3. Business Segment Mapping
4. Segment Analytics
5. Save Segment Model
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerSegmentation:

    def __init__(self):

        self.scaler = StandardScaler()

        self.model = None

        self.df = None

        self.features = [
            "tenure",
            "MonthlyCharges",
            "TotalCharges",
            "ChurnProbability"
        ]

    def load_data(
        self,
        path="data/customer_predictions.csv"
    ):

        self.df = pd.read_csv(path)

        return self.df

    def prepare_features(self):

        X = self.df[self.features]

        X_scaled = self.scaler.fit_transform(X)

        return X_scaled

    def train_kmeans(self, X):

        self.model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        self.df["Cluster"] = (
            self.model.fit_predict(X)
        )

        return self.df

    def analyze_clusters(self):

        cluster_summary = (
            self.df
            .groupby("Cluster")[self.features]
            .mean()
            .round(2)
        )

        print("\n" + "=" * 70)
        print("CLUSTER ANALYSIS")
        print("=" * 70)

        print(cluster_summary)

        return cluster_summary

    def assign_business_segments(self):

        cluster_stats = (
            self.df
            .groupby("Cluster")[self.features]
            .mean()
        )

        mapping = {}

        # Highest TotalCharges
        champions_cluster = (
            cluster_stats["TotalCharges"]
            .idxmax()
        )
        mapping[champions_cluster] = "Champions"

        # Highest Churn Probability
        remaining = cluster_stats.drop(
            index=list(mapping.keys())
        )

        at_risk_cluster = (
            remaining["ChurnProbability"]
            .idxmax()
        )
        mapping[at_risk_cluster] = "At Risk"

        # Lowest Tenure
        remaining = cluster_stats.drop(
            index=list(mapping.keys())
        )

        new_customer_cluster = (
            remaining["tenure"]
            .idxmin()
        )
        mapping[new_customer_cluster] = "New Customers"

        # Highest Monthly Charges
        remaining = cluster_stats.drop(
            index=list(mapping.keys())
        )

        price_sensitive_cluster = (
            remaining["MonthlyCharges"]
            .idxmax()
        )
        mapping[price_sensitive_cluster] = (
            "Price Sensitive"
        )

        # Remaining clusters
        remaining_clusters = [
            cluster
            for cluster in cluster_stats.index
            if cluster not in mapping
        ]

        for cluster in remaining_clusters:

            mapping[cluster] = (
                "Loyal Customers"
            )

        print("\nBusiness Segment Mapping")
        print(mapping)

        self.df["Segment"] = (
            self.df["Cluster"]
            .map(mapping)
        )

        unmapped = (
            self.df["Segment"]
            .isna()
            .sum()
        )

        print(
            f"\nUnmapped Segments: {unmapped}"
        )

        return self.df

    def display_segment_stats(self):

        print("\n" + "=" * 70)
        print("SEGMENT DISTRIBUTION")
        print("=" * 70)

        print(
            self.df["Segment"]
            .value_counts()
        )

    def save_models(self):

        Path("models").mkdir(
            exist_ok=True
        )

        joblib.dump(
            self.model,
            "models/segment_model.pkl"
        )

        joblib.dump(
            self.scaler,
            "models/segment_scaler.pkl"
        )

        print("\nSegment models saved.")

    def save_results(self):

        self.df.to_csv(
            "data/customer_segments.csv",
            index=False
        )

        print(
            "\ncustomer_segments.csv saved."
        )

    def run(self):

        self.load_data()

        X = self.prepare_features()

        self.train_kmeans(X)

        self.analyze_clusters()

        self.assign_business_segments()

        self.display_segment_stats()

        self.save_models()

        self.save_results()

        return self.df


if __name__ == "__main__":

    segmentation = CustomerSegmentation()

    result = segmentation.run()

    print("\n" + "=" * 70)
    print("SEGMENTATION COMPLETE")
    print("=" * 70)

    print(
        result[
            [
                "customerID",
                "ChurnProbability",
                "RiskLevel",
                "Segment"
            ]
        ].head()
    )