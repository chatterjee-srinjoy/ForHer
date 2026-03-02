# Zena

**Healthcare in the U.S. explained without the confusion.**

Zena is an interactive Shiny for Python web application designed to help first-generation and international female students better understand preventive healthcare in the United States. Many students come from countries where healthcare systems operate differently — where you only see a doctor when you're sick. In the U.S., preventive care like screenings, vaccinations, and annual checkups is encouraged even when you feel healthy. Zena bridges that gap by translating official health guidelines into clear, culturally understandable information.

## How It Works

1. Users enter a simple profile: age, country background, vaccination status, and insurance status.
2. The app calls the **MyHealthfinder API** (U.S. HHS) to retrieve age-appropriate preventive care recommendations.
3. Recommendations are categorized (Screenings, Vaccinations, Lifestyle & Mental Health), prioritized (High, Routine, Informational), and displayed in an interactive checklist table.
4. AI-generated insights provide a personalized summary and cultural context in plain language.
5. A Myth vs. Fact quiz reinforces health literacy in a low-pressure format.

## Features

- **Interactive Checklist Table** — Click rows to mark recommendations as complete. Selected rows are shaded by priority (darker pink = higher priority). A live Preventive Readiness Score shows your progress as a percentage.
- **AI Personalized Summary** — An Ollama-powered plain-language summary of your top health priorities based on age and vaccination status.
- **Cultural Context** — An AI-generated explanation of how U.S. preventive care differs from healthcare norms in other countries.
- **Myth vs. Fact Quiz** — 8 predefined statements to test and build health knowledge.
- **CSV Download** — Export your full checklist to take to a doctor's appointment.
- **Defensive Fallbacks** — If AI or API services are unavailable, culturally sensitive fallback text is shown so the app never crashes.

## Tech Stack

- Python 3.10+
- Shiny for Python 1.5+
- pandas
- Ollama Cloud or local Ollama (for AI summaries)
- MyHealthfinder API (U.S. HHS, no key required)
