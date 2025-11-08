
# ai_daily_routine_coach.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import json
import random
import os
import re
from dateutil import parser as dateparser

DATA_FILE = "routine_state.json"

def load_state():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)

def parse_task_line(line, default_hours=1.0):
    m = re.search(r"(\d+(\.\d+)?)(h|hr|hrs|hours)", line, re.IGNORECASE)
    if m:
        hours = float(m.group(1))
        name = line[:m.start()].strip(" -:()")
        return name if name else "Task", hours
    m2 = re.search(r"(\d+)\s*m(in)?", line, re.IGNORECASE)
    if m2:
        mins = int(m2.group(1))
        return line[:m2.start()].strip(" -:()") or "Task", mins/60.0
    if "-" in line:
        parts = line.split("-",1)
        name = parts[0].strip()
        try:
            hours = float(parts[1].strip().replace("h",""))
            return name, hours
        except:
            return line.strip(), default_hours
    return line.strip(), default_hours

def build_schedule(tasks, wake_time, sleep_time):
    start_dt = datetime.combine(datetime.today(), wake_time)
    end_dt = datetime.combine(datetime.today(), sleep_time)
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    available_minutes = int((end_dt - start_dt).total_seconds() // 60)
    needed_minutes = int(sum([t["hours"]*60 for t in tasks]))
    scale = 1.0
    if needed_minutes > available_minutes:
        scale = available_minutes / max(1, needed_minutes)
    schedule = []
    cur = start_dt
    for t in tasks:
        minutes = int(t["hours"]*60*scale)
        if minutes <= 0:
            continue
        stime = cur
        etime = cur + timedelta(minutes=minutes)
        schedule.append({
            "name": t["name"],
            "start": stime.isoformat(),
            "end": etime.isoformat(),
            "minutes": minutes,
            "completed": False
        })
        cur = etime
        if cur >= end_dt:
            break
    return schedule

INSULTS = [
    "Honestly — that was weak. You promised more.",
    "You said you'd do it. Today's proof says otherwise. Lazy much?",
    "You're capable of better. This half-effort is embarrassing.",
    "That's it? You call that commitment?",
]
KIND_INSULTS = [
    "You missed it — try harder tomorrow.",
    "Not your best day. Dust off and push again.",
    "You didn't finish this time. Learn and rebound.",
]
MOTIVATIONS = [
    "Push your limits — your potential is bigger than your excuses.",
    "One more attempt. Small steps compound into big wins.",
    "You can do this. Discipline beats motivation — start now.",
    "Remember why you started. Let that fuel you.",
]
QUOTES = [
    "“Small daily improvements are the key to staggering long-term results.”",
    "“Discipline is choosing between what you want now and what you want most.”",
    "“Don’t stop when you’re tired. Stop when you’re done.”",
    "“Strive for progress, not perfection.”",
]

def choose_daily_quote(seed=None):
    random.seed(seed or datetime.today().toordinal())
    return random.choice(QUOTES)

st.set_page_config(page_title="AI Daily Routine Coach", layout="wide")
st.title("MindForgeAI — Your AI Daily Routine Coach")

state = load_state()
today_key = datetime.today().strftime("%Y-%m-%d")
if "history" not in state:
    state["history"] = {}

col1, col2 = st.columns([2,1])

with col1:
    st.header("Enter today's tasks (one per line). Add '- 1.5h' or '(30m)' to set duration)")
    default_tasks = state.get("draft_tasks", "Read ML notes - 2h\nPractice coding - 1.5h\nGym - 1h\nMeditation - 0.25h")
    tasks_text = st.text_area("Tasks", value=default_tasks, height=160)
    st.markdown("**Available time**")
    wake = st.time_input("Wake up at", value=time(7,0))
    sleep = st.time_input("Sleep at", value=time(23,0))
    st.markdown("---")
    st.subheader("Completion criteria")
    st.number_input("Minimum % of scheduled minutes to be completed to consider day SUCCESS", min_value=1, max_value=100, value=70, step=5, key="criteria_percent")
    st.checkbox("Save tasks as default next time", key="save_default")

    if st.button("Generate Timetable"):
        lines = [l.strip() for l in tasks_text.splitlines() if l.strip()]
        parsed = []
        for ln in lines:
            name, hours = parse_task_line(ln, default_hours=1.0)
            parsed.append({"name":name, "hours":hours})
        schedule = build_schedule(parsed, wake, sleep)
        state["today"] = {
            "date": today_key,
            "schedule": schedule,
            "criteria_percent": st.session_state.criteria_percent
        }
        if st.session_state.get("save_default"):
            state["draft_tasks"] = tasks_text
        save_state(state)
        st.success("Timetable generated — scroll down to view and track it.")

with col2:
    st.header("Preferences & Tone")
    insult_mode = st.selectbox("Insult intensity", options=["Off (Nice)","Mild", "Brutal"], index=1)
    safety_toggle = st.checkbox("Safer Language (don’t use harsh insults)", value=True)
    seed_for_quote = st.number_input("Quote seed (optional)", value=0)
    daily_quote = choose_daily_quote(seed=seed_for_quote if seed_for_quote!=0 else None)
    st.markdown("**Today's quote:**")
    st.info(daily_quote)

st.markdown("---")
st.header("Today's Timetable")
today_block = state.get("today", {})
if not today_block or today_block.get("date") != today_key:
    st.info("No timetable for today yet — generate one from the left.")
else:
    schedule = today_block["schedule"]
    if not schedule:
        st.warning("No scheduled tasks fit in the available time.")
    else:
        df = pd.DataFrame([{
            "Task": s["name"],
            "Start": s["start"].replace("T"," "),
            "End": s["end"].replace("T"," "),
            "Minutes": s["minutes"],
            "Completed": s.get("completed", False)
        } for s in schedule])
        st.dataframe(df[["Task","Start","End","Minutes","Completed"]])

        st.subheader("Mark tasks as completed (check and click Save Progress):")
        comps = []
        for i, s in enumerate(schedule):
            key = f"chk_{i}_{today_key}"
            completed = st.checkbox(f"{s['name']}  ({s['minutes']} min)", value=s.get("completed", False), key=key)
            comps.append(completed)
        if st.button("Save Progress / Evaluate"):
            for i, c in enumerate(comps):
                schedule[i]["completed"] = bool(c)
            state["today"]["schedule"] = schedule
            total_minutes = sum([s["minutes"] for s in schedule])
            done_minutes = sum([s["minutes"] for s in schedule if s["completed"]])
            percent = (done_minutes / total_minutes * 100) if total_minutes>0 else 0
            criteria = state["today"].get("criteria_percent", 70)
            st.write(f"Completed: {done_minutes} / {total_minutes} minutes — {percent:.1f}% (Threshold: {criteria}%)")
            if percent >= criteria:
                st.success("You hit your goal today — great job! Keep the momentum.")
                st.balloons()
                st.info(random.choice(MOTIVATIONS))
            else:
                use_brutal = (insult_mode == "Brutal") and (not safety_toggle)
                if use_brutal:
                    line = random.choice(INSULTS)
                else:
                    line = random.choice(KIND_INSULTS)
                st.error(line)
                st.warning(random.choice(MOTIVATIONS))
            state["history"].setdefault(today_key, {})
            state["history"][today_key]["total_minutes"] = total_minutes
            state["history"][today_key]["done_minutes"] = done_minutes
            state["history"][today_key]["percent"] = percent
            save_state(state)

st.markdown("---")
st.header("Manual Controls & Extra Tools")
st.write("Re-run the daily evaluation or reset today's schedule.")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Reset today's progress"):
        if "today" in state:
            for s in state["today"]["schedule"]:
                s["completed"] = False
            save_state(state)
            st.success("Progress reset.")
with c2:
    if st.button("Force 'Motivate me' now"):
        st.info(random.choice(MOTIVATIONS))
with c3:
    if st.button("Force 'Insult' now"):
        if safety_toggle:
            st.warning(random.choice(KIND_INSULTS))
        else:
            st.error(random.choice(INSULTS))

st.markdown("---")
st.header("Viva talking points (for presentation)")
st.markdown("""
- **Project Name:** MindForgeAI — AI Daily Routine Coach  
- **Goal:** Generate a practical timetable from tasks, track completion, and provide accountability + motivation.  
- **Core Idea:** Behavioral nudging using AI — automatic scheduling + feedback loop (insult + motivation).  
- **Tech:** Streamlit frontend, JSON persistence, NLP-style duration parsing, proportional scheduling.  
- **Uniqueness:** Combines psychological nudging (customizable tone) with practical daily planning.
""")
st.caption("Demo tip: Toggle insult intensity to show live feedback dynamics.")
