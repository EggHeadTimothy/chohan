"""
Chohan by Timothy Eden
Date Last Updated: September 10, 2023

This program is based off of the description of a program called Chohan from Al Sweigart's "The Big Book of Small Python
Projects". These are the project specifications:

---
Cho-han is a dice game played in gambling houses of feudal Japan. Two six-sided dice are rolled in a cup, and gamblers
must guess if the sum is even (cho) or odd (han). The house takes a small cut of all winnings.

Your code should implement the following:
- The player begins with 5000 mon
- The game automatically ends when the player runs out of money
- After the dice are rolled, the output should include a display of the Japanese words for the numbers one to six for
each die as well as the integer
- The house takes a 10 % fee on all winnings
- The program should prevent the player from betting more money than they have
- Player bonus 1: if the player bets odd and rolls eleven ( 5 - 6 ) or ( 6 - 5 ), the player gets a 10% bonus
- Player bonus 2: if the player bets cho and rolls snake eyes ( 1 - 1 ), the player gets a 20% bonus
---

I previously wrote this program in Python a few months back, and even created an alternate version involving a
computer-controlled player (not included in this version). Recently, in my quest to become familiar with C, I rewrote
this program in C as practice, and in doing that I noticed that my original Python version could be improved. This code
is my new rendition of the project, and it is based off of my C program. The most notable improvement is a separate
function for calculating the bonus instead of having the win_or_lose function calculate it, as that code was messy and
difficult to read.
"""


import random
japanese_numbers = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六'}


def get_bet(mon):
    """
    This function gets the bet from the user. It first takes in the input, then it runs the input through three tests
    to ensure it is valid; the input can be converted to an integer, the bet is not more than they have, and it is not
    0 or a negative number. If these conditions are not met, the user must try again.
    """
    while True:
        bet = input('')
        try:
            bet = int(bet)
            assert bet <= mon
            assert bet > 0
            return bet
        except:
            print('Invalid input.')
            pass


def get_cho_or_han():
    """
    This function gets the user input for whether they will bet on cho or han. Once a valid input is received, the
    function returns the corresponding string to the user's selection (either 'cho' or 'han).
    """
    while True:
        result = input('')
        if result.lower() == 'cho':
            return 'cho'
        if result.lower() == 'han':
            return 'han'
        else:
            print('Invalid input.')
            pass


def roll_dice():
    """
    This function creates a variable for each of the dice, generates a random number between 1 and 6 to assign to each
    variable (simulating a dice roll), then stores the sum of the two dice in a separate variable. After printing the
    result of the dice roll to the console, it returns the sum of the two dice.
    """
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    print('{} - {}'.format(japanese_numbers[dice1], japanese_numbers[dice2]))
    print('{} - {}'.format(dice1, dice2))
    return dice_sum


def win_or_lose(cho_or_han, dice_sum):
    """
    The variable win is either False or True. This function walks through all the different possibilites of whether the
    user bet cho or han, and whether the dice sum was even or odd, and returns the result.
    """
    win = False
    if cho_or_han == 'cho':
        if dice_sum % 2 == 0:
            win = True
        else:
            win = False
    if cho_or_han == 'han':
        if dice_sum % 2 != 0:
            win = True
        else:
            win = False
    return win


def get_bonus(cho_or_han, dice_sum):
    """
    This function should only be called if the user wins. If they bet cho and the dice sum is 2, they will receive a 20%
    bonus. If they bet han and the dice sum is 11, they will receive a 10% bonus. Otherwise, the bonus remains at 0.
    """
    bonus = 0
    if cho_or_han == 0:
        if dice_sum == 2:
            bonus = 20
    if cho_or_han == 1:
        if dice_sum == 11:
            bonus = 10
    return bonus


def display_result(bet, win, bonus):
    """
    The variable winnings is a positive or negative number representing the change to the user's mon balance. If the
    user loses, they lose how much they bet. If they win, they take double their bet, plus whatever bonus they got if
    applicable. The house collects a 10% fee on all winnings and this is also accounted for. This function prints the
    results of the game to the console, as well as returning the variable winnings, which is subsequently added to the
    mon variable.
    """
    winnings = 0
    if not win:
        print('\nYou lost! You lose {} mon.'.format(bet))
        winnings = bet * -1
    if win:
        if bonus == 0:
            print('\nYou won! You take {} mon.'.format(round(bet * 2)))
            print('The house collects a fee of {} mon.'.format(round((bet * 2) * .10)))
            winnings = round((bet * 2) - ((bet * 2) * .10))
        if bonus == 10:
            gross_winnings = (bet * 2) + (bet * .10)
            print('\nYou won! You take {} mon.'.format(round(gross_winnings)))
            print('The house collects a fee of {} mon.'.format(round(gross_winnings * .10)))
            winnings = round(gross_winnings - (gross_winnings * .10))
        if bonus == 20:
            gross_winnings = (bet * 2) + (bet * .20)
            print('\nYou won! You take {} mon.'.format(round(gross_winnings)))
            print('The house collects a fee of {} mon.'.format(round(gross_winnings * .10)))
            winnings = round(gross_winnings - (gross_winnings * .10))
    return winnings


def main():
    mon = 5000
    print('\nIn this traditional Japanese dice game, two dice are rolled in a')
    print('bamboo cup by the dealer sitting on the floor. The player must guess')
    print('if the dice total to an even (cho) or odd (han) number.')
    while mon > 0:
        mon = round(mon)
        print('\nYou have {} mon. How much do you bet?'.format(mon))
        bet = get_bet(mon)
        print('\nThe dealer swirls the cup and you hear the rattle of dice.')
        print('The dealer slams the cup on the floor, still covering the')
        print('dice and asks for your bet.')
        print('\nCHO (even) or HAN (odd)?')
        cho_or_han = get_cho_or_han()
        print('\nThe dealer lifts the cup to reveal:')
        dice_sum = roll_dice()
        win = win_or_lose(cho_or_han, dice_sum)
        bonus = 0
        if win:
            bonus = get_bonus(cho_or_han, dice_sum)
        winnings = display_result(bet, win, bonus)
        mon += winnings
    if mon <= 0:
        print('\nYou have 0 mon.')


if __name__ == '__main__':
    main()
