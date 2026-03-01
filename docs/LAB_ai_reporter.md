# LAB: AI-Powered Reporting (Python Shiny)

## Overview

ForHer uses AI to generate friendly, plain-language summaries of preventive health recommendations. This helps first-gen and international students understand U.S. healthcare guidance without medical jargon.

## AI Provider: Ollama Cloud (Recommended)

Use **Ollama Cloud** for larger models that run on Ollama's servers:

1. Create an API key at [ollama.com/settings/keys](https://ollama.com/settings/keys)
2. Copy `.env.example` to `.env` and set `OLLAMA_API_KEY=your_key`

## Alternative: Local Ollama

No API key required. Run models locally:

1. Install [Ollama](https://ollama.ai)
2. Run: `ollama run llama3.2`
3. Leave `OLLAMA_API_KEY` unset in `.env`

## Configuration

In `.env`:

```bash
OLLAMA_API_KEY=your_key   # For Ollama Cloud (get at ollama.com/settings/keys)
OLLAMA_MODEL=llama3.2     # Optional, default model
OLLAMA_HOST=https://ollama.com   # Optional, default when using key
```

## Implementation

See `src/ai_insights.py`:
- `generate_ai_insights()` – calls Ollama's `/api/chat` endpoint
- If `OLLAMA_API_KEY` is set → uses Ollama Cloud with `Authorization: Bearer <key>`
- If not set → uses local `http://localhost:11434` (no auth)

## Prompt Design

The AI is prompted to:
- Act as a health educator for international and first-gen students
- Summarize in plain, friendly language
- Keep the response under 150 words
- Provide 2–3 key takeaways

If Ollama is unavailable, the app shows a helpful message and still displays all recommendations and visualizations.
