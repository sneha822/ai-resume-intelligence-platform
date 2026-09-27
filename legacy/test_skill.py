from src.skill_analysis import SkillAnalyzer
import pandas as pd

df = pd.read_csv(
    "data/processed_candidates.csv"
)

analyzer = SkillAnalyzer()

result = analyzer.skill_frequency(df)

print(result)