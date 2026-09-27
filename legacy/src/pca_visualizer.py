import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class CandidatePCAVisualizer:
    """Reduce candidate features to two dimensions using PCA."""

    FEATURE_COLUMNS = [
        "skill_count",
        "experience_years",
        "project_count",
        "certification_count"
    ]

    def __init__(self) -> None:

        self.scaler = StandardScaler()

        self.pca = PCA(
            n_components=2
        )

    def prepare_features(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """Select numerical candidate features."""

        return dataframe[
            self.FEATURE_COLUMNS
        ]

    def transform(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """Scale features and reduce them to two PCA components."""

        dataframe = dataframe.copy()

        features = self.prepare_features(
            dataframe
        )

        scaled_features = (
            self.scaler.fit_transform(
                features
            )
        )

        components = (
            self.pca.fit_transform(
                scaled_features
            )
        )

        dataframe["PC1"] = (
            components[:, 0]
        )

        dataframe["PC2"] = (
            components[:, 1]
        )

        return dataframe

    def plot_clusters(
        self,
        dataframe: pd.DataFrame,
        save_path: str
    ) -> None:
        """Create a 2D PCA visualization of candidate clusters."""

        plt.figure(
            figsize=(9, 6)
        )

        for cluster in sorted(
            dataframe["cluster"].unique()
        ):

            cluster_data = dataframe[
                dataframe["cluster"] == cluster
            ]

            plt.scatter(
                cluster_data["PC1"],
                cluster_data["PC2"],
                label=f"Cluster {cluster}"
            )

        plt.title(
            "Candidate Clusters Using PCA"
        )

        plt.xlabel(
            "Principal Component 1"
        )

        plt.ylabel(
            "Principal Component 2"
        )

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            save_path
        )

        plt.close()