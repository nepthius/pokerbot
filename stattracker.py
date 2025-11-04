from pokerhelpers import deck
import random

class Game:
    def __init__(self, starting_amt=2000, players=[]):
        self.players = players
        self.starting_amt = starting_amt
        self.round = 0
        self.deck = deck


    def reset(self):
        self.deck = deck

    def deal(self):
        def pickCard():
            possible_vals = list(self.deck.keys())
            card1 = random.choice(possible_vals)
            suit1 = random.choice(self.deck[card1])
            self.deck[card1].remove(suit1)
            if self.deck[card1] == []:
                del self.deck[card1]
            return [card1, suit1]
        
        first = pickCard()
        second = pickCard()

        return [first, second]

    def play(self):
        if self.round == 0:
            for player in self.number_players:
                player.assignHand(self.deal())
        

        





class Player:
    def __init__(self, starting_amt):
        self.pot = starting_amt
        self.hand = []
    
    def assignHand(self, cards):
        self.hand = cards


if __name__ == "__main__":
    print("Starting game...")
    players = int(input("Please enter the number of players: "))
    starting_amt = int(input("Please enter the starting amount: "))

    game = Game(starting_amt, players)
    
    
    print(game.deal())