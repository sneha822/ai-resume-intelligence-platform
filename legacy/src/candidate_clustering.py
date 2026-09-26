import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CandidateClusterer:
    """Cluster candidates based on their numerical features."""

    FEATURE_COLUMNS = [
        "skill_count",
        "experience_years",
        "project_count",
        "certification_count"
    ]

    def __init__(
        self,
        n_clusters: int = 3
    ) -> None:
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )

    def prepare_features(
        self,
        dataframe: pd.DataFrame
    ):
        return dataframe[self.FEATURE_COLUMNS]

    def fit_predict(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Scale candidate features and assign
        each candidate to a cluster.
        """
        dataframe = dataframe.copy()
        features = self.prepare_features(dataframe)
        scaled_features = self.scaler.fit_transform(features)
        dataframe["cluster"] = self.model.fit_predict(scaled_features)
        return dataframe

    def get_cluster_summary(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate average candidate features
        for each cluster.
        """
        return (
            dataframe
            .groupby("cluster")[self.FEATURE_COLUMNS]
            .mean()
            .round(2)
        )

    def assign_cluster_levels(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Map clusters to Beginner, Intermediate,
        and Advanced based on average feature strength.
        """
        dataframe = dataframe.copy()
        summary = self.get_cluster_summary(dataframe)

        summary["overall_score"] = summary[self.FEATURE_COLUMNS].mean(axis=1)

        ordered_clusters = (
            summary["overall_score"]
            .sort_values()
            .index
            .tolist()
        )

        level_mapping = {
            ordered_clusters[0]: "Beginner",
            ordered_clusters[1]: "Intermediate",
            ordered_clusters[2]: "Advanced"
        }

        dataframe["cluster_level"] = dataframe["cluster"].map(level_mapping)

        return dataframe