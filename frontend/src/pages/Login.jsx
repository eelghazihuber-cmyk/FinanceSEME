import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useSession } from "../auth.jsx";
import { supabase, supabaseConfigured } from "../lib/supabase.js";

export default function Login() {
  const session = useSession();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState(null);
  const [busy, setBusy] = useState(false);

  if (session) return <Navigate to="/" replace />;

  if (!supabaseConfigured) {
    return (
      <div className="login">
        <h1>FinanceSEME</h1>
        <p className="error">
          Supabase ist nicht eingerichtet. Trage VITE_SUPABASE_URL und VITE_SUPABASE_KEY in frontend/.env ein
          (online: in den Vercel-Einstellungen).
        </p>
      </div>
    );
  }

  async function submit(mode) {
    setBusy(true);
    setMessage(null);
    const { data, error } =
      mode === "login"
        ? await supabase.auth.signInWithPassword({ email, password })
        : await supabase.auth.signUp({ email, password, options: { emailRedirectTo: window.location.origin } });
    setBusy(false);
    if (error) setMessage({ type: "error", text: error.message });
    else if (mode === "signup" && !data.session)
      setMessage({ type: "info", text: "Fast geschafft: Bitte bestätige deine E-Mail-Adresse über den Link in der Mail." });
  }

  return (
    <div className="login">
      <h1>FinanceSEME</h1>
      <p className="muted">Anmelden oder neues Konto anlegen</p>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          submit("login");
        }}
      >
        <label>
          E-Mail
          <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Passwort
          <input type="password" required minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <div className="row">
          <button type="submit" disabled={busy}>
            Anmelden
          </button>
          <button type="button" className="secondary" disabled={busy || !email || password.length < 6} onClick={() => submit("signup")}>
            Registrieren
          </button>
        </div>
      </form>
      {message && <p className={message.type}>{message.text}</p>}
    </div>
  );
}
