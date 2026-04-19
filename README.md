<div align="center">

# 🚀 APEX Lite

**The Next-Generation AI-Powered Project Management Suite**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Transform your project ideation into professional-grade artifacts in minutes with APEX Lite.*

---

📖 **[Read our Research Paper Here]([(https://zenodo.org/records/19649211)])** 📖

</div>

## 🌟 Overview

**APEX Lite** is a cutting-edge, professional-grade SaaS application designed to revolutionize project management and business analysis workflows. Built on top of extremely capable Large Language Models (LLMs), APEX Lite acts as your intelligent project management co-pilot. 

Whether you are following traditional Waterfall or modern Agile methodologies, APEX Lite dynamically generates comprehensive documentation, structural breakdowns, risk analysis, and cost estimations based on your project description. 

## ✨ Key Features

- **🧠 Intelligent Prompt Strategy Selector:** Dynamically switch between prompt engineering strategies like **Role Prompting** and **Structured Prompting** to tailor the AI's output to your exact needs.
- **🏗️ Comprehensive Engines:**
  - 📝 **BRD Engine:** Automatically generates detailed Business Requirement Documents.
  - 📊 **WBS Engine:** Drafts Work Breakdown Structures visualized dynamically.
  - ⚠️ **Risk Engine:** Identifies potential project risks and formulates mitigation strategies.
  - 💰 **Cost Engine:** Provides structural cost estimations and budget breakdowns.
  - 🏃 **Agile Engine:** Transforms requirements into robust Agile artifacts (Epics, User Stories, Sprints).
- **📈 Interactive Visualizations:** Built-in interactive Gantt charts and structured data tables using `Plotly` and `Pandas` for a clear, bird's-eye view of your project lifecycle.
- **📄 Professional Export:** Export your generated insights directly into crisp, professionally formatted `.docx` reports utilizing our advanced DOCX writer module.
- **🎨 Modern UI/UX:** A sleek, premium dashboard built with Streamlit designed for an intuitive, portfolio-ready user experience.

---

## 🛠️ Technology Stack

| Component | Technology |
| --- | --- |
| **Frontend UI** | [Streamlit](https://streamlit.io/) |
| **Language** | Python 3 |
| **Data processing** | Pandas |
| **Visualizations** | Plotly |
| **Export Generator**| python-docx |
| **AI Integration** | `ollama` / Gemini (via dotenv) |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/apex-lite.git
   cd apex-lite
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Configuration:**
   Create a `.env` file in the root directory and add any necessary API keys or configurations.
   ```bash
   touch .env
   # Add your environment variables (e.g., GEMINI_API_KEY) inside .env
   ```

### Running the App

Start the Streamlit application by running the following command:

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your web browser to access the dashboard.

---

## 📸 Screenshots

*(Replace the placeholders below with actual screenshots of your application)*

| Dashboard Overview | Engine Selection |
| :---: | :---: |
| <img src="https://via.placeholder.com/600x350.png?text=Dashboard+Screenshot" alt="Dashboard" /> | <img src="https://via.placeholder.com/600x350.png?text=Engine+Selection" alt="Engines" /> |

| Gantt Visualization | Exported Report |
| :---: | :---: |
| <img src="https://via.placeholder.com/600x350.png?text=Gantt+Chart+Screenshot" alt="Charts" /> | <img src="https://via.placeholder.com/600x350.png?text=Docx+Export+Screenshot" alt="Export" /> |

---

## 📦 Project Structure

```text
apex-lite/
├── app.py                 # Main Streamlit application entry point
├── requirements.txt       # Project dependencies
├── utils.py               # Core utility functions and visualizers
├── docx_writer.py         # Module for generating structural .docx exports
├── ba_engine.py           # Business Analyst (BRD) Logic
├── pm_engine.py           # Project Manager (WBS) Logic
├── risk_engine.py         # Risk Assessment Logic
├── cost_engine.py         # Cost Estimation Logic 
├── agile_engine.py        # Agile Scrum artifact generation
├── prompts/               # Directory containing system prompt templates
└── ...
```

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## ✉️ Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/apex-lite](https://github.com/yourusername/apex-lite)

---
<div align="center">
  <i>Built with ❤️ for modern project managers.</i>
</div>
