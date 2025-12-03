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

    names ={1: 'A', 11: 'J', 12: 'Q', 13: 'K', 10: 'T'}

    rank_str = names.get(r, str(r))
    return f"{rank_str}{s}"

def random_hand():
    d = make_deck() 
    random.shuffle(d)
    return [d.pop(), d.pop()]


