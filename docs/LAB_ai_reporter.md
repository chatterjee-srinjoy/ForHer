# LAB: AI-Powered Reporting (Python Shiny)

## Overview

ForHer uses AI to generate friendly, plain-language summaries of preventive health recommendations. This helps first-gen and international students understand U.S. healthcare guidance without medical jargon.

## AI Provider: OpenAI

1. Get API key from `https://platform.openai.com`
2. Set environment variable before running the app:

```bash
export OPENAI_API_KEY=your-key-here
```

On Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY="your-key-here"
```

## Implementation

See `src/ai_insights.py`:
- `generate_ai_insights()` – main entry point used by the app
- `_generate_openai_insights()` – OpenAI Chat Completions API call

The app passes a concise bullet list of recommendations plus user context (age, sex, background) to the model.

## Prompt Design

The AI is prompted to:
- Act as a health educator for international and first-gen students
- Summarize in plain, friendly language
- Keep the response under 150 words
- Provide 2–3 key takeaways

If `OPENAI_API_KEY` is not set, the app falls back to a non-AI message but still shows all recommendations and visualizations.
