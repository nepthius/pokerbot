import { useState }  from "react";
import axios  from "axios";

// yeah localhost for now
const API  =  "http://127.0.0.1:5010";


export default function  PreflopTrainer( ){
  
  const [ scenario , setScenario ] = useState( null );
  const [ result ,   setResult   ] = useState( null );
  const [ mode ,     setMode     ] = useState( "cash" );
  const [ loading ,  setLoading  ] = useState( false );  

  
  async function   newScenario( ){
        setLoading( true );
        setResult( null );

        try{
            const resp  = await axios.post( `${API}/api/trainer/new` , { mode } );
            setScenario( resp.data );
        } catch(err){
            console.log("oops:", err);
            setScenario( null );
        } finally{
            setLoading( false );
        }
  }


  async function answer( action ){
      if(!scenario) return;

      try{
          const r  = await axios.post(
              `${API}/api/trainer/answer`,
              { id : scenario.id , action }
          );
          setResult( r.data );
      } catch(e){
          console.error("bad req?", e);
      }
  }


  //random styling 
  const wrap  = { maxWidth: 800 , margin: "20px auto" , fontFamily: "Arial, sans-serif" };
  const btn   = { padding:"8px 12px" , marginRight:8 , border:"none" , borderRadius:6 ,
                  cursor:"pointer" , background:"#007bff" , color:"#fff" };
  const muted = { color:"#555" };


  return(
    <div style={ wrap }>

      <h2>Preflop Trainer</h2>

      <div style={{ marginBottom:12 }}>
          <label> Mode:&nbsp; </label>

          <select
            value={ mode }
            onChange={ (e)=> setMode( e.target.value ) }
            style={{ padding:"6px 8px" }}
          >
            <option value="cash">Cash (200bb-ish, low rake)</option>
            <option value="mtt">MTT (ChipEV, 0.125bb ante)</option>
          </select>

          <button
            onClick={ newScenario }
            disabled={ loading }
            style={{ ...btn , marginLeft:10 }}
          >
            { loading ? "Generating..." : "New Scenario" }
          </button>
      </div>


      { scenario && (
        <>
          <div style={{
              padding:12 , border:"1px solid #ddd" , borderRadius:8 , marginBottom:12
          }}>
              <div><b>Hero</b>: { scenario.hero_pos }</div>
              <div>
                <b>Hand</b>: { scenario.hero_hand[0] } { scenario.hero_hand[1] }
                &nbsp;<span style={ muted }>({ scenario.hero_canonical })</span>
              </div>
              <div><b>Facing</b>: { scenario.facing }</div>
          </div>

          <div style={{
              padding:12 , border:"1px dashed #ccc" , borderRadius:8 , marginBottom:12
          }}>
              <b>Actions so far</b>
              <ol>
                 { scenario.actions.map( (a,ix)=>(
                      <li key={ ix }>
                        <b>{ a.pos }</b> → { a.action }
                        &nbsp;<span style={ muted }>
                          [{ a.hand } | { a.canonical }]
                        </span>
                      </li>
                   ))
                 }
              </ol>
          </div>

          <div style={{ marginBottom:12 }}>
              <b>Your move:</b>&nbsp;

              <button onClick={ ()=>answer("fold") }  style={ btn }>
                  Fold
              </button>

              <button onClick={ ()=>answer("call") }  style={ btn }>
                  Call
              </button>

              <button onClick={ ()=>answer("raise") } style={ btn }>
                  Raise
              </button>
          </div>
        </>
      )}


      { result && !result.error && (
        <div
          style={{
            padding:12 , border:"1px solid #ddd" , borderRadius:8 ,
            background: result.correct ? "#e8f5e9" : "#ffebee"
          }}
        >
            <div>
              You chose <b>{ result.your_action }</b>.
              Correct action: <b>{ result.correct_action }</b>.&nbsp;
              { result.correct ? "Nice!" : "Incorrect..." }
            </div>

            <button
              onClick={ newScenario }
              style={{ ...btn , marginTop:8 }}
            >
              Next Hand
            </button>
        </div>
      )}


      { result && result.error && (
          <div style={{ color:"red" }}>{ result.error }</div>
      )}

    </div>
  );
}
