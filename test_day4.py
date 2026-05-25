from src.parser import ResumeParser

parser = ResumeParser()

data = parser.parse_resume("data/raw/sample_resume.txt")

print(data)