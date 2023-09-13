"""
Chohan by Timothy Eden
Date Last Updated: June 8, 2023

This program is based off of the description of a program called Chohan from
Al Sweigart's "The Big Book of Small Python Projects". My version includes bonuses
for certain rolls and a computer-controlled Player 2.

This was my initial version of the project for reference. The file chohan.py is my later
reimplementation of the code, although it lacks the computer-controlled player. This version
may be difficult to read and may have some errors.
"""


import random
from textwrap import dedent
japanese_numbers = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六'}


def get_bet(mon):
    """
    This function gets the player's bet through user input. It only allows the player to bet
    a positive number that is equal or lower than how much money they have. It also allows the
    input 'QUIT', which breaks the while loop that runs the game, effectively quitting the game.
    """
    while True:
        bet = input('> ')
        if bet == 'QUIT':
            return 'QUIT'
        else:
            try:
                bet = int(bet)
                assert bet <= mon
                assert bet > 0
                return bet
            except:
                print('Please enter a valid bet. (or QUIT)')
                pass


def get_cho_or_han():
    """
    This function is used when the player is asked whether the player bets cho (even) or
    han (odd). It only allows "cho" or "han" as the input, and it will just ask again if
    the input is anything else.
    """
    while True:
        result = input('> ')
        if result.lower() == 'cho':
            return 'cho'
        elif result.lower() == 'han':
            return 'han'
        else:
            print('CHO (even) or HAN (odd)?')
            pass


def roll_dice():
    """
    This function simulates the rolling of two dice, each with six sides. It does this by
    generating a random number between 1 and 6 for each dice and assigning it to a variable.
    It is also important in this game to have the sum of the two dice rolled, so it calculates
    this. This function prints what was rolled on each dice in the form of both Japanese characters
    and numerical characters.
    """
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    print('{} - {}'.format(japanese_numbers[dice1], japanese_numbers[dice2]))
    print('{} - {}'.format(dice1, dice2))
    return dice_sum


def win_or_lose(cho_or_han, dice_sum):
    """
    This function figures out whether the player won or lost, based on whether their
    guess was cho or han, and whether the sum of the dice was even or odd. If the player
    loses, Player 2 wins and vice versa. In this game, the winning player can also get a
    bonus of 10% if they bet han and the sum of the two dice was 11, or a bonus of 20% if they
    bet cho and the sum of the two dice was 2.
    """
    if cho_or_han == 'cho':
        if dice_sum % 2 == 0:
            win = True
            bonus = 0
            p2bonus = 0
            if dice_sum == 2:
                bonus = 20
            return win, bonus, p2bonus
        else:
            win = False
            bonus = 0
            p2bonus = 0
            if dice_sum == 11:
                p2bonus = 10
            return win, bonus, p2bonus
    elif cho_or_han == 'han':
        if dice_sum % 2 != 0:
            win = True
            bonus = 0
            p2bonus = 0
            if dice_sum == 11:
                bonus = 10
            return win, bonus, p2bonus
        else:
            win = False
            bonus = 0
            p2bonus = 0
            if dice_sum == 2:
                p2bonus = 20
            return win, bonus, p2bonus


def display_result(bet, win, bonus, p2bonus):
    """
    This function prints to the console the results of the game, as well as returning the
    winnings of each player, as a positive or negative number. The calculations of winnings
    account for the bonuses received by players, as well as the fee paid to the house.
    """
    if not win:
        if p2bonus == 0:
            print('You lost! You lose {} mon.'.format(bet))
            print('Player 2 takes {} mon.'.format(round(bet * 2)))
            print('The house collects a fee of {} mon.'.format(round(bet * .10)))
            winnings = -abs(bet)
            p2winnings = round((bet * 2) - (bet * .10))
            return winnings, p2winnings
        elif p2bonus == 10:
            gross_winnings = (bet * 2) + (bet * .10)
            print('You lost! You lose {} mon.'.format(bet))
            print('Player 2 takes {} mon.'.format(round(gross_winnings)))
            print('The house collects a fee of {} mon.'.format(round(gross_winnings * .10)))
            winnings = -abs(bet)
            p2winnings = round(gross_winnings - (gross_winnings * .10))
            return winnings, p2winnings
        elif p2bonus == 20:
            gross_winnings = (bet * 2) + (bet * .20)
            print('You lost! You lose {} mon.'.format(bet))
            print('Player 2 takes {} mon.'.format(round(gross_winnings)))
            print('The house collects a fee of {} mon.'.format(round(gross_winnings * .10)))
            winnings = -abs(bet)
            p2winnings = round(gross_winnings - (gross_winnings * .10))
            return winnings, p2winnings
    else:
        if bonus == 0:
            print('You won! You take {} mon.'.format(round(bet * 2)))
            print('Player 2 loses {} mon.'.format(bet))
            print('The house collects a fee of {} mon.'.format(round(bet * .10)))
            winnings = round((bet * 2) - (bet * .10))
            p2winnings = -abs(bet)
            return winnings, p2winnings
        elif bonus == 10:
            gross_winnings = (bet * 2) + (bet * .10)
            print('You won! You take {} mon.'.format(round(gross_winnings)))
            print('Player 2 loses {} mon.'.format(bet))
            print('The house collects a fee of {} mon.'.format(round(gross_winnings * .10)))
            winnings = round(gross_winnings - (gross_winnings * .10))
            p2winnings = -abs(bet)
            return winnings, p2winnings
        elif bonus == 20:
            gross_winnings = (bet * 2) + (bet * .20)
            print('You won! You take {} mon.'.format(round(gross_winnings)))
            print('Player 2 loses {} mon.'.format(bet))
            print('The house collects a fee of {} mon.'.format(round(gross_winnings * .10)))
            winnings = round(gross_winnings - (gross_winnings * .10))
            p2winnings = -abs(bet)
            return winnings, p2winnings


def __main__():
    """
    This function runs the game.
    """
    mon = 5000
    p2mon = 5000
    print(dedent('''
    In this traditional Japanese dice game, two dice are rolled in a 
    bamboo cup by the dealer sitting on the floor. The player must guess 
    if the dice total to an even (cho) or odd (han) number.'''))
    while mon > 0 and p2mon > 0:
        mon = round(mon)
        p2mon = round(p2mon)
        print('')
        print('You have {} mon.'.format(mon))
        print('Player 2 has {} mon.'.format(p2mon))
        print('How much do you bet? (or QUIT)')
        bet = get_bet(mon)
        if bet == 'QUIT':
            break
        else:
            print(dedent('''
            The dealer swirls the cup and you hear the rattle of dice.
            The dealer slams the cup on the floor, still covering the
            dice and asks for your bet.'''))
            print('')
            print('CHO (even) or HAN (odd)?')
            cho_or_han = get_cho_or_han()
            print('')
            print('The dealer lifts the cup to reveal:')
            dice_sum = roll_dice()
            win, bonus, p2bonus = win_or_lose(cho_or_han, dice_sum)
            winnings, p2winnings = display_result(bet, win, bonus, p2bonus)
            mon += winnings
            p2mon += p2winnings
    if mon <= 0:
        print('You have 0 mon.')
        print('Player 2 has {} mon.'.format(p2mon))
    elif p2mon <= 0:
        print('You have {} mon.'.format(mon))
        print('Player 2 has 0 mon.')


__main__()
