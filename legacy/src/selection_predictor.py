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
        """Trains a Random Forest classifier to predict candidate selection status."""
        dataframe = dataframe.copy()

        # 1. Check for missing feature or target columns
        missing_cols = [col for col in self.FEATURE_COLUMNS + ["selection_status"] if col not in dataframe.columns]
        if missing_cols:
            raise KeyError(f"Missing required columns in dataset: {missing_cols}")

        # 2. Clean rows where selection_status contains NaN values
        dataframe = dataframe.dropna(subset=["selection_status"])

        X = dataframe[self.FEATURE_COLUMNS]
        y = dataframe["selection_status"].astype(int)

        # 3. Ensure at least 2 target classes exist for training
        if y.nunique() < 2:
            raise ValueError(
                f"Training requires at least 2 distinct selection statuses (0 and 1), "
                f"but found only: {y.unique().tolist()}."
            )

        # 4. Stratified Train-Test Split to avoid single-class issues in split
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42, 
            stratify=y
        )

        # 5. Fit model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # 6. Evaluate score
        accuracy = model.score(X_test, y_test)

        # 7. Save model artifact safely
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/candidate_selection_model.pkl")

        return accuracy

    def predict_candidate(self, sample_features: dict) -> int:
        """Predict selection status (1 for Selected, 0 for Rejected) for a single candidate feature dict."""
        model_path = "models/candidate_selection_model.pkl"
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at '{model_path}'. Please run train() first.")

        model = joblib.load(model_path)
        
        # Convert feature dict into DataFrame with proper column headers
        sample_df = pd.DataFrame([sample_features], columns=self.FEATURE_COLUMNS)
        
        prediction = model.predict(sample_df)
        return int(prediction[0])