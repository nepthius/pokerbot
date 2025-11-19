from flask import Flask, request, jsonify
from flask_cors import CORS

from engine.deck_engine import str_to_card
from engine.equity import simulate_equity

app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)