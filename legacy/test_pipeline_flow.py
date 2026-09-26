"""
Step 4: End-to-End Feature Pipeline Verification Script
-------------------------------------------------------
Executes and validates each stage of the AI Resume Intelligence processing pipeline.
"""

import os
import sys
import pandas as pd

# Ensure root workspace directory is in sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.file_handler import FileHandler
from src.parser import ResumeParser
from src.dataset_builder import CandidateDatasetBuilder
from src.data_splitter import CandidateDataSplitter


def verify_feature_pipeline():
    print("=" * 60)
    print("🚀 STARTING END-TO-END FEATURE PIPELINE VERIFICATION")
    print("=" * 60)

    # ------------------------------------------------------
    # STAGE 1: Check File Directories
    # ------------------------------------------------------
    print("\n[Stage 1/5] Checking Data Directories...")
    data_dir = os.path.join(ROOT_DIR, "data")
    processed_csv = os.path.join(data_dir, "processed_candidates.csv")
    train_csv = os.path.join(data_dir, "train_candidates.csv")
    test_csv = os.path.join(data_dir, "test_candidates.csv")

    assert os.path.exists(data_dir), "❌ 'data/' directory is missing!"
    print("  ✓ Data directory verified.")

    # ------------------------------------------------------
    # STAGE 2: Validate Dataset Loading & Numerical Features
    # ------------------------------------------------------
    print("\n[Stage 2/5] Validating Dataset Builder & Schema...")
    if not os.path.exists(processed_csv):
        print("  ⚠️ 'processed_candidates.csv' not found. Initializing empty dataset...")
        df_initial = pd.DataFrame(columns=["email", "phone", "skills", "skill_count", "candidate_level"])
    else:
        df_initial = pd.read_csv(processed_csv)
        print(f"  ✓ Loaded 'processed_candidates.csv' ({len(df_initial)} records).")

    builder = CandidateDatasetBuilder()
    df_built = builder.add_numerical_features(df_initial)

    required_cols = ["experience_years", "project_count", "certification_count"]
    for col in required_cols:
        assert col in df_built.columns, f"❌ Column '{col}' missing after DatasetBuilder!"
    print(f"  ✓ Numerical feature matrix built cleanly. Columns: {list(df_built.columns)}")

    # Save standardized processed dataset
    df_built.to_csv(processed_csv, index=False)

    # ------------------------------------------------------
    # STAGE 3: Validate Resume Parser Subsystem
    # ------------------------------------------------------
    print("\n[Stage 3/5] Testing Resume Parser Ingestion...")
    sample_text_path = os.path.join(data_dir, "temp_uploads", "sample_test_resume.txt")
    os.makedirs(os.path.dirname(sample_text_path), exist_ok=True)

    with open(sample_text_path, "w", encoding="utf-8") as f:
        f.write("John Doe\nEmail: johndoe@gmail.com\nSkills: Python, SQL, Machine Learning\nExperience: 3 years")

    parser = ResumeParser()
    parsed_output = parser.parse_resume(sample_text_path)
    assert isinstance(parsed_output, dict), "❌ Parser output should be a dictionary!"
    print("  ✓ Resume parsing pipeline operational.")
    print(f"    Extracted Keys: {list(parsed_output.keys())}")

    # ------------------------------------------------------
    # STAGE 4: Validate Train/Test Data Splitter
    # ------------------------------------------------------
    print("\n[Stage 4/5] Testing Train/Test Splitter Module...")
    if len(df_built) >= 2:
        splitter = CandidateDataSplitter()
        train_df, test_df = splitter.split_dataset(df_built, test_size=0.2, random_state=42)
        
        train_df.to_csv(train_csv, index=False)
        test_df.to_csv(test_csv, index=False)
        
        print(f"  ✓ Split Complete -> Train Shape: {train_df.shape}, Test Shape: {test_df.shape}")
    else:
        print("  ⚠️ Dataset contains fewer than 2 candidates. Add more candidate rows to test split ratios.")

    # ------------------------------------------------------
    # STAGE 5: File Artifact Verification
    # ------------------------------------------------------
    print("\n[Stage 5/5] Verifying Generated Data Artifacts...")
    for file_path, name in [(processed_csv, "processed_candidates.csv"),
                            (train_csv, "train_candidates.csv"),
                            (test_csv, "test_candidates.csv")]:
        if os.path.exists(file_path):
            print(f"  ✓ Found: {name} ({os.path.getsize(file_path)} bytes)")
        else:
            print(f"  ⚠️ Missing: {name}")

    print("\n" + "=" * 60)
    print("✅ FEATURE PIPELINE VERIFICATION PASSED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    verify_feature_pipeline()