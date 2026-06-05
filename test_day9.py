import os
import pandas as pd
from src.skill_analysis import SkillAnalyzer
from src.visualization import CandidateVisualizer

# 1. Ensure the output directory exists so matplotlib doesn't crash
os.makedirs("artifacts/plots", exist_ok=True)

# 2. Extract skill counts using your analyzer
df = pd.read_csv("data/processed_candidates.csv")
analyzer = SkillAnalyzer()
skills_count = analyzer.skill_frequency(df)

# 3. Generate both visual charts
visualizer = CandidateVisualizer()

print("Generating charts...")

# Generates the Bar Chart
visualizer.plot_skill_frequency(
    skills_count, 
    "artifacts/plots/top_skills.png"
)

# Generates the Pie Chart (New Upgrade!)
visualizer.plot_pie_chart(
    skills_count, 
    "artifacts/plots/skill_distribution.png"
)

print("✅ Success! Check your 'artifacts/plots/' folder for both PNG images.")