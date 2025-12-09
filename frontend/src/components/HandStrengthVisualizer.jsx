import { useState } from "react";
import axios   from "axios";

//local host - will change
const API = "http://127.0.0.1:5010";
export default function HandStrengthVisualizer( ){

  const [hand , setHand] = useState("");
  const [info , setInfo]=useState(null);
  const [error, setError]  = useState(null);


  async function doAnalyze( ){
      // reset any old stuff 
      setInfo(null);
      setError(null);

      try{
          const r = await axios.post(`${API}/api/hand_strength` , { hand });
          setInfo( r.data );
      } catch(err){
          //usertyped something weird prob
          setError("Invalid hand format (try 'Ah Kh', 'AKs', 'QJo', etc.)");
      }
  }


  //styles dumped here… could reorganize but idk
  const wrap = {
      maxWidth: 680,
      margin: "30px auto",
      background: "linear-gradient(180deg,#0f1012,#161a1f)",
      padding: "30px",
      borderRadius: "16px",
      color: "#eee",
      fontFamily: "Inter, Arial, sans-serif",
      boxShadow: "0 10px 30px rgba(0,0,0,0.45)"
  };

  const btn = {
      padding:"10px 16px",
      borderRadius:10,
      border:"none",
      cursor:"pointer",
      fontWeight:700,
      background:"#2b7cff",
      color:"#fff",
      marginLeft:10
  };

  const tierColor = (tier)=>{
        switch(tier){
          case "Premium": return "#00c878";
          case "Strong":return "#4aa3ff";
          case "Playable": return "#ffc04d";
          case "Speculative": return "#ff7f3f";
          default: return "#d33";
        }
  };


  return(
    <div style={ wrap }>

      <h2 style={{ fontSize:26 , marginBottom:20 }}>
        Hand Strength Visualizer
      </h2>

      <p style={{ opacity:0.8 }}>
        Enter a hand like <b>"Ah Kh"</b>, <b>"AKs"</b>, <b>"QJo"</b>, <b>"76s"</b>.
      </p>

      <div style={{ marginTop:16, display:"flex" }}>
        
        <input
          style={{
            flex:1,
            padding:"10px",
            borderRadius:10,
            border:"1px solid #444",
            background:"#1d2128",
            color:"#fff"
          }}
          value={ hand }
          onChange={e=> setHand(e.target.value)}
          placeholder="Enter starting hand..."
        />

        <button
          style={btn}
          onClick={doAnalyze}
        >
          Analyze
        </button>

      </div>


      {error && (
        <div style={{ marginTop:16 , color:"#ff6060" }}>
          { error }
        </div>
      )}


      {info && (
        <div style={{ marginTop:24 }}>
          
          <h3>
            Canonical: <span>{info.canonical}</span>
          </h3>

          <div style={{
              marginTop:10,
              padding:"12px 16px",
              borderRadius:12,
              background:"rgba(255,255,255,0.06)",
              border:"1px solid rgba(255,255,255,0.1)"
          }}>

            <h3 style={{ color: tierColor(info.tier) }}>
                Strength Tier: {info.tier}
            </h3>


            <div style={{ marginTop:10 }}>
                <b>Percentile Strength:</b> {info.percentile}%

                <div style={{
                    width:"100%",
                    height:12,
                    marginTop:6,
                    background:"#333",
                    borderRadius:6,
                    position:"relative"
                }}>
                    <div style={{
                      width:`${info.percentile}%`,
                      height:"100%",
                      background: tierColor(info.tier),
                      borderRadius:6
                    }} />
                </div>
            </div>


            <div style={{ marginTop:16 }}>
                <b>Recommended Positions:</b>

                <ul>
                    {info.recommended_positions.map(p=>(
                        <li key={p}>{p}</li>
                    ))}
                </ul>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
