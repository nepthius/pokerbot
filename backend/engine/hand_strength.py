from .ranges import canonical_from_text

#add hand strength listing stuff
HAND_STRENGTH_ORDER = [
    "AA","KK","QQ","JJ","TT","99","88","AKs","AQs","AJs","ATs","KQs","AKo","A5s","KJs","QJs","JTs","KQo","AQo","AJo","KTs","QTs","T9s","98s","A9s","A8s","A7s","KJo","QJo","A6s","A4s","A9o","KTo","QTo","JTo","76s","65s","54s",

]

#buckets
PREMIUM = set(["AA","KK","QQ","AKs","AKo"])
STRONG = set(["JJ","TT","AQs","AJs","KQs","AQo"])
PLAYABLE = set([
    "99","88","ATs","A9s","KJs","KQo","QJs","JTs","T9s","98s","87s","AJo","ATo","KJo","QJo"
]) 
SPECULATIVE = set(["A5s","A4s","76s","65s","54s"])
TRASH = set() 

def classify_hand(canon):
    if canon in PREMIUM: return "Premium"
    if canon in STRONG: return "Strong"

    if canon in PLAYABLE: return "Playable"
    if canon in SPECULATIVE: return "Speculative"
    return "Trash"
def strength_percentile(canon):
    if canon not in HAND_STRENGTH_ORDER:
        return 60.0
    idx = HAND_STRENGTH_ORDER.index(canon)

    pct = (idx / len(HAND_STRENGTH_ORDER)) * 100
    return round(pct, 1)
def best_positions(canon):
    if canon in PREMIUM: return ["All Positions"]
    if canon in STRONG: return ["UTG+", "LJ", "HJ", "CO", "BTN"]
    if canon in PLAYABLE: return ["LJ", "HJ", "CO", "BTN"]
    if canon in SPECULATIVE: return ["CO", "BTN"]
    return ["BTN Only"]





def analyze_hand(text):
    canon = canonical_from_text(text)
    tier = classify_hand(canon)
    pct = strength_percentile(canon)
    pos = best_positions(canon)
    return {
        "canonical": canon,
        "tier": tier,
        "percentile": pct,
        "recommended_positions": pos
    }
