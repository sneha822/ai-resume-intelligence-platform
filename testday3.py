from src.reader import read_text_file

# Test existing file
text = read_text_file("data/raw/sample_resume.txt")

print(text)

# Test missing file
read_text_file("data/raw/fake_resume.txt")