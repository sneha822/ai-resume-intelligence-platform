from src.validation import DataValidator

validator = DataValidator()

print(
    validator.has_email(
        "john@gmail.com"
    )
)

print(
    validator.has_valid_skills(
        ["python", "sql"]
    )
)