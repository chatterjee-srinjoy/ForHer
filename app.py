"""
ForHer 💗 - Preventive Healthcare for First-Gen & International Female Students
Pink theme, interactive checklist, Myth vs Fact quiz.
"""

from dotenv import load_dotenv

load_dotenv()

from shiny import App, Inputs, Outputs, Session, reactive, render, ui
import pandas as pd
from io import StringIO
import random

from src.api_client import fetch_myhealthfinder
from src.data_processing import process_recommendations, get_clean_for_llm
from src.ai_insights import (
    cultural_context,
    personalized_summary,
    myth_vs_fact,
    MYTH_FACT_QUIZ,
)

# Pink theme CSS - responsive
PINK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
:root {
  --primary-pink: #F48FB1;
  --light-bg: #FFF0F5;
  --accent-rose: #EC407A;
  --text: #444;
  --white: #ffffff;
}
* { box-sizing: border-box; }
body { font-family: 'Poppins', sans-serif !important; background: var(--light-bg) !important; color: var(--text) !important; margin: 0; }
.bslib-page-fill { background: var(--light-bg) !important; min-height: 100vh; }
.main-content { max-width: min(1000px, 95vw); margin: 0 auto; padding: clamp(16px, 3vw, 24px); }
.forher-header {
  background: linear-gradient(135deg, var(--primary-pink), var(--accent-rose));
  color: white;
  padding: clamp(24px, 4vw, 32px);
  border-radius: 0;
  text-align: center;
  margin-bottom: 0;
  box-shadow: 0 4px 20px rgba(244, 143, 177, 0.3);
  width: 100%;
}
/* Horizontal filter dropdowns for DataTable */
[data-data-grid-filters] { display: flex !important; flex-wrap: wrap !important; gap: 8px !important; flex-direction: row !important; }
[data-data-grid-filters] input, [data-data-grid-filters] select { min-width: 100px !important; }
.forher-card {
  background: var(--white);
  border-radius: 16px;
  padding: clamp(16px, 3vw, 20px);
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: box-shadow 0.2s;
}
.forher-card:hover { box-shadow: 0 4px 20px rgba(244, 143, 177, 0.2); }
.badge-high { background: var(--accent-rose); color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; }
.badge-routine { background: var(--primary-pink); color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; }
.badge-info { background: #e0e0e0; color: #555; padding: 4px 10px; border-radius: 20px; font-size: 12px; }
.disclaimer {
  font-size: 12px; color: #888;
  padding: 12px; background: #fafafa;
  border-radius: 8px; margin-bottom: 20px;
  border-left: 4px solid var(--accent-rose);
}
.score-circle {
  width: clamp(60px, 12vw, 80px); height: clamp(60px, 12vw, 80px);
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-pink), var(--accent-rose));
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: clamp(18px, 4vw, 24px); font-weight: 700;
  margin: 0 auto 8px;
}
.welcome-section {
  text-align: center;
  padding: clamp(40px, 8vw, 80px) 24px;
}
.welcome-section h1 { color: var(--accent-rose); font-size: clamp(24px, 5vw, 32px); }
.welcome-section p { color: #666; font-size: clamp(14px, 2.5vw, 16px); max-width: 600px; margin: 16px auto; line-height: 1.6; }
.quiz-card {
  background: linear-gradient(135deg, #fff5f8, #ffe4ec);
  border: 2px solid var(--primary-pink);
  border-radius: 16px;
  padding: 24px;
  margin: 16px 0;
}
.quiz-statement { font-size: 18px; font-weight: 500; margin-bottom: 16px; }
.quiz-buttons { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
.quiz-result { font-weight: 600; margin-top: 12px; padding: 8px; border-radius: 8px; }
.quiz-correct { background: #c8e6c9; color: #2e7d32; }
.quiz-wrong { background: #ffcdd2; color: #c62828; }
@media (max-width: 768px) {
  .main-content { padding: 12px; }
  .quiz-buttons { flex-direction: column; }
}
</style>
"""

COUNTRIES = [
    "United States", "India", "China", "Mexico", "South Korea", "Vietnam",
    "Nigeria", "Brazil", "Canada", "Philippines", "Colombia", "Pakistan",
    "Bangladesh", "Egypt", "Ethiopia", "Iran", "Germany", "Turkey",
    "Indonesia", "Thailand", "Kenya",
]

app_ui = ui.page_fluid(
    ui.HTML(PINK_CSS),
    # Title full width at top
    ui.div(
        ui.div(
            ui.h2("💗 ForHer 💗", style="margin:0; font-size:clamp(24px, 5vw, 32px);"),
            ui.p("Healthcare in the U.S. explained without the confusion.", style="margin:8px 0 0; opacity:0.95;"),
            class_="forher-header",
        ),
        style="width:100%; padding:0 16px;",
    ),
    ui.div(
        ui.div(
            "This tool provides educational guidance based on U.S. preventive care recommendations. It is not medical advice.",
            class_="disclaimer",
        ),
        class_="main-content",
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Your Profile", style="color: var(--accent-rose);"),
            ui.input_numeric("age", "Age", 25, min=16, max=60),
            ui.input_select(
                "country",
                "Country Background",
                {c: c for c in COUNTRIES},
                selected="United States",
            ),
            ui.h5("Vaccination Status", style="margin-top:16px; color:#555;"),
            ui.input_checkbox_group(
                "vaccines",
                "Completed",
                choices=["HPV", "Tdap", "Flu", "MMR"],
                selected=[],
            ),
            ui.input_checkbox("unsure", "Unsure about some vaccines", False),
            ui.input_radio_buttons(
                "insurance",
                "Insurance Status",
                {"yes": "Yes", "no": "No"},
                selected="yes",
            ),
            ui.input_action_button(
                "generate",
                "Generate My Preventive Plan",
                class_="btn-primary",
                style="background: var(--accent-rose); border-color: var(--accent-rose); margin-top:16px; width:100%;",
            ),
            width=280,
        ),
        ui.div(
            ui.output_ui("main_output"),
            class_="main-content",
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session) -> None:
    @reactive.calc
    @reactive.event(input.generate)
    def processed_df() -> pd.DataFrame | None:
        data = fetch_myhealthfinder(
            age=int(input.age()),
            sex="female",
            pregnant="no",
            sexually_active="yes",
            tobacco_use="no",
        )
        if not data or "Result" not in data:
            return None
        result = data["Result"]
        recs = result.get("Resources", {}).get("All", {}).get("Resource")
        if not recs:
            return None
        if isinstance(recs, dict):
            recs = [recs]
        completed = list(input.vaccines()) if input.vaccines() else []
        unsure_list = ["unsure"] if input.unsure() else []
        return process_recommendations(recs, completed, unsure_list)

    @reactive.calc
    def ai_summary_text() -> str:
        df = processed_df()
        if df is None or df.empty:
            return ""
        clean = get_clean_for_llm(df, 5)
        vax = list(input.vaccines()) if input.vaccines() else []
        return personalized_summary(clean, vax, int(input.age()))

    @reactive.calc
    def ai_cultural() -> str:
        return cultural_context()

    @reactive.calc
    def ai_mythfact() -> str:
        return myth_vs_fact()

    # Quiz state - store current question (statement, is_fact)
    current_quiz = reactive.Value(("", False))
    last_answered = reactive.Value(None)  # Clear when Next clicked so feedback resets

    @reactive.Effect
    @reactive.event(processed_df)
    def _set_quiz():
        df = processed_df()
        if df is not None and not df.empty:
            current_quiz.set(random.choice(MYTH_FACT_QUIZ))

    @reactive.Effect
    @reactive.event(input.quiz_next)
    def _next_quiz():
        last_answered.set(None)
        current_quiz.set(random.choice(MYTH_FACT_QUIZ))

    @reactive.Effect
    @reactive.event(input.quiz_myth, input.quiz_fact)
    def _on_answer():
        last_answered.set(current_quiz())


    @render.ui
    def main_output():
        if input.generate() == 0:
            return ui.div(
                ui.div(
                    ui.h1("💗 Welcome to ForHer 💗", style="margin-bottom:12px;"),
                    ui.p(
                        "We're here to help you understand preventive healthcare in the United States—without the confusion.",
                        style="font-size:18px;",
                    ),
                    ui.h3("About ForHer", style="margin-top:32px; color: var(--accent-rose);"),
                    ui.p(
                        "ForHer is designed for first-generation and international female students who may come from "
                        "countries where healthcare works differently. In the U.S., preventive care—like screenings, "
                        "vaccinations, and annual checkups—is encouraged even when you feel healthy.",
                    ),
                    ui.p(
                        "Enter your profile on the left, then click **Generate My Preventive Plan** to get your "
                        "personalized checklist, AI summary, and a fun Myth vs Fact quiz!",
                    ),
                    class_="welcome-section",
                ),
            )
        df = processed_df()
        if df is None or df.empty:
            return ui.div(
                ui.p("Could not load recommendations. Please try again.", style="text-align:center; padding:48px; color:#666;"),
            )

        total = len(df)
        # Build checklist choices: (value, label) - index for uniqueness
        checklist_choices = {
            str(i): f"{row['title']} ({row['category']})"
            for i, (_, row) in enumerate(df.iterrows())
        }

        # 1. Checklist with score (score updates as user checks)
        header = ui.div(
            ui.h3(f"Hi! Based on your age ({input.age()}) and inputs, here are your preventive priorities."),
            class_="forher-card",
        )
        checklist_section = ui.div(
            ui.div(
                ui.h4("💗 Your Preventive Checklist"),
                ui.div(
                    ui.div(ui.output_text("readiness_score"), class_="score-circle"),
                    ui.span("Preventive Readiness Score (check off items as you complete them)", style="font-size:14px; color:#666;"),
                    style="text-align:center; margin:0 0 16px 0;",
                ),
                ui.input_checkbox_group(
                    "checklist_items",
                    "Check off completed items:",
                    choices=checklist_choices,
                    selected=[],
                ),
                ui.output_data_frame("checklist_table"),
                ui.download_button("download_btn", "📥 Download Checklist", style="margin-top:12px;"),
            ),
            class_="forher-card",
        )

        # 3. Personalized summary
        try:
            summary_text = ai_summary_text()
        except Exception:
            summary_text = f"Based on your age ({input.age()}), focus on cervical cancer screening, blood pressure checks, and annual well-woman visits. Talk to your doctor about what's right for you."
        if not summary_text or not str(summary_text).strip():
            summary_text = f"Based on your age ({input.age()}), prioritize routine screenings and preventive visits. These help catch issues early."
        try:
            cultural_text = ai_cultural()
        except Exception:
            cultural_text = "In the U.S., preventive care is encouraged even when you feel healthy. Regular checkups help catch issues early."
        if not cultural_text or not str(cultural_text).strip():
            cultural_text = "In the U.S., preventive care is encouraged even when you feel healthy."
        summary_section = ui.div(
            ui.h4("💗 Your Personalized Summary"),
            ui.p(str(summary_text)),
            ui.h5("Cultural Context"),
            ui.p(str(cultural_text)),
            class_="forher-card",
        )

        # 4. Myth vs Fact Quiz
        statement, is_fact = current_quiz()

        quiz_section = ui.div(
            ui.h4("💗 Myth vs Fact Quiz"),
            ui.p("Test your knowledge! Is this statement a Myth or a Fact?", style="font-size:14px; color:#666; margin-bottom:12px;"),
            ui.div(
                ui.div(statement, class_="quiz-statement") if statement else ui.p("Loading..."),
                ui.div(
                    ui.input_action_button("quiz_myth", "❌ Myth", style="background:#ffcdd2; border-color:#ef9a9a;"),
                    ui.input_action_button("quiz_fact", "✅ Fact", style="background:#c8e6c9; border-color:#a5d6a7;"),
                    ui.input_action_button("quiz_next", "➡️ Next Question", style="background:var(--primary-pink); border-color:var(--primary-pink);"),
                    class_="quiz-buttons",
                ),
                ui.output_ui("quiz_feedback"),
                class_="quiz-card",
            ),
            class_="forher-card",
        )

        return ui.TagList(
            header,
            checklist_section,
            summary_section,
            quiz_section,
        )

    @render.data_frame
    def checklist_table():
        if input.generate() == 0:
            return pd.DataFrame()
        df = processed_df()
        if df is None or df.empty:
            return pd.DataFrame()
        out = df[["title", "category", "priority", "status"]].copy()
        out.columns = ["Recommendation", "Category", "Priority", "Status"]
        return render.DataTable(out, height=300, filters=True, width="100%")

    @render.ui
    def quiz_feedback():
        # Only show feedback for the question they just answered (not after Next)
        if last_answered() != current_quiz():
            return ui.div()
        if input.quiz_myth() == 0 and input.quiz_fact() == 0:
            return ui.div()
        _, is_fact = current_quiz()
        picked_fact = input.quiz_fact() > input.quiz_myth()
        correct = picked_fact == is_fact
        msg = "Correct! 💗" if correct else "Not quite. It's a " + ("Fact" if is_fact else "Myth") + "."
        cls = "quiz-result quiz-correct" if correct else "quiz-result quiz-wrong"
        return ui.div(msg, class_=cls)

    @render.download(filename="forher_checklist.csv")
    def download_btn():
        if input.generate() == 0:
            yield "Recommendation,Category,Priority,Status\nNo data yet. Click Generate first.\n"
            return
        df = processed_df()
        if df is None or df.empty:
            yield "Recommendation,Category,Priority,Status\nNo data\n"
            return
        out = StringIO()
        df[["title", "category", "priority", "status"]].to_csv(
            out, index=False, header=["Recommendation", "Category", "Priority", "Status"]
        )
        yield out.getvalue()


app = App(app_ui, server)
