"""
ForHer - Women's Health for First-Gen / International Students
Healthcare in the U.S. explained without the confusion.
Python Shiny App: API + AI Insights + Visualizations
"""

from shiny import App, Inputs, Outputs, Session, reactive, render, ui
import pandas as pd
import matplotlib.pyplot as plt

from src.api_client import fetch_myhealthfinder, fetch_itemlist
from src.ai_insights import generate_ai_insights


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Your Profile"),
        ui.input_numeric("age", "Age", 25, min=18, max=100),
        ui.input_select("sex", "Sex", {"female": "Female", "male": "Male"}, selected="female"),
        ui.input_select("pregnant", "Pregnant?", {"no": "No", "yes": "Yes"}, selected="no"),
        ui.input_select("sexually_active", "Sexually Active?", {"yes": "Yes", "no": "No"}, selected="yes"),
        ui.input_select("tobacco_use", "Tobacco Use?", {"no": "No", "yes": "Yes"}, selected="no"),
        ui.input_select(
            "country_bg",
            "Country Background",
            {"International": "International", "U.S. First-Gen": "U.S. First-Gen", "Other": "Other"},
            selected="International",
        ),
        ui.input_action_button("fetch", "Get Recommendations"),
    ),
    ui.layout_column_wrap(
        ui.panel_title("ForHer - Women's Health for First-Gen / International Students"),
        ui.markdown("Healthcare in the U.S. explained without the confusion."),
    ),
    ui.row(
        ui.column(4, ui.value_box("Recommendations", ui.output_text("vb_recs"), theme="bg-gradient-indigo-purple")),
        ui.column(4, ui.value_box("Health Topics", ui.output_text("vb_topics"), theme="primary")),
        ui.column(4, ui.value_box("Categories", ui.output_text("vb_cats"), theme="success")),
    ),
    ui.card(
        ui.card_header("AI-Powered Summary"),
        ui.output_text("ai_summary"),
    ),
    ui.row(
        ui.column(6, ui.card(ui.card_header("Recommendations by Category"), ui.output_plot("plot_category"))),
        ui.column(6, ui.card(ui.card_header("Recommendation Types"), ui.output_plot("plot_type"))),
    ),
    ui.card(
        ui.card_header("Your Preventive Care Checklist"),
        ui.output_table("recs_table"),
    ),
    ui.card(
        ui.card_header("Summary"),
        ui.output_text("reactive_summary"),
    ),
    ui.card(
        ui.card_header("Browse Health Topics"),
        ui.output_table("topics_table"),
    ),
)


def server(input: Inputs, output: Outputs, session: Session) -> None:
    @reactive.calc
    @reactive.event(input.fetch)
    def recs_df() -> pd.DataFrame | None:
        data = fetch_myhealthfinder(
            age=int(input.age()),
            sex=input.sex(),
            pregnant=input.pregnant(),
            sexually_active=input.sexually_active(),
            tobacco_use=input.tobacco_use(),
        )
        if not data or "Result" not in data:
            return None
        result = data["Result"]
        recs = (
            result.get("Recommendations")
            or result.get("Topics")
            or result.get("Items", {}).get("Item")
            or result.get("Item")
        )
        if recs is None:
            return None
        if isinstance(recs, dict):
            recs = [recs]
        df = pd.DataFrame(recs)
        return df

    @reactive.calc
    def topics_items():
        data = fetch_itemlist("topic")
        if not data or "Result" not in data:
            return None
        items = data["Result"].get("Items", {}).get("Item")
        if items is None:
            return None
        if isinstance(items, dict):
            items = [items]
        return pd.DataFrame(items)

    @reactive.calc
    def cats_items():
        data = fetch_itemlist("category")
        if not data or "Result" not in data:
            return None
        items = data["Result"].get("Items", {}).get("Item")
        if items is None:
            return None
        if isinstance(items, dict):
            items = [items]
        return pd.DataFrame(items)

    # Value boxes
    @render.text
    def vb_recs() -> str:
        df = recs_df()
        return str(len(df)) if df is not None else "0"

    @render.text
    def vb_topics() -> str:
        df = topics_items()
        return str(len(df)) if df is not None else "0"

    @render.text
    def vb_cats() -> str:
        df = cats_items()
        return str(len(df)) if df is not None else "0"

    # AI summary
    @render.text
    def ai_summary() -> str:
        df = recs_df()
        if df is None or df.empty:
            return "Click 'Get Recommendations' to fetch your personalized health data, then AI will generate insights."
        title_col = next((c for c in df.columns if "title" in c.lower()), df.columns[0])
        desc_col = next((c for c in df.columns if "desc" in c.lower() or "myhf" in c.lower()), None)
        parts: list[str] = []
        for _, row in df.head(5).iterrows():
            t = row.get(title_col, "")
            d = row.get(desc_col, "") if desc_col else ""
            parts.append(f"- {t}: {d}")
        summary_text = "\n".join(parts)
        ctx = f"Age {input.age()}, {input.sex()}, {input.country_bg()} background"
        return generate_ai_insights(summary_text, ctx)

    # Plots
    @render.plot
    def plot_category():
        df = recs_df()
        if df is None or df.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "Fetch data to see chart", ha="center", va="center")
            ax.axis("off")
            return fig
        cat_col = next((c for c in df.columns if "category" in c.lower() or "type" in c.lower()), None)
        if cat_col is None:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No category column in data", ha="center", va="center")
            ax.axis("off")
            return fig
        counts = df[cat_col].value_counts()
        fig, ax = plt.subplots()
        counts.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Count")
        ax.set_ylabel("Category")
        ax.set_title("Recommendations by Category")
        plt.tight_layout()
        return fig

    @render.plot
    def plot_type():
        df = recs_df()
        if df is None or df.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "Fetch data to see chart", ha="center", va="center")
            ax.axis("off")
            return fig
        type_col = next((c for c in df.columns if "type" in c.lower() or "title" in c.lower()), df.columns[0])
        counts = df[type_col].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
        ax.set_title("Recommendation Types")
        return fig

    # Tables
    @render.table
    def recs_table():
        df = recs_df()
        if df is None or df.empty:
            return pd.DataFrame()
        cols = [c for c in ["Title", "Category", "Type"] if c in df.columns]
        if not cols:
            cols = list(df.columns)[:3]
        return df[cols]

    @render.table
    def topics_table():
        df = topics_items()
        if df is None or df.empty:
            return pd.DataFrame()
        return df

    # Reactive text summary
    @render.text
    def reactive_summary() -> str:
        df = recs_df()
        if df is None or df.empty:
            return (
                f"Hi! You're a {input.age()}-year-old {input.sex()} with {input.country_bg()} background. "
                "Click 'Get Recommendations' to see your personalized U.S. preventive care guidance."
            )
        return (
            f"Based on your profile (age {input.age()}, {input.sex()}, {input.country_bg()}), the U.S. MyHealthfinder API "
            f"recommends {len(df)} preventive care items. These are evidence-based guidelines from the U.S. Department "
            "of Health and Human Services."
        )


app = App(app_ui, server)

