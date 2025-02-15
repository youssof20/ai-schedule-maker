import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const ScheduleApp = () => {
  const [tasks, setTasks] = useState([]);
  const [taskName, setTaskName] = useState("");
  const [priority, setPriority] = useState(1);
  const [duration, setDuration] = useState(1);
  const [schedule, setSchedule] = useState([]);

  const addTask = () => {
    setTasks([...tasks, { name: taskName, priority: parseInt(priority), duration: parseInt(duration) }]);
    setTaskName("");
    setPriority(1);
    setDuration(1);
  };

  const generateSchedule = async () => {
    const response = await axios.post("http://localhost:5000/generate", { tasks });
    setSchedule(response.data.schedule);
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">AI Schedule Maker</h1>
      <div className="mb-4">
        <Input value={taskName} onChange={(e) => setTaskName(e.target.value)} placeholder="Task Name" className="mb-2" />
        <Input type="number" value={priority} onChange={(e) => setPriority(e.target.value)} placeholder="Priority (1-10)" className="mb-2" />
        <Input type="number" value={duration} onChange={(e) => setDuration(e.target.value)} placeholder="Duration (hrs)" className="mb-2" />
        <Button onClick={addTask} className="mr-2">Add Task</Button>
        <Button onClick={generateSchedule}>Generate Schedule</Button>
      </div>
      <div className="mt-4">
        {schedule.length > 0 && (
          <Card>
            <CardContent>
              <h2 className="text-xl font-semibold mb-2">Generated Schedule</h2>
              <ul>
                {schedule.map((item, index) => (
                  <li key={index} className="mb-1">{item.time} - {item.task}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ScheduleApp;
