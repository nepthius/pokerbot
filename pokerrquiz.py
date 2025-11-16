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

def eval5(cards5):
    ranks_list = []
    for c in cards5:

        v = rank_val(c) 
        ranks_list.append(v)

    ranks = sorted(ranks_list, reverse=True)
    suits = []
    for c in cards5:
        suit_char = c[1]   
        suits.append(suit_char) 
        counts = {} 
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1

    is_flush = len(set(suits)) == 1

    temp = sorted(set(ranks), reverse=True)
    def straight_high(temp_ranks):
        if len(temp_ranks) < 5:
            return None
        for i in range(len(temp_ranks)-4):
            w = temp_ranks[i:i+5]


            if w[0]-w[4] == 4:
                return w[0]
        if set([14,5,4,3,2]).issubset(set(temp_ranks)):
            return 5
        return None
    



    st_hi = straight_high(temp)

    by_count = sorted(counts.items(), key=lambda x:(x[1], x[0]), reverse=True)
    if is_flush and st_hi:
        return (8, st_hi)
    if by_count[0][1] == 4:
        return (7, by_count[0][0])
    if by_count[0][1] == 3 and len(by_count) > 1 and by_count[1][1] == 2:
        return (6, by_count[0][0])
    if is_flush:
        return (5, *ranks)
    if st_hi: 

        return (4, st_hi)
    if by_count[0][1] == 3:
        return (3, by_count[0][0])
    
    if by_count[0][1] == 2 and len(by_count) > 1 and by_count[1][1] == 2:
        hi, lo = by_count[0][0], by_count[1][0]
        return (2, hi, lo)
    if by_count[0][1] == 2:

        return (1, by_count[0][0])
    return (0, *ranks)

def best_hand_rank(c):
    best = None
    for combo in itertools.combinations(c, 5):
        r = eval5(combo)
        if (best is None) or (r > best):
            best = r
    return best