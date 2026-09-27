from typing import Dict, List, Any


class InterviewQuestionGenerator:
    """Generate technical interview questions from candidate skills."""

    DEFAULT_QUESTIONS: List[str] = [
        "Can you describe a challenging project you built using {skill} and how you solved key technical problems?",
        "What best practices do you follow when writing production-level code in {skill}?",
    ]

    QUESTIONS: Dict[str, List[str]] = {
        "python": [
            "What is the difference between a list and a tuple in Python?",
            "Explain list comprehensions in Python.",
            "What are decorators and where would you use them?",
            "How does exception handling work in Python?",
        ],
        "sql": [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "What is database normalization?",
            "What is the difference between WHERE and HAVING?",
            "How would you optimize a slow SQL query?",
        ],
        "machine learning": [
            "What is the difference between supervised and unsupervised learning?",
            "What is overfitting and how can you prevent it?",
            "Explain the bias-variance tradeoff.",
            "How would you evaluate a classification model?",
        ],
        "java": [
            "What is the difference between an interface and an abstract class?",
            "Explain inheritance and polymorphism in Java.",
            "What is the difference between == and equals()?",
            "How does exception handling work in Java?",
        ],
        "c++": [
            "What is the difference between a pointer and a reference?",
            "Explain inheritance in C++.",
            "What is the purpose of a virtual function?",
            "What is the difference between stack and heap memory?",
        ],
        "docker": [
            "What is a Docker container?",
            "What is the difference between a Docker image and a container?",
            "What is a Dockerfile?",
            "Why is Docker useful for deploying machine learning applications?",
        ],
        "aws": [
            "What is AWS and why is it useful for deploying applications?",
            "What is the difference between EC2 and S3?",
            "What is an AWS IAM role?",
            "How would you deploy a machine learning application on AWS?",
        ],
    }

    def generate_questions(self, skills: List[str]) -> List[str]:
        """Generate questions based on candidate skills with fallback for unknown skills."""
        generated_questions = []

        for skill in skills:
            normalized_skill = skill.strip().lower()

            if normalized_skill in self.QUESTIONS:
                generated_questions.extend(self.QUESTIONS[normalized_skill])
            else:
                # Dynamic fallback for unknown skills
                fallback = [
                    q.format(skill=skill.title()) for q in self.DEFAULT_QUESTIONS
                ]
                generated_questions.extend(fallback)

        return generated_questions

    def generate_questions_with_skills(
        self, skills: List[str]
    ) -> Dict[str, List[str]]:
        """Group generated questions by skill."""
        result = {}

        for skill in skills:
            normalized_skill = skill.strip().lower()

            if normalized_skill in self.QUESTIONS:
                result[normalized_skill] = self.QUESTIONS[normalized_skill]
            else:
                result[normalized_skill] = [
                    q.format(skill=skill.title()) for q in self.DEFAULT_QUESTIONS
                ]

        return result

    def generate_candidate_report(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete interview preparation report for a candidate."""
        skills = candidate_data.get("skills", [])

        return {
            "email": candidate_data.get("email"),
            "skills": skills,
            "questions": self.generate_questions(skills=skills),
            "questions_by_skill": self.generate_questions_with_skills(skills=skills),
        }