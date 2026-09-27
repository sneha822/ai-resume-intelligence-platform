import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


class ModelComparator:
    """Compare multiple machine learning models for candidate selection prediction."""

    FEATURE_COLUMNS = [
        "skill_count",
        "experience_years",
        "project_count",
        "certification_count"
    ]

    def compare_models(self, dataframe: pd.DataFrame) -> dict:
        dataframe = dataframe.copy()

        # 1. Target column name (check both selection_status and candidate_level)
        target_col = "selection_status" if "selection_status" in dataframe.columns else "candidate_level"

        # 2. Drop any rows where target column has NaN
        dataframe = dataframe.dropna(subset=[target_col])

        X = dataframe[self.FEATURE_COLUMNS]
        y = dataframe[target_col]

        # 3. Stratified Train-Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=42, 
            stratify=y
        )

        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
        }

        results = {}

        for name, model in models.items():
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            results[name] = accuracy

        return results