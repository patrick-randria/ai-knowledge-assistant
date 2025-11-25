const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function uploadPdf(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/ingest/upload`, {
    method: "POST",
    body: form
  });
  return res.json();
}

export async function askQuestion(question) {
  const res = await fetch(`${API_BASE}/chat/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  // Parse the response as text since it is expected to be Markdown
  const markdown = await res.text();
  return markdown;
}

export async function listDocuments(limit = 10) {
  const res = await fetch(`${API_BASE}/ingest/documents?limit=${limit}`, {
    method: "GET",
  });
  return res.json();
}
