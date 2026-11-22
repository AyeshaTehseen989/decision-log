import { useState } from "react";

export default function DecisionForm({ onSubmit, submitLabel }) {
  const [title, setTitle] = useState("");
  const [context, setContext] = useState("");
  const [decision, setDecision] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      await onSubmit({ title, context, decision });
      setTitle("");
      setContext("");
      setDecision("");
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
      />
      <textarea
        value={context}
        onChange={(e) => setContext(e.target.value)}
        placeholder="Context: why did this come up?"
        rows={3}
      />
      <textarea
        value={decision}
        onChange={(e) => setDecision(e.target.value)}
        placeholder="Decision: what did we decide?"
        rows={3}
      />
      <button type="submit">{submitLabel}</button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}