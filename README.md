# Canoga
Revised version of the famous game Shut The Box built for OPL course at Ramapo College.

## Description of the game: 
Canoga

Canoga is a two-player dice game. This is a variant of the popular Canoga game.

## The Objective
The objective of this game is to either cover all one's squares or uncover all the opponent's squares.

## The Players
Two players play this game - one player will be the human user of your program, and the other player will be your program/computer. (Initially, you may want to implement the program for two human players to play against each other for testing purposes.)

## The Setup
The game uses a board with two rows of squares - one for the human player and the other for the opponent. Each row of squares will be numbered 1 through n, where n can be 9, 10 or 11.

## A Round
The two players take alternate turns till one of them wins.

## A Turn
During one's turn, a player repeatedly throws dice.
If all the squares 7 through n are covered, the player can choose to throw one die or both dice.
If any of the squares 7 through n is uncovered, the player must throw both dice.
The player adds the pips on the thrown die/dice. The player must now cover up a set of the player's squares that add up to the sum thrown, that are currently uncovered. For example, if the sum of the two dice is 6, the player can cover the following squares, assuming they are all uncovered at the time:
4 and 2
5 and 1
3, 2 and 1
The player may be able to cover up to 4 squares for one throw of the dice. Alternatively, the player can uncover covered squares of the opponent, subject to the same rules as above. For a given sum of dice, the player must either only cover own squares or only uncover opponent's squares, but not a combination of the two. Eventually, the player throws dice with a total number of pips for which neither of the following is possible:
no combination of uncovered squares on one's own row;
no combination of covered squares on opponent's row.
This is when the player's turn ends.

## Winning
A player wins as soon as (s)he covers all of own squares or uncovers all of the opponent's squares.

## Score
If the player wins by covering all of own squares, the winner earns a score equal to the sum of all the uncovered squares of the opponent. If the player wins by uncovering all of opponent's squares, the winner earns a score equal to the sum of all the player's covered squares. (This provides the incentive for both players to cover squares with larger numbers first.)

## First Player
Human throws dice followed by the computer. The player with the greater sum takes the first turn. Thereafter, the two players alternate within the turn. If the sum of both players is the same, human and computer throw dice repeatedly (in that order) till a first player can be determined.

## Handicap
After the first round, a handicap is placed on the game as follows:
If the winner of the previous round was also the one who took the first turn, the opponent gets the advantage;
If the winner of the previous round was not the one who took the first turn, the winner gets the advantage.
In other words, the first player of a round never gets advantage on the next round. The advantage is determined as follows: the digits of the winning score are added to a sum in the range 0 through 9. e.g., if the winning score is 27, the sum of 2 + 7 is 9. The next round starts with the coresponding square of the player with the advantage already covered, e.g., the square 9 is covered in the opponent's row if the winner of the previous round took the first turn and vice versa.
The advantage square cannot be uncovered by the opponent until the player with the advantage gets at least one turn on the current round.

## A Game
A game consists of as many rounds as the human player wants to play. After each round, the human player is asked whether she/he wants to play another round.
If yes, another round is played as described above and the process is repeated.
If no, the winner of the game is announced and the game quits. The winner of the game is the player who has won the most number of points, calculated as the sum of the points earned on all the rounds. If both the players earn the same number of points, the game is a draw.

## Computer Player's Strategy
Your computer player must play to win. It must have a strategy for each of the following:
Covering its squares;
Uncovering opponent's squares;
Whether to cover own squares or uncover opponent's squares after each throw of dice;
Determining whether to throw one die or two dice when all its squares 7 through n are covered.

## Implementation
User Interface: You must provide a user-friendly interface for the game. For C++, LISP and Prolog, ASCII graphics and command-line input are sufficient. For Java/Android project, graphical user interface is required - both for input (e.g,. buttons, not text input) and output (images, not text output).
The squares must be labeled with their numbers. The player's row and the opponent's row must be clearly marked. Both rows read from left to right.
All human inputs must be validated.
Before each player's turn, the following menu must be displayed and processed:

1. Save the game
2. Make a move
3. Ask for help (only before human player plays)
4. Quit the game
The turn played by the computer as well as the strategy it uses must be displayed on the screen, e.g.,
      The computer tossed the dice 3 and 5.
      The sum is 8.
      The computer chose to uncover opponent's squares because it had no option to cover its own squares.
      It uncovered the following opponent's squares: 4, 3, 1 to maximize the number of squares uncovered. 
    
The following must be displayed always on the screen:
human squares and score
computer squares and score
thrown dice

At the end of each round, the points earned during that round as well as total points earned in the game so far by the two players must be declared.

# Help Mode: 
When the human player is playing, the computer must provide a help mode:
If the human player asks for a recommendation, the computer must suggest:
Whether to cover own squares or uncover opponent's squares and why
The squares that must be covered (on own side) or uncovered (on opponent's side) and why
The computer must use its own playing strategy to come up with this recommendation. It must print the rationale for its recommendation, e.g.,
     I suggest you uncover your opponent's squares because..
     I suggest you uncover the following squares of the opponent 1, 3, 5 because...
   
## Generalization: 
At the beginning of each round, the human player must be asked for the size of the rows: A row can be 9, 10 or 11 squares long.
## Expected Classes:
Your implementation must have at least the following classes: Player, Human (inherits from Player), Computer (inherits from Player), Board, BoardView, Round and Game.
## Serialization:
The user should be able to suspend the game after either player has completed a turn, and resume at a later time from where the game was left off. In order to do this:
Provide the option to serialize after each player's turn has ended
When the serialization option is exercised, your program should save the current state of the game into a file and quit.
