from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os
import sqlite3
from openai import OpenAI

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




# ---------- SQLITE ----------
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(e)
        return []

# ---------- UI ----------
st.set_page_config(page_title="Text to SQL (OpenRouter)")
st.title("Text to SQL App (LLM Powered)")

question = st.text_input("Enter your question")

if st.button("Generate SQL"):
    sql = get_sql_from_text(question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    result = read_sql_query(sql, "student.db")
    st.subheader("Result")
    if result:
        for r in result:
            st.write(r)
    else:
        st.info("No data found")
