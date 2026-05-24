# libraries:
from deck import *
from players import *

name = input("enter your name: ")
player = Player(name)

print(f'welcome {player.name}')

start = input("do you wanna start playing? (y/n): ")

if (start == 'y' or start == 'Y'):
    croupier = Player("Croupier")
    deck = Deck()

    print("first hit -----------")

    player.hit(deck)
    croupier.hit(deck)

    print(f'player hand: {player.hand} -> value of hand {player.hand_value}')
    print(f'croupier hand: {croupier.hand} -> value of hand {croupier.hand_value}')

    print("second hit --------------")

    player.hit(deck)
    croupier.hit(deck)

    print(f'player hand: {player.hand} -> value of hand {player.hand_value}')
    print(f'croupier hand: {croupier.hand} -> value of hand {croupier.hand_value}')



else:
    print("closing game...")

