import random
cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]

class Player:
    def __init__(self, starting_amt):
        self.pot = starting_amt 
        self.cards = []
    def __str__(self):
        return f"Pot={self.pot}, Cards={self.cards}"

class Game:
    def __init__(self, starting_amt=50, ante=1):
        self.players = [Player(starting_amt), Player(starting_amt)]
        self.ante = ante
    def make_deck(self): 
        deck = cards * 4
        random.shuffle(deck)
        return deck

  
    def deal_cards(self, deck):
        for p in self.players:
            p.cards = [deck.pop(), deck.pop()]

    def hand_value(self, player):
        val = 0
        for temp in player.cards:
            val+=temp
        return val

    def collect_antes(self):
        for p in self.players:
            if p.pot < self.ante:
                return False
            p.pot -= self.ante
        return True

    #to see who wins
    def give_winnings(self, winner, total_pot):
        if winner == None:
            half = total_pot //2
            self.players[0].pot+= half
            self.players[1].pot  +=total_pot - half
        else:
            self.players[winner].pot +=total_pot




    def play_hand(self, verbose=False):
        if not self.collect_antes():
            return False
        deck = self.make_deck()
        self.deal_cards(deck)
        pot = self.ante * 2
   
        temp = self.hand_value(self.players[0])
        temp2 = self.hand_value(self.players[1])
        if temp > temp2:
            win = 0
        elif temp2 > temp:
            win = 1
        else:
            win = None
   
        self.give_winnings(win, pot)
 
        if verbose:
            if win == None:
                print("TIE:", self.players[0].cards, "vs", self.players[1].cards)
            else:
                print("YES THE PLAYER", win+1, "WINS!", self.players[0].cards, "vs", self.players[1].cards)
        for p in self.players:
            p.cards = []
        return True
    def run(self, rounds=10, verbose=False):
        i = 0
        while i < rounds:
            if any(p.pot <= 0 for p in self.players):
                break
            ok = self.play_hand(verbose=verbose)
            if not ok:
                break
            i += 1
        return i
if __name__ == "__main__":
    g = Game(starting_amt=50, ante=1)

    hands = g.run(rounds=10, verbose=True)
    print("\n--------------------------------------")
    print("P1:", g.players[0].pot)
    print("P2:", g.players[1].pot)
