"""
model_trainer.py

Purpose
-------
1. Train XGBoost Churn Model
2. Evaluate Performance
3. Generate Churn Probabilities
4. Save Artifacts
5. Prepare Data for SHAP
6. Feed Executive Dashboard KPIs
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

from xgboost import XGBClassifier

from preprocessing import DataPreprocessor

class ChurnModelTrainer:

    def __init__(
        self,
        data_path: str,
        model_path: str = "models/churn_model.pkl",
        preprocessor_path: str = "models/preprocessor.pkl"
    ):

        self.data_path = data_path

        self.model_path = Path(model_path)
        self.preprocessor_path = Path(preprocessor_path)

        self.model = None
        self.preprocessor = None

        self.X = None
        self.y = None

        self.feature_names = None
        self.raw_df = None

    def prepare_data(self):
        """
        Execute preprocessing pipeline
        """

        processor = DataPreprocessor(
            self.data_path
        )

        result = processor.process()

        self.X = result["X"]
        self.y = result["y"]

        self.feature_names = result["feature_names"]

        self.raw_df = result["raw_dataframe"]

        self.preprocessor = result["preprocessor"]

        return result

    def split_data(self):
        """
        Train/Test Split
        """

        return train_test_split(
            self.X,
            self.y,
            test_size=0.20,
            random_state=42,
            stratify=self.y
        )

    def build_model(self):
        """
        Churn Prediction Model
        """

        self.model = XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=42
        )

        return self.model

    def train(self):
        """
        Train XGBoost
        """

        (
            X_train,
            X_test,
            y_train,
            y_test
        ) = self.split_data()

        self.build_model()

        self.model.fit(
            X_train,
            y_train
        )

        predictions = self.model.predict(X_test)

        probabilities = self.model.predict_proba(
            X_test
        )[:, 1]

        metrics = {
            "accuracy":
                accuracy_score(
                    y_test,
                    predictions
                ),

            "precision":
                precision_score(
                    y_test,
                    predictions
                ),

            "recall":
                recall_score(
                    y_test,
                    predictions
                ),

            "f1":
                f1_score(
                    y_test,
                    predictions
                ),

            "auc":
                roc_auc_score(
                    y_test,
                    probabilities
                )
        }

        print("\n" + "=" * 60)
        print("MODEL PERFORMANCE")
        print("=" * 60)

        for metric, value in metrics.items():

            print(
                f"{metric.upper():<15}: "
                f"{value:.4f}"
            )

        print("\nClassification Report:\n")

        print(
            classification_report(
                y_test,
                predictions
            )
        )

        return metrics

    def generate_probabilities(self):
        """
        Generate churn scores
        for all customers
        """

        churn_probabilities = (
            self.model
            .predict_proba(self.X)
        )[:, 1]

        self.raw_df[
            "ChurnProbability"
        ] = churn_probabilities

        return self.raw_df

    def assign_risk_levels(
        self,
        dataframe
    ):
        """
        Create Business Risk Classes
        """

        def risk_mapper(prob):

            if prob >= 0.80:
                return "High"

            elif prob >= 0.50:
                return "Medium"

            return "Low"

        dataframe["RiskLevel"] = (
            dataframe["ChurnProbability"]
            .apply(risk_mapper)
        )

        return dataframe

    def save_artifacts(self):
        """
        Save Model Assets
        """

        self.model_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            self.model,
            self.model_path
        )

        joblib.dump(
            self.preprocessor,
            self.preprocessor_path
        )

        print("\nArtifacts Saved")

        print(
            f"Model -> {self.model_path}"
        )

        print(
            f"Preprocessor -> "
            f"{self.preprocessor_path}"
        )

    def run(self):
        """
        Complete Training Workflow
        """

        self.prepare_data()

        metrics = self.train()

        customer_df = (
            self.generate_probabilities()
        )

        customer_df = (
            self.assign_risk_levels(
                customer_df
            )
        )

        self.save_artifacts()

        customer_df.to_csv(
            "data/customer_predictions.csv",
            index=False
        )

        print(
            "\nPredictions Saved -> "
            "data/customer_predictions.csv"
        )

        return {
            "metrics": metrics,
            "customer_df": customer_df,
            "model": self.model,
            "feature_names": self.feature_names
        }


if __name__ == "__main__":

    trainer = ChurnModelTrainer(
        data_path=
        "data/telco_customer_churn_cleaned.csv"
    )

    result = trainer.run()

    print("\nTraining Complete")