"""
ai_query.py
Simple natural-language-to-filter parser for the Dumroo assignment.
This is a lightweight fallback implementation (no external LLM required).
It supports queries like:
 - "Which students haven't submitted their homework yet?"
 - "Show me performance data for Grade 8 from last week"
 - "List all upcoming quizzes scheduled for next week"

Role scoping: pass admin_scope dict, e.g. {"grades":[8], "regions":["North"]}
"""
from datetime import datetime, timedelta
import pandas as pd
import re

DATE_FMT = "%Y-%m-%d"

def load_data(path):
    return pd.read_csv(path, parse_dates=["last_submission_date","quiz_date"], dayfirst=False)

def within_scope(df, admin_scope):
    # Filter by grades and regions if provided
    if admin_scope is None:
        return df
    df2 = df.copy()
    if "grades" in admin_scope and admin_scope["grades"]:
        df2 = df2[df2["grade"].isin(admin_scope["grades"])]
    if "regions" in admin_scope and admin_scope["regions"]:
        df2 = df2[df2["region"].isin(admin_scope["regions"])]
    return df2

def parse_query_and_filter(query, df, admin_scope=None, as_of_date=None):
    \"\"\"Return filtered DataFrame and a short explanation string.\"\"\"
    if as_of_date is None:
        as_of_date = datetime.utcnow().date()
    df = within_scope(df, admin_scope)

    q = query.lower().strip()
    # haven't submitted / not submitted
    if re.search(r"(haven'?t submitted|not_submitted|not submitted|haven t submitted|haven't submitted)", q):
        res = df[df["submission_status"].str.lower().isin(["not_submitted","not submitted","not_submitted".replace("_"," ")] ) | (df["submission_status"].fillna("").str.lower().str.contains("not"))]
        return res, f\"Students in scope who haven't submitted (as of {as_of_date})\"

    # performance for Grade X from last week
    m = re.search(r"grade\s*(\d+)", q)
    if "performance" in q or "performance data" in q or "show me performance" in q:
        grade = int(m.group(1)) if m else None
        # detect 'last week'
        if "last week" in q:
            end = as_of_date - timedelta(days=as_of_date.weekday()+1) + timedelta(days=6)  # last week's Sunday
            start = end - timedelta(days=6)
        else:
            # default to last 7 days
            end = as_of_date
            start = as_of_date - timedelta(days=7)
        mask = (df["quiz_date"].dt.date >= start) & (df["quiz_date"].dt.date <= end)
        if grade is not None:
            mask = mask & (df["grade"] == grade)
        res = df[mask]
        return res, f\"Performance data for Grade {grade if grade else 'ALL'} from {start} to {end}\"

    # upcoming quizzes next week
    if "upcoming" in q and "next week" in q or (("next week" in q) and ("quiz" in q or "quizzes" in q)):
        # next week's Monday-Sunday
        today = as_of_date
        next_monday = today + timedelta(days=(7 - today.weekday()))
        start = next_monday
        end = start + timedelta(days=6)
        mask = (df["quiz_date"].dt.date >= start) & (df["quiz_date"].dt.date <= end)
        res = df[mask]
        return res, f\"Upcoming quizzes between {start} and {end}\"

    # fallback: try to return rows that match grade or class keywords
    if m:
        grade = int(m.group(1))
        res = df[df["grade"] == grade]
        return res, f\"Filtered for Grade {grade}\"

    # default: return empty with message
    return df.head(0), \"Sorry — couldn't understand the query. Try example queries in README.\"
