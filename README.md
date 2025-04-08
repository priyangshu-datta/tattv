# Tattv

🚧 Work in Progress

---

## 🔍 Overview

Tattv is a powerful, modular lead intelligence tool designed for extracting meaningful business attributes from websites using both traditional scraping and LLM-based analysis. Think of it as an AI-driven extractor that **sees the essence** (Tattva) behind a company’s digital presence.

It is built for businesses and professionals looking for a practical, extendible tool that demonstrates a real understanding of the lead generation pipeline and its challenges.

---

## 🔧 Key Features

- 🧩 **Multi-URL Input Table**: Add multiple URLs for scraping.
- ⚙️ **Multiprocessing Scraper**: Scrapes multiple websites in parallel using `multiprocessing`.
- 💡 **Status Indicator**: Visual indicator showing app status (idle or busy).
- 📋 **Real-time Logs**: View logs in a separate tab with live updates.
- 🔄 **Interactive Results Table**: Displays scraping results with dynamic column generation.
- 💾 **Export Options**: Save logs and results to external files (CSV, TXT).

---

## 🧠 Name Meaning

"Tattv" (Sanskrit: तत्त्व) means *essence*, *principle*, or *truth*. This tool aims to extract the most essential truth from public web data.

---

## 🏗 Architecture

- **Backend**: Headless, modular scraping engine (Python)
- **Frontend**: PySide6-based desktop interface (current), extendable to web/mobile
- **Extractor**: Pluggable vanilla extractors
- **Scrapers**: Configurable with optional LLM-based fallback
- **LLM Clients**: Pluggable (OpenAI, Groq, Transformers)

The backend and frontend are cleanly decoupled, enabling multiple UI implementations over time.

---

## ⚙️ Requirements

- Python 3.13+
- `transformers` (optional), `openai` (optional), `groq` (optional), `pyside6`, `playwright`, `beautifulsoup`

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/priyangshu-datta/tattv.git
cd tattv
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

> Make sure Playwright is installed and set up:
```bash
playwright install
```

---

## Running the App
```bash
python run.py
```