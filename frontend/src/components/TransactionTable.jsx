import { euro } from "../lib/format.js";

// Liste der Buchungen.
// Props: transactions, accounts, categories, onDelete
export default function TransactionTable({ transactions, accounts, categories, onDelete }) {
  const accountName = (id) => accounts.find((a) => a.id === id)?.name ?? "–";
  const categoryName = (id) => categories.find((c) => c.id === id)?.name ?? "–";

  if (!transactions.length) return <p className="muted">Noch keine Buchungen.</p>;

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Datum</th>
          <th>Beschreibung</th>
          <th>Kategorie</th>
          <th>Konto</th>
          <th className="num">Betrag</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((t) => (
          <tr key={t.id}>
            <td>{new Date(t.booking_date).toLocaleDateString("de-AT")}</td>
            <td>{t.description || "–"}</td>
            <td>{categoryName(t.category_id)}</td>
            <td>{accountName(t.account_id)}</td>
            <td className={`num ${Number(t.amount) < 0 ? "neg" : "pos"}`}>{euro(t.amount)}</td>
            <td className="num">
              <button className="link" onClick={() => onDelete(t.id)}>
                Löschen
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
