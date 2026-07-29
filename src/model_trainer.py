import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class RoleClassifierTrainer:

    def train(
        self,
        dataframe: pd.DataFrame
    ):

        feature_columns = [
            "skill_count",
            "experience_years",
            "project_count",
            "certification_count"
        ]

        X = dataframe[feature_columns]

        y = dataframe["candidate_level"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = LogisticRegression(
            max_iter=1000
        )

        model.fit(
            X_train,
            y_train
        )

        accuracy = model.score(
            X_test,
            y_test
        )

        joblib.dump(
            model,
            "models/role_classifier.pkl"
        )

        return accuracy