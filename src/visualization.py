import matplotlib.pyplot as plt


class CandidateVisualizer:

    def plot_skill_frequency(
        self,
        skills_count: dict,
        save_path: str
    ) -> None:
        """Generates a vertical bar chart representing top candidate skills."""
        skills = list(
            skills_count.keys()
        )

        counts = list(
            skills_count.values()
        )

        plt.figure(
            figsize=(8, 5)
        )

        plt.bar(
            skills,
            counts,
            color="skyblue",
            edgecolor="black"
        )

        plt.title(
            "Top Candidate Skills",
            fontsize=14,
            fontweight="bold"
        )

        plt.xlabel(
            "Skills",
            fontsize=12
        )

        plt.ylabel(
            "Frequency (Count)",
            fontsize=12
        )

        plt.tight_layout()

        plt.savefig(
            save_path
        )

        plt.close()

    def plot_pie_chart(
        self,
        skills_count: dict,
        save_path: str
    ) -> None:
        """Generates a pie chart displaying the percentage distribution of skills."""
        plt.figure(
            figsize=(6, 6)
        )

        plt.pie(
            skills_count.values(),
            labels=skills_count.keys(),
            autopct="%1.1f%%",
            startangle=140
        )

        plt.title(
            "Skill Distribution Percentage",
            fontsize=14,
            fontweight="bold"
        )

        plt.tight_layout()

        plt.savefig(
            save_path
        )

        plt.close()