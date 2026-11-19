const money = new Intl.NumberFormat("de-AT", { style: "currency", currency: "EUR" });

export const euro = (value) => money.format(Number(value ?? 0));

// Datum als "2026-11-19" in lokaler Zeit (toISOString allein wäre UTC)
export const isoDate = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);

export const shortDate = (iso) => `${iso.slice(8, 10)}.${iso.slice(5, 7)}.`;

const MONTHS = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
export const monthName = (iso) => `${MONTHS[Number(iso.slice(5, 7)) - 1]} ${iso.slice(2, 4)}`;
