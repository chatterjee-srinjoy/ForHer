# LAB: Python Shiny Application - ForHer

## App Structure

```text
ForHer/
├── app.py                 # Main Shiny for Python app
├── src/
│   ├── __init__.py
│   ├── api_client.py      # MyHealthfinder API integration
│   └── ai_insights.py     # AI-powered reporting (OpenAI)
├── docs/
│   ├── ABOUT.md
│   ├── LAB_your_good_api_query.md
│   └── LAB_cursor_shiny_app.md
├── requirements.txt
└── README.md
```

## Required Components (Assignment Checklist)

| Requirement        | Implementation                                      |
|--------------------|-----------------------------------------------------|
| API Integration    | MyHealthfinder API via `src/api_client.py`          |
| Key Statistics     | `ui.value_box` components: recommendations, topics, categories |
| AI-Powered Insights| `src/ai_insights.py` – OpenAI summaries             |
| Clean UI           | `ui.page_sidebar` layout, cards, readable text      |
| Reactive Text      | `reactive_summary` output updates with user inputs  |
| Value Boxes        | 3 value boxes for key metrics                       |
| Visualizations     | Bar chart, pie chart, recommendations table, topics table |
| Deployment         | Posit Connect or other Python Shiny hosting         |

## Running Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
shiny run --reload app.py
```

## Cursor Usage

- Use Cursor to edit `app.py`, `src/api_client.py`, and `src/ai_insights.py`.
- Ask Cursor to add new visualizations or adjust the layout.
- Use Cursor to help with deployment configuration.
