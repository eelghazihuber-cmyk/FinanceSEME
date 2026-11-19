import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { euro, monthName } from "../lib/format.js";

// Einnahmen vs. Ausgaben pro Monat.
// Props: data = [{ month, income, expenses }]
export default function IncomeExpenseChart({ data }) {
  const rows = data.map((d) => ({ month: d.month, Einnahmen: Number(d.income), Ausgaben: Number(d.expenses) }));
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={rows} margin={{ top: 8, right: 16, bottom: 0, left: 8 }}>
        <CartesianGrid stroke="#e7e7e2" vertical={false} />
        <XAxis dataKey="month" tickFormatter={monthName} />
        <YAxis tickFormatter={(v) => euro(v).replace(",00", "")} width={90} />
        <Tooltip formatter={(v) => euro(v)} labelFormatter={monthName} />
        <Legend />
        <Bar dataKey="Einnahmen" fill="#1d7350" radius={[4, 4, 0, 0]} />
        <Bar dataKey="Ausgaben" fill="#a7b0aa" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
