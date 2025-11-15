import random
import itertools
from pokerhelpers import deck

def make_deck():
    ret = []
    for r, s in deck.items():
        for x in s:
            ret.append((r,s))
    return ret
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
def rank_val(c): 
    return c[0]
def str_to_card(s):
    r = s[:-1]
    ss = s[-1]
    lookup = {'A':1, 'J':11, 'Q':12, 'K':13}
    try:
        rank = int(r)
    except:
        rank = lookup[r.upper()]
    return (rank, ss)
