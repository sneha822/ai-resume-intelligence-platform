from flask import Flask, request, jsonify
import sys
import os

# Fix Python path so 'src' can be discovered
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Day 14 scoring engine
from src.scoring import CandidateScorer

app = Flask(__name__)
scorer = CandidateScorer()

# 1. Health Check Endpoint (GET)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "message": "AI Resume Intelligence API Running"})

# 2. Predict/Receive Endpoint (POST)
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    return jsonify({"received_data": data, "status": "success"})

# 3. Score Endpoint (POST)
@app.route("/score", methods=["POST"])
def score_candidate():
    data = request.json
    
    # Extract values sent by the client
    skill_count = data.get("skill_count", 0)
    candidate_level = data.get("candidate_level", "Beginner")
    
    # Calculate the score using your core engine
    score = scorer.calculate_total_score(skill_count, candidate_level)
    
    return jsonify({
        "candidate_score": score,
        "skill_count": skill_count,
        "candidate_level": candidate_level
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)