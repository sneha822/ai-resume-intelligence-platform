import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class CandidateSelectionPredictor:
    """Train and predict candidate selection status (shortlisted/rejected)."""

    FEATURE_COLUMNS = [
        "skill_count",
        "experience_years",
        "project_count",
        "certification_count"
    ]

    def train(self, dataframe: pd.DataFrame) -> float:
        X = dataframe[self.FEATURE_COLUMNS]
        y = dataframe["selection_status"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.4, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/candidate_selection_model.pkl")

        return accuracy

    def predict_candidate(self, sample_features: dict) -> str:
        """Predict selection status for a single candidate dictionary without UserWarnings."""
        model = joblib.load("models/candidate_selection_model.pkl")
        
        # Convert dictionary to DataFrame with matching feature names
        sample_df = pd.DataFrame([sample_features], columns=self.FEATURE_COLUMNS)
        
        prediction = model.predict(sample_df)
        return prediction[0]