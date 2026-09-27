import os
from src.parser import ResumeParser
from src.storage import DataStorage

def run_verification():
    print("--- Starting Day 5 Verification ---")
    
    # 1. Test Reading & Parsing
    # Using the sample text resume you already have in data/raw/
    sample_resume_path = os.path.join("data", "raw", "sample_resume.txt")
    
    if not os.path.exists(sample_resume_path):
        print(f"[!] Error: Please make sure {sample_resume_path} has text content to test.")
        return

    print("[*] Testing ResumeParser...")
    parser = ResumeParser()
    parsed_data = parser.parse_resume(sample_resume_path)
    print(f"[✓] Parsed Data Result: {parsed_data}")
    
    # 2. Test Pandas Data Conversion & Storage
    print("\n[*] Testing DataStorage with Pandas...")
    storage = DataStorage()
    
    # Structuring data into a list format that pandas expects
    candidate_records = [{
        "email": parsed_data.get("email"),
        "phone": parsed_data.get("phone"),
        "skills": ", ".join(parsed_data.get("skills", []))
    }]
    
    output_csv_path = os.path.join("data", "processed_candidates.csv")
    storage.save_candidates(candidate_records, output_csv_path)
    
    # 3. Final Check
    if os.path.exists(output_csv_path):
        print(f"[✓] Success! Processed data saved cleanly to: {output_csv_path}")
    else:
        print("[!] Error: CSV file was not created.")

if __name__ == "__main__":
    run_verification()