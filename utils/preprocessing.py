"""
preprocessing.py

Purpose:
---------
Data preprocessing pipeline for the
Agentic AI Customer Retention Platform.

Responsibilities:
------------------
1. Load Telco Churn Dataset
2. Clean data
3. Handle TotalCharges
4. Encode target variable
5. Prepare features for XGBoost
6. Preserve customer IDs
7. Save encoded feature names
"""

from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer


class DataPreprocessor:
    """
    Handles all preprocessing required
    for churn prediction and segmentation.
    """

    def __init__(self, data_path: str):

        self.data_path = Path(data_path)

        self.df = None
        self.customer_ids = None

        self.categorical_cols = []
        self.numeric_cols = []

        self.preprocessor = None

    def load_data(self):
        """
        Load customer dataset
        """

        self.df = pd.read_csv(self.data_path)

        return self.df

    def clean_data(self):
        """
        Clean and prepare dataset
        """

        df = self.df.copy()

        # Remove leading/trailing spaces
        df.columns = df.columns.str.strip()

        # Convert TotalCharges safely
        if "TotalCharges" in df.columns:

            df["TotalCharges"] = pd.to_numeric(
                df["TotalCharges"],
                errors="coerce"
            )

        # Replace missing charges with 0
        df["TotalCharges"] = df["TotalCharges"].fillna(0)

        # Preserve customer ids
        self.customer_ids = df["customerID"]

        self.df = df

        return df

    def encode_target(self):
        """
        Encode churn target
        """

        df = self.df.copy()

        df["Churn"] = (
            df["Churn"]
            .map({"Yes": 1, "No": 0})
            .astype(int)
        )

        self.df = df

        return df

    def identify_columns(self):
        """
        Separate categorical and numeric columns
        """

        df = self.df.copy()

        features = df.drop(
            columns=["customerID", "Churn"]
        )

        self.categorical_cols = (
            features
            .select_dtypes(include=["object"])
            .columns
            .tolist()
        )

        self.numeric_cols = (
            features
            .select_dtypes(
                include=["int64", "float64"]
            )
            .columns
            .tolist()
        )

        return self.categorical_cols, self.numeric_cols

    def build_preprocessor(self):
        """
        Build sklearn preprocessing pipeline
        """

        categorical_pipeline = Pipeline([
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ])

        numeric_pipeline = Pipeline([
            (
                "imputer",
                SimpleImputer(strategy="median")
            )
        ])

        self.preprocessor = ColumnTransformer([
            (
                "categorical",
                categorical_pipeline,
                self.categorical_cols
            ),
            (
                "numeric",
                numeric_pipeline,
                self.numeric_cols
            )
        ])

        return self.preprocessor

    def transform_data(self):
        """
        Generate training matrix
        """

        df = self.df.copy()

        X = df.drop(
            columns=["customerID", "Churn"]
        )

        y = df["Churn"]

        X_processed = self.preprocessor.fit_transform(X)

        return X_processed, y

    def get_feature_names(self):
        """
        Obtain feature names after
        one-hot encoding
        """

        ohe = (
            self.preprocessor
            .named_transformers_["categorical"]
            .named_steps["onehot"]
        )

        categorical_names = (
            ohe.get_feature_names_out(
                self.categorical_cols
            )
        )

        feature_names = (
            list(categorical_names)
            + self.numeric_cols
        )

        return feature_names

    def process(self):
        """
        Execute full preprocessing flow
        """

        self.load_data()

        self.clean_data()

        self.encode_target()

        self.identify_columns()

        self.build_preprocessor()

        X, y = self.transform_data()

        feature_names = self.get_feature_names()

        return {
            "X": X,
            "y": y,
            "feature_names": feature_names,
            "customer_ids": self.customer_ids,
            "raw_dataframe": self.df,
            "preprocessor": self.preprocessor
        }


if __name__ == "__main__":

    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATASET_PATH = (
        BASE_DIR
        / "data"
        / "telco_customer_churn_cleaned.csv"
    )

    processor = DataPreprocessor(DATASET_PATH)

    result = processor.process()

    print("=" * 60)
    print("Dataset Processed Successfully")
    print("=" * 60)

    print(
        f"Rows: {result['raw_dataframe'].shape[0]}"
    )

    print(
        f"Columns: {result['raw_dataframe'].shape[1]}"
    )

    print(
        f"Features Generated: "
        f"{len(result['feature_names'])}"
    )