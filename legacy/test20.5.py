# test_pdf_reader.py

from src.parser import ResumeParser

parser = ResumeParser()

result = parser.parse_resume(
    "data/raw/sample_resume.pdf"
)

print(result)