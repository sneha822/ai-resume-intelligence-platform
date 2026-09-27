from src.parser import ResumeParser

parser = ResumeParser()

result = parser.parse_resume(
    "data/raw/sample_resume.txt"
)

print(result)