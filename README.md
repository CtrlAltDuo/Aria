# Aria - AI Automation Agent

Aria is an AI-powered desktop agent for recruiting firms. It automates repetitive tasks by observing the screen and controlling the computer just like a human would.

## Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **Supported OS:** Windows and Linux.

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. API Key Configuration

Copy the example environment file:
```bash
cp .env.example .env
```
Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com). You can set it in the `.env` file or directly in the app's Settings page.

## Running the Application

To start both the frontend and backend simultaneously (dev mode):

```bash
cd frontend
npm run dev
```

The Electron desktop app will open. You can now submit your first task (e.g., "Open calculator and type 5 + 5").

## Submitting Your First Task

1. Navigate to **New Task**.
2. Describe what you want Aria to do (e.g., "Open a new browser tab, go to linkedin.com, and search for Software Engineer").
3. Click **Start Task**.
4. Watch the live action log as Aria completes the task!
