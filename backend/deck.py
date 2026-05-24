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


# deck class: in this class we use card() nodes as elements in a deck -----
class Deck():

    _suits = ["spades", "hearts", "diamonds", "clubs"]
    _values = ["ace", "one", "two", "three", "four", "five", "six", 
               "seven", "eight", "nine", "jack", "queen", "king"]

    def __init__(self):
        self._cards = []

        # We fill the deck with cards
        for i in range(4):
            for j in range(13):
                card = Card(self._suits[i], self._values[j])
                self._cards.append(card)

    # getters -----------------------------------------------

    # Methods -----------------------------------------------

    # this method shuffles the cards in the deck
    def shuffle():
        return