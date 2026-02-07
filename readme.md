# 🚀 Text to SQL – LLM Powered Application

An intelligent **LLM-powered Text-to-SQL application** that converts natural language questions into SQL queries and executes them on a SQLite database.

Built using **OpenRouter (Mistral LLM)**, **Streamlit**, and **SQLite**, this project demonstrates real-world usage of Large Language Models for database querying.

---

## ✨ Features

- 🧠 Converts natural language questions into SQL queries
- ⚡ Uses LLM (Mistral via OpenRouter)
- 📊 Executes queries on a SQLite database
- 🔡 Handles case-insensitive data using `UPPER()`
- 🖥️ Interactive Streamlit UI
- 🔐 API keys secured using `.env`

---

## 🛠️ Tech Stack

- Frontend: Streamlit  
- LLM: Mistral 7B (via OpenRouter)  
- Backend: Python  
- Database: SQLite  
- API Gateway: OpenRouter  

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/Chhavi001/text-to-sql-llm.git
cd text-to-sql-llm
pip install -r requirements.txt
