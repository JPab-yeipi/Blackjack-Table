# libraries:
from deck import *
import random

# Player class: it would be used by the player and the croupier
class Player():
    def __init__(self, name: str, money: float = 100.0):
        self._name = name
        self._hand: list[Card] = []
        self._money = money
        self._current_bet = 0.0

    # Money getter
    @property
    def balance(self) -> float:
        return self._money

    # Place a bet: subtracts money from balance and stores the current bet amount
    def place_bet(self, amount: float):
        if amount <= 0:
            raise ValueError("Bet amount must be positive.")
        if amount > self._money:
            raise ValueError("Insufficient balance to place bet.")
        self._money -= amount
        self._current_bet = amount

    # Award winnings: receives a multiplier and rewards accordingly, resets current bet to zero after
    def award_winnings(self, multiplier: float):
        # winnings = bet * multiplier; can be negative for losses or positive for wins
        winnings = self._current_bet * multiplier
        self._money += winnings
        self._current_bet = 0.0

    # getter for the current bet amount
    @property
    def current_bet(self) -> float:
        return self._current_bet

    # getters ---------------------
    @property
    def name(self):
        return self._name
    
    @property
    def hand(self):
        return self._hand

    def hand_str(self) -> str:
        return ", ".join(str(card) for card in self._hand)

    # gives the player´s hand value, counting aces
    @property
    def hand_value(self) -> int:
        if (len(self._hand) == 0):
            return 0
        else:
            total_v = 0
            aces = False

            for card in self._hand:
                if(card.value in ['2', '3', '4', '5', '6', '7', '8', '9']):
                    total_v += int(card.value)
                elif(card.value in ['J', 'Q', 'K']):
                    total_v += 10
                elif(card.value == 'A'):
                    if (aces):
                        total_v += 1
                    else:
                        if (total_v <= 10):
                            total_v += 11
                        else:
                            total_v += 1

                    aces = True

            if (total_v > 21 and aces):
                total_v -= 10

            return total_v
    
    # setters ---------------------
    @name.setter
    def name(self, new_name:str):
        self._name = new_name

    # Methods ---------------------

    # Method to know how many cards each player have
    def num_cards(self):
        num = 0
        for c in self.hand:
            num += 1

        return num

    # this method gives the player cards based on if its the firts time or not
    def hit(self, d:Deck):
        card: Card
        if (len(self._hand) == 0):
            for i in range(2):
                card = d.pop_card()
                self._hand.append(card)

        else:
            card = d.pop_card()
            self._hand.append(card)

    # this method acts like an AI for the croupier to play against player
    def play(self, d:Deck):
        # if the hand value is less than 16, 100% the AI would hit
        while(self.hand_value < 16):
            self.hit(d)
            print(f'{self._name} hits a {self._hand[-1]} -> new total value: {self.hand_value}')

        # if the hand value is exactly 16, theres a 50/50 chance the AI will hit 
        if(self.hand_value == 16):
            risk = random.randint(0, 1)
            print(f'{self._name} hits -> total value: {self.hand_value}')

            if (risk == 1):
                self.hit(d)

    # we restart the player hand so we can play again
    def restart_hand(self):
        self._hand: list[Card] = []
