/*
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

 I originally wrote this program in Python, and this program is one of many in which I "translated" one of my Python
 practice exercises into C in order to become more familiar with the language. As I am not as knowledgeable in C as I am
 with Python, this version is slightly different and contains some limitations. The most notable difference is that in
 the Python version, if the user input is invalid, there is a failsafe that simply prints "Invalid input" and allows the
 user to retry until they figure it out. It also accounts for "cho" and "han" not being in all lowercase. The C version
 does not contain these failsafes, and relies on the user to only enter valid inputs, or else the program will terminate.
 Also, due to the limitations on C's int datatype, if the user were to accumulate more than 2,147,483,647 mon, the score
 would become wildly inaccurate (although I suppose this does create some sort of final objective for the game, similar
 to reaching the kill-screen on the original Pac-Man).
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <math.h>


struct Dictionary
 /*
 C does not have the dictionary datatype like Python, so I had to make my own.
 */
{
    int key;
    char value[3];
};


int get_bet(int mon)
 /*
 This function gets the bet from the user. It creates a variable named bet, gets the value from the user, verifies if
 the bet is valid (over 0 and not more than they have), and finally returns the bet.
 */
{
    int bet;
    scanf("\n%d", &bet);
    assert(bet <= mon);
    assert(bet > 0);
    return bet;
}


int get_cho_or_han(void)
 /*
 This function gets the user input for whether their bet will be cho or han. Although in my Python program I return
 either 'cho' or 'han' as a string, due to the nature of C I felt it would be less problematic to just return an integer,
 so the function returns 0 for cho or 1 for han. This function does rely on the user to input either 'cho' or 'han' in
 all lowercase without any spaces, and if this is not the case, it simply terminates the program.
 */
{
    char result[3];
    scanf("\n%s", result);
    if (strcmp(result, "cho") == 0)
    {
        return 0;
    }
    if (strcmp(result, "han") == 0)
    {
        return 1;
    }
    exit(1);
}


int roll_dice(struct Dictionary japanese_numbers[6])
 /*
  This function generates 2 random numbers between 1 and 6 (simulating a dice roll) then assigns them to the variables
  dice1 and dice2. It then stores the sum of the two dice in a variable which is what the function actually returns. This
  function is also responsible for printing the result of the dice roll to the console.
 */
{
    int dice1 = rand() % 6 + 1;
    int dice2 = rand() % 6 + 1;
    int dice_sum = dice1 + dice2;
    printf("\n\n%s - %s", japanese_numbers[dice1 - 1].value, japanese_numbers[dice2 - 1].value);
    printf("\n%d - %d", dice1, dice2);
    return dice_sum;
}


int win_or_lose(int cho_or_han, int dice_sum)
 /*
 The variable win is set to either 1 (win) or 0 (lose), based on whether the user selected cho or han and the sum of the
 dice rolled. There is an if block for each possible user selection, and within each if block is another if block for
 the possibilities of the dice sum being even or odd.
 */
{
    int win;
    if (cho_or_han == 0)
    {
        if (dice_sum % 2 == 0)
        {
            win = 1;
        }
        else
        {
            win = 0;
        }
    }
    if (cho_or_han == 1)
    {
        if (dice_sum % 2 != 0)
        {
            win = 1;
        }
        else
        {
            win = 0;
        }
    }
    return win;
}


int get_bonus(int cho_or_han, int dice_sum)
 /*
 This function should only be called if the user wins, as there is no possible bonus for losing. There are two possible
 ways to get a bonus; betting cho and the dice sum being 2 (20% bonus), or betting han and the dice sum being 1 (10%
 bonus). Otherwise the bonus will remain at 0.
 */
{
    int bonus;
    if (cho_or_han == 0)
    {
        if (dice_sum == 2)
        {
            bonus = 20;
        }
        else
        {
            bonus = 0;
        }
    }
    else if (cho_or_han == 1)
    {
        if (dice_sum == 11)
        {
            bonus = 10;
        }
        else
        {
            bonus = 0;
        }
    }
    return bonus;
}


int display_result(int bet, int win, int bonus)
 /*
 This function creates a variable called winnings, which is either a positive or negative number representing the change
 to the user's mon balance. If the user lost, they lose the amount they bet. If the user won, they win double their bet,
 plus there are different possibilities of a bonus being added on. The house collects a 10% fee on all winnings, and this
 is accounted for. This function is responsible for printing all information to the console regarding winnings, and then
 returns the number that will be added to the user's balance.
 */
{
    int winnings;
    if (win == 0)
    {
        printf("\n\nYou lost! You lose %d mon.", bet);
        winnings = bet * -1;
    }
    if (win == 1)
    {
        if (bonus == 0)
        {
            printf("\n\nYou won! You take %.0f mon.", round(bet * 2));
            printf("\nThe house collects a fee of %.0f mon.", round((bet * 2) * .10));
            winnings = round((bet * 2) - ((bet * 2) * .10));
        }
        if (bonus == 10)
        {
            int gross_winnings = (bet * 2) + (bet * .10);
            printf("\n\nYou won! You take %.0f mon.", round(gross_winnings));
            printf("\nThe house collects a fee of %.0f mon.", round(gross_winnings * .10));
            winnings = round((gross_winnings) - (gross_winnings * .10));
        }
        if (bonus == 20)
        {
            int gross_winnings = (bet * 2) + (bet * .20);
            printf("\n\nYou won! You take %.0f mon.", round(gross_winnings));
            printf("\nThe house collects a fee of %.0f mon.", round(gross_winnings * .10));
            winnings = round((gross_winnings) - (gross_winnings * .10));
        }
    }
    return winnings;
}


int main(void)
{
    struct Dictionary japanese_numbers[6] = {
        {1, "一"}, {2, "二"}, {3, "三"}, {4, "四"}, {5, "五"}, {6, "六"}
    };
    
    srand(time(NULL));
    int mon = 5000;
    printf("\n\nIn this traditional Japanese dice game, two dice are rolled in a");
    printf("\nbamboo cup by the dealer sitting on the floor. The player must guess");
    printf("\nif the dice total to an even (cho) or odd (han) number.");
    while (mon > 0)
    {
        mon = round(mon);
        printf("\n\nYou have %d mon. How much do you bet? ", mon);
        int bet = get_bet(mon);
        printf("\n\nThe dealer swirls the cup and you hear the rattle of dice.");
        printf("\nThe dealer slams the cup on the floor, still covering the");
        printf("\ndice and asks for your bet.");
        printf("\n\nCHO (even) or HAN (odd)? (type your answer in all lowercase) ");
        int cho_or_han = get_cho_or_han();
        printf("\n\nThe dealer lifts the cup to reveal:");
        int dice_sum = roll_dice(japanese_numbers);
        int win = win_or_lose(cho_or_han, dice_sum);
        int bonus = 0;
        if (win == 1)
        {
            int bonus = get_bonus(cho_or_han, dice_sum);
        }
        int winnings = display_result(bet, win, bonus);
        mon += winnings;
    }
    if (mon <= 0)
    {
        printf("\n\nYou have 0 mon.");
    }
    return 0;
}
