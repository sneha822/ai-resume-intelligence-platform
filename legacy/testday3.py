from src.reader import read_text_file

# 1. Test reading an existing file
try:
    text = read_text_file("data/raw/sample_resume.txt")
    print("=== FILE CONTENT START ===")
    print(text)
    print("=== FILE CONTENT END ===")
except Exception as e:
    print(f"Error reading sample resume: {e}")

# 2. Test missing file error handling
print("\nTesting missing file error handling...")
try:
    read_text_file("data/raw/fake_resume.txt")
except Exception as e:
    print(f"Caught expected error: {e}")