# libraries:
from deck import *
from players import *

name = input("enter your name: ")
player = Player(name)
print(f'welcome {player.name}')

croupier = Player("Croupier")
deck = Deck()

again = "yes"
while(again[0] == 'y' or again[0] == 'Y'):
    # we check decks number of cards every round so we can re-shuffle or continue 
    deck()
    
    player.restart_hand()
    croupier.restart_hand()

    print("first hit -------------------")

    player.hit(deck)
    croupier.hit(deck)

    print("---------------------------------------------------------------------")
    print(f'croupier hand: {croupier.hand[0]}, ********* -> total value: {croupier.hand[0].value} + ???')
    print(f'player hand: {player.hand} -> total value: {player.hand_value}')
    print("---------------------------------------------------------------------")

    if (player.hand_value == 21):
        print(f"{player.name} won!")

    else:
        hitStand = ''
        hitStand = input("do you wanna hit or stand? ")

        while(hitStand[0] == 'h' or hitStand[0] == 'H'):
            player.hit(deck)
            print("---------------------------------------------------------------------")
            print(f'player hand: {player.hand} -> total value: {player.hand_value}')
            print("---------------------------------------------------------------------")
            if(player.hand_value < 21):
                hitStand = input("do you wanna hit or stand? ")
            else:
                break;

        if(player.hand_value > 21):
            print(f"{croupier.name} won!")

        else:
            print("---------------------------------------------------------------------")
            print(f'{croupier.name} hand: {croupier.hand} -> value: {croupier.hand_value}')
            print("---------------------------------------------------------------------")
            print(f'{croupier.name} turn --------')
            croupier.play(deck)

            print("---------------------------------------------------------------------")
            print(f'croupier hand: {croupier.hand} -> total value: {croupier.hand_value}')
            print(f'player hand: {player.hand} -> total value: {player.hand_value}')
            print("---------------------------------------------------------------------")

            if (croupier.hand_value > 21):
                print(f"{player.name} won!")

            elif (player.hand_value == croupier.hand_value):
                print("Its a tie")

            elif (player.hand_value > croupier.hand_value):
                print(f"{player.name} won!")

            elif (player.hand_value < croupier.hand_value):
                print(f"{croupier.name} won!")

    print("---------------------------------------------------------------------")
    again = input("play again? ")

print("Thanks for playing!")
