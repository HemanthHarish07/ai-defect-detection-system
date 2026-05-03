import axios from "axios";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api";

export async function uploadImage(file) {
  const form = new FormData();
  form.append("file", file);
  const response = await axios.post(`${backendUrl}/upload`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function fetchHistory() {
  const response = await axios.get(`${backendUrl}/history`);
  return response.data;
}

export async function fetchStats() {
  const response = await axios.get(`${backendUrl}/stats`);
  return response.data;
}
