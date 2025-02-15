import openai  # Or deepseek/gemini API
import random
import json
import pulp  # Optimization library for advanced scheduling
import sqlite3  # Database support
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API key from environment variable or config
API_KEY = "your-api-key-here"

# Database setup
def init_db():
    conn = sqlite3.connect("schedule.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, user TEXT, data TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Function to call AI model
def generate_schedule(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Change to your preferred model
        messages=[{"role": "system", "content": "You are an expert schedule maker."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

# Advanced Scheduling Algorithm using Constraint Optimization
def create_optimized_schedule(tasks, max_hours=8):
    prob = pulp.LpProblem("OptimalSchedule", pulp.LpMaximize)
    task_vars = {task["name"]: pulp.LpVariable(task["name"], cat='Binary') for task in tasks}
    
    # Objective Function: Maximize priority tasks being scheduled
    prob += pulp.lpSum(task["priority"] * task_vars[task["name"]] for task in tasks), "Maximize_Priority"
    
    # Constraint: Total working hours should not exceed max_hours
    prob += pulp.lpSum(task["duration"] * task_vars[task["name"]] for task in tasks) <= max_hours, "Time_Limit"
    
    prob.solve()
    
    schedule = []
    time_slot = 8  # Start at 8 AM
    for task in tasks:
        if pulp.value(task_vars[task["name"]]) == 1:
            schedule.append({"task": task["name"], "time": f"{time_slot}:00"})
            time_slot += task["duration"]
    
    return schedule

# API Endpoint to generate schedules
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    tasks = data.get("tasks", [])
    if not tasks:
        return jsonify({"error": "No tasks provided"}), 400
    schedule = create_optimized_schedule(tasks)
    return jsonify({"schedule": schedule})

# Save and Retrieve Schedules
@app.route("/save_schedule", methods=["POST"])
def save_schedule():
    data = request.json
    user = data.get("user", "guest")
    schedule = json.dumps(data.get("schedule", {}))
    conn = sqlite3.connect("schedule.db")
    c = conn.cursor()
    c.execute("INSERT INTO schedules (user, data) VALUES (?, ?)", (user, schedule))
    conn.commit()
    conn.close()
    return jsonify({"message": "Schedule saved successfully"})

@app.route("/get_schedule", methods=["GET"])
def get_schedule():
    user = request.args.get("user", "guest")
    conn = sqlite3.connect("schedule.db")
    c = conn.cursor()
    c.execute("SELECT data FROM schedules WHERE user=?", (user,))
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({"schedule": json.loads(result[0])})
    return jsonify({"error": "No schedule found"}), 404

# School Timetable Generator (Balanced distribution of subjects)
@app.route("/timetable", methods=["POST"])
def generate_timetable():
    data = request.json
    subjects = data.get("subjects", [])
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    timetable = {day: [] for day in days}
    subject_counts = {subject: 0 for subject in subjects}
    
    for day in days:
        daily_subjects = random.sample(subjects, min(len(subjects), 5))
        for subject in daily_subjects:
            subject_counts[subject] += 1
            timetable[day].append(subject)
    
    return jsonify({"timetable": timetable})

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task  # Import the models

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    task = Task(name=data["name"], priority=data["priority"], duration=data["duration"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

if __name__ == "__main__":
    app.run(debug=True)


