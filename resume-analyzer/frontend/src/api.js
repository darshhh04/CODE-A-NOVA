const API_BASE = `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/api`;

async function handleResponse(response) {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${response.status})`);
  }
  return response.json();
}

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
  return handleResponse(response);
}

export async function getFeedback(resumeText, jdText) {
  const response = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_text: resumeText, jd_text: jdText }),
  });
  return handleResponse(response);
}