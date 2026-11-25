import { supabase } from "../lib/supabase.js";

// Lokal: http://localhost:8000, online: Adresse des Backends (VITE_API_URL)
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  // Token vom Supabase-Login holen und bei jeder Anfrage mitschicken
  const { data } = supabase ? await supabase.auth.getSession() : { data: {} };
  const token = data.session?.access_token;

  const response = await fetch(BASE_URL + path, {
    ...options,
    headers: {
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (response.status === 204) return null;
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body?.detail === "string" ? body.detail : `Fehler ${response.status}`;
    throw new Error(detail);
  }
  return body;
}

const query = (params) => {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "");
  return entries.length ? `?${new URLSearchParams(entries)}` : "";
};
const post = (path, data) => request(path, { method: "POST", body: JSON.stringify(data) });
const notYet = () => Promise.reject(new Error("Noch nicht implementiert"));

export const api = {
  me: () => request("/auth/me"),

  // Konten, Kategorien, Buchungen
  getAccounts: () => request("/accounts/"),
  createAccount: (data) => post("/accounts/", data),
  getCategories: () => request("/categories/"),
  createCategory: (data) => post("/categories/", data),
  getTransactions: (filters = {}) => request(`/transactions/${query(filters)}`),
  createTransaction: (data) => post("/transactions/", data),
  deleteTransaction: (id) => request(`/transactions/${id}`, { method: "DELETE" }),
  importCsv: notYet, // Phase 3

  // Budgets (Phase 4)
  getBudgetStatus: notYet,

  // Auswertung
  getMonthlySummary: (from, to) => request(`/reports/monthly${query({ date_from: from, date_to: to })}`),
  getByCategory: (from, to) => request(`/reports/by-category${query({ date_from: from, date_to: to })}`),
  getKpis: notYet, // Phase 4

  // Prognose
  getForecast: (monthsAhead = 6) => request(`/forecast/${query({ months_ahead: monthsAhead })}`),
  getShortfalls: (buffer, monthsAhead = 6) => request(`/forecast/shortfalls${query({ buffer, months_ahead: monthsAhead })}`),

  // KI-Analyse (Machbarkeitstest)
  getAiAnalyse: () => request("/ai/analyse"),

  // Planung (Phase 5)
  getRecurring: notYet,
  getGoals: notYet,
  getScenarios: notYet,
};

export default request;
