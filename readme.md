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
