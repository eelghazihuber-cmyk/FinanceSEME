import { Navigate, Route, Routes } from "react-router-dom";
import { RequireAuth } from "./auth.jsx";
import Layout from "./components/Layout.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Transactions from "./pages/Transactions.jsx";
import Budgets from "./pages/Budgets.jsx";
import Forecast from "./pages/Forecast.jsx";
import Goals from "./pages/Goals.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <RequireAuth>
            <Layout />
          </RequireAuth>
        }
      >
        <Route path="/" element={<Dashboard />} />
        <Route path="/buchungen" element={<Transactions />} />
        <Route path="/prognose" element={<Forecast />} />
        <Route path="/budgets" element={<Budgets />} />
        <Route path="/sparziele" element={<Goals />} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
