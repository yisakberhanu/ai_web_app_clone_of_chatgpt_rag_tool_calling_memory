# AI Web App with RAG

Build a complete AI web app with RAG using **Flask**, **OpenRouter**, **ChromaDB**, **PDF/TXT upload**, **chat memory**, and **tool calling**.

This project shows how a modern AI assistant works behind the scenes. It can upload files, store document knowledge in ChromaDB, retrieve relevant information using RAG, remember previous conversations, and use external tools like news, date/time, and calculator.

## YouTube Tutorial

Watch the full step-by-step video here:

[Watch on YouTube](YOUR_YOUTUBE_LINK_HERE)

## Features

- AI chat interface
- Flask backend
- OpenRouter model integration
- ChromaDB vector database
- PDF and TXT upload
- RAG document retrieval
- Chat history memory
- Tool calling
- Latest news tool using Currents API
- Current date and time tool
- Calculator tool
- Modern HTML/CSS/JavaScript frontend

## What This Project Teaches

This project teaches the real building blocks behind AI web apps:

- How RAG works
- How to store documents in a vector database
- How to retrieve relevant chunks from uploaded files
- How to save and retrieve chat memory
- How tool calling works
- How Flask connects the frontend, vector database, tools, and AI model

## How It Works

The app follows this flow:

```txt
User
 ↓
Flask Web App
 ↓
Upload PDF/TXT or send message
 ↓
ChromaDB stores documents and chat memory
 ↓
Retrieve relevant document chunks
 ↓
Retrieve relevant chat memories
 ↓
Build system prompt
 ↓
Send request to OpenRouter model
 ↓
Model can call tools if needed
 ↓
Flask runs the tool
 ↓
Final answer is returned to the chat UI

````md
# AI Web App with RAG

Build a complete AI web app with RAG using **Flask**, **OpenRouter**, **ChromaDB**, **PDF/TXT upload**, **chat memory**, and **tool calling**.

This project shows how a modern AI assistant works behind the scenes. It can upload files, store document knowledge in ChromaDB, retrieve relevant information using RAG, remember previous conversations, and use external tools like news, date/time, and calculator.

## YouTube Tutorial

Watch the full step-by-step video here:

[Watch on YouTube](YOUR_YOUTUBE_LINK_HERE)

## Features

- AI chat interface
- Flask backend

## Simple RAG Explanation

RAG means **Retrieval-Augmented Generation**.

In simple words:

```txt
Search first, answer second.
```

Example:

Imagine you give your friend a 30-page document and ask:

> What are the important points?

A good friend will not answer from memory. They will open the document, search for the useful parts, and then explain.

That is exactly what RAG does.

The AI retrieves useful information first, then generates an answer.

## Tech Stack

* Python
* Flask
* OpenRouter API
* ChromaDB
* Currents API
* HTML
* CSS
* JavaScript
* pypdf
* requests

## Project Structure

```txt
ai-rag-web-app/
│
├── app.py
├── requirements.txt
├── .env
│
├── uploads/
│
├── chroma_db/
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

Create a `requirements.txt` file:

```txt
flask
python-dotenv
requests
chromadb
pypdf
```

## Environment Variables

Create a `.env` file in the root folder:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=qwen/qwen3.6-flash
CURRENTS_API_KEY=your_currents_api_key
```

Important:

Do not expose your API keys in frontend JavaScript. Keep all API keys inside the backend.

## Run the App

Start the Flask server:

```bash
python app.py
```

Then open:

```txt
http://127.0.0.1:5000
```

## Example Prompts

### RAG from Uploaded File

Upload a PDF or TXT file, then ask:

```txt
Summarize the uploaded document.
```

```txt
What are the key points from the file?
```

```txt
Based on the uploaded document, what should I remember?
```

### Chat Memory

First say:

```txt
My project name is Ismae.
```

Then ask:

```txt
What is my project name?
```

### Tool Calling

Ask:

```txt
What is today’s date?
```

```txt
Give me today’s latest news.
```

```txt
What is 25 * 8 + 13?
```

## Tools Included

### Latest News Tool

Uses Currents API to get latest news or topic-based news.

Example:

```txt
Give me latest news about AI.
```

### Date and Time Tool

Returns the current date and time.

Example:

```txt
What is today’s date?
```

### Calculator Tool

Calculates simple math expressions.

Example:

```txt
Calculate 12 * 78.
```

## Notes

This project is made for learning and teaching.

For production, you should improve:

* User authentication
* Separate memory per user
* Safer calculator instead of `eval()`
* File validation
* Rate limiting
* Better error handling
* Source citations
* Streaming responses
* Database-backed user sessions
* Deployment security

## Future Improvements

Possible next features:

* Streaming AI responses
* PDF source citations
* User login
* Save multiple chat sessions
* Better document chunking
* Web search tool
* Deployment to Render, Railway, or VPS
* Better UI animations
* Admin dashboard for uploaded files

## Credits

Built by **Yisak Birhanu Bule**.

YouTube: [Watch the tutorial](YOUR_YOUTUBE_LINK_HERE)

## License

This project is open source and available under the MIT License.

```
```
