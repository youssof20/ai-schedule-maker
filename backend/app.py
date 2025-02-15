import openai  # Or deepseek/gemini API
import json
import pulp  # Optimization library
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task  # Import models

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Initialize Database
@app.before_first_request
def create_tables():
    db.create_all()

# AI API Key
API_KEY = "your-api-key-here"

# Function to call AI model
def generate_schedule_with_ai(prompt):
    if not API_KEY:
        return {"error": "Missing API key"}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an expert schedule maker."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return {"error": str(e)}

# Optimized Scheduling Algorithm
def create_optimized_schedule(tasks, max_hours=8):
    prob = pulp.LpProblem("OptimalSchedule", pulp.LpMaximize)
    task_vars = {task["name"]: pulp.LpVariable(task["name"], cat='Binary') for task in tasks}

    # Maximize priority
    prob += pulp.lpSum(task["priority"] * task_vars[task["name"]] for task in tasks), "Maximize_Priority"

    # Total working hours constraint
    prob += pulp.lpSum(task["duration"] * task_vars[task["name"]] for task in tasks) <= max_hours, "Time_Limit"

    prob.solve()

    schedule = []
    time_slot = 8  # Start at 8 AM
    for task in tasks:
        if pulp.value(task_vars[task["name"]]) == 1:
            schedule.append({"task": task["name"], "time": f"{time_slot}:00"})
            time_slot += task["duration"]

    return schedule

# API: Generate Schedule
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    tasks = data.get("tasks", [])
    if not tasks:
        return jsonify({"error": "No tasks provided"}), 400

    schedule = create_optimized_schedule(tasks)
    return jsonify({"schedule": schedule})

# API: Save Schedule
@app.route("/save_schedule", methods=["POST"])
def save_schedule():
    data = request.json
    user = data.get("user", "guest")
    schedule = json.dumps(data.get("schedule", {}))

    new_schedule = Schedule(user=user, data=schedule)
    db.session.add(new_schedule)
    db.session.commit()

    return jsonify({"message": "Schedule saved successfully"})

# API: Retrieve Schedule
@app.route("/get_schedule", methods=["GET"])
def get_schedule():
    user = request.args.get("user", "guest")
    schedule = Schedule.query.filter_by(user=user).first()

    if schedule:
        return jsonify({"schedule": json.loads(schedule.data)})
    return jsonify({"error": "No schedule found"}), 404

# API: Add Task
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    task = Task(name=data["name"], priority=data["priority"], duration=data["duration"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

# API: Get All Tasks
@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

if __name__ == "__main__":
    app.run(debug=True)
