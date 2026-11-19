import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import TransactionTable from "../components/TransactionTable.jsx";
import { euro, isoDate } from "../lib/format.js";

const emptyTx = () => ({ kind: "out", amount: "", booking_date: isoDate(new Date()), description: "", category_id: "" });

export default function Transactions() {
  const [accounts, setAccounts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [error, setError] = useState(null);
  const [account, setAccount] = useState({ name: "", opening_balance: "" });
  const [tx, setTx] = useState(emptyTx());
  const [accountId, setAccountId] = useState("");
  const [newCategory, setNewCategory] = useState("");

  const load = () =>
    Promise.all([api.getAccounts(), api.getCategories(), api.getTransactions()])
      .then(([a, c, t]) => {
        setAccounts(a);
        setCategories(c);
        setTransactions(t);
        setAccountId((current) => current || (a[0] ? String(a[0].id) : ""));
      })
      .catch((e) => setError(e.message));

  useEffect(() => {
    load();
  }, []);

  const run = (promise) =>
    promise.then(() => {
      setError(null);
      return load();
    }).catch((e) => setError(e.message));

  function addAccount(e) {
    e.preventDefault();
    run(api.createAccount({ name: account.name, opening_balance: account.opening_balance || "0" })).then(() =>
      setAccount({ name: "", opening_balance: "" })
    );
  }

  function addTransaction(e) {
    e.preventDefault();
    const amount = Math.abs(Number(tx.amount)) * (tx.kind === "out" ? -1 : 1);
    run(
      api.createTransaction({
        account_id: Number(accountId),
        category_id: tx.category_id ? Number(tx.category_id) : null,
        booking_date: tx.booking_date,
        amount: amount.toFixed(2),
        description: tx.description,
      })
    ).then(() => setTx(emptyTx()));
  }

  function addCategory() {
    if (newCategory.trim()) run(api.createCategory({ name: newCategory.trim() })).then(() => setNewCategory(""));
  }

  return (
    <>
      <h1>Buchungen</h1>
      {error && <p className="error">{error}</p>}

      <section className="card">
        <h2>Konten</h2>
        {accounts.length > 0 && (
          <ul className="plain">
            {accounts.map((a) => (
              <li key={a.id}>
                {a.name} <span className="muted">· Startsaldo {euro(a.opening_balance)}</span>
              </li>
            ))}
          </ul>
        )}
        <form className="inline" onSubmit={addAccount}>
          <input placeholder="Name, z. B. Girokonto" required value={account.name} onChange={(e) => setAccount({ ...account, name: e.target.value })} />
          <input type="number" step="0.01" placeholder="Startsaldo in €" value={account.opening_balance} onChange={(e) => setAccount({ ...account, opening_balance: e.target.value })} />
          <button type="submit">Konto anlegen</button>
        </form>
      </section>

      {accounts.length > 0 && (
        <section className="card">
          <h2>Neue Buchung</h2>
          <form className="inline" onSubmit={addTransaction}>
            <select value={tx.kind} onChange={(e) => setTx({ ...tx, kind: e.target.value })}>
              <option value="out">Ausgabe</option>
              <option value="in">Einnahme</option>
            </select>
            <input type="number" step="0.01" min="0.01" placeholder="Betrag in €" required value={tx.amount} onChange={(e) => setTx({ ...tx, amount: e.target.value })} />
            <input type="date" required value={tx.booking_date} onChange={(e) => setTx({ ...tx, booking_date: e.target.value })} />
            <input placeholder="Beschreibung" value={tx.description} onChange={(e) => setTx({ ...tx, description: e.target.value })} />
            <select value={tx.category_id} onChange={(e) => setTx({ ...tx, category_id: e.target.value })}>
              <option value="">Ohne Kategorie</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
            <select value={accountId} onChange={(e) => setAccountId(e.target.value)}>
              {accounts.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))}
            </select>
            <button type="submit">Speichern</button>
          </form>
          <div className="inline small-gap">
            <input placeholder="Neue Kategorie" value={newCategory} onChange={(e) => setNewCategory(e.target.value)} />
            <button type="button" className="secondary" onClick={addCategory}>
              Kategorie anlegen
            </button>
          </div>
        </section>
      )}

      <section className="card">
        <h2>Alle Buchungen</h2>
        <TransactionTable
          transactions={transactions}
          accounts={accounts}
          categories={categories}
          onDelete={(id) => run(api.deleteTransaction(id))}
        />
      </section>
    </>
  );
}
