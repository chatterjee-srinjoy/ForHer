"""
AI-Powered Insights Module
Supports OpenAI API (Ollama can be added via openai-compatible endpoint)
"""

import os
from typing import Optional


def generate_ai_insights(data_summary: str, user_context: str = "") -> str:
    """Generate AI insights from health data. Uses OpenAI if OPENAI_API_KEY is set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return _generate_openai_insights(data_summary, user_context, api_key)
    return (
        "AI unavailable. Set OPENAI_API_KEY in your environment for AI-powered summaries. "
        "The app works without it—you'll still see your recommendations."
    )


def _generate_openai_insights(
    data_summary: str, user_context: str, api_key: str
) -> str:
    """OpenAI API integration."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""You are a helpful health educator for first-generation and international female students in the U.S.
Summarize these preventive health recommendations in plain, friendly language. Keep it under 150 words.

{data_summary}

User context: {user_context or "General audience"}

Provide a brief, encouraging summary with 2-3 key takeaways."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return response.choices[0].message.content or "No response."
    except Exception as e:
        return f"AI error: {e}"
