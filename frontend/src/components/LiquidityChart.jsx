import { CartesianGrid, Legend, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { euro, shortDate } from "../lib/format.js";

// Liquiditätsverlauf: durchgezogen = echter Stand, gestrichelt = Prognose.
// Props: points = [{ day, balance, is_forecast }], buffer = Mindestpuffer (optional)
export default function LiquidityChart({ points, buffer }) {
  const lastReal = points.filter((p) => !p.is_forecast).at(-1);
  const data = points.map((p) => ({
    day: p.day,
    ist: p.is_forecast ? null : Number(p.balance),
    // Die Prognose startet beim letzten echten Punkt, damit die Linien verbunden sind
    prognose: p.is_forecast || p === lastReal ? Number(p.balance) : null,
  }));

  if (!points.length) return <p className="muted">Noch keine Daten.</p>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 8 }}>
        <CartesianGrid stroke="#e7e7e2" vertical={false} />
        <XAxis dataKey="day" tickFormatter={shortDate} minTickGap={24} />
        <YAxis tickFormatter={(v) => euro(v).replace(",00", "")} width={90} />
        <Tooltip formatter={(v) => euro(v)} labelFormatter={shortDate} />
        <Legend />
        {buffer > 0 && <ReferenceLine y={buffer} stroke="#c9492e" strokeDasharray="4 4" label="Puffer" />}
        <Line type="stepAfter" dataKey="ist" name="Kontostand" stroke="#1d7350" strokeWidth={2} dot={false} />
        <Line type="linear" dataKey="prognose" name="Prognose" stroke="#1d7350" strokeWidth={2} strokeDasharray="6 5" dot />
      </LineChart>
    </ResponsiveContainer>
  );
}
