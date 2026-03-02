# LAB: AI-Powered Reporting - Zena

## Overview

Zena uses Ollama (cloud or local LLM) to generate plain-language health insights
for first-gen and international students. All AI outputs are defensive — if the
model is unavailable or returns an error, culturally sensitive fallback strings
are displayed so the app never crashes or shows raw errors.

## AI Functions (`src/ai_insights.py`)

| Function                | Purpose                                              | Cache Key       |
|-------------------------|------------------------------------------------------|-----------------|
| `personalized_summary()` | Encouraging summary of top priorities for the user's age and vaccination status | Per content hash |
| `cultural_context()`     | Explains how U.S. preventive care differs from countries where you only visit when sick | `"cultural"`    |
| `myth_vs_fact()`         | Generates myth/fact pairs (used as supplementary content) | `"mythfact"`    |
| `simplify_text()`        | Rewrites a recommendation at 8th-grade reading level | Per content hash |
| `why_this_matters()`     | 1–2 sentence explanation of why a recommendation matters for the user's age | Per content hash |

All functions call `_call_ollama()`, which posts to Ollama's `/api/chat` endpoint
with `temperature=0.4` and `num_predict=350`.

## Predefined Quiz Data (`MYTH_FACT_QUIZ`)

The interactive quiz uses a hardcoded list of 8 `(statement, is_fact)` tuples rather
than live LLM generation, ensuring reliability and instant response:

```python
("You only need to see a doctor when you're sick.", False)
("Cervical cancer screening is recommended starting at age 21.", True)
("The flu shot can give you the flu.", False)
# ... 5 more items
```

## Defensive Error Handling

`_call_ollama()` returns error strings (not exceptions) on failure. The app detects
these with `_is_usable()`, which checks for markers like `"error:"`, `"unavailable"`,
`"not found"`, and `"unable to generate"`. When detected, fallback text is shown:

- **Summary fallback**: "Based on your profile, key preventive steps include routine
  screenings, staying up to date on vaccinations, and scheduling an annual well-woman visit."
- **Cultural fallback**: "In the U.S., preventive care is encouraged even when you feel
  healthy. Regular checkups, screenings, and vaccinations help catch issues early."

## AI Provider: Ollama Cloud (Recommended)

Use **Ollama Cloud** for larger models that run on Ollama's servers:

1. Create an API key at [ollama.com/settings/keys](https://ollama.com/settings/keys)
2. Copy `.env.example` to `.env` and set `OLLAMA_API_KEY=your_key`
3. Set `OLLAMA_MODEL=gpt-oss:120b` for the cloud model

## Alternative: Local Ollama

No API key required. Run models locally:

1. Install [Ollama](https://ollama.ai)
2. Run: `ollama run llama3.2`
3. Leave `OLLAMA_API_KEY` unset in `.env`

## Configuration (`.env`)

```bash
OLLAMA_API_KEY=your_key            # Ollama Cloud auth
OLLAMA_MODEL=gpt-oss:120b          # Cloud model (default: llama3.2 for local)
OLLAMA_HOST=https://ollama.com     # Auto-set when API key is present
```

## Prompt Design

The AI is prompted to:
- Write in plain, friendly language at an 8th-grade reading level
- Use complete sentences only (no truncation)
- Keep responses under 100 words
- Avoid bullet points and medical jargon
- Speak as a health educator for international students
