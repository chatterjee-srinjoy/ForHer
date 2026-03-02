# LAB: Python Shiny Application - Zena

## App Structure

```text
Zena/
├── app.py                    # Main Shiny for Python app (UI + server)
├── src/
│   ├── __init__.py
│   ├── api_client.py         # MyHealthfinder API integration
│   ├── data_processing.py    # Rule-based filtering, categorization, priority
│   └── ai_insights.py        # Ollama LLM: summaries, cultural context, quiz
├── docs/
│   ├── ABOUT.md
│   ├── LAB_your_good_api_query.md
│   ├── LAB_cursor_shiny_app.md
│   └── LAB_ai_reporter.md
├── requirements.txt
├── .env                      # OLLAMA_API_KEY, OLLAMA_MODEL (not committed)
└── README.md
```

## Architecture Decisions

### 1. Static skeleton with `ui.panel_conditional`

The dashboard layout (checklist, summary, quiz) lives in `app_ui` as static HTML,
toggled by `ui.panel_conditional("input.generate > 0", ...)`. This avoids wrapping
the entire results page in a single `@render.ui`, which would wipe interactive
state (row selections, quiz answers) on every reactive invalidation.

### 2. Isolated render outputs

Each section is its own output so reactive dependencies don't cross-contaminate:

| Output               | Type              | Reactive dependency              |
|----------------------|-------------------|----------------------------------|
| `results_header`     | `render.ui`       | `processed_df()`                 |
| `checklist_table`    | `render.data_frame` | `processed_df()`               |
| `readiness_score`    | `render.text`     | `checklist_table.cell_selection()`, `processed_df()` |
| `summary_content`    | `render.ui`       | `ai_summary_text()`, `ai_cultural_text()` |
| `quiz_statement_ui`  | `render.ui`       | `current_quiz`                   |
| `quiz_feedback`      | `render.ui`       | `user_answer`, `current_quiz`    |

### 3. Toggle-select via JS injection

Shiny's DataTable `selection_mode="rows"` requires Cmd/Ctrl+click for multi-select.
A small `<script>` overrides `metaKey` on click events in the capture phase so every
click toggles, making the table behave like a checklist.

### 4. Priority-shaded rows

A `MutationObserver` stamps `data-priority` on each `<tr>` from the Priority column.
CSS rules apply different pink shades on selected rows:
- **High** → `#f8bbd0` (dark pink)
- **Routine** → `#fce4ec` (medium pink)
- **Informational** → `#fef0f5` (light pink)

## Required Components

| Requirement            | Implementation                                                     |
|------------------------|--------------------------------------------------------------------|
| API Integration        | MyHealthfinder API via `src/api_client.py` — age-filtered recs     |
| Data Processing        | `src/data_processing.py` — categorization, priority, vaccine filtering |
| AI-Powered Insights    | `src/ai_insights.py` — Ollama summaries, cultural context          |
| Clean UI               | `ui.page_fluid` + `ui.layout_sidebar`, pink theme, responsive CSS  |
| Reactive Interactivity | Readiness score updates live on row selection; quiz with reactive state |
| Data Table             | `render.DataTable` with `selection_mode="rows"` (toggle-select)    |
| Download               | CSV export of checklist via `render.download`                      |

## Running Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
shiny run --reload app.py
```
