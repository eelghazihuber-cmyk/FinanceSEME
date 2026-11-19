import { createClient } from "@supabase/supabase-js";

// Werte aus frontend/.env (lokal) bzw. aus den Vercel-Einstellungen (online)
const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_KEY;

export const supabaseConfigured = Boolean(url && key);
export const supabase = supabaseConfigured ? createClient(url, key) : null;
