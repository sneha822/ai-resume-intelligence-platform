import os
from src.reader import read_text_file
from src.nlp_preprocessor import NLPPreprocessor  # Imports from src/nlp_preprocessor.py

def main():
    print("=== TESTING DAY 34 NLP PREPROCESSING ===")
    
    # Path to sample resume
    sample_path = os.path.join("data", "raw", "sample_resume.txt")
    
    if not os.path.exists(sample_path):
        print(f"Error: Could not find sample resume at '{sample_path}'.")
        print("Please ensure the file exists in the 'data/raw/' directory.")
        return

    # 1. Read the raw text file
    raw_text = read_text_file(sample_path)
    
    # 2. Initialize preprocessor engine
    preprocessor = NLPPreprocessor()

    # 3. Preprocess text
    cleaned_text = preprocessor.preprocess(raw_text)

    # 4. Output comparison
    print("\n=== ORIGINAL TEXT PREVIEW ===")
    print(raw_text[:200].strip())

    print("\n=== PREPROCESSED TEXT PREVIEW ===")
    print(cleaned_text[:200].strip())
    
    print("\n✅ Day 34 Test Complete!")

if __name__ == "__main__":
    main()