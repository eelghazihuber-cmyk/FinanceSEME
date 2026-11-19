import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import LiquidityChart from "../components/LiquidityChart.jsx";
import { euro } from "../lib/format.js";

export default function Forecast() {
  const [months, setMonths] = useState(6);
  const [buffer, setBuffer] = useState(500);
  const [points, setPoints] = useState([]);
  const [shortfalls, setShortfalls] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.getForecast(months), api.getShortfalls(buffer, months)])
      .then(([p, s]) => {
        setPoints(p);
        setShortfalls(s);
        setError(null);
      })
      .catch((e) => setError(e.message));
  }, [months, buffer]);

  return (
    <>
      <h1>Prognose</h1>
      {error && <p className="error">{error}</p>}
      <section className="card">
        <div className="inline">
          <label>
            Monate voraus{" "}
            <select value={months} onChange={(e) => setMonths(Number(e.target.value))}>
              {[3, 6, 12].map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </label>
          <label>
            Mindestpuffer in €{" "}
            <input type="number" step="50" min="0" value={buffer} onChange={(e) => setBuffer(Number(e.target.value))} />
          </label>
        </div>
        <LiquidityChart points={points} buffer={buffer} />
        {shortfalls.length > 0 ? (
          <p className="error">
            Achtung: Am {new Date(shortfalls[0].day).toLocaleDateString("de-AT")} fällt der Kontostand voraussichtlich auf{" "}
            {euro(shortfalls[0].balance)}, also unter den Puffer von {euro(buffer)}.
          </p>
        ) : (
          <p className="muted">Kein Engpass unter {euro(buffer)} in den nächsten {months} Monaten erwartet.</p>
        )}
        <p className="muted small">Machbarkeitsstudie: Fixkosten, Budgets und Szenarien kommen in Phase 5 dazu.</p>
      </section>
    </>
  );
}
