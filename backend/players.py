# libraries:
from deck import *
import random

# Player class: it would be used by the player and the croupier
class Player():
    def __init__(self, name:str):
        self._name = name
        self._hand: list[Card] = []

    # getters ---------------------
    @property
    def name(self):
        return self._name
    
    @property
    def hand(self):
        return self._hand

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
                elif(card.value == 'A' and not aces):
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

