
import { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:5010"; //localhost gonna change up later
const SEATS = ["UTG","UTG+1","UTG+2","LJ","HJ","CO","BTN","SB","BB"];

export default function PreflopTablePro() {

  const [scenario, setScenario] = useState(null);
  const [result,   setResult]   = useState(null);
  const [mode,     setMode]     = useState("cash");
  const [loading,  setLoading]  = useState(false);
  const [dealStep, setDealStep] = useState(0);

  const timerRef = useRef(null);


  //some helpers
  const actionsByPos = useMemo(() => {
    const map = {};
    if (scenario?.actions) {
      for (const a of scenario.actions) {
        map[a.pos] = a.action;
      }
    }
    return map;
  }, [scenario]);
  function clearTimer() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }
  function startDeal() {
    clearTimer();
    setDealStep(0);
    timerRef.current = setInterval(() => {
      setDealStep((p) => (p >= 9 ? (clearTimer(), 9) : p + 1));
    }, 110);
  }
  async function newHand() {
    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(`${API}/api/trainer/new`, { mode });
      setScenario(res.data);
      startDeal();
    } catch (e) {
      console.error("newHand error", e);
      setScenario(null);
    } finally {
      setLoading(false);
    }
  }

  async function answer(action) {
    if (!scenario) return;

    try {
      const res = await axios.post(`${API}/api/trainer/answer`, {
        id: scenario.id,
        action
      });
      setResult(res.data);
    } catch (e) {
      console.error("answer error", e);
    }
  }

  useEffect(() => {
    return () => clearTimer();
  }, []);
  const W = 1100, H = 680;
  const tableW = 860, tableH = 420;
  const cx = W / 2, cy = H / 2 + 10;
  const ANG0 = -90;
  const seatAngles = useMemo(() => {
    const step = 360 / SEATS.length;
    const map = {};
    SEATS.forEach((p, i) => {
      map[p] = ANG0 + i * step;
    });
    return map;
  }, []);
  const seatXY = (pos) => {
    const a = (seatAngles[pos] * Math.PI) / 180;
    const rx = tableW / 2 - 80;
    const ry = tableH / 2 - 40;
    const x = cx + rx * Math.cos(a);
    const y = cy + ry * Math.sin(a) - 8;
    return [x, y];
  };
  const suitGlyph = { h: "♥", d: "♦", c: "♣", s: "♠" };
  const suitColor = { h: "#d33", d: "#c33", c: "#1f7a44", s: "#2a2a2a" };

  const faceText = (card) => {
    if (!card) return ["", ""];
    const r = card.slice(0, card.length - 1);
    const s = card.slice(-1);
    return [r, s];
  };

  //lots of styling
  const s = {
    stage: {
      width: W,
      height: H,
      margin: "18px auto",
      borderRadius: 18,
      background: "linear-gradient(180deg,#0f1012,#13151a)",
      boxShadow: "inset 0 50px 150px rgba(0,0,0,0.6)",
    },

    header: {
      display: "flex",
      gap: 12,
      padding: "14px 18px",
      alignItems: "center",
      color: "#e9e9e9",
    },

    select: {
      padding: "6px 10px",
      borderRadius: 8,
      border: "1px solid #333",
      background: "#1d2128",
      color: "#ddd",
    },
    btn: {
      padding: "10px 16px",
      borderRadius: 10,
      border: "none",
      cursor: "pointer",
      fontWeight: 700,
      boxShadow: "0 4px 16px rgba(0,0,0,0.25)",
    },
    btnPrimary: { background: "#2b7cff", color: "#fff" },
    btnNeutral: { background: "#2a2d33", color: "#ddd" },

    tableWrap: {
      position: "relative",
      width: "100%",
      height: H - 62,
    },

    felt: {
      position: "absolute",
      left: cx - tableW / 2,
      top: cy - tableH / 2,
      width: tableW,
      height: tableH,
      borderRadius: tableH,
      background:
        "radial-gradient(ellipse at 50% 45%, #1aa34a 0%, #12893e 55%, #0e6f31 100%)",
      border: "10px solid #6d4c2f",
      boxShadow:
        "inset 0 0 110px rgba(0,0,0,0.45), 0 18px 60px rgba(0,0,0,0.6)",
    },

    boardTray: {
      position: "absolute",
      left: cx - 260,
      top: cy - 40,
      width: 520,
      height: 80,
      borderRadius: 50,
      background: "linear-gradient(180deg,#0d5f2c,#0a4c23)",
      border: "1px solid rgba(255,255,255,0.08)",
      boxShadow: "inset 0 0 16px rgba(0,0,0,0.35)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: 10,
    },

    boardSlot: {
      width: 76,
      height: 108,
      borderRadius: 8,
      background: "rgba(255,255,255,0.08)",
      border: "1px solid rgba(255,255,255,0.15)",
      boxShadow: "inset 0 0 10px rgba(0,0,0,0.4)",
    },

    potChip: {
      position: "absolute",
      left: cx - 18,
      top: cy - 110,
      width: 36,
      height: 36,
      borderRadius: "50%",
      background: "radial-gradient(circle at 35% 35%,#ffdd66,#d7a90d)",
      border: "2px solid #815400",
      boxShadow: "0 2px 8px rgba(0,0,0,0.35)",
      color: "#2b2000",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontWeight: 800,
      fontSize: 12,
    },

    dealerBtn: (x, y) => ({
      position: "absolute",
      left: x - 14,
      top: y - 14,
      width: 28,
      height: 28,
      borderRadius: "50%",
      background: "#fff",
      color: "#111",
      border: "1px solid #aaa",
      boxShadow: "0 2px 6px rgba(0,0,0,0.35)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontWeight: 800,
      fontSize: 12,
    }),

    panel: (x, y, isHero, action) => ({
      position: "absolute",
      left: x - 110,
      top: y - 64,
      width: 220,
      height: 70,
      borderRadius: 12,
      background: "linear-gradient(180deg,#1b1f26,#14171c)",
      border: "1px solid rgba(255,255,255,0.08)",
      boxShadow:
        action === "3bet"
          ? "0 0 18px rgba(165,105,255,0.5)"
          : isHero
          ? "0 0 16px rgba(0,200,255,0.4)"
          : action === "open"
          ? "0 0 14px rgba(0,200,120,0.45)"
          : "0 4px 14px rgba(0,0,0,0.5)",
      color: "#e9e9e9",
      display: "flex",
      alignItems: "center",
      padding: "6px 10px",
      gap: 8,
      opacity: action === "fold" ? 0.45 : 1,
    }),

    posTag: {
      fontSize: 10,
      padding: "2px 6px",
      borderRadius: 999,
      background: "rgba(255,255,255,0.08)",
      border: "1px solid rgba(255,255,255,0.12)",
      marginLeft: 6,
    },

    cardBack: (faded) => ({
      width: 44,
      height: 60,
      borderRadius: 6,
      background:
        "repeating-linear-gradient(45deg,#193319,#193319 7px,#204020 7px,#204020 14px)",
      border: "1px solid rgba(0,0,0,0.6)",
      boxShadow:
        "inset 0 0 10px rgba(0,0,0,0.6), 0 2px 6px rgba(0,0,0,0.4)",
      opacity: faded ? 0.25 : 1,
    }),

    cardFace: {
      width: 44,
      height: 60,
      borderRadius: 6,
      background: "linear-gradient(180deg,#fff,#f4f4f4)",
      border: "1px solid #bbb",
      boxShadow: "0 2px 6px rgba(0,0,0,0.25)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      fontWeight: 800,
    },

    rank: (color) => ({
      position: "absolute",
      top: 6,
      left: 6,
      fontSize: 16,
      color,
    }),

    suit: (color) => ({
      position: "absolute",
      bottom: 6,
      right: 6,
      fontSize: 18,
      color,
    }),

    badge: (type) => ({
      marginLeft: "auto",
      padding: "4px 8px",
      borderRadius: 8,
      fontSize: 11,
      fontWeight: 800,
      letterSpacing: 0.5,
      color: "#fff",
      background:
        type === "open"
          ? "linear-gradient(180deg,#00b36b,#009e5e)"
          : type === "call"
          ? "linear-gradient(180deg,#4aa3ff,#2a7be8)"
          : type === "3bet"
          ? "linear-gradient(180deg,#a46bff,#7d49db)"
          : "linear-gradient(180deg,#888,#666)",
      border: "1px solid rgba(255,255,255,0.2)",
    }),

    hud: {
      marginTop: 6,
      textAlign: "center",
      color: "#dcdcdc",
      fontSize: 13,
    },

    actions: {
      marginTop: 10,
      display: "flex",
      gap: 12,
      justifyContent: "center",
    },

    verdict: (ok) => ({
      margin: "14px auto 0",
      width: 520,
      padding: "12px 14px",
      borderRadius: 12,
      background: ok
        ? "rgba(0,180,90,0.14)"
        : "rgba(220,40,70,0.14)",
      border: ok
        ? "1px solid rgba(0,180,90,0.4)"
        : "1px solid rgba(220,40,70,0.4)",
      color: "#eee",
      textAlign: "center",
      fontWeight: 700,
    }),

    footerInfo: {
      marginTop: 8,
      textAlign: "center",
      color: "#a9a9a9",
      fontSize: 12,
    },
  };
  const hero = scenario?.hero_pos;
  const isUnopened = scenario?.facing === "unopened";
  const dealerSeat = "BTN";

  return (
    <div style={s.stage}>
      <div style={s.header}>
        <label>Mode:</label>
        <select
          value={mode}
          onChange={(e)=> setMode(e.target.value)}
          style={s.select}
        >
          <option value="cash">Cash (pro baseline)</option>
          <option value="mtt" disabled>MTT (soon)</option>
        </select>
        <button
          onClick={newHand}
          disabled={loading}
          style={{ ...s.btn, ...(loading ? s.btnNeutral : s.btnPrimary) }}
        >
          {loading ? "Shuffling…" : "New Hand"}
        </button>
      </div>

      <div style={s.tableWrap}>
        <div style={s.felt} />

        <div style={s.boardTray}>
          {[0,1,2,3,4].map((i) => (
            <div key={i} style={s.boardSlot} />
          ))}
        </div>

        <div style={s.potChip}>0</div>

        {SEATS.map((p, i) => {
          const [x, y] = seatXY(p);
          const isHeroSeat = scenario && p === hero;
          const dealt = dealStep > i || isHeroSeat; // not really used, but leaving it
          const heroCards = scenario?.hero_hand || [];
          const action = actionsByPos[p];

          const [r1, s1] = faceText(heroCards[0]);
          const [r2, s2] = faceText(heroCards[1]);

          return (
            <div key={p}>
              {p === dealerSeat && (
                <div style={s.dealerBtn(x + 70, y - 36)}>D</div>
              )}

              <div style={s.panel(x, y, isHeroSeat, action)}>
                <div style={{ display: "flex", gap: 6 }}>
                  {isHeroSeat ? (
                    <>
                      <div style={s.cardFace}>
                        <div style={s.rank(suitColor[s1])}>{r1}</div>
                        <div style={s.suit(suitColor[s1])}>
                          {suitGlyph[s1] || ""}
                        </div>
                      </div>
                      <div style={s.cardFace}>
                        <div style={s.rank(suitColor[s2])}>{r2}</div>
                        <div style={s.suit(suitColor[s2])}>
                          {suitGlyph[s2] || ""}
                        </div>
                      </div>
                    </>
                  ) : (
                    <>
                      <div style={s.cardBack(action === "fold")} />
                      <div style={s.cardBack(action === "fold")} />
                    </>
                  )}
                </div>

                <div style={{ marginLeft: 10 }}>
                  <div style={{ fontWeight: 800, letterSpacing: 0.3 }}>
                    {p}
                    {isHeroSeat ? " • YOU" : ""}
                    <span style={s.posTag}>
                      {action ? action.toUpperCase() : "—"}
                    </span>
                  </div>
                  {scenario && isHeroSeat && (
                    <div
                      style={{
                        marginTop: 2,
                        fontSize: 12,
                        opacity: 0.8,
                      }}
                    >
                      {scenario.hero_canonical} • facing {scenario.facing}
                    </div>
                  )}
                </div>

                {!isHeroSeat && action && (
                  <div style={s.badge(action)}>
                    {action === "open" ? "RAISE" : action.toUpperCase()}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {scenario && (
          <>
            <div style={s.hud}>
              {scenario.opened_by
                ? `Opened by ${scenario.opened_by}`
                : "Unopened pot"}
              {scenario.three_bet_by
                ? ` • 3-bet by ${scenario.three_bet_by}`
                : ""}
            </div>

            <div style={s.actions}>
              <button
                onClick={() => answer("fold")}
                disabled={!scenario || !!result}
                style={{ ...s.btn, background: "#2b2b2b", color: "#fff" }}
              >
                Fold
              </button>
              <button
                onClick={() => answer("call")}
                disabled={!scenario || !!result || isUnopened}
                style={{ ...s.btn, background: "#ffd54f", color: "#241c00" }}
              >
                Call
              </button>
              <button
                onClick={() => answer("raise")}
                disabled={!scenario || !!result}
                style={{ ...s.btn, background: "#00c853", color: "#fff" }}
              >
                Raise
              </button>
            </div>
          </>
        )}

        {result && !result.error && (
          <div style={s.verdict(result.correct)}>
            You chose <b>{result.your_action}</b>. Correct action:{" "}
            <b>{result.correct_action}</b>{" "}
            {result.correct ? " - Correct!" : " - Wrong..."}
            <div
              style={{
                marginTop: 6,
                opacity: 0.9,
                fontWeight: 500,
              }}
            >
              {result.hero_canonical} • {result.hero_pos} • {result.facing}
            </div>
            <div style={{ marginTop: 10 }}>
              <button
                onClick={newHand}
                style={{ ...s.btn, ...s.btnPrimary }}
              >
                Next Hand
              </button>
            </div>
          </div>
        )}

        {result && result.error && (
          <div style={s.verdict(false)}>{result.error}</div>
        )}

        {!scenario && (
          <div style={s.footerInfo}>
            Click <b>New Hand</b> to begin.
          </div>
        )}
      </div>
    </div>
  );
}
