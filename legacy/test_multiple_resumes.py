from src.pipeline import ResumePipeline

pipeline = ResumePipeline()

resume_files = [
    "data/raw/sample_resume.txt",
    "data/raw/candidate_2.txt",
    "data/raw/candidate_3.txt",
    "data/raw/candidate_4.txt",
    "data/raw/candidate_5.txt"
]

for resume in resume_files:

    try:

        result = pipeline.process_resume(
            resume
        )

        print(
            f"Processed: {result['email']}"
        )

    except Exception as error:

        print(
            f"Error: {error}"
        )