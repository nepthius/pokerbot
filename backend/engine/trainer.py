import random
import uuid
from typing import Dict, Optional

from .deck_engine import make_deck, card_to_str
from .ranges import canonical_from_cards

POSITIONS_9 = ["UTG","UTG+1","UTG+2","LJ","HJ","CO","BTN","SB","BB"]

EARLY = {"UTG","UTG+1","UTG+2"}
MIDDLE = {"LJ","HJ"}
LATE   = {"CO","BTN"}
def hero_group(pos: str) -> str:
    if pos in EARLY:  return "E"
    if pos in MIDDLE: return "M"
    if pos in LATE:   return "L"
    if pos == "SB":   return "SB"
    if pos == "BB":   return "BB"
    return "?"

def opener_group(pos: str) -> str:
    if pos in EARLY:  return "E"
    if pos in MIDDLE: return "M"
    if pos in LATE:   return "L"
    if pos == "SB":   return "SB"
    return "?"

PREMIUM = set(["AA","KK","QQ","AKs","AKo"])
STRONG  = set(["JJ","TT","AQs","AJs","KQs","AQo"])
MEDIUMs = set([
    "99","88","ATs","KJs","QJs","JTs","T9s","98s","87s",
    "KQo","AJo","A5s","KTs","QTs"
])
RFI_CASH = {
    "UTG":   set([
        "AA","KK","QQ","JJ","TT","99",
        "AKs","AQs","AJs","KQs",
        "AKo"
    ]),
    "UTG+1": set([
        "AA","KK","QQ","JJ","TT","99","88",
        "AKs","AQs","AJs","ATs","KQs",
        "AKo","AQo",
        "AJo","KQo"
    ]),
    "UTG+2": set([
        "AA","KK","QQ","JJ","TT","99","88","77",
        "AKs","AQs","AJs","ATs","KQs","KJs","QJs",
        "AKo","AQo","KQo"
        "AKo","AQo","KQo","AJo"
    ]),
    "LJ":    set([
        "AA","KK","QQ","JJ","TT","99","88","77","66",
        "AKs","AQs","AJs","ATs","A5s",
        "KQs","KJs","KTs","QJs","QTs","JTs","T9s","98s",
        "AKo","AQo","AJo","KQo","QJo"
    ]),
    "HJ":    set([
        "AA","KK","QQ","JJ","TT","99","88","77","66","55",
        "AKs","AQs","AJs","ATs","A9s","A5s",
        "KQs","KJs","KTs","QJs","QTs","JTs","T9s","98s","87s",
        "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
    ]),
    "CO":    set([
        "AA","KK","QQ","JJ","TT","99","88","77","66","55","44",
        "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A5s",
        "KQs","KJs","KTs","QJs","QTs","JTs","T9s","98s","87s",
        "AKo","AQo","AJo","ATo","KQo","KJo","QJo","KTo","QJo","QTo","JTo"
    ]),
    "BTN":   set([
        "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
        "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
        "KQs","KJs","KTs","K9s","QJs","QTs","Q9s","JTs","J9s","T9s","98s","87s","76s",
        "AKo","AQo","AJo","ATo","A9o",
        "KQo","KJo","KTo","QJo","QTo","JTo"
    ]),
    "SB":    set([
        "AA","KK","QQ","JJ","TT","99","88","77","66",
        "AKs","AQs","AJs","ATs","A9s","A5s",
        "KQs","KJs","QJs","JTs","T9s","98s",
        "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
    ]),
    "BB":    set([
        "AA","KK","QQ","JJ","TT","99","88",
        "AKs","AQs","AJs","ATs","KQs","KJs","QJs","JTs",
        "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
    ]),
}

VS_OPEN_3BET_CASH_SPEC = {
    ("HJ","UTG"):  set(["AA","KK","QQ","JJ","AKs","AQs","AKo"]),
    ("CO","UTG"):  set(["AA","KK","QQ","JJ","AKs","AQs","AKo"]),
    ("CO","LJ"):   set(["AA","KK","QQ","JJ","TT","AKs","AQs","AKo","A5s"]),
    ("BTN","UTG"): set(["AA","KK","QQ","JJ","TT","AKs","AQs","AKo"]),
    ("BTN","HJ"):  set(["AA","KK","QQ","JJ","TT","99","AKs","AQs","AKo","A5s","KQs"]),
    ("BTN","CO"):  set(["AA","KK","QQ","JJ","TT","99","AKs","AQs","A5s","KQs","AKo"]),
    ("SB","BTN"):  set(["AA","KK","QQ","JJ","TT","AKs","AQs","AKo"]),
    ("SB","CO"):   set(["AA","KK","QQ","JJ","TT","AKs","AQs","AKo","A5s"]),
    ("BB","BTN"):  set(["AA","KK","QQ","JJ","TT","99","AKs","AQs","A5s","KQs","KJs","AKo"]),
    ("BB","CO"):   set(["AA","KK","QQ","JJ","TT","99","AKs","AQs","A5s","KQs","AKo"]),
    ("BB","SB"):   set(["AA","KK","QQ","JJ","TT","AKs","AQs","AKo"]),
}
VS_OPEN_CALL_CASH_SPEC = {
    ("HJ","UTG"):  set(["TT","99","AQo","AJs","KQs"]),
    ("CO","UTG"):  set(["TT","99","AQo","AJs","KQs"]),
    ("CO","LJ"):   set(["AQo","AJs","ATs","KQs","KJs","QJs","JTs","T9s","99","88","77"]),
    ("BTN","UTG"): set(["TT","99","88","AQo","AJs","ATs","KQs","QJs","JTs"]),
    ("BTN","HJ"):  set(["AQo","AJs","ATs","KQs","KJs","QJs","JTs","T9s","99","88","77"]),
    ("BTN","CO"):  set(["AQo","AJs","ATs","A5s","KQs","KJs","QJs","JTs","T9s","98s","99","88","77","66"]),
    ("SB","BTN"):  set(["AQo","AJs","ATs","KQs","QJs","JTs","TT","99","88"]),
    ("SB","CO"):   set(["AQo","AJs","ATs","A5s","KQs","QJs","JTs","TT","99"]),
    ("BB","BTN"):  set([
        "AQo","AJo","ATo","AJs","ATs","A5s",
        "KQo","KJo","KQs","KJs","QJo","QJs","JTs","T9s","98s","87s",
        "TT","99","88","77","66"
    ]),
    ("BB","CO"):   set([
        "AQo","AJo","ATo","AJs","ATs","A5s",
        "KQo","KJo","KQs","KJs","QJo","QJs","JTs","T9s","98s",
        "TT","99","88","77"
    ]),
    ("BB","SB"):   set(["AQo","AJs","ATs","KQo","KQs","QJs","JTs","TT","99","88"]),
}

def _pack(*hands): 
    return set(hands)

VS_OPEN_GROUP = {
    ("L","E"):  (PREMIUM | _pack("JJ"), STRONG | _pack("KJs","QJs","JTs","T9s","99","88")),
    ("L","M"):  (PREMIUM | _pack("JJ","TT","A5s","KQs"), STRONG | MEDIUMs | _pack("77")),
    ("L","L"):  (PREMIUM | _pack("JJ","TT","99","A5s","KQs","KJs"), STRONG | MEDIUMs | _pack("77","66")),
    ("SB","E"): (PREMIUM | _pack("JJ","TT"), STRONG | _pack("AQo","KQs","QJs","JTs","TT","99")),
    ("SB","M"): (PREMIUM | _pack("JJ","TT","99"), STRONG | MEDIUMs | _pack("TT","99")),
    ("SB","L"): (PREMIUM | _pack("JJ","TT","99","A5s","KQs"), STRONG | MEDIUMs | _pack("77")),
    ("BB","E"): (PREMIUM | _pack("JJ","TT"), STRONG | _pack("AQo","AJs","KQs","QJs","JTs","TT","99")),
    ("BB","M"): (PREMIUM | _pack("JJ","TT","99"), STRONG | MEDIUMs | _pack("88")),
    ("BB","L"): (PREMIUM | _pack("JJ","TT","99","A5s","KQs"), STRONG | MEDIUMs | _pack("77","66")),
    ("BB","SB"): (PREMIUM | _pack("JJ","TT"), STRONG | _pack("AQo","AJo","ATo","AJs","ATs","KQo","KQs","QJs","JTs","TT","99","88")),
    ("M","E"):  (PREMIUM | _pack("JJ"), STRONG | _pack("AQo","AJs","KQs","QJs","JTs","TT","99")),
    ("M","M"):  (PREMIUM | _pack("JJ","TT"), STRONG | MEDIUMs | _pack("77")),
    ("M","L"):  (PREMIUM | _pack("JJ","TT","99","A5s","KQs"), STRONG | MEDIUMs | _pack("77","66")),
    ("E","E"):  (PREMIUM, STRONG & _pack("JJ","TT","AQs","AJs","KQs")),
    ("E","M"):  (PREMIUM | _pack("JJ"), STRONG & _pack("TT","AQs","AJs","KQs")),
    ("E","L"):  (PREMIUM | _pack("JJ","TT"), STRONG | _pack("AQo","AJs","KQs","QJs","JTs","TT","99")),
}
VS_3BET_4BET =PREMIUM | set(["QQ"]) 
VS_3BET_CALL = STRONG | set(["KQs","AJs","JJ"])
_SESSION: Dict[str, dict]={}

def _deal_deck():
    d = make_deck()
    random.shuffle(d)
    return d

def _canon2(cards2):
    return canonical_from_cards(cards2[0], cards2[1])

def _decide_vs_open(hero_canon: str, hero_pos: str, opener_pos: str,
                    spec3: dict, specC: dict) -> str:
    """Return 'raise'|'call'|'fold' using specific maps, else group maps, else universal fallback."""
    key = (hero_pos, opener_pos)
    s3 = spec3.get(key)
    sc = specC.get(key)
    if s3 and hero_canon in s3: return "raise"
    if sc and hero_canon in sc: return "call"

    hg = hero_group(hero_pos)
    og = opener_group(opener_pos)
    gkey = (hg, og)
    if gkey in VS_OPEN_GROUP:
        g3, gc = VS_OPEN_GROUP[gkey]
        if hero_canon in g3: return "raise"
        if hero_canon in gc: return "call"

    if hero_canon in PREMIUM: return "raise"
    if hero_canon in STRONG:  return "call"
    return "fold"

def new_scenario(mode="cash") -> dict:
    """Generate one 9-handed preflop scenario, stop at hero action."""
    RFI   = RFI_CASH
    SPEC3 = VS_OPEN_3BET_CASH_SPEC
    SPECC = VS_OPEN_CALL_CASH_SPEC

    deck = _deal_deck()
    seats = POSITIONS_9[:]
    hero_idx = random.randrange(len(seats))
    hero_pos = seats[hero_idx]
    hands = {p: [deck.pop(), deck.pop()] for p in seats}
    actions = []
    opened_by: Optional[str] = None
    three_bet_by: Optional[str] = None

    for step_pos in seats:
        if step_pos == hero_pos:
            break
        hand_canon = _canon2(hands[step_pos])
        act = "fold"
        if opened_by is None and three_bet_by is None:
            if hand_canon in RFI.get(step_pos, set()):
                act = "open"
                opened_by = step_pos
        elif opened_by is not None and three_bet_by is None:
            d = _decide_vs_open(hand_canon, step_pos, opened_by, SPEC3, SPECC)
            if d == "raise":
                act = "3bet"
                three_bet_by = step_pos
            elif d == "call":
                act = "call"
            else:
                act = "fold"
        else:
            act = "fold"

        actions.append({
            "pos": step_pos,
            "hand": f"{card_to_str(hands[step_pos][0])} {card_to_str(hands[step_pos][1])}",
            "canonical": hand_canon,
            "action": act
        })

    hero_hand = hands[hero_pos]
    hero_canon = _canon2(hero_hand)
    facing = "unopened" if opened_by is None else ("open" if three_bet_by is None else "3bet")
    if facing == "unopened":
        correct = "raise" if hero_canon in RFI.get(hero_pos, set()) else "fold"
        if hero_pos == "BB" and opened_by is None:
            correct = "raise" if hero_canon in RFI.get("BB", set()) else "fold"
    elif facing == "open":
        correct = _decide_vs_open(hero_canon, hero_pos, opened_by, SPEC3, SPECC)
    else:
        if hero_canon in VS_3BET_4BET:
            correct = "raise"
        elif hero_canon in VS_3BET_CALL:
            correct = "call"
        else:
            correct = "fold"

    sid = str(uuid.uuid4())
    scenario = {
        "id": sid,
        "mode": mode,
        "seats": seats,
        "hero_pos": hero_pos,
        "hero_hand": [card_to_str(hero_hand[0]), card_to_str(hero_hand[1])],
        "hero_canonical": hero_canon,
        "actions": actions,
        "opened_by": opened_by,
        "three_bet_by": three_bet_by,
        "facing": facing,
        "correct": correct,
    }
    _SESSION[sid] = scenario
    return scenario
def grade_answer(sid: str, user_action: str) -> dict:
    sc = _SESSION.get(sid)
    if not sc:
        return {"error": "scenario not found"}
    ua = user_action.lower()
    is_correct = (ua == sc["correct"])
    return {
        "id": sid,
        "hero_pos": sc["hero_pos"],
        "hero_hand": sc["hero_hand"],
        "hero_canonical": sc["hero_canonical"],
        "facing": sc["facing"],
        "your_action": ua,
        "correct_action": sc["correct"],
        "correct": is_correct,
    }
