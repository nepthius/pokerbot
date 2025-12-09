import React from "react";
export default function PokerTerminology() {
  const sectionStyle = {
    background: "linear-gradient(180deg,#0f1013,#1b1f25)",
    color: "#eee",
    padding: "30px",
    borderRadius: "16px",

    maxWidth: "800px",
    margin: "30px auto",
    boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
    fontFamily: "Inter, Arial, sans-serif"
  };
  const heading = { color: "#4bc06f", fontWeight: 800, letterSpacing: 0.4, fontSize: 26, marginBottom: 20 };
  const sub = { color: "#ccc", fontWeight: 600, fontSize: 18, marginTop: 24, marginBottom: 10 };
  const table = { width: "100%", borderCollapse: "collapse", color: "#ddd" };




  const th = { textAlign: "left", borderBottom: "1px solid rgba(255,255,255,0.1)", padding: "8px", color: "#4bc06f" };
  const td = { padding: "8px", borderBottom: "1px solid rgba(255,255,255,0.05)" };
  const note = { fontSize: 14, color: "#aaa", marginTop: 18, fontStyle: "italic" };

  return (
    <div style={sectionStyle}>
      <h1 style={heading}>Poker Terminology Reference</h1>
      <p style={{ fontSize: 15, lineHeight: 1.6, color: "#ccc" }}>
        A GUIDE I MADE BECAUSE I DON'T KNOW A LOT OF POKER
      </p>

      <h3 style={sub}> Table Positions and other stuff</h3>
      <table style={table}>
        <thead>
          <tr><th style={th}>Term</th><th style={th}>Meaning</th></tr>
        </thead>
        <tbody>
          <tr><td style={td}>UTG</td><td style={td}><b>Under The Gun</b> – first player to act preflop (immediately left of the Big Blind).</td></tr>

          <tr><td style={td}>UTG+1 / UTG+2</td><td style={td}>Players acting after UTG in early position.</td></tr>

          <tr><td style={td}>LJ</td><td style={td}><b>LoJack</b> – first middle-position player after early positions.</td></tr>

          <tr><td style={  td}>HJ</td><td style={td}><b>Hijack</b> – right of the Cutoff; often steals when others fold.</td></tr>
          <tr><td style={td}>CO</td><td style={td}><b>Cutoff</b> – second to act before the Button; great spot for opening wider.</td></tr>
          <tr><td style={td}>BTN</td><td style={td}><b>Button / Dealer</b> – acts last postflop; strongest position.</td></tr>

          <tr><td style={td}>SB</td><td style={td}><b>Small Blind</b> – posts half a blind, acts first postflop.</td></tr>
          <tr><td style={td}>BB</td><td style={td}><b>Big Blind</b> – posts a full blind, closes preflop action.</td></tr>
        </tbody>
      </table>

      <h3 style={sub}>Betting Actions</h3>
      <table style={table}>
        <thead>
          <tr><th style={th}>Term</th><th style={th}>Meaning</th></tr>
        </thead>
        <tbody>
          <tr><td style={td }>Open</td><td style={td}>First voluntary raise preflop.</td></tr>
          <tr><td style={td}>Call</td><td style={td}>Match another player's bet or raise.</td></tr>
          <tr><td style={td}>Raise / 3-bet / 4-bet</td><td style={td}>Re-raising; a "3-bet" is the 2nd raise in a hand, "4-bet" is the 3rd, and so on.</td></tr>
          <tr><td style={td}>Fold</td><td style={td}>Give up your hand and any chips in the pot.</td></tr>

          <tr><td style={td}>Check</td><td style={td}>Pass action without betting when no one has bet yet.</td></tr>
          <tr><td style={td}>C-Bet</td><td style={td}><b>Continuation Bet</b> – the preflop raiser bets again on the flop.</td></tr>
        </tbody>
      </table>

      <h3 style={sub}> Strategy & Math</h3>
      <table style={table}>
        <thead>
          <tr><th style={th}>Term</th><th style={th}>Meaning</th></tr>
        </thead>
        <tbody>
          <tr><td style={td} >Equity</td><td style={td}>Your hand’s chance to win the pot against opponents’ ranges.</td></tr>
          <tr><td style={td}>EV (Expected Value)</td><td style={td}>Long-term average profit or loss of a decision.</td></tr>



          <tr><td style={td}>Pot Odds</td><td style={td}>Ratio of current bet to total pot; used to decide profitable calls.</td></tr>
          <tr><td style={td}>Implied Odds</td><td style={td}>Potential future winnings compared to current call cost.</td></tr>
          <tr><td style={td}>GTO</td><td style={td}><b>Game Theory Optimal</b> – mathematically balanced strategy that cannot be exploited.</td></tr>
          <tr><td style={td}>Exploitative Play</td><td style={td}>Adjusting strategy to take advantage of opponents’ tendencies.</td></tr>
        </tbody>
      </table>

      <h3 style={sub}> Miscellaneous stuff</h3>
      <table style={table}>
        <thead>
          <tr><th style={th}>Term</th><th style={th}>Meaning</th></tr>
        </thead>
        <tbody>
          <tr><td style={td}>Hole Cards</td><td style={td}>The two private cards each player is dealt.</td></tr>
          <tr><td style={td}>Board</td><td style={td}>The five community cards shared by all players.</td></tr>
          <tr><td style={td}>Showdown</td><td style={td}>When players reveal hands after final betting round.</td></tr>
          <tr><td style={td}>Suited (s)</td><td style={td}>Two hole cards of the same suit (e.g., A♥K♥ = AKs).</td></tr>

          <tr>< td style={td}>Offsuit (o)</td><td style={td}>Two hole cards of different suits (e.g., A♥K♣ = AKo).</td></tr>
          <tr><td style={td}>Range</td><td style={td}>The set of hands a player could have in a given situation.</td></tr>
          <tr><td style={td}>Nuts</td><td style={td}>The strongest possible hand on a given board.</td></tr>
        </tbody>
      </table>

      <div style={note} >

        Tip: In your <b>Preflop Trainer</b>, these positions and terms determine the correct “Fold / Call / Raise” logic.
      </div>
    </div>
  );
}
