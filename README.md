# ForHer

**Healthcare in the U.S. explained without the confusion.**

An AI-powered **Python Shiny** app for first-generation and international female students to understand preventive healthcare in the United States.

## Project Overview

| | |
|---|---|
| **Topic** | Women's Health for First-Gen / International Students |
| **API** | MyHealthfinder API (U.S. HHS) |
| **Stack** | Python, Shiny for Python, pandas, matplotlib, OpenAI |

## Quick Start

```bash
# 1. Create venv and install
python -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# 2. Run app
shiny run --reload app.py
```

## Features (Matches Assignment)

- **API Integration**: MyHealthfinder – personalized preventive care recommendations
- **Key Statistics**: Value boxes (recommendations, topics, categories)
- **AI Insights**: OpenAI for plain-language summaries (optional; app still works without)
- **UI**: Python Shiny sidebar layout, clean cards, reactive text
- **Visualizations**: Category bar chart, type pie chart, recommendations table, topics table
- **Deployment**: Can be deployed to Posit Connect or other Python/Shiny-capable platforms

## Files

- `app.py` – Main Python Shiny app (UI + server)
- `src/api_client.py` – MyHealthfinder API client
- `src/ai_insights.py` – AI summarization via OpenAI
- `requirements.txt` – Python dependencies
