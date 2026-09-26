import pandas as pd
from src.validation import DataValidator

# 1. Initialize the validator
validator = DataValidator()

# 2. Test individual row validation methods
print("--- Testing Individual Row Validation ---")
print(f"Is email valid ('test@gmail.com'): {validator.has_email('test@gmail.com')}")
print(f"Is email valid ('   '): {validator.has_email('   ')}")
print(f"Are skills valid (['python', 'sql']): {validator.has_valid_skills(['python', 'sql'])}")
print(f"Are skills valid (['rust']): {validator.has_valid_skills(['rust'])}")
print()

# 3. Test DataFrame duplicate validation
print("--- Testing DataFrame Duplicate Email Validation ---")

# Create a sample dataset with duplicate emails to trigger the validator
mock_data = {
    "email": ["johndoe@gmail.com", "aryan@gmail.com", "johndoe@gmail.com"],
    "phone": ["9876543210", "9876543211", "9876543214"],
    "skills": ["python, sql", "python, java", "sql"]
}

df = pd.DataFrame(mock_data)

# Run the validation check
has_duplicates = validator.has_duplicate_emails(df)
print(f"Does the dataframe contain duplicate emails?: {has_duplicates}")

if has_duplicates:
    print("Warning: Duplicate candidate emails detected in the dataset!")
else:
    print("Success: No duplicate emails found.")