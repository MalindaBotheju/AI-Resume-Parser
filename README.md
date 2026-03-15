# 📄 AI Resume Parser (Llama-3 + FastAPI)

A containerized, privacy-first web application that leverages a locally hosted Llama-3 AI model to automatically extract and structure data from PDF resumes into clean JSON format.

## 🚀 Features
* **Privacy-First AI:** Uses a local Llama-3 GGUF model via Ollama. No sensitive resume data is ever sent to third-party APIs like OpenAI.
* **Document Parsing:** Efficiently extracts raw text from PDF files using `PyMuPDF`.
* **Intelligent Extraction:** Prompts the LLM to identify and categorize key information (Skills, Experience, Education, Contact Info) into a structured format.
* **Full-Stack Architecture:** Responsive HTML/JS frontend connected to a high-performance Python FastAPI backend.
* **Fully Containerized:** Packaged with Docker, bundling the Linux OS, web server, and the multi-gigabyte LLM into a single portable container.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Engine:** Llama-3 (8B), Ollama
* **Document Processing:** PyMuPDF (`fitz`)
* **Frontend:** HTML, Vanilla JavaScript, CSS
* **DevOps:** Docker

## 📓 Model Experimentation
The repository includes the original Google Colab notebook (`.ipynb`) used for initial prompt engineering and model testing before migrating to a full-stack Dockerized application.

## 🐳 How to Run Locally

1. **Build the Docker Image:**
   ```bash
   docker build -t resume-parser .