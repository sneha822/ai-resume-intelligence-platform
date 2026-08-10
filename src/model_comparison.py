import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier


class ModelComparator:
    """Compares multiple classification models on candidate data."""

    FEATURE_COLUMNS = [
        "skill_count",
        "experience_years",
        "project_count",
        "certification_count"
    ]

    def prepare_data(self, dataframe: pd.DataFrame):

        X = dataframe[self.FEATURE_COLUMNS]
        y = dataframe["selection_status"]

        # Convert labels into numerical values for XGBoost
        y = y.map({
            "rejected": 0,
            "shortlisted": 1
        })

        return train_test_split(
            X,
            y,
            test_size=0.4,
            random_state=42
        )

    def compare_models(self, dataframe: pd.DataFrame) -> dict:

        X_train, X_test, y_train, y_test = self.prepare_data(
            dataframe
        )

        models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000
            ),

            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),

            "XGBoost": XGBClassifier(
                n_estimators=100,
                max_depth=3,
                learning_rate=0.1,
                random_state=42,
                eval_metric="logloss"
            )
        }

        results = {}

        for model_name, model in models.items():

            model.fit(
                X_train,
                y_train
            )

            predictions = model.predict(
                X_test
            )

            accuracy = accuracy_score(
                y_test,
                predictions
            )

            results[model_name] = accuracy

        return results