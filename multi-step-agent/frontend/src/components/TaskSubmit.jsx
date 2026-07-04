import React, { useState } from "react";

export default function TaskSubmit({ onTaskCreated }) {
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!goal.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal: goal.trim() }),
      });
      if (!res.ok) throw new Error("Failed to create task");
      const data = await res.json();
      onTaskCreated(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "8px", padding: "20px", marginBottom: "16px" }}>
      <h2 style={{ margin: "0 0 14px", fontSize: "14px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", color: "#999" }}>
        Research Goal
      </h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="e.g. AI trends in healthcare 2026"
          rows={4}
          disabled={loading}
          style={{
            width: "100%",
            background: "#111",
            color: "#e8e8e8",
            border: "1px solid #333",
            borderRadius: "6px",
            padding: "10px",
            fontSize: "14px",
            resize: "vertical",
            boxSizing: "border-box",
            outline: "none",
          }}
        />
        {error && (
          <p style={{ margin: "8px 0", fontSize: "13px", color: "#f87171" }}>{error}</p>
        )}
        <button
          type="submit"
          disabled={loading || !goal.trim()}
          style={{
            marginTop: "10px",
            width: "100%",
            padding: "10px",
            background: loading ? "#333" : "#3b82f6",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            fontSize: "14px",
            fontWeight: 500,
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Starting..." : "Run Pipeline"}
        </button>
      </form>
    </div>
  );
}
