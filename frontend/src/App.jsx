import { useEffect, useState } from "react";
import { createDecision, listDecisions } from "./api";
import DecisionForm from "./DecisionForm";
import "./App.css";

export default function App() {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      setDecisions(await listDecisions());
      setError("");
    } catch (err) {
      setError("Could not load decisions. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleCreate(data) {
    await createDecision(data);
    await refresh();
  }

  return (
    <main className="container">
      <h1>Decision Log</h1>
      <p className="subtitle">A written record of what we decided and why.</p>

      <h2>Record a decision</h2>
      <DecisionForm onSubmit={handleCreate} submitLabel="Save decision" />

      <h2>Decisions</h2>
      {error && <p className="error">{error}</p>}
      {loading && <p>Loading...</p>}
      {!loading && !error && decisions.length === 0 && (
        <p>No decisions yet.</p>
      )}
      <ul className="list">
        {decisions.map((d) => (
          <li key={d.id} className="card">
            <div className="card-header">
              <strong>
                #{d.id} {d.title}
              </strong>
              <span className={`badge ${d.status}`}>{d.status}</span>
            </div>
            <p>
              <em>Context:</em> {d.context}
            </p>
            <p>
              <em>Decision:</em> {d.decision}
            </p>
          </li>
        ))}
      </ul>
    </main>
  );
}