import { createContext, useContext, useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { supabase } from "./lib/supabase.js";

// undefined = wird noch geladen, null = nicht eingeloggt, sonst die Supabase-Session
const SessionContext = createContext(undefined);

export function SessionProvider({ children }) {
  const [session, setSession] = useState(undefined);

  useEffect(() => {
    if (!supabase) {
      setSession(null);
      return;
    }
    supabase.auth.getSession().then(({ data }) => setSession(data.session));
    const { data } = supabase.auth.onAuthStateChange((_event, s) => setSession(s));
    return () => data.subscription.unsubscribe();
  }, []);

  return <SessionContext.Provider value={session}>{children}</SessionContext.Provider>;
}

export const useSession = () => useContext(SessionContext);

// Seiten nur für eingeloggte Nutzer
export function RequireAuth({ children }) {
  const session = useSession();
  if (session === undefined) return <p className="muted page">Lädt …</p>;
  if (!session) return <Navigate to="/login" replace />;
  return children;
}
