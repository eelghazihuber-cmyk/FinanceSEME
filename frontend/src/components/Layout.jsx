import { NavLink, Outlet } from "react-router-dom";
import { useSession } from "../auth.jsx";
import { supabase } from "../lib/supabase.js";

const links = [
  { to: "/", label: "Übersicht" },
  { to: "/buchungen", label: "Buchungen" },
  { to: "/prognose", label: "Prognose" },
  { to: "/budgets", label: "Budgets" },
  { to: "/sparziele", label: "Sparziele" },
];

export default function Layout() {
  const session = useSession();
  return (
    <div className="app">
      <header className="topbar">
        <span className="brand">FinanceSEME</span>
        <nav>
          {links.map((link) => (
            <NavLink key={link.to} to={link.to} end={link.to === "/"}>
              {link.label}
            </NavLink>
          ))}
        </nav>
        <div className="user">
          <span className="muted">{session?.user?.email}</span>
          <button className="link" onClick={() => supabase.auth.signOut()}>
            Abmelden
          </button>
        </div>
      </header>
      <main className="page">
        <Outlet />
      </main>
    </div>
  );
}
