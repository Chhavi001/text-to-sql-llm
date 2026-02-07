from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os
import sqlite3
import pandas as pd
from openai import OpenAI

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Text to SQL (LLM Powered)",
    page_icon="🤖",
    layout="centered"
)

# ---------- ENV ----------
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    st.error("OPENROUTER_API_KEY missing")
    st.stop()

# ---------- OPENROUTER CLIENT ----------
client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ---------- SIDEBAR ----------
st.sidebar.header("🧪 Example Queries")
st.sidebar.write("• Students in DATA SCIENCE class")
st.sidebar.write("• Students who scored more than 80")
st.sidebar.write("• Names and sections of DEVOPS students")
st.sidebar.markdown("---")
st.sidebar.caption("LLM Powered Text to SQL")

# ---------- HEADER ----------
st.title("🤖 Text to SQL App")
st.caption(
    "Upload your own CSV and ask questions in plain English to get SQL results 🚀"
)
st.markdown("---")

# ---------- CSV TO SQLITE ----------
def load_csv_to_db(csv_file, db_name="student.db"):
    try:
        df = pd.read_csv(csv_file)

        # Normalize column names
        df.columns = [c.strip().upper() for c in df.columns]

        required_cols = {"NAME", "CLASS", "SECTION", "MARKS"}
        if not required_cols.issubset(set(df.columns)):
            st.error("CSV must contain columns: NAME, CLASS, SECTION, MARKS")
            return False

        conn = sqlite3.connect(db_name)
        df.to_sql("STUDENT", conn, if_exists="replace", index=False)
        conn.close()
        return True
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return False

# ---------- CSV UPLOAD UI ----------
st.subheader("📂 Upload Student CSV")

uploaded_file = st.file_uploader(
    "Upload a CSV file (NAME, CLASS, SECTION, MARKS)",
    type=["csv"]
)

if uploaded_file:
    if load_csv_to_db(uploaded_file):
        st.success("✅ CSV uploaded successfully! You can now ask questions.")
    st.markdown("---")

# ---------- LLM FUNCTION ----------
def get_sql_from_text(question):
    prompt = f"""
Convert the following question into SQL.

Table: STUDENT
Columns: NAME, CLASS, SECTION, MARKS

Rules:
- Return ONLY SQL
- CAPITAL LETTERS
- Use UPPER() for string comparisons
- No explanation

Question: {question}
SQL:
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

# ---------- SQLITE QUERY ----------
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return []

# ---------- QUESTION INPUT + BUTTON (FORM) ----------
with st.form("query_form"):
    question = st.text_input(
        "💬 Enter your question",
        placeholder="e.g. Show students who scored more than 80",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate = st.form_submit_button("✨ Generate SQL")


# ---------- ACTION ----------
if generate and question:
    sql = get_sql_from_text(question)

    st.subheader("🧾 Generated SQL")
    st.code(sql, language="sql")

    result = read_sql_query(sql, "student.db")

    st.subheader("📊 Result")
    if result:
        for r in result:
            st.success(r)
    else:
        st.info("No data found")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built by Chhavi Gautam 💙 | LLM Powered Text to SQL App")
