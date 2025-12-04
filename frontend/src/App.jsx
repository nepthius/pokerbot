import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import EquityQuiz from "./components/EquityQuiz";
import PreflopTrainer from "./components/PreflopTrainer";

export default function App() {
  const nav = { display: "flex", gap: 16, padding: 12, background: "#eee" };
  const link = { textDecoration: "none", color: "#333", fontWeight: "bold" };
  return (
    <Router>
      <nav style={nav}>
        <Link to="/equity" style={link}>Equity</Link>
        <Link to="/preflop" style={link}>Preflop Trainer</Link>
      </nav>
      <div style={{ padding: 20 }}>
        <Routes>
          <Route path="/" element={<EquityQuiz />} />
          <Route path="/equity" element={<EquityQuiz />} />
          <Route path="/preflop" element={<PreflopTrainer />} />
        </Routes>
      </div>
    </Router>
  );
}
