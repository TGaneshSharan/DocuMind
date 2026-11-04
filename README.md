# 📚 DocuMind

### AI-Powered Document Intelligence System

DocuMind is a Retrieval-Augmented Generation (RAG) application
that allows users to upload PDF documents and ask questions
about their content.

## Features

- PDF text extraction
- Text chunking with overlap
- Gemini embeddings
- ChromaDB vector database
- Semantic document retrieval
- Gemini-powered question answering
- Document-specific retrieval
- Page-number source references
- Streamlit chat interface

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- ChromaDB
- PyMuPDF
- Retrieval-Augmented Generation (RAG)

## Architecture

PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Gemini Embeddings
    ↓
ChromaDB Vector Database
    ↓
User Question
    ↓
Question Embedding
    ↓
Semantic Search
    ↓
Relevant Context
    ↓
Gemini LLM
    ↓
Final Answer with Sources

## Installation

1. Clone the repository.

2. Install dependencies:

   pip install -r requirements.txt

3. Create a `.env` file:

   GEMINI_API_KEY=your_api_key_here

4. Run the application:

   python -m streamlit run app.py

## Project Purpose

This project demonstrates practical implementation
of Retrieval-Augmented Generation (RAG), vector databases,
embeddings, document processing and LLM integration.