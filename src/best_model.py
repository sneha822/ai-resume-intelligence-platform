import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


class BestModelTrainer:
    """Trains and saves the selected best model, and makes sample predictions."""

    FEATURE_COLUMNS = [
        "skill_count",
        "experience_years",
        "project_count",
        "certification_count"
    ]

    MODEL_PATH = "models/best_model.pkl"

    def train_and_save(self, dataframe: pd.DataFrame, best_model_name: str) -> str:
        X = dataframe[self.FEATURE_COLUMNS]
        y = dataframe["selection_status"]

        # Select architecture based on best_model_name
        if best_model_name == "Logistic Regression":
            model = LogisticRegression(max_iter=1000)
        elif best_model_name == "XGBoost":
            # Map target labels to 0 and 1 for XGBoost
            y = y.map({"rejected": 0, "shortlisted": 1})
            model = XGBClassifier(
                n_estimators=100, 
                max_depth=3, 
                learning_rate=0.1, 
                random_state=42, 
                eval_metric="logloss"
            )
        else:
            # Default to Random Forest
            model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Fit model on the full processing dataset
        model.fit(X, y)

        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, self.MODEL_PATH)

        return self.MODEL_PATH

    def predict(self, feature_list: list) -> str:
        """Predict selection status for a candidate feature list."""
        if not os.path.exists(self.MODEL_PATH):
            raise FileNotFoundError(f"No saved model found at {self.MODEL_PATH}")

        model = joblib.load(self.MODEL_PATH)
        
        # Wrap as DataFrame to match feature names and prevent UserWarnings
        sample_df = pd.DataFrame([feature_list], columns=self.FEATURE_COLUMNS)
        pred = model.predict(sample_df)[0]

        # Map integer back to text label if model was XGBoost
        if isinstance(pred, (int, float)):
            label_map = {0: "rejected", 1: "shortlisted"}
            return label_map.get(pred, str(pred))

        return str(pred)