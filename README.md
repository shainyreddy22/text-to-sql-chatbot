# Text-to-SQL Bot 🗄️

An intelligent, completely free Text-to-SQL bot powered by **Hugging Face's Free Inference API** and **LangChain**. 
It translates plain-English questions into complex SQL queries, executes them against a local SQLite database (`chinook.db`), and returns beautifully formatted Markdown tables—all without requiring any paid APIs!

---

## 🌟 Key Features
* **Triple Interface:** Access the bot via an interactive visual `Streamlit` Dashboard, a standard `FastAPI` REST endpoint, or a rapid `CLI` terminal interface!
* **100% Free AI Engine:** Runs natively using **Qwen 2.5 Coder 32B** (or any model of your choice) via the Hugging Face Serverless API. No Google Gemini or OpenAI credit limits.
* **Intelligent Auto-Correction:** The LangChain ReAct agent automatically coaches the LLM to adhere perfectly to correct output syntax, preventing common API chat parsing errors.

---

## ⚡ Setup & Installation

### 1. Prerequisites
Ensure you have Python installed (Python 3.9+ recommended).

### 2. Install Dependencies
Navigate into the project folder and install all required packages:
```powershell
pip install -r requirements.txt
```

### 3. Environment Variables
You need a free Hugging Face API Token since this project does not rely on Gemini.
1. Create a completely free account at [Hugging Face](https://huggingface.co/join).
2. Navigate to your [Access Tokens Settings](https://huggingface.co/settings/tokens).
3. Click **"Create new token"**. 
4. Under "Token Type", select **Read** (a "Write" token is NOT required because the bot only reads from the inference API).
5. Name your token, copy it, and open or create a `.env` file in the root folder to add it:
```ini
HUGGINGFACEHUB_API_TOKEN="hf_your_token_here_..."

# (Optional) Override the default model
HUGGINGFACE_REPO_ID="Qwen/Qwen2.5-Coder-32B-Instruct"
```

---

## 🚀 How to Run the Application

This project supports three separate ways to interact with the bot! Run exactly one of the commands below depending on your preference:

### Option A: The Streamlit Web UI (Recommended)
Launch the beautiful, user-friendly graphical chat interface.
```powershell
python -m streamlit run app.py
```
*Your browser will quickly open to `http://localhost:8501`.*

### Option B: The Command Line Interface (CLI)
Interact with the SQL agent directly in your terminal window in text mode.
```powershell
python main.py
```

### Option C: The FastAPI Backend Server
Run the headless REST API (useful if you are connecting this bot to your own custom frontend application).
```powershell
python -m uvicorn app.main:app --reload
```
*Test the interactive API Swagger docs at `http://localhost:8000/docs`.*

---

## 🛠️ Technologies Built-In
- **LangChain:** Core orchestration and ReAct SQL Agent pipeline.
- **Hugging Face Hub:** Free serverless inference API hosting `Qwen/Qwen2.5-Coder-32B-Instruct`.
- **Streamlit:** Fast, clean conversational web framework frontend.
- **FastAPI:** High-performance async REST backend framework.
- **SQLite3:** Local lightweight testing database based on the standard `Chinook` dataset track records.
