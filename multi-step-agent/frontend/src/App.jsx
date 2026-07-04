import React, { useState, useEffect, useRef } from "react";
import TaskSubmit from "./components/TaskSubmit";
import StepTrace from "./components/StepTrace";
import OutputPanel from "./components/OutputPanel";

const POLL_INTERVAL = 2000;

export default function App() {
  const [task, setTask] = useState(null);
  const pollRef = useRef(null);

  const stopPolling = () => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  };

  const startPolling = (taskId) => {
    stopPolling();
    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(`/tasks/${taskId}`);
        const data = await res.json();
        setTask(data);
        if (data.status === "complete" || data.status === "failed") {
          stopPolling();
        }
      } catch (_) {}
    }, POLL_INTERVAL);
  };

  const handleTaskCreated = (newTask) => {
    setTask(newTask);
    startPolling(newTask.id);
  };

  useEffect(() => () => stopPolling(), []);

  const isActive = task && (task.status === "queued" || task.status === "running");

  return (
    <div style={{ minHeight: "100vh", background: "#0f0f0f", color: "#e8e8e8", fontFamily: "system-ui, sans-serif" }}>
      <header style={{ borderBottom: "1px solid #222", padding: "16px 32px" }}>
        <h1 style={{ margin: 0, fontSize: "20px", fontWeight: 600, letterSpacing: "-0.3px" }}>
          Multi-Step Agent
        </h1>
        <p style={{ margin: "4px 0 0", fontSize: "13px", color: "#666" }}>
          Content research pipeline — plan, search, filter, summarise, outline, draft
        </p>
      </header>

      <div style={{ display: "flex", gap: "24px", padding: "32px", maxWidth: "1200px", margin: "0 auto" }}>
        <div style={{ width: "340px", flexShrink: 0 }}>
          <TaskSubmit onTaskCreated={handleTaskCreated} />
          {task && (
            <StepTrace stepLogs={task.step_logs || []} status={task.status} />
          )}
        </div>

        <div style={{ flex: 1 }}>
          {task && <OutputPanel output={task.output} status={task.status} isActive={isActive} />}
        </div>
      </div>
    </div>
  );
}
