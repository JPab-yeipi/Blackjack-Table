# libraries:
import random

# card class: here is the internal structure of a card in the deck -----
class Card():
    def __init__(self, s: str, v: str):
        self._suit = s
        self._value = v

    # getters --------------------------------------------------
    @property
    def suit(self):
        return self._suit
    
    @property
    def value(self):
        return self._value
    
    # Representation -------------------------------------------
    def __str__(self):
        return (f'{self._value} of {self._suit}')

    def __repr__(self):
        return (f'{self._value} of {self._suit}')


# deck class: in this class we use card() nodes as elements in a deck -----
class Deck():

    _suits = ["spades", "hearts", "diamonds", "clubs"]
    _values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K"]

    def __init__(self):
        self._cards = []

        # We fill the deck with cards
        for s in self._suits:
            for v in self._values:
                card = Card(s, v)
                self._cards.append(card)

    # getters -----------------------------------------------
    @property
    def cards(self):
        return self._cards
    
    @property
    def num_cards(self):
        num = 0
        for c in self._cards:
            num += 1
        return num

    # Methods -----------------------------------------------

    # this method shuffles the cards in the deck
    def shuffle(self):
        print("Mixing Deck ----------")
        random.shuffle(self._cards)

    def pop_card(self):
        return self._cards.pop(random.randrange(len(self._cards)))

    # Representation -------------------------------------------
    def __str__(self):
        return ", ".join(str(card) for card in self._cards)
    
    def __call__(self):
        print(f'remaining cards: {self.num_cards}')

        # if theres not enought cards left on deck, We fill the deck with cards again
        if(self.num_cards < 5):
            print("deck has been re-shuffle ----")
            self._cards = []

            for s in self._suits:
                for v in self._values:
                    card = Card(s, v)
                    self._cards.append(card)