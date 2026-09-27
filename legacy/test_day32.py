from src.skill_recommender import (
    SkillRecommendationEngine
)


engine = SkillRecommendationEngine()


candidate_skills = [
    "python",
    "sql",
    "machine learning"
]


candidate_skills = [
    "python",
    "sql",
    "machine learning"
]

result = engine.recommend_skills(
    candidate_skills,
    "Data Scientist"
)

print(
    result["missing_skills"]
)