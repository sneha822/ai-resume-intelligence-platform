# API Documentation

## GET /

Returns API status.

## GET /health

Returns health status.

## POST /predict

Input:

{
  "skills": ["python"]
}

## POST /score

Input:

{
  "skill_count": 5,
  "candidate_level": "Advanced"
}

Output:

{
  "candidate_score": 100
}