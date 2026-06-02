import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

export const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

export const ChatAPI = {
  getModels: () => api.get("/models").then((r) => r.data),
  listSessions: () => api.get("/sessions").then((r) => r.data),
  createSession: (payload) => api.post("/sessions", payload).then((r) => r.data),
  updateSession: (id, payload) => api.patch(`/sessions/${id}`, payload).then((r) => r.data),
  deleteSession: (id) => api.delete(`/sessions/${id}`).then((r) => r.data),
  listMessages: (id) => api.get(`/sessions/${id}/messages`).then((r) => r.data),
  sendMessage: (id, payload) => api.post(`/sessions/${id}/messages`, payload).then((r) => r.data),
};
