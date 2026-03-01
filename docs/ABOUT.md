# ForHer

**Healthcare in the U.S. explained without the confusion.**

ForHer is an interactive Shiny web application designed to help first-generation and international female students better understand preventive healthcare in the United States. Many students come from countries where healthcare systems operate differently, which can make U.S. recommendations confusing or overwhelming. Our app simplifies this process by translating official preventive health guidelines into clear, culturally understandable information.

Users enter basic information such as their age and country background. The app then retrieves relevant preventive care recommendations from the MyHealthfinder API and presents them in an easy-to-digest format. Instead of overwhelming users with dense medical language, ForHer organizes the information into interactive flip cards, "Myth vs. Fact" sections, and personalized checklists.

Our goal is to reduce healthcare confusion, increase health literacy, and empower young women to make informed decisions about screenings, vaccinations, and routine care. ForHer acts as a bridge between official U.S. health recommendations and students who may not be familiar with the system.

## Tech Stack

- Python 3.10+
- Shiny for Python
- pandas, matplotlib
- Ollama Cloud or local Ollama (optional, for AI summaries)
