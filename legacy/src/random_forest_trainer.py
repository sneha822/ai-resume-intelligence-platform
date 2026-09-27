import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class RandomForestTrainer:
    """Train and save the Random Forest candidate classifier."""

    def train(
        self,
        dataframe: pd.DataFrame
    ) -> float:

        feature_columns = [
            "skill_count",
            "experience_years",
            "project_count",
            "certification_count"
        ]

        X = dataframe[feature_columns]

        # We keep candidate_level because this is the
        # target currently available in your dataset.
        y = dataframe["candidate_level"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        accuracy = model.score(
            X_test,
            y_test
        )

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            model,
            "models/random_forest_classifier.pkl"
        )

        return accuracy