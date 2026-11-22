const BASE = "http://127.0.0.1:8000";

async function request(path, options) {
  const response = await fetch(BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    if (Array.isArray(body.detail)) {
      throw new Error("Please fill in every field.");
    }
    throw new Error(body.detail || "Request failed");
  }
  return response.json();
}

export const listDecisions = () => request("/decisions");

export const createDecision = (data) =>
  request("/decisions", { method: "POST", body: JSON.stringify(data) });

export const updateStatus = (id, status) =>
  request(`/decisions/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });

export const supersedeDecision = (id, data) =>
  request(`/decisions/${id}/supersede`, {
    method: "POST",
    body: JSON.stringify(data),
  });