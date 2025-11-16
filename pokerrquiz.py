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


def simulate_equity(h, b=None, o=1, t=2000):
    b = b
    if not b:
        b = []
    d= make_deck()  
    u = h +b
    a =[]
    for x in d:

        if x not in u:
            a.append(x)

    w =0
    q =0
    l= 0
    for temp in range(t):
        random.shuffle(a)
        p = []  
        i = 0
        for temptemp in range(o):
            pair = [a[i], a[i+1]]
            p.append(pair)
            i += 2

        n = 5 -len(b)
        sb= b + a[i:i+n]

        hr = best_hand_rank(h + sb)
        orr = []
        for yy in p:

            orr.append(best_hand_rank(yy + sb))
        tmp =[hr]
        for rr in orr:
            tmp.append(rr)
        mx = max(tmp)
        hb = (hr == mx)
        ct = 0
        for rr in orr:
            if rr == mx:
                ct += 1
        if hb:
            ct += 1
        if hb:
            if ct == 1:
                w += 1
            else:
                q += 1
        else:
            l += 1
    z = w + q + l
    return w / z, q / z, l / z
def run_equity_quiz():
    print("=== Poker Equity Quiz (Custom Deck) ===\n")
    while True:
        d =make_deck()
        random.shuffle(d)
        hero =[d.pop(), d.pop()]
        _n = random.choice([0,3,4,5])
        board= []
        for _i in range(_n):
            board.append(d[_i])
        n_opp = random.choice([1,2,3])



        hero_parts = []
        for c in hero:
            hero_parts.append(card_to_str(c))
        hero_str = " ".join(hero_parts)
        if board:
            board_parts = []
            for c in board:

                board_parts.append(card_to_str(c))
            board_str =" ".join(board_parts)
        else:
            board_str= "(no board)"
        print(f"\nHand: {hero_str} | Board: {board_str} | Opponents: {n_opp}")
        win,tie, lose = simulate_equity(hero, board, n_opponents=n_opp)
        eq = win +tie/2
        eq_pct = round(eq*100,1)
        guess = input("Guess win equity (in percent) or yo can press q to quit: ")
        if guess.lower().startswith('q'):
            break
        try:
            g = float(guess)
        except:
            print("Please enter a number")
            continue
        diff = abs(g - eq_pct)
        if diff <= 5:
            print(f"Almost correct! Actual: {eq_pct}%")
        elif diff <= 10:
            print(f"Meh (actual {eq_pct}%)")
        else:
            print(f"RUH ROH. Actual: {eq_pct}%")

if __name__ == "__main__":
    run_equity_quiz()