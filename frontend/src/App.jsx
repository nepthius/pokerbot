import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import EquityQuiz from "./components/EquityQuiz";
import PreflopTablePro from "./components/PreflopTable";
import PokerTerminology from "./components/PokerTerminology";
import HandStrengthVisualizer from "./components/HandStrengthVisualizer";


export default function App() {
  const nav = { display: "flex", gap: 16, padding: 12, background: "#0e1116" };
  const link = { textDecoration: "none", color: "#e6e6e6", fontWeight: 700 };

  return (
    <Router>
      <nav style={nav}>
        <Link to="/equity" style={link}>Equity</Link>
        <Link to="/preflop" style={link}>Preflop Trainer</Link>
        <Link to="/terms" style={link}>Terminology</Link>
        <Link to="/strength" style={link}>Hand Strength</Link>

      </nav>

      <Routes>
        <Route path="/" element={<PreflopTablePro />} />
        <Route path="/equity" element={<EquityQuiz />} />
        <Route path="/strength" element={<HandStrengthVisualizer />} />
        <Route path="/preflop" element={<PreflopTablePro />} />
        <Route path="/terms" element={<PokerTerminology />} />
      </Routes>
    </Router>
  );
}
