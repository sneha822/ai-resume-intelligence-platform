from src.pipeline import (
    ResumePipeline
)

pipeline = ResumePipeline()

result = pipeline.process_resume(
    "data/raw/sample_resume.txt"
)

print(
    "\nCandidate Data:"
)

print(result)