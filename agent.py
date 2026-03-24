import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from db import get_db

load_dotenv()

def build_agent():
    db = get_db()

    repo_id = os.getenv("HUGGINGFACE_REPO_ID", "Qwen/Qwen2.5-Coder-32B-Instruct")
    base_llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        task="text-generation",
        max_new_tokens=512,
        temperature=0.01,
        repetition_penalty=1.03,
    )
    chat_llm = ChatHuggingFace(llm=base_llm)

    toolkit = SQLDatabaseToolkit(db=db, llm=chat_llm)

    agent = create_sql_agent(
        llm=chat_llm,
        toolkit=toolkit,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors="Check your formatting! You MUST start with 'Thought:' on a new line, then 'Action:' with the tool name, and 'Action Input:' with the input. No conversational greetings!",
        max_iterations=8,
        prefix="""You are an expert SQL assistant.
CRITICAL: You are a strict robot. Do NOT output conversational greetings like "I'll help you find..." or "Let me examine...". 
Instead, immediately output your 'Thought:', 'Action:', and 'Action Input:'.

When you have the final answer, output:
Thought: I now know the final answer
Final Answer: <Markdown Table>"""
    )

    return agent


_agent = None

def get_agent():
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


def run_query(user_question: str) -> str:
    try:
        agent = get_agent()
        result = agent.invoke({"input": user_question})
        return result["output"]
    except Exception as e:
        return f"Error: {str(e)}\n\nTry rephrasing your question."