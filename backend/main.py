# libraries:
from deck import *
from players import *

INITIAL_PLAYER_BALANCE = 500.0
MIN_BET = 100.0

name = input("enter your name: ")
player = Player(name, money=INITIAL_PLAYER_BALANCE)
print(f'welcome {player.name}')

croupier = Player("Croupier")
deck = Deck()
deck.shuffle()

again = "yes"
first_round = True

while again.strip().lower().startswith('y'):
    deck()
    # if deck has less than 5 cards, deck().__call__ repopulates
    deck.shuffle()

    player.restart_hand()
    croupier.restart_hand()

    if player.balance < MIN_BET:
        print("You don't have enough funds to continue playing. Game over!")
        break

    print(f"Your current balance: {player.balance:.2f}")
    # --- Player bets ---
    while True:
        try:
            bet = float(input(f"How much do you want to bet? (minimum {MIN_BET}): "))
            if bet < MIN_BET:
                print(f"Minimum bet is {MIN_BET}.")
                continue
            player.place_bet(bet)
            break
        except Exception as e:
            print(f"Error: {e}")

    print("first hit -------------------")
    player.hit(deck)
    croupier.hit(deck)

    print("---------------------------------------------------------------------")
    print(f'croupier hand: {croupier.hand[0]}, ********* -> total value: {croupier.hand[0].value} + ???')
    print(f'player hand: {player.hand_str()} -> total value: {player.hand_value}')
    print("---------------------------------------------------------------------")

    # --- Player blackjack on initial deal ---
    if player.hand_value == 21:
        print(f"{player.name} has blackjack!")
        print(f"{player.name} won!")
        # Classic blackjack pays 3:2 (win 1.5x bet), so total 2.5x (bet back + 1.5x winnings)
        player.award_winnings(2.5)  
        print(f"Your new balance: {player.balance:.2f}")

    else:
        hitStand = input("do you wanna hit or stand? [hit/stand] ").strip().lower()
        while hitStand.startswith('h'):
            player.hit(deck)
            print("---------------------------------------------------------------------")
            print(f'player hand: {player.hand_str()} -> total value: {player.hand_value}')
            print("---------------------------------------------------------------------")
            if player.hand_value >= 21:
                break
            hitStand = input("do you wanna hit or stand? [hit/stand] ").strip().lower()

        if player.hand_value > 21:
            print(f"Bust! {croupier.name} won!")
            player.award_winnings(0)
            print(f"Your new balance: {player.balance:.2f}")
        else:
            print("---------------------------------------------------------------------")
            print(f'{croupier.name} hand: {croupier.hand_str()} -> value: {croupier.hand_value}')
            print("---------------------------------------------------------------------")
            print(f"{croupier.name}'s turn --------")

            # Modern blackjack dealer: hit until 17 or more
            croupier.play(deck)

            print("---------------------------------------------------------------------")
            print(f"{croupier.name} stands with: {croupier.hand_str()} -> value: {croupier.hand_value}")
            print("---------------------------------------------------------------------")

            player_total = player.hand_value
            dealer_total = croupier.hand_value

            if dealer_total > 21:
                print(f"{croupier.name} busts! {player.name} wins!")
                # Win: get bet back + winnings (here: 1x bet for regular win)
                player.award_winnings(2)  
                print(f"Your new balance: {player.balance:.2f}")
            elif player_total > dealer_total:
                print(f"{player.name} wins!")
                player.award_winnings(2)
                print(f"Your new balance: {player.balance:.2f}")
            elif player_total < dealer_total:
                print(f"{croupier.name} wins!")
                player.award_winnings(0)
                print(f"Your new balance: {player.balance:.2f}")
            else:
                print("It's a push (tie)!")
                # Push: get only bet back
                player.award_winnings(1)
                print(f"Your new balance: {player.balance:.2f}")

    again = input("\nDo you want to play another round? [yes/no]: ")

print("Thank you for playing! Goodbye!")