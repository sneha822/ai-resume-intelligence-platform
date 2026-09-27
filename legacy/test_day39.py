from src.parser import ResumeParser
from src.interview_question_generator import InterviewQuestionGenerator


def main():
    # Initialize components
    parser = ResumeParser()
    generator = InterviewQuestionGenerator()

    # ---------------------------------------------------------
    # 1. Test Static & Fallback Question Generation
    # ---------------------------------------------------------
    print("=== TEST 1: KNOWN AND UNKNOWN SKILLS ===")
    sample_skills = ["Python", "SQL", "Docker", "React"]
    sample_questions = generator.generate_questions(skills=sample_skills)

    for idx, q in enumerate(sample_questions, start=1):
        print(f"{idx}. {q}")
    print("\n" + "=" * 45 + "\n")

    # ---------------------------------------------------------
    # 2. Test Step 6: Live Resume Parsing & Skill Extraction
    # ---------------------------------------------------------
    print("=== TEST 2: PARSE CANDIDATE RESUME & GENERATE QUESTIONS ===")
    # Update this path if your test resume is located elsewhere
    resume_path = "data/raw/sample_resume.pdf"

    try:
        parsed_data = parser.parse_resume(resume_path)
        extracted_skills = parsed_data.get("skills", [])

        print(f"Parsed Candidate Email: {parsed_data.get('email', 'N/A')}")
        print(f"Extracted Skills: {extracted_skills}\n")

        live_questions = generator.generate_questions(skills=extracted_skills)

        print("Generated Interview Questions:")
        for idx, q in enumerate(live_questions, start=1):
            print(f"{idx}. {q}")

    except Exception as e:
        print(f"Error parsing resume at {resume_path}: {e}")

    print("\n" + "=" * 45 + "\n")

    # ---------------------------------------------------------
    # 3. Test Step 8: Full Candidate Report Generation
    # ---------------------------------------------------------
    print("=== TEST 3: CANDIDATE REPORT ===")
    candidate_profile = {
        "email": "johndoe@gmail.com",
        "skills": ["Python", "Machine Learning", "Kubernetes"],
    }

    report = generator.generate_candidate_report(candidate_profile)

    print(f"Report Email: {report.get('email')}")
    print(f"Assessed Skills: {', '.join(report.get('skills', []))}\n")
    print("Report Questions:")
    for idx, q in enumerate(report.get("questions", []), start=1):
        print(f"{idx}. {q}")


if __name__ == "__main__":
    main()