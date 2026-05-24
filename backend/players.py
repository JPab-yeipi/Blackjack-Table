# Player class: it would be used by the player and the croupier
class Player():
    def __init__(self, name:str):
        self._name = name
        self._hand = []

    # getters ---------------------
    @property
    def name(self):
        return self._name
    
    @property
    def hand(self):
        return self._hand
    
    # setters ---------------------
    @name.setter
    def name(self, new_name:str):
        self._name = new_name

    # Methods ---------------------

    #

