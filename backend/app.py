from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from engine.deck_engine import str_to_card
from engine.equity import simulate_equity
from engine.ranges import (
    RANKS, load_range_csv, grid_from_range_map, canonical_from_text, action_for_hand
)
from engine.trainer import new_scenario, grade_answer
app = Flask(__name__)
CORS(app)
RANGES_DIR = Path(__file__).parent / "data" / "ranges"

@app.route("/api/equity", methods=["POST"])
def get_equity():
    data = request.get_json()

    hand_str =data.get("hand", "")
    board_str= data.get("board", "") 
    n_opp = int(data.get("opponents", 1)) 
    hero =[str_to_card(x) for x in hand_str.split() if x.strip()]
    board = [str_to_card(x) for x in board_str.split() if x.strip()]



    win, tie, lose = simulate_equity(hero, board, o=n_opp, t=3000)
    eq = (win + tie/2) * 100
    return jsonify({"equity": eq})

@app.route(   "/api/ranges/positions" , methods=["GET"] )
def list_positions(   ):
    
    found_pos   = set()  
    
    for pp in   RANGES_DIR.glob( "*.csv" ):
        nm   = pp.stem
        found_pos.add( nm )

    #sorting j cuz flask/json doesn't like sets
    return   jsonify( sorted( found_pos ) )

@app.route("/api/ranges/<name>", methods=["GET"])
def  get_range_grid( name ):
    the_csv   =   (RANGES_DIR   /   f"{name}.csv")
    if not the_csv.exists( ) :
        return jsonify({
            "error" : f"range {name} not found"
        }),   404
    
    rm   = load_range_csv( the_csv )
    g =    grid_from_range_map( rm )
    
    return jsonify({
            "ranks" :    RANKS,
            "grid"  : g
        })



@app.route( "/api/ranges/check",methods = [ "POST" ] )
def check_hand_action( ):
    body  =  request.get_json(   )
    nm = body.get( "name" , "" )
    raw_hand   =   body.get( "hand" , "")
    
    fpath = RANGES_DIR / (f"{nm}.csv")
    
    if not fpath.exists():
        return jsonify({ "error" :   f"range {nm} not found" }), 404
    loaded_map = load_range_csv(   fpath )

    can = canonical_from_text( raw_hand )
    act   = action_for_hand( loaded_map , can )
    return jsonify({
        "canonical" : can ,
        "action" :   act
    })

@app.route("/api/trainer/new", methods=["POST"])
def trainer_new():
    data= request.get_json(silent=True) or {}
    mode= data.get("mode","cash")
    sc =new_scenario(mode=mode)
    return jsonify(sc)

@app.route("/api/trainer/answer", methods=["POST"])
def trainer_answer():
    data = request.get_json()
    sid = data.get("id")

    action = data.get("action")
    if action not in ("raise","call","fold"):
        return jsonify({"error":"invalid action"}), 400
    result = grade_answer(sid, action)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)