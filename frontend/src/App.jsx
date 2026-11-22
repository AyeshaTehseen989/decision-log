import { useEffect, useState } from "react";
import {
  createDecision,
  listDecisions,
  supersedeDecision,
  updateStatus,
} from "./api";
import DecisionCard from "./DecisionCard";
import DecisionForm from "./DecisionForm";
import "./App.css";

export default function App() {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");

  async function refresh() {
    try {
      setDecisions(await listDecisions());
      setError("");
    } catch {
      setError("Could not load decisions. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let active = true;
    listDecisions()
      .then((data) => {
        if (active) {
          setDecisions(data);
          setError("");
        }
      })
      .catch(() => {
        if (active) {
          setError("Could not load decisions. Is the backend running?");
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  async function handleCreate(data) {
    await createDecision(data);
    await refresh();
  }

  async function handleStatusChange(id, status) {
    try {
      await updateStatus(id, status);
      setActionError("");
      await refresh();
    } catch (err) {
      setActionError(err.message);
    }
  }

  async function handleSupersede(id, data) {
    await supersedeDecision(id, data);
    setActionError("");
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
      {actionError && <p className="error">{actionError}</p>}
      {loading && <p>Loading...</p>}
      {!loading && !error && decisions.length === 0 && (
        <p>No decisions yet.</p>
      )}
      <ul className="list">
        {decisions.map((d) => (
          <DecisionCard
            key={d.id}
            decision={d}
            onStatusChange={handleStatusChange}
            onSupersede={handleSupersede}
          />
        ))}
      </ul>
    </main>
  );
}