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
