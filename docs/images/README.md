# Demo images

Drop your own screenshots / GIF here so the README (and your resume link) show a
populated, working app. Your own captures are more authentic than generated ones.

## Capture in ~3 minutes

1. **Seed demo data** (one job, 3 candidates with resumes + pre-computed evaluations —
   no LLM calls, no quota used):
   ```bash
   .venv/Scripts/python -m backend.db.seed
   ```
2. **Run the app** (two terminals):
   ```bash
   API_PORT=8123 .venv/Scripts/python -m backend
   AIRI_API_URL=http://127.0.0.1:8123 .venv-ui/Scripts/python -m streamlit run frontend/Home.py
   ```
3. **Screenshot these three screens** and save with these exact names:
   - `dashboard.png` — the Home page (shows 🟢 Healthy + candidate/job counts)
   - `candidate-deep-dive.png` — Candidates → pick a seeded candidate (e.g. "Sam Patel"
     or "Aisha Khan"); shows the fit badge, score, and the competency **radar chart**
   - `search.png` — Search → e.g. "nlp machine learning engineer" → the ranked results

## Optional: a short GIF (best for a resume)
Record a 60–90s screen capture doing: search → open a candidate deep-dive → ask the
copilot a question. Save as `demo.gif` and reference it at the top of the main README.
Free tools: ScreenToGif (Windows), Loom, or the built-in Xbox Game Bar (`Win+G`).
