import { useState } from "react";
import axios from "axios";

export default function EquityQuiz() {
  const [hand, setHand] = useState("");
  const [board, setBoard] = useState("");
  const [opponents, setOpponents] = useState(1);
  const [equity, setEquity] = useState(null);
  const [loading, setLoading] = useState(false);
  async function getEquity() {
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5010/api/equity", {
        hand,
        board,
        opponents: parseInt(opponents, 10)
      });
      setEquity(res.data.equity);
    } catch (err) {
      console.error("Error fetching equity:", err);
    } finally {
      setLoading(false);
    }
  }

  {/* gonna add better styling later */}
  const containerStyle = {
    maxWidth: "420px",
    margin: "40px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "12px",
    backgroundColor: "#f8f8f8",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
    fontFamily: "Arial, sans-serif"
  };

  const labelStyle = { display: "block", marginBottom: "4px", fontWeight: "bold" };
  const inputStyle = {
    width: "100%",
    padding: "6px 8px",
    marginBottom: "12px",
    border: "1px solid #ccc",
    borderRadius: "6px",
    fontSize: "14px"
  };
  const buttonStyle = {
    width: "100%",
    backgroundColor: "#007bff",
    color: "#fff",
    padding: "10px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "15px"
  };
  return (
    <div style={containerStyle}>
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>Equity Quiz</h2>
      <label style={labelStyle}>Hole Cards (e.g. Ah Kh):</label>
      <input
        value={hand}
        onChange={(e) => setHand(e.target.value)}
        style={inputStyle}
        placeholder="Ah Kh"
      />


      <label style={labelStyle}>Board (optional, e.g. Qh Td 3c):</label>
      <input
        value={board}
        onChange={(e) => setBoard(e.target.value)}
        style={inputStyle}
        placeholder="Qh Jh 3c"
      />
      <label style={labelStyle}>Number of Opponents:</label>
      <input
        type="number"
        value={opponents}
        onChange={(e) => setOpponents(e.target.value)}
        style={inputStyle}
        min="1"
        max="6"
      />
      <button onClick={getEquity} disabled={loading} style={buttonStyle}>
        {loading ? "Calculating..." : "Run Simulation"}
      </button>

      {equity !== null && (
        <div style={{ marginTop: "20px", textAlign: "center", fontSize: "18px" }}>
          <strong>Equity:</strong> {equity.toFixed(2)}%
        </div>
      )}
    </div>
  );
}
