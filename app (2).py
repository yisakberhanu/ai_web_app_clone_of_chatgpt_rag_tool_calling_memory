import os
import uuid
import json
from datetime import datetime

import chromadb
import requests
from flask import Flask, request, jsonify, render_template
from pypdf import PdfReader


# =========================
# Flask App
# =========================

app = Flask(__name__)


# =========================
# ChromaDB Setup
# =========================

chroma_client = chromadb.PersistentClient(path="./chroma_db")

documents_collection = chroma_client.get_or_create_collection(
    name="documents"
)

memory_collection = chroma_client.get_or_create_collection(
    name="chat_memory"
)


# =========================
# Config
# =========================

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "qwen/qwen3.6-flash")
CURRENTS_API_KEY = os.getenv("CURRENTS_API_KEY")


# =========================
# File Extraction
# =========================

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    return ""


def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


# =========================
# Upload Route
# =========================

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    if not file.filename.endswith((".pdf", ".txt")):
        return jsonify({"error": "Only PDF and TXT files are allowed"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    text = extract_text_from_file(file_path)
    chunks = chunk_text(text)

    if not chunks:
        return jsonify({"error": "No readable text found in file"}), 400

    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        metadatas.append({
            "source": file.filename,
            "chunk_index": i,
            "type": "document"
        })

    documents_collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return jsonify({
        "message": f"Uploaded and indexed {len(chunks)} chunks from {file.filename}"
    })


# =========================
# Memory
# =========================

def save_memory(role, content):
    if content is None:
        return

    content = str(content).strip()

    if not content:
        return

    memory_collection.add(
        ids=[str(uuid.uuid4())],
        documents=[content],
        metadatas=[{
            "role": role,
            "type": "chat_memory",
            "created_at": datetime.now().isoformat()
        }]
    )


def retrieve_documents(query, top_k=4):
    if not query:
        return ""

    try:
        results = documents_collection.query(
            query_texts=[query],
            n_results=top_k
        )

        docs = results.get("documents", [[]])[0]
        return "\n\n".join(docs)

    except Exception:
        return ""


def retrieve_memories(query, top_k=4):
    if not query:
        return ""

    try:
        results = memory_collection.query(
            query_texts=[query],
            n_results=top_k
        )

        memories = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        formatted_memories = []

        for memory, metadata in zip(memories, metadatas):
            role = metadata.get("role", "unknown")
            formatted_memories.append(f"{role}: {memory}")

        return "\n".join(formatted_memories)

    except Exception:
        return ""


# =========================
# OpenRouter
# =========================

def call_openrouter(messages, tools=None):
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing in .env file.")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    return response.json()


# =========================
# Tools Schema
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_latest_news",
            "description": "Get latest general news or latest news about a specific topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Optional topic. Use empty string for general latest news. Examples: AI, Ethiopia, OpenAI, sports."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic math expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression like 25 * 4 + 10."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# =========================
# Tool Functions
# =========================

def get_latest_news(topic=""):
    api_key = os.getenv("CURRENTS_API_KEY")

    if not api_key:
        return "CURRENTS_API_KEY is missing in .env file."

    topic = str(topic or "").strip()

    general_words = [
        "",
        "today",
        "latest",
        "news",
        "latest news",
        "today news",
        "news today",
        "general",
        "general news"
    ]

    if topic.lower() in general_words:
        url = "https://api.currentsapi.services/v1/latest-news"
        params = {
            "language": "en",
            "page_size": 5
        }
    else:
        url = "https://api.currentsapi.services/v1/search"
        params = {
            "keywords": topic,
            "language": "en",
            "page_size": 5
        }

    headers = {
        "Authorization": api_key
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        try:
            data = response.json()
        except Exception:
            return f"News API returned non-JSON response: {response.text}"

        if response.status_code != 200:
            return f"News API error: {data}"

        articles = data.get("news", [])

        if not articles:
            return f"No news found for: {topic or 'latest news'}"

        results = []

        for i, article in enumerate(articles[:5], start=1):
            title = article.get("title", "No title")
            description = article.get("description", "No description")
            source_url = article.get("url", "")
            published = article.get("published", "Unknown date")
            author = article.get("author", "")

            results.append(
                f"{i}. {title}\n"
                f"Published: {published}\n"
                f"Author: {author or 'Unknown'}\n"
                f"Description: {description}\n"
                f"URL: {source_url}"
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"News tool failed: {str(e)}"


def run_tool(tool_name, arguments):
    if arguments is None:
        arguments = {}

    if tool_name == "get_latest_news":
        topic = arguments.get("topic", "")
        return str(get_latest_news(topic))

    if tool_name == "get_current_datetime":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if tool_name == "calculator":
        expression = arguments.get("expression", "")

        try:
            result = eval(expression, {"__builtins__": {}})
            return str(result)
        except Exception:
            return "Invalid math expression."

    return "Tool not found."


# =========================
# Chat Route
# =========================

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    save_memory("user", user_message)

    document_context = retrieve_documents(user_message)
    memory_context = retrieve_memories(user_message)

    system_prompt = f"""
You are a helpful AI assistant.

You have three abilities:
1. Answer using uploaded documents.
2. Remember relevant past conversations.
3. Use tools when current information is needed.

Uploaded document context:
{document_context}

Relevant chat memory:
{memory_context}

Rules:
- Use uploaded document context when relevant.
- Use chat memory when relevant.
- Use get_latest_news for current/latest information.
- Use get_current_datetime for current date and time.
- Use calculator for basic math operations.
- If the user asks for today's news, latest news, or current news, call get_latest_news with an empty topic.
- If the user asks news about a specific topic, call get_latest_news with that topic.
- When a tool gives results, summarize the tool results clearly for the user.
- If you do not know, say you do not know.
- Do not invent sources.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        first_result = call_openrouter(messages, tools=tools)
        assistant_message = first_result["choices"][0]["message"]

        assistant_reply = ""
        last_tool_result = ""

        if assistant_message.get("tool_calls"):
            messages.append(assistant_message)

            for tool_call in assistant_message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                arguments_raw = tool_call["function"].get("arguments", "{}")

                try:
                    arguments = json.loads(arguments_raw)
                except Exception:
                    arguments = {}

                tool_result = run_tool(tool_name, arguments)
                tool_result = str(tool_result)
                last_tool_result = tool_result

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": tool_name,
                    "content": tool_result
                })

            final_result = call_openrouter(messages)
            assistant_reply = final_result["choices"][0]["message"].get("content") or ""

            # If the model does not generate final text after tool call,
            # return the tool result directly.
            if not assistant_reply.strip():
                assistant_reply = last_tool_result

        else:
            assistant_reply = assistant_message.get("content") or ""

        if not assistant_reply.strip():
            assistant_reply = "I could not generate a response."

        save_memory("assistant", assistant_reply)

        return jsonify({"reply": assistant_reply})

    except Exception as e:
        return jsonify({
            "error": f"Chat failed: {str(e)}"
        }), 500


# =========================
# Frontend Route
# =========================

@app.route("/")
def index():
    return render_template("index.html")


# =========================
# Run App
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)