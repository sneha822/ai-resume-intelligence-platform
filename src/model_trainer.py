import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class RoleClassifierTrainer:

    def train(self, dataframe: pd.DataFrame) -> float:
        """Trains a Logistic Regression model to classify candidate levels."""
        
        feature_columns = [
            "skill_count",
            "experience_years",
            "project_count",
            "certification_count"
        ]

        # 1. Ensure required feature columns exist in dataset
        missing_cols = [col for col in feature_columns if col not in dataframe.columns]
        if missing_cols:
            raise KeyError(f"Missing required feature columns in dataset: {missing_cols}")

        X = dataframe[feature_columns]
        y = dataframe["candidate_level"]

        # 2. Safety check: Ensure dataset has at least 2 distinct target classes
        if y.nunique() < 2:
            raise ValueError(
                f"Training requires at least 2 distinct classes in 'candidate_level', "
                f"but found only: {y.unique().tolist()}. Please add more diverse samples to your dataset."
            )

        # 3. Stratified Train-Test Split (Ensures proportional representation of all classes)
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42, 
            stratify=y
        )

        # 4. Initialize and fit the classifier
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        # 5. Evaluate model accuracy on unseen test data
        accuracy = model.score(X_test, y_test)

        # 6. Save model weights safely
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/role_classifier.pkl")

        return accuracy