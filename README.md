# ⚡ ForgeMyMind — The AI Routine Coach

> **"Discipline is forged, not found."**  
> _ForgeMyMind_ is an AI-powered daily routine and motivation coach that helps you stay consistent, track your habits, and push your mental limits — with a touch of tough love 💪.

🎯 **Live Demo:** [Try it on Streamlit →](https://mindforgeai-mqwvhuz9ha9oitafnd7o62.streamlit.app/)

![Banner](assets/banner.png)

---

## 🚀 Features

- 🧩 **Smart Task Parsing** — Just type your daily tasks like `Read ML notes - 2h` or `Workout (30m)`  
- ⏰ **Auto Timetable Generator** — AI calculates your schedule between wake-up and sleep time  
- 💬 **Mood Coach Mode** — Choose “Nice”, “Mild”, or “Brutal” insult intensity  
- 🧠 **Motivational Engine** — Daily quotes + real-time motivational feedback  
- 📊 **Progress Tracker** — Calculates your completion percentage  
- 🔥 **Tough Love System** — If you fail tasks, AI gives you reality checks (customizable intensity)  
- 📁 **Persistent History** — Keeps a JSON record of your progress across days  

---

## 🧰 Tech Stack

| Component | Description |
|------------|--------------|
| 🧠 **AI Logic** | Rule-based task parsing + proportional time allocation |
| 💻 **Frontend** | [Streamlit](https://streamlit.io/) |
| 💾 **Storage** | Local JSON persistence |
| 🎨 **Design** | Minimal UI + motivational visuals |

---

## 🧩 Setup Guide

### 🖥️ Local Installation
```bash
git clone https://github.com/<your-username>/ForgeMyMind.git
cd ForgeMyMind
Then open 👉 http://localhost:8501

☁️ Streamlit Cloud

Push this repo to GitHub

Visit share.streamlit.io

Deploy your app from your repo (main branch)

Done 🎉

📅 Viva / Presentation Points

Concept: Behavioral nudging using AI — motivates or challenges users to finish tasks

Core Algorithm: Duration parsing, proportional scheduling, accountability feedback

Unique Twist: Combines psychology (motivation + insult logic) with AI task planning

Future Scope:

Voice input for tasks

GPT-based motivation quotes

Telegram/Discord bot integration

💬 Example Daily Flow

1️⃣ Enter your tasks
2️⃣ Generate your schedule
3️⃣ Complete tasks through the day
4️⃣ Click Save Progress to track results
5️⃣ Get rewarded — or roasted 🔥

🧠 Sample Quotes

“Push your limits — your potential is bigger than your excuses.”
“Discipline is choosing between what you want now and what you want most.”
“Don’t stop when you’re tired. Stop when you’re done.”

🏗️ Folder Structure
ForgeMyMind/
│
├── ai_daily_routine_coach.py   # Main Streamlit app
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── assets/
│   ├── logo.png
│   └── banner.png
└── sample_log.json             # Example history

🧡 Author

Aryan Sandhu
🎓 Machine Learning Intern @ Zion Technology
💡 Passionate about AI, psychology, and productivity tools

⭐ Support the Project

If you like this project:

🌟 Star this repo

🔗 Share the app

💬 Give feedback or ideas for v2
pip install -r requirements.txt
streamlit run ai_daily_routine_coach.py
