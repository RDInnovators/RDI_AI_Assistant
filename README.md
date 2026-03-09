# RDI AI Prompt Assistant

A simple research-intake and AI prompt-generation system.

## Features
- Collects research idea information
- Recommends the best AI tool to use next
- Generates prompt packs for Bohrium, Perplexity, Gemini, and ChatGPT
- Designed for public and group use
- Dark themed UI

## Tech Stack
- Frontend: HTML/CSS/JavaScript
- Backend: FastAPI
- Storage: Google Sheets (next step)

## Local Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload