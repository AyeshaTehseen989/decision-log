import { useState } from "react";
import DecisionForm from "./DecisionForm";

export default function DecisionCard({ decision, onStatusChange, onSupersede }) {
  const [replacing, setReplacing] = useState(false);
  const isSuperseded = decision.status === "superseded";
  const nextStatus = decision.status === "proposed" ? "accepted" : "proposed";
  const statusLabel =
    decision.status === "proposed" ? "Accept" : "Move back to proposed";

  async function handleSupersede(data) {
    await onSupersede(decision.id, data);
    setReplacing(false);
  }

  return (
    <li className={`card ${isSuperseded ? "faded" : ""}`}>
      <div className="card-header">
        <strong>
          #{decision.id} {decision.title}
        </strong>
        <span className={`badge ${decision.status}`}>{decision.status}</span>
      </div>
      <p>
        <em>Context:</em> {decision.context}
      </p>
      <p>
        <em>Decision:</em> {decision.decision}
      </p>

      {isSuperseded && (
        <p className="note">Replaced by decision #{decision.superseded_by}</p>
      )}

      {!isSuperseded && (
        <div className="actions">
          <button onClick={() => onStatusChange(decision.id, nextStatus)}>
            {statusLabel}
          </button>
          <button onClick={() => setReplacing(!replacing)}>
            {replacing ? "Cancel" : "Supersede"}
          </button>
        </div>
      )}

      {replacing && (
        <div className="replace-box">
          <p>Write the new decision that replaces #{decision.id}:</p>
          <DecisionForm
            onSubmit={handleSupersede}
            submitLabel="Save replacement"
          />
        </div>
      )}
    </li>
  );
}