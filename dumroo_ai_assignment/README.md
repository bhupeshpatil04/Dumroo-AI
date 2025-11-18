# Dumroo.ai — AI Developer Assignment (Demo)

This repository contains a small demo that implements a natural-language query interface over a small student dataset with role-based scoping for admins.

## What’s included
- `students.csv` — sample dataset
- `ai_query.py` — lightweight parser + filters (no external LLM required)
- `app.py` — Streamlit demo app
- `requirements.txt` — packages to install
- `README.md` — this file
- `example_queries.txt` — suggested queries

## Setup (local)
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS / Linux
   venv\Scripts\activate    # Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the demo:
   ```bash
   streamlit run app.py
   ```

## Notes
- This demo uses a simple rule-based parser (see `ai_query.py`). If you want to plug in an LLM (OpenAI + LangChain), the code is modular to replace the `parse_query_and_filter` function with an LLM-backed handler.
- Role-based scoping: the sidebar controls `grades` and `regions` which restrict what an admin can see.

## Example queries
See `example_queries.txt` for 3 example queries used in the assignment.

## Files to submit
Zip folder `dumroo_ai_assignment.zip` containing the above files.

---
Generated automatically on 2025-11-18.
