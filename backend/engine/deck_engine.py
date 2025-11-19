import random
import itertools
from pokerhelpers import deck

def make_deck():
    ret = []
    for r, s in deck.items():
        for x in s:
            ret.append((r,x))
    return ret
def str_to_card(s):
    s = s.strip()
    r = s[:-1].upper()
    ss = s[-1].lower()
    lookup = {'A':1, 'J':11, 'Q':12, 'K':13}
    try:
        rank = int(r)
    except:
        rank = lookup.get(r, None)
    return (rank, ss)

def card_to_str(card):
    r, s = card 
    name = ""
    if r == 11:
        name = 'J'
    elif r == 12:
        name = 'Q'
    elif r == 13:
        name = 'K'
    elif r == 1:
        name = 'A'
    return f"{name}{s}"
def random_hand():
    d = make_deck() 
    random.shuffle(d)
    return [d.pop(), d.pop()]


