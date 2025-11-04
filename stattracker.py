from pokerhelpers import deck
import random

class Game:
    def __init__(self, starting_amt, number_players):
        self.number_players = number_players
        self.starting_amt = starting_amt
        self.turn = 0
        self.deck = deck


    def reset(self):
        self.deck = deck

    def deal(self):
        possible_vals = self.deck.keys()
        card1 = random.choice(possible_vals)
        suit1 = random.choice(self.deck[possible_vals])
        self.deck[possible_vals].remove(suit1)
        if self.deck[possible_vals] == []:
            del self.deck[possible_vals]
        
        card2 = random.choice(possible_vals)
        suit2 = random.choice(self.deck[possible_vals])
        self.deck[possible_vals].remove(suit1)
        if self.deck[possible_vals] == []:
            del self.deck[possible_vals]

        return [[card1, suit1], [card2, suit2]]

class Player:
    def __init__(self, starting_amt):
        self.pot = starting_amt
        self.hand = []

if __name__ == "__main__":
    print("Starting game...")
    players = int(input("Please enter the number of players: "))
    starting_amt = int(input("Please enter the starting amount: "))