import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import IncomeExpenseChart from "../components/IncomeExpenseChart.jsx";
import LiquidityChart from "../components/LiquidityChart.jsx";
import { euro, isoDate } from "../lib/format.js";

export default function Dashboard() {
  const [state, setState] = useState({ loading: true });

  useEffect(() => {
    const now = new Date();
    const from = isoDate(new Date(now.getFullYear(), now.getMonth() - 5, 1));
    Promise.all([api.getAccounts(), api.getMonthlySummary(from, isoDate(now)), api.getForecast(6)])
      .then(([accounts, monthly, forecast]) => setState({ accounts, monthly, forecast }))
      .catch((e) => setState({ error: e.message }));
  }, []);

  if (state.loading) return <p className="muted">Lädt …</p>;
  if (state.error) return <p className="error">{state.error}</p>;
  if (!state.accounts.length)
    return (
      <div className="card">
        <h1>Willkommen</h1>
        <p>
          Lege zuerst unter <Link to="/buchungen">Buchungen</Link> ein Konto an.
        </p>
      </div>
    );

  const today = state.forecast.filter((p) => !p.is_forecast).at(-1);
  const in6 = state.forecast.at(-1);
  const thisMonth = state.monthly.at(-1);

  return (
    <>
      <h1>Übersicht</h1>
      <div className="kpis">
        <Kpi label="Kontostand heute" value={euro(today.balance)} />
        <Kpi label="Einnahmen diesen Monat" value={euro(thisMonth.income)} />
        <Kpi label="Ausgaben diesen Monat" value={euro(thisMonth.expenses)} />
        <Kpi label="Prognose in 6 Monaten" value={euro(in6.balance)} />
      </div>
      <section className="card">
        <h2>Liquiditätsverlauf</h2>
        <LiquidityChart points={state.forecast} />
        <p className="muted small">Prognose: Durchschnitt der letzten 3 Monate fortgeschrieben.</p>
      </section>
      <section className="card">
        <h2>Einnahmen und Ausgaben</h2>
        <IncomeExpenseChart data={state.monthly} />
      </section>
    </>
  );
}

function Kpi({ label, value }) {
  return (
    <div className="kpi">
      <span className="muted small">{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
