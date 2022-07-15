""" Author: Shreeja Dahal """
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from regex import F
from sklearn.svm import OneClassSVM
from computer_module import Computer
from round_module import round_module
from player_module import Player
from computer_module import Computer
from human_module import Human
import random
from collections import Counter
from itertools import combinations
import re
from kivy.clock import Clock
import os
import time
from datetime import date
from pathlib import Path


class MainScreen(Screen):
    pass

class Resume(Screen):
    def resumeGame(self, filename):
        '''
        Function Name: resumeGame
        Purpose: Gets information from a saved game
        Parameters: filename
        Return Value:
        Algorithm:
                1) Get the filename of the saved game
                2) Get both players' name, covered squares, uncovered squares, and scores
                3) Get current player and next player
        Assistance Received: none
        '''
        
        self.round_module = round_module
        self.Computer = Computer
        self.Player = Player
        self.Human = Human
        self.round_module.dice_rolls = []
        path = Path(filename)

        if path.is_file():
            file = open(filename)
            # read the content of the file opened
            content = file.readlines()
            self.Player.player2_name  = content[0].strip(':\n')
            self.Player.player2_board_squares = []

            player2_squares = content[1].strip('\n')
            player2_squares = player2_squares[player2_squares.index(':') + 1 : ]
            player2_squares = player2_squares.replace(" ", "")

            for i in range(0, len(player2_squares)):
                if player2_squares[i] == "*":
                    self.Player.player2_board_squares.append(True)
                elif player2_squares[i] == '0':
                    pass
                else:
                    self.Player.player2_board_squares.append(False)

            player2_score = content[2].strip('\n')
            player2_score = player2_score[player2_score.index(':') + 1 : ]
            player2_score = player2_score.replace(" ", "")
            self.Player.player2_score = int(player2_score)

            self.Player.player1_name = content[4].strip(':\n')
            self.Player.player1_board_squares = []

            player1_squares = content[5].strip('\n')
            player1_squares = player1_squares[player1_squares.index(':') + 1 : ]
            player1_squares = player1_squares.replace(" ", "")

            for i in range(0, len(player1_squares)):
                if player1_squares[i] == "*":
                    self.Player.player1_board_squares.append(True)
                elif player1_squares[i] == '0':
                    pass
                else:
                    self.Player.player1_board_squares.append(False)

            player1_score = content[6].strip('\n')
            player1_score = player1_score[player1_score.index(':') + 1 : ]
            player1_score = player1_score.replace(" ", "")
            self.Player.player1_score = int(player1_score)

            first_turn = content[8][content[8].index(':') + 1 : ].strip()

            if first_turn == 'Computer':
                self.Player.player2_first_turn = True
                self.Player.player1_last_round_first_turn =  False
                self.Player.player2_last_round_first_turn = True
                self.Player.player1_first_turn = False
            else:
                self.Player.player1_first_turn = True
                self.Player.player2_first_turn = False
                self.Player.player1_last_round_first_turn = True
                self.Player.player2_last_round_first_turn = False

            current_turn = content[9][content[9].index(':') + 1 : ].strip() 
            if current_turn == 'Computer':
                self.round_module.current_player = self.Player.player2_name
                self.round_module.next_player = self.Player.player1_name
            else:
                self.round_module.current_player = self.Player.player1_name
                self.round_module.next_player = self.Player.player2_name
            self.round_module.resume = True
            self.round_module.squares = len(self.Player.player1_board_squares)
            self.round_module.player1_squares = self.Player.player1_board_squares
            self.round_module.player2_squares = self.Player.player2_board_squares
            self.round_module.first_round = False
            self.round_module.new_round_first_turn = False
            self.round_module.new_round = False
            self.round_module.winning_score = 0

            for i in range(12, len(content)):
                number = content[i].strip('\n')
                number = number.replace(" ", "")
                self.round_module.dice_rolls.append(number)


class NewGameModeScreen(Screen):
    pass


class ComputerVSComputer(Screen):
    def get_number_rows_comp_vs_comp(self, num_squares):
        '''
        Function Name: get_number_rows_comp_vs_comp
        Purpose: Set rows for computer vs computer mode
        Parameters: num_squares
        Return Value:
        Algorithm:
                1) Set the number of squares for the game
                2) Set the name of player1 and player2
        Assistance Received: none
        '''
        self.round_module = round_module
        self.Computer = Computer
        self.Player = Player
        self.Human = Human
        self.round_module.squares = num_squares
        self.Player.player1_name = "Computer"
        self.Player.player2_name = "Computer"


class ComputerVSPlayer(Screen):
    def get_number_rows_comp_vs_player(self, num_squares):
        '''
        Function Name: get_number_rows_comp_vs_player
        Purpose: Set rows for computer vs player mode
        Parameters: num_squares
        Return Value:
        Algorithm:
                1) Set the number of squares for the game
                2) Sets player1 as the human player and player2 as the computer
        Assistance Received: none
        '''
        self.round_module = round_module
        self.Computer = Computer
        self.Player = Player
        self.Human = Human
        self.round_module.squares = num_squares
        name = self.ids.player1_name_input.text
        self.Human.name = name
        self.Player.player2_name = "Computer"

class NewGameRowScreen(Screen):
    def get_number_rows(self, num_squares):
        '''
        Function Name: get_number_rows
        Purpose: Set rows for player1 vs player2
        Parameters: num_squares
        Return Value:
        Algorithm:
                1) Set the number of squares for the game
                2) Gets player1 and player2 name
        Assistance Received: none
        '''
        self.round_module = round_module
        self.Player = Player
        self.round_module.squares = num_squares
        self.Player.player1_name = self.ids.player1_name_input.text
        self.Player.player2_name = self.ids.player2_name_input.text


class NewGameMainScreen(Screen):

    def get_dice_pic(self, die1, die2):
        '''
        Function Name: get_dice_pic
        Purpose: Changes the image of dice according to the rolled dice number
        Parameters: die1, die2
        Return Value:
        Algorithm:
                1) Gets the die1 and die2 value and sets image1 and image2 source accordingly
                2) Set die2 = 7, set image opacity to 0 to indicate that only one die has been rolled 
        Assistance Received: none
        '''
        if die1 == 1:
            self.ids.dice_image2.source = "1.png"
        elif die1 == 2:
            self.ids.dice_image2.source = "2.png"
        elif die1 == 3:
            self.ids.dice_image2.source = "3.png"
        elif die1 == 4:
            self.ids.dice_image2.source = "4.png"
        elif die1 == 5:
            self.ids.dice_image2.source = "5.png"
        elif die1 == 6:
            self.ids.dice_image2.source = "6.png"

        if die2 == 1:
            self.ids.dice_image1.source = "1.png"
        elif die2 == 2:
            self.ids.dice_image1.source = "2.png"
        elif die2 == 3:
            self.ids.dice_image1.source = "3.png"
        elif die2 == 4:
            self.ids.dice_image1.source = "4.png"
        elif die2 == 5:
            self.ids.dice_image1.source = "5.png"
        elif die2 == 6:
            self.ids.dice_image1.source = "6.png"
        elif die2 == 7:
            self.ids.dice_image1.source = "dice_0.png"


    def roll_first_time(self, playerId):
        '''
        Function Name: roll_first_time
        Purpose: Roll dice for both players at the very beginning of the game
        Parameters: playerId
        Return Value:
        Algorithm:
                1) Gets the playerId for player1
                2) For Player1 Vs Player2: Player1 rolls first followed by Player2
                3) For Player Vs Computer: Player1 rolls first followed by Computer
        Assistance Received: none
        '''
        self.ids.dice_image1.opacity = 100
        self.ids.dice_image2.opacity = 100
        if hasattr(self.round_module, 'restart') and len(self.round_module.dice_rolls) > 0 and hasattr(self.round_module, 'resume'):
            if self.Player.player1_name == "Human":
                dice = self.round_module.dice_rolls.pop(0)
                die1 = int(dice[0])
                die2 = int(dice[1])
                self.Player.player1_score = die1 + die2
                self.ids.winner.text = ""
                self.get_dice_pic(die1, die2)

                if self.Player.player2_name == "Computer":
                    dice = self.round_module.dice_rolls.pop(0)
                    die1 = int(dice[0])
                    die2 = int(dice[1])
                    self.Player.player2_score = die1 + die2
                    self.ids.winner.text = ""
                    self.get_dice_pic(die1, die2)
 
            if(self.Player.player1_score and self.Player.player2_score):
                self.who_goes_first(self.Player.player1_score, self.Player.player2_score)
        else:
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)

        #Player 1 always goes first, and when it does, player 2's rolling option is disabled
        # Once player 1 is done rolling, player 2's rolling option is turned on again, and that of player 1 is off

            if playerId == "Player 1 Roll" or playerId.text == "Player 1 Roll":
                self.ids.player2_roll.disabled = False
                self.ids.player1_roll.disabled = True
                self.Player.player1_score = die1 + die2
                self.ids.player1_score.text = str(die1 + die2)
                self.get_dice_pic(die1, die2)

                # If the player is playing against the computer
                # we want the computer to roll automatically, right after player is done rolling
                if self.Player.player2_name == "Computer":
                    die1, die2 = self.Computer.roll(self)
                    self.ids.player2_roll.disabled = True
                    self.ids.player1_roll.disabled = True
                    self.Player.player2_score = die1 + die2
                    self.ids.player2_score.text = str(die1 + die2)
                    self.get_dice_pic(die1, die2)
                if(self.Player.player1_score and self.Player.player2_score):
                    self.who_goes_first(self.Player.player1_score, self.Player.player2_score)

            #Player 2 goes next, and when it does, player 2's rolling option is disabled    
            # Once player 2 is done rolling, player 2's rolling option is turned off again

            elif playerId == "Player 2 Roll" or playerId.text == "Player 2 Roll":
                self.ids.player2_roll.disabled = True
                self.Player.player2_score = die1 + die2
                self.ids.player2_score.text = str(die1 + die2)
                self.get_dice_pic(die1, die2)

                # Once both players have a score, check who goes first
            if(self.Player.player1_score and self.Player.player2_score):
                self.who_goes_first(self.Player.player1_score, self.Player.player2_score)


    def who_goes_first(self, player_1_score, player_2_score):
        '''
        Function Name: who_goes_first
        Purpose: Compares the total scores of player1 and player2/computer and decides who goes first
        Parameters: player_1_score, player_2_score
        Return Value:
        Algorithm:
                1) Compare the total scores for both players and set current_player and next_player
        Assistance Received: none
        '''

        self.player_module = Player
        if player_1_score != player_2_score:
            if player_1_score < player_2_score:
                # setting player2_first_turn as True and player1_first_turn as False 
                self.Player.player1_first_turn = False
                self.Player.player2_first_turn = True
                if hasattr(self.Player, 'player2_name') and hasattr(self.Player, 'player1_name'):
                    self.ids.who_starts.text = self.Player.player2_name + " scored higher. \n" + self.Player.player1_name + " Score: " + str(player_1_score) + " " + self.Player.player2_name + " Score: " + str(player_2_score) +"\n"+ self.Player.player2_name + " will start the game."  
                else:
                    self.ids.who_starts.text = self.Player.player2_name + " scored higher. \n" + self.Human.name + " Score: " + str(player_1_score) + " " + self.Player.player2_name + " Score: " + str(player_2_score) +"\n"+ self.Player.player2_name + " will start the game."  
                self.ids.start.text = "OK"
                self.ids.start.disabled = False
                self.round_module.current_player = self.Player.player2_name
                self.ids.player1_roll.disabled = True
                self.ids.player2_roll.disabled = True
                
            # set the first player to true, meaning we have a player that goes first
            elif player_1_score > player_2_score:
                self.Player.player1_first_turn = True
                self.Player.player2_first_turn = False
                if hasattr(self.Player, 'player2_name') and hasattr(self.Player, 'player1_name'):
                    self.ids.who_starts.text = self.Player.player1_name + "  scored higher. \n" + self.Player.player1_name + " Score: " + str(player_1_score) + " " +  self.Player.player2_name + " Score: " +  str(player_2_score) +"\n"+ self.Player.player1_name + " will start the game."
                else:
                    self.ids.who_starts.text = self.Human.name  + " scored higher. " + self.Human.name  + " will start the game."
                self.ids.start.text = "OK"
                self.ids.start.disabled = False
                self.round_module.current_player = self.Player.player1_name
                self.ids.player1_roll.disabled = True
                self.ids.player2_roll.disabled = True
        else:
            self.ids.who_starts.text = "Both players scored " + str(player_1_score) + " It's a tie.  Please reroll"
            self.ids.player1_roll.disabled = False


    def board_setup(self):
        '''
        Function Name: board_setup
        Purpose: Set up the board for game.
        Parameters: None
        Return Value:
        Algorithm:
                1) Checks if it's a new game or a resumed game.
                2) If resumed, get the number of squares, each player's name,
                   their scores, and covered and uncovered squares
                3) If new, set the board for each players.
        Assistance Received: none
        '''

        self.round_module = round_module
        self.Player = Player
        self.Human = Human
        self.Computer = Computer
        self.ids.start_game.color = "black"
        self.ids.start_game.disabled = True
        self.round_module.player2_roll1 = False
        self.round_module.player2_roll1 = False
        self.round_module.round_num = 1
        self.ids.end_game.disabled = True
        self.ids.play_again9.disabled = True
        self.ids.play_again10.disabled = True
        self.ids.play_again11.disabled = True
        self.ids.play_again12.disabled = True
        self.round_module.new_round_first_turn = True
        self.round_module.winning_score = 0
        
        if hasattr(self.round_module,'resume') :
            if self.round_module.resume:
                self.round_module.new_round = False
                self.ids.dice_image1.source = "dice_0.png"
                self.ids.dice_image2.source = "dice_0.png"
                self.ids.player1_score.text = str(self.Player.player1_score)
                self.ids.player2_score.text = str(self.Player.player2_score)
                self.Player.player1_last_round_score = self.Player.player1_score
                self.Player.player2_last_round_score = self.Player.player2_score
                self.ids.player1_roll.disabled = True
                self.ids.player2_roll.disabled = True
                self.ids.roll.disabled = False
                for i in range(0, len(self.Player.player1_board_squares)):
                    if self.Player.player1_board_squares[i] is True:
                        iden = 'player1Square'+str(i+1)
                        self.ids[iden].disabled = True
                        self.ids[iden].background_disabled_normal= ''
                        self.ids[iden].disabled_color= 1, 1, 1, 1
                for i in range(0, len(self.Player.player2_board_squares)):
                    if self.Player.player2_board_squares[i] is True:
                        iden = 'player2Square'+str(i+1)
                        self.ids[iden].disabled = True
                        self.ids[iden].background_disabled_normal= ''
                        self.ids[iden].disabled_color= 1, 1, 1, 1

                if self.Player.player2_first_turn:
                   self.ids.winner.text = "First Turn: " + self.Player.player2_name + "\n" + "Current Turn: " + self.Player.player1_name
                else:
                   self.ids.winner.text = "First Turn: " + self.Player.player1_name + "\n" + "Current Turn: " + self.Player.player2_name
            self.ids.winner.disabled = False
        
        elif hasattr(self.Player, 'player1_board_squares'):
            self.round_module.player1_squares = [False]*self.Player.player1_board_squares
            self.round_module.player2_squares = [False]*self.Player.player1_board_squares
        else:
            self.round_module.player1_squares = [False]*self.round_module.squares
            self.round_module.player2_squares = [False]*self.round_module.squares
            self.Player.player1_last_round_score = 0
            self.Player.player2_last_round_score = 0
            self.Player.player1_score = 0
            self.Player.player2_score = 0
            self.round_module.new_round = True

        if hasattr(self.Player, 'player1_name'):
            self.ids.player1_name.text = self.Player.player1_name
        else:
            self.ids.player1_name.text = self.Human.name

        if hasattr(self.Player, 'player2_name'):
            self.ids.player2_name.text = self.Player.player2_name
        else:
            self.Player.player2_name = "Computer"
            self.ids.player2_name.text = "Computer"

        if self.round_module.squares == 9:
            self.ids.player1Square10.disabled = True
            self.ids.player1Square11.disabled = True
            self.ids.player1Square12.disabled = True
            self.ids.player2Square10.disabled = True
            self.ids.player2Square11.disabled = True
            self.ids.player2Square12.disabled = True
            self.ids.player1Square10.disabled_color = "black"
            self.ids.player1Square11.disabled_color = "black"
            self.ids.player1Square12.disabled_color = "black"
            self.ids.player2Square11.disabled_color = "black"
            self.ids.player2Square12.disabled_color = "black"
            self.ids.player2Square10.disabled_color = "black"

        if self.round_module.squares == 10:
            self.ids.player1Square11.disabled = True
            self.ids.player1Square12.disabled = True
            self.ids.player2Square11.disabled = True
            self.ids.player2Square12.disabled = True
            self.ids.player1Square11.disabled_color = "black"
            self.ids.player1Square12.disabled_color = "black"
            self.ids.player2Square11.disabled_color = "black"
            self.ids.player2Square12.disabled_color = "black"

        elif self.round_module.squares == 11:
            self.ids.player1Square12.disabled = True
            self.ids.player2Square12.disabled = True
            self.ids.player1Square12.disabled_color = "black"
            self.ids.player2Square12.disabled_color = "black"
        

        self.ids.player2_roll.disabled = True
        self.ids.save.disabled = True
        

    def start_game(self):
        '''
        Function Name: start_game
        Purpose: Disable board for player that goes second
        Parameters: None
        Return Value:
        Algorithm:
                1) By default, the player that goes second has their board disabled for the first turn.
        Assistance Received: none
        '''
        self.ids.player1_score.text = str(self.Player.player1_last_round_score)
        self.ids.player2_score.text = str(self.Player.player2_last_round_score)
        self.ids.who_starts.text = ""
        self.ids.start.disabled = True
        self.ids.player1_roll.disabled = True
        self.ids.player2_roll.disabled = True
        self.round_module.first_round = True
        self.round_module.player1_roll1 = False
        self.round_module.player2_roll1 = False
        self.ids.save.disabled = False
        self.ids.dice_image1.opacity = 100
        self.ids.dice_image2.opacity = 100

        if hasattr(self.round_module, 'restart'):
            self.round_module.new_round_first_turn = True
            self.round_module.new_round = True
            self.round_module.player1_squares = [False]*self.round_module.squares
            self.round_module.player2_squares = [False]*self.round_module.squares
            self.Player.player1_squares = self.round_module.player1_squares
            self.Player.player2_squares = self.round_module.player2_squares
            self.round_module.player1_roll1 = False
            self.round_module.player2_roll1 = False

            if self.round_module.squares == 9:
                self.ids.player1Square10.disabled = True
                self.ids.player1Square11.disabled = True
                self.ids.player1Square12.disabled = True
                self.ids.player2Square10.disabled = True
                self.ids.player2Square11.disabled = True
                self.ids.player2Square12.disabled = True

            if self.round_module.squares == 10:
                self.ids.player1Square11.disabled = True
                self.ids.player1Square12.disabled = True
                self.ids.player2Square11.disabled = True
                self.ids.player2Square12.disabled = True

            elif self.round_module.squares == 11:
                self.ids.player1Square12.disabled = True
                self.ids.player2Square12.disabled = True

             #Checking to see if player1 had the first turn
            if self.Player.player1_last_round_first_turn:
                self.ids.roll.disabled = False
                if self.round_module.round_winner == self.Player.player1_name:
                    sum = self.round_module.squares + 1
                    score = self.round_module.winning_score
                    while sum > self.round_module.squares:
                        sum = 0
                        for i in str(score):
                            sum += int(i)
                        score = str(sum)
                    self.round_module.winning_score = sum
                    self.round_module.player2_squares[sum - 1] = True
                    iden2 = 'player2Square'+str(sum)          
                    self.ids[iden2].disabled = True
                    self.ids[iden2].background_disabled_normal= ''
                    self.ids[iden2].disabled_color= 1, 1, 1, 1
                    self.ids.handicapped.text = "Handicapped placed on " + self.Player.player1_name + "\n" + self.Player.player2_name + " has " + str(sum) + " covered."
                    self.ids.handicapped.disabled = False
                elif self.round_module.round_winner == self.Player.player2_name:
                    sum = self.round_module.squares + 1
                    score = self.round_module.winning_score
                    while sum > self.round_module.squares:
                        sum = 0
                        for i in str(score):
                            sum += int(i)
                        score = str(sum)  
                    self.round_module.winning_score = sum    
                    self.round_module.player2_squares[sum - 1] = True
                    iden1 = 'player2Square'+str(sum)          
                    self.ids[iden1].disabled = True
                    self.ids[iden1].background_disabled_normal= ''
                    self.ids[iden1].disabled_color= 1, 1, 1, 1
                    self.ids.handicapped.text = "Handicapped placed on " + self.Player.player1_name + "\n" + self.Player.player2_name + " has " + str(sum) + " covered."
                    self.ids.handicapped.disabled = False

            # Checking to see if player2 had the first turn
            elif self.Player.player2_last_round_first_turn:
                if self.round_module.round_winner == self.Player.player1_name:
                    sum = self.round_module.squares + 1
                    score = self.round_module.winning_score
                    while sum > self.round_module.squares:
                        sum = 0
                        for i in str(score):
                            sum += int(i)
                        score = str(sum)
                    self.round_module.winning_score = sum
                    self.round_module.player1_squares[sum - 1] = True
                    iden2 = 'player1Square'+str(sum)          
                    self.ids[iden2].disabled = True
                    self.ids[iden2].background_disabled_normal= ''
                    self.ids[iden2].disabled_color= 1, 1, 1, 1
                    self.ids.handicapped.text = "Handicapped placed on " + self.Player.player2_name + "\n" + self.Player.player1_name + " has " + str(sum) + " covered."
                    self.ids.handicapped.disabled = False
                
                elif self.round_module.round_winner == self.Player.player2_name:
                    sum = self.round_module.squares + 1
                    score = self.round_module.winning_score
                    while sum > self.round_module.squares:
                        sum = 0
                        for i in str(score):
                            sum += int(i)
                        score = str(sum)
                    self.round_module.winning_score = sum
                    self.round_module.player1_squares[sum - 1] = True
                    iden2 = 'player1Square'+str(sum)          
                    self.ids[iden2].disabled = True
                    self.ids[iden2].background_disabled_normal= ''
                    self.ids[iden2].disabled_color= 1, 1, 1, 1
                    self.ids.handicapped.text = "Handicapped placed on " + self.Player.player2_name + "\n" + self.Player.player1_name + " has " + str(sum) + " covered."
                    self.ids.handicapped.disabled = False
                
                if self.Player.player1_first_turn is True:
                    self.ids.roll.disabled = False

                elif self.Player.player2_first_turn is True:
                    self.ids.roll.text = "OK"
                    self.ids.roll.disabled = False

        else:
            if hasattr(self.Player, 'player1_name') and hasattr(self.Player, 'player2_name'):
                if self.Player.player1_first_turn is True:
                    self.round_module.current_player = self.Player.player1_name
                    self.round_module.next_player = self.Player.player2_name
                    self.ids.player2_board.disabled = True
                    self.ids.roll.disabled = False

                elif self.Player.player2_first_turn is True:
                    self.round_module.current_player = self.Player.player2_name
                    self.round_module.next_player = self.Player.player1_name
                    self.ids.player1_board.disabled = True
                    self.ids.roll.disabled = False
            else:
                if self.Player.player1_first_turn is True:
                    self.round_module.current_player = self.Human.name
                    self.round_module.next_player = "Computer"
                    self.ids.player2_board.disabled = True
                    self.ids.roll.disabled = False

                elif self.Player.player2_first_turn is True:
                    self.round_module.current_player = "Computer"
                    self.round_module.next_player = self.Human.name
                    self.ids.player1_board.disabled = True
                    self.roll()
        
        self.Player.player1_score = 0
        self.Player.player2_score = 0  


    def roll(self):
        '''
        Function Name: roll
        Purpose: Roll the die/dice
        Parameters: None
        Return Value:
        Algorithm:
                1) Roll die/dice for players
                2) Call get_options() to get all the move options available
        Assistance Received: none
        '''
        if hasattr(self.Player, 'player2_name') and hasattr(self.Player, 'player1_name'):
            pass
        else:
            self.Player.player1_name = self.Human.name
            self.Player.player2_name = "Computer"

        if hasattr(self.round_module, 'resume') and len(self.round_module.dice_rolls) > 0 and self.round_module.resume: 
            if self.round_module.current_player == self.Player.player1_name:
                dice = self.round_module.dice_rolls.pop(0)
                die1 = int(dice[0])
                die2 = int(dice[1])
                self.Player.player1_total = die1 + die2
                self.get_dice_pic(die1, die2)
            elif self.round_module.current_player == self.Player.player2_name:
                dice = self.round_module.dice_rolls.pop(0)
                die1 = int(dice[0])
                die2 = int(dice[1])
                self.Player.player2_total = die1 + die2
                self.get_dice_pic(die1, die2)
            self.resetWidgets()

        else:
            if self.round_module.current_player == self.Player.player1_name:
                die1_pl1 = random.randint(1, 6)
                die2_pl1 = random.randint(1, 6)
                if hasattr(self.round_module, 'player1_roll1'):
                    if self.round_module.player1_roll1 is True:
                        self.Player.player1_total = die1_pl1
                        self.get_dice_pic(die1_pl1, 7)
                    else:
                        self.Player.player1_total = die1_pl1 + die2_pl1
                        self.get_dice_pic(die1_pl1, die2_pl1)
                else:
                    self.Player.player1_total = die1_pl1 + die2_pl1
                    self.get_dice_pic(die1_pl1, die2_pl1)

            # if current player is player 2
            elif self.round_module.current_player == self.Player.player2_name :
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                if self.round_module.player2_roll1 is True:
                    self.Player.player2_total = die1
                    self.get_dice_pic(die1, 7)
                elif self.round_module.player2_roll1 is not True:
                    self.Player.player2_total = die1 + die2
                    self.get_dice_pic(die1, die2)

        self.resetWidgets()
        self.get_options()


    def resetWidgets(self):
        '''
        Function Name: resetWidgets
        Purpose: disables roll,roll1,handicapped,end_game, play_again9, play_again10, play_again11, and play_again12 widgets 
        Parameters: self
        Return Value:
        Algorithm:
                disables roll,roll1,handicapped,end_game, play_again9, play_again10, play_again11, and play_again12 widgets 
        Assistance Received: none
        '''
        self.ids.roll1.disabled = True
        self.ids.roll.disabled = True
        self.ids.handicapped.disabled = True
        self.ids.end_game.disabled = True
        self.ids.play_again9.disabled = True
        self.ids.play_again10.disabled = True
        self.ids.play_again11.disabled = True
        self.ids.play_again12.disabled = True


    def act_cover(self, identifier):
        '''
        Function Name: act_cover
        Purpose: Covers the squares selected by the player 
        Parameters: identifier
        Return Value:
        Algorithm:
                1) Extracts the squares selected by the player from the Button clicked 
                2) Perform string manipulates on the string squares to eventually cover them
                3) On cover, the buttons get disabled and their values turn True
                4) Once covered, the "Help" option disappears.
        Assistance Received: none
        '''

        if self.round_module.current_player == "Computer":
            self.ids.roll.text = "OK"
        else:
            self.ids.roll.text = "Roll"
        self.ids.roll.disabled = False
        self.ids.roll1.disabled = True

        if self.ids.cover_options.children:
            for i in range(0, len(self.ids.cover_options.children)):
                for child in self.ids.cover_options.children:
                    self.ids.cover_options.remove_widget(child)
        if self.ids.uncover_options.children:
            for i in range(0, len(self.ids.uncover_options.children)):
                for child in self.ids.uncover_options.children:
                    self.ids.uncover_options.remove_widget(child)

        if isinstance(identifier, Button):
            identifier = identifier.text

        identifier = identifier.strip(')')
        identifier = identifier.strip('(')
        identifier = identifier.split(', ')
        sentence = ""
        if self.round_module.current_player == "Computer":
            pass
        else:
            sentence = self.round_module.current_player + " covered  "

        if self.round_module.current_player == self.Player.player1_name:
            for iden in identifier:
                if iden == '':
                    break
                num = int(iden)
                iden = 'player1Square'+str(iden)
                self.ids[iden].disabled = True
                self.ids[iden].background_disabled_normal= ''
                self.ids[iden].disabled_color= 1, 1, 1, 1
                self.round_module.player1_squares[num - 1] = True
                if self.round_module.current_player != "Computer":
                    sentence += str(num) + " "

        elif self.round_module.current_player == self.Player.player2_name:
                for iden in identifier:
                    if iden == '':
                        break
                    num = int(iden)
                    iden = 'player2Square'+str(iden)
                    self.ids[iden].disabled = True
                    self.ids[iden].background_disabled_normal= ''
                    self.ids[iden].disabled_color= 1, 1, 1, 1
                    self.round_module.player2_squares[num - 1] = True
                    if self.round_module.current_player != "Computer":
                        sentence += str(num) + " "
        self.ids.winner.text = sentence
        self.ids.winner.disabled = False

        if self.round_module.current_player == self.Player.player1_name:
            if hasattr(self.round_module, 'resume') and self.round_module.resume:
                pass
            else:
                if self.Player.is7Up(self, "player1", self.Player.covered_squares_player1(self)):
                    self.round_module.player1_roll1 = True
                    self.ids.roll1.disabled = False
                else:
                    self.round_module.player1_roll1 = False
                    self.ids.roll1.disabled = True
        elif self.round_module.current_player == self.Player.player2_name:
            if hasattr(self.round_module, 'resume') and self.round_module.resume:
                pass
            else:
                if self.Player.is7Up(self, "player2", self.Player.covered_squares_player2(self)):
                    if self.round_module.current_player == 'Computer':
                        self.ids.roll1.disabled = True
                        self.round_module.player2_roll1 = True
                    else:
                        self.ids.roll1.disabled = False
                        self.round_module.player2_roll1 = True
                else:
                    self.round_module.player2_roll1 = False
                    self.ids.roll1.disabled = True
        #here what we can do instead is, if it's the first round, onyl check if the coverables are covered, else check both

        if self.round_module.first_round is False:
            self.checkIfWon()
        
        else:
            self.checkIfAllCovered()

        self.ids.help.disabled = True


    def act_uncover(self, identifier):
        '''
        Function Name: act_uncover
        Purpose: Uncovers the squares selected by the player
        Parameters: identifier
        Return Value:
        Algorithm:
                1) Extracts the squares selected by the player from the Button clicked 
                2) Perform string manipulates on the string squares to eventually uncover them
                3) On uncover, the buttons get abled again and their values turn False
                4) Once uncovered, the "Help" option disappears.
        Assistance Received: none
        '''

        if self.round_module.current_player == "Computer":
            self.ids.roll.text = "OK"
        else:
            self.ids.roll.text = "Roll"
        self.ids.roll.disabled = False
        self.ids.roll1.disabled = True
        sentence = ""
        if self.ids.cover_options.children:
            for i in range(0, len(self.ids.cover_options.children)):
                for child in self.ids.cover_options.children:
                    self.ids.cover_options.remove_widget(child)
        if self.ids.uncover_options.children:
            for i in range(0, len(self.ids.uncover_options.children)):
                for child in self.ids.uncover_options.children:
                    self.ids.uncover_options.remove_widget(child)

        if isinstance(identifier, Button):
            identifier = identifier.text

        if self.round_module.current_player == "Computer":
            pass
        else:
            sentence = self.round_module.current_player + " uncovered "
        identifier = identifier.strip(')')
        identifier = identifier.strip('(')
        identifier = identifier.split(', ')

        if self.round_module.current_player == self.Player.player1_name:
                for iden in identifier:
                    if iden == '':
                        break
                    num = int(iden)
                    iden = 'player2Square'+iden
                    self.ids[iden].disabled = False
                    self.round_module.player2_squares[num - 1] = False
                    if self.round_module.current_player != "Computer":
                        sentence += str(num) + " "

        elif self.round_module.current_player == self.Player.player2_name:
                for iden in identifier:
                    if iden == '':
                        break
                    num = int(iden)
                    iden = 'player1Square'+iden
                    self.ids[iden].disabled = False
                    self.round_module.player1_squares[num - 1] = False
                    if self.round_module.current_player != "Computer":
                        sentence += str(num) + " "
        self.ids.winner.text = sentence
        self.ids.winner.disabled = False
            
        if self.round_module.current_player == self.Player.player1_name:
            if hasattr(self.round_module, 'resume') and self.round_module.resume:
                pass
            else:
                if self.Player.is7Up(self, "player1", self.Player.covered_squares_player1(self)):
                    self.round_module.player1_roll1 = True
                    self.ids.roll1.disabled = False
                else:
                    self.round_module.player1_roll1 = False
                    self.ids.roll1.disabled = True
        elif self.round_module.current_player == self.Player.player2_name:
            if hasattr(self.round_module, 'resume') and self.round_module.resume:
                pass
            else:
                if self.Player.is7Up(self, "player2", self.Player.covered_squares_player2(self)):
                    if self.round_module.current_player == 'Computer':
                        self.ids.roll1.disabled = True
                        self.round_module.player2_roll1 = True
                    else:
                        self.ids.roll1.disabled = False
                        self.round_module.player2_roll1 = True
                else:
                    self.round_module.player2_roll1 = False
                    self.ids.roll1.disabled = True
       
        if self.round_module.first_round is False:
            self.checkIfWon()
        else:
            self.checkIfAllCovered()
        self.ids.help.disabled = True
    

    def get_options(self):
        '''
        Function Name: get_options
        Purpose: Get all the options available to make a move
        Parameters: identifier
        Return Value:
        Algorithm:
                1) Extract information on all the coverable and uncoverable squares for each player
                2) Call getAllCombinations() function to get all possible combinations for the squares extracted 
                3) Display cover and uncover options in the form of buttons for each turn. 
        Assistance Received: none
        '''

        self.ids.uncovers.disabled = False
        self.ids.covers.disabled = False
        self.ids.roll.disabled = True
        self.ids.roll1.disabled = True
        sentence = ""

        if hasattr(self.Player, 'player2_name') and hasattr(self.Player, 'player1_name'):
            pass
        else:
            self.Player.player1_name = self.Human.name
            self.Player.player2_name = "Computer"

        if self.round_module.current_player == self.Player.player1_name:
            self.round_module.coverables = self.getAllCombinations(self.Player.uncovered_squares_player1(self), self.Player.player1_total)
            score = self.round_module.winning_score
            uncoverables = self.Player.covered_squares_player2(self)
            if(score in uncoverables):
                uncoverables.remove(score) 
            self.round_module.uncoverables = self.getAllCombinations(uncoverables, self.Player.player1_total)

        elif self.round_module.current_player == self.Player.player2_name:
            self.round_module.coverables = self.getAllCombinations(self.Player.uncovered_squares_player2(self), self.Player.player2_total)
            score =  self.round_module.winning_score
            uncoverables = self.Player.covered_squares_player1(self)
            if(score in uncoverables):
                uncoverables.remove(score)
            self.round_module.uncoverables = self.getAllCombinations(uncoverables, self.Player.player2_total)

        if len(self.round_module.coverables) == 0 or len(self.round_module.uncoverables) == 0:
            self.checkIfNextRound(self.round_module.coverables, self.round_module.uncoverables)

        if self.round_module.current_player == "Computer":
            hint = False
            moves, cover_or_uncover, message = self.Computer.make_a_move(self,self.round_module.coverables, self.round_module.uncoverables, hint)           
            if cover_or_uncover:
                if moves:
                    sentence += self.round_module.current_player + " covered  " + str(moves) + message 
                    self.ids.who_starts.text= str(sentence)
                    self.ids.who_starts.disabled = False
                    self.act_cover(str(moves))
            else:
                if moves:
                    sentence += self.round_module.current_player + " uncovered " + str(moves) + message 
                    self.ids.who_starts.text = str(sentence)
                    self.ids.who_starts.disabled = False
                    self.act_uncover(str(moves))

        else:
            for button in self.round_module.coverables:
                buttons1 = Button(
                    text= str(button),
                    size_hint= (0.7, 0.7),
                    background_disabled_normal = '',
                    background_color = 'purple',
                )
                self.ids.cover_options.add_widget(buttons1)
                buttons1.bind(on_press= self.act_cover)
                self.ids.cover_options.disabled = False

            for button in self.round_module.uncoverables:
                buttons2 = Button(
                    text= str(button),
                    size_hint= (0.7, 0.7),
                    background_disabled_normal = '',
                    background_color = 'purple'
                )
                self.ids.uncover_options.add_widget(buttons2)
                buttons2.bind(on_press= self.act_uncover)
                self.ids.uncover_options.disabled = False
            self.ids.help.disabled = False
            self.ids.roll1.disabled = True


    def getAllCombinations(self, list_squares, K):
        '''
        Function Name: getAllCombinations
        Purpose: From the list of squares available for cover/uncover, 
                 get all the possible combinations that add up to the target K
        Parameters: list_squares, K
        Return Value:
        Algorithm:
                1) Call findPlairs(), findThree(), and findFour() functions to get upto 4 combinations.
        Assistance Received: none
        '''

        all_possible_combinations = []
        # an empty square list means either this is the first round
        # or we have a winner

        if K in list_squares:
            all_possible_combinations.append(K)

        if len(list_squares) == 0:
            return []
        else:
            pairs = self.findPairs(list_squares, K)
            triples = self.findThree(list_squares, K)

            for pair in pairs:
                all_possible_combinations.append(pair)

            for triple in triples:           
                all_possible_combinations.append(triple)

            if K == 10 or K == 11 or K == 12:
                result = self.findFour(list_squares, K)
                if result is not None:
                    all_possible_combinations.append(result)

            return all_possible_combinations

    def findPairs(self,list_squares, K):
        '''
        Function Name: findPairs
        Purpose: Find two unique numbers from the list_squares that add up to the target K
        Parameters: list_squares, K
        Return Value:
        Algorithm:
                1) Call python's in built itertools.combinations() to get the unique pairs
        Assistance Received: geeksforgeeks on itertools.combinations()
        '''

        def test(val):
            return sum(val) == K

        res = tuple(filter(test, combinations(list_squares, 2)))
        return res

    def findThree(self,list_squares, K):
        '''
        Function Name: findThree
        Purpose: Find three unique numbers from the list_squares that add up to the target K
        Parameters: list_squares, K
        Return Value:
        Algorithm:
                1) Call python's in built itertools.combinations() to get the unique pairs
        Assistance Received: geeksforgeeks on itertools.combinations()
        '''

        def test(val):
            return sum(val) == K

        res = tuple(filter(test, combinations(list_squares, 3)))
        return res

    def findFour(self, list_squares, K):
        '''
        Function Name: findFour
        Purpose: Find four unique numbers from the list_squares that add up to the target K
        Parameters: list_squares, K
        Return Value:
        Algorithm:
                1) Call python's in built itertools.combinations() to get the unique pairs
        Assistance Received: geeksforgeeks on itertools.combinations()
        '''
        if K == 10:
            list_fours = (1,2,3,4)
            if all(item in list_squares for item in list_fours):
                return (1,2,3,4)
        elif K == 11:
            list_fours = (1,2,3,5)
            if all(item in list_squares for item in list_fours):
                return (1,2,3,5)
        elif K == 12:
            list_fours = (1,2,3,6)
            if all(item in list_squares for item in list_fours):
                return (1,2,3,6)

    def checkIfWon(self):
        '''
        Function Name: checkIfWon
        Purpose: Checks to see if a player won the round
        Parameters: None
        Return Value:
        Algorithm:
                1) Check to see if any player covered all their squares or uncovered all their squares.
                2) If won, display message on the screen and disable all other widgets
        Assistance Received: None
        '''
        if self.round_module.current_player == self.Player.player1_name:
            self.Player.player1_score = 0
            self.Player.player2_score = 0
            if self.Player.isCovered_player1(self) or self.Player.isUncovered_player2(self):
                if self.Player.isCovered_player1(self):
                    self.round_module.round_winner = self.Player.player1_name
                    for item in self.Player.uncovered_squares_player2(self):
                        self.Player.player1_score += int(item)
                        self.Player.player1_last_round_score += int(item)
                    self.round_winner_score = self.Player.player1_score
                    self.round_module.winning_score = self.round_winner_score
                    self.ids.winner.text = self.Player.player1_name + " covered all their squares and is declared the winner for this round. \n Current score is:" + " Human:  " + str(self.Player.player1_score) + "  Computer:  "+ str(self.Player.player2_score) +  " Play again? \n If yes, select a square."
                    self.ids.winner.disabled = False
                    self.ids.player1_score.text = str(self.Player.player1_last_round_score )
                elif self.Player.isUncovered_player2(self):
                    self.round_module.round_winner = self.Player.player1_name
                    for item in self.Player.covered_squares_player1(self):
                        self.Player.player1_last_round_score += int(item)
                        self.Player.player1_score += int(item)
                    self.round_winner_score = self.Player.player1_score
                    self.round_module.winning_score = self.round_winner_score
                    self.ids.winner.text = self.Player.player1_name + " uncovered all of " + self.Player.player2_name + "'s squares and is declared the winner for this round. \n Current score is:" + " Human: " + str(self.Player.player1_score) + "  Computer:  "+ str(self.Player.player2_score) +  " Play again? \n If yes, select a square."
                    self.ids.winner.disabled = False
                    self.ids.player1_score.text = str(self.Player.player1_last_round_score)
                self.resetWidgetsAfterGame()


        elif self.round_module.current_player == self.Player.player2_name:
            self.Player.player1_score = 0
            self.Player.player2_score = 0
            if self.Player.isCovered_player2(self) or self.Player.isUncovered_player1(self):
                if self.Player.isCovered_player2(self):
                    self.round_module.round_winner = self.Player.player2_name
                    for item in self.Player.uncovered_squares_player1(self):
                        self.Player.player2_score += int(item)
                        self.Player.player2_last_round_score += int(item)
                    self.round_winner_score = self.Player.player2_score
                    self.ids.player2_score.text = str(self.Player.player2_last_round_score)
                    self.ids.who_starts.text = ""
                    self.ids.winner.text = self.Player.player2_name + " covered all their squares and is declared the winner for this round. \n Current score is:" + " Human:  " + str(self.Player.player1_score) + "  Computer:  "+ str(self.Player.player2_score) +  " Play again? \n If yes, select a square."
                    self.ids.winner.disabled = False
                elif self.Player.isUncovered_player1(self):
                    self.round_module.round_winner = self.Player.player2_name
                    for item in self.Player.covered_squares_player2(self):
                        self.Player.player2_last_round_score += int(item)
                        self.Player.player2_score += int(item)
                        self.ids.who_starts.text = ""
                    self.ids.winner.text += self.Player.player2_name + " uncovered all of " + self.Player.player1_name + "'s square and is declared the winner for this round. \n Current score is:" + "  Human:  " + str(self.Player.player1_score) + " Computer:  "+ str(self.Player.player2_score) +  " Play again? \n If yes, select a square."
                    self.ids.winner.disabled = False
                    self.ids.player2_score.text = str(self.Player.player2_last_round_score )
                self.resetWidgetsAfterGame()


    def checkIfNextRound(self, coverables, uncoverables):
        '''
        Function Name: checkIfNextRound
        Purpose: To change turns/rounds
        Parameters: coverables, uncoverables
        Return Value:
        Algorithm:
                1) If there are no more coverables or uncoverables left, the next_player gets to roll the die/dice
                2) Display message on the screen that tells which player's turn it is now
        Assistance Received: None
        '''
        if (len(coverables) == 0) and (len(uncoverables) == 0):
            if self.round_module.current_player == self.Player.player1_name:
                self.round_module.current_player, self.round_module.next_player = self.Player.player2_name, self.Player.player1_name
                self.ids.player2_board.disabled = False
                self.round_module.new_round_first_turn = False
                self.round_module.new_round = False
                self.Player.player1_first_turn = False
                self.round_module.winning_score = 0
                self.ids.who_starts.text = ""
                self.ids.who_starts.disabled = True
                self.ids.roll.disabled = False
                self.checkIfWon()

            elif self.round_module.current_player == self.Player.player2_name:
                self.round_module.current_player, self.round_module.next_player = self.Player.player1_name, self.Player.player2_name
                self.ids.player1_board.disabled = False
                self.round_module.new_round_first_turn = False
                self.round_module.new_round = False
                self.Player.player2_first_turn = False
                self.round_module.winning_score = 0
                self.ids.who_starts.text = ""
                self.ids.who_starts.disabled = True
                self.ids.roll.disabled = False
                self.checkIfWon()

        self.ids.turn.text =  self.round_module.current_player + "'s turn"
        self.ids.turn.disabled = False
        self.ids.roll.text = "Roll"
        self.ids.roll.disabled = False
        self.ids.winner.disabled = True

    def saveGame(self):
        '''
        Function Name: saveGame
        Purpose: To save the current game
        Parameters:
        Return Value:
        Algorithm:
                1) Create a file according named as the current time
                2) Record both players' name, squares, and scores
                3) Record the player that rolled first and the next player as well
                4) Record all the die/dice rolled so far.
        Assistance Received: None
        '''
        self.ids.roll1.disabled = True
        self.ids.roll.disabled = True
        self.ids.turn.disabled = True
        self.ids.player1_board.disabled = True
        self.ids.player1_board.disabled_color = "black"
        self.ids.player2_board.disabled = True
        self.ids.player2_board.disabled_color = "black"
        self.ids.covers.disabled = True
        self.ids.uncovers.disabled = True
        self.ids.winner.disabled = True
        number = random.randrange(1000)
        filename = str(number)

        with open(filename+'.txt', 'w') as f:

            #for player2
            player2_squares = self.round_module.player2_squares
            f.write(self.Player.player2_name)
            f.write(": ")
            f.write("\n")
            f.write(" Squares: ")
            for i in range(0, len(player2_squares)):
                if player2_squares[i]:
                    f.write("* ")
                else:
                    f.write(str(i+1)+ " ")
            f.write("\n")
            f.write("Score: ")
            f.write(str(self.Player.player2_last_round_score))
            f.write("\n")
            f.write("\n")

            #for player1
            player1_squares = self.round_module.player1_squares
            f.write(self.Player.player1_name)
            f.write(": ")
            f.write("\n")
            f.write(" Squares: ")
            for i in range(0, len(player1_squares)):
                if player1_squares[i]:
                    f.write("* ")
                else:
                    f.write(str(i+1) + " ")

            f.write("\n")
            f.write(" Score: ")
            f.write(str(self.Player.player1_last_round_score))
            f.write("\n")
            f.write("\n")

            if self.Player.player1_first_turn:
                first_turn = "First Turn: " + self.Player.player1_name
                f.write(first_turn)
                f.write("\n")
            elif self.Player.player2_first_turn:
                first_turn = "First Turn: " + self.Player.player2_name
                f.write(first_turn)
                f.write("\n")

            next_turn = "Next Turn: " + self.round_module.current_player
            f.write(next_turn)
            f.write("\n")

            f.write("Dice:")
            f.write("\n")
            for item in self.round_module.dice_rolls:
                f.write(str(item))
                f.write("\n")

    def getHelp(self):
        '''
        Function Name: getHelp
        Purpose: To get suggestions on what move to make next
        Parameters: None
        Return Value: None
        Algorithm:
                1) Call make_a_move() function from the computer_module and get the best move
                2) Display message on the screen suggesting a move to the Player.
                3) Only human players can get help.
        Assistance Received: None
        '''
        self.round_module = round_module
        self.Computer = Computer

        if self.round_module.current_player == "Computer":
            hint = False
            self.ids.winner.text = "Only human players can get help! "
            self.ids.winner.disabled = False
        else:
            hint = True
            moves, cover_or_uncover, messages = self.Computer.make_a_move(self, self.round_module.coverables, self.round_module.uncoverables, hint)
            self.ids.winner.text = messages
            self.ids.winner.disabled = False

    def restart(self, square):
        '''
        Function Name: restart
        Purpose: To restart the game if the players decides to play another round
        Parameters: self
        Return Value:
        Algorithm:
                1) Enable all the squares and set default values for all other variables
                2) Give players advantage depending on the handicap situation
        Assistance Received: none
        '''
        self.round_module.restart = True
        self.ids.end_game.disabled = True
        iden1 = ""
        iden2 = ""
        for i in range(0, 12):
           iden1 = 'player1Square'+str(i+1)
           iden2 = 'player2Square'+str(i+1)
           self.ids[iden1].disabled = False        
           self.ids[iden2].disabled = False
           self.ids[iden1].background_color = "purple"
           self.ids[iden2].background_color = "purple"
        self.ids.player1_board.disabled = False
        self.ids.player2_board.disabled = False
        self.ids.winner.text = ""
        self.ids.winner.disabled = True
        self.ids.play_again9.disabled = True
        self.ids.play_again10.disabled = True
        self.ids.play_again11.disabled = True
        self.ids.play_again12.disabled = True
        self.ids.player1_roll.disabled = False
        self.ids.player2_roll.disabled = False
        self.round_module.player1_roll1 = False
        self.round_module.player2_roll1 = False
        self.ids.start.disabled = True
        self.ids.save.disabled = False
        self.round_module.round_num += 1
        self.ids.round.text = 'Round ' + str(self.round_module.round_num)
        self.ids.round.disabled = False
        if self.round_module.resume:
            if len(self.round_module.dice_rolls) > 0:
                self.round_module.resume = True
            else:
                self.round_module.resume = False
        self.round_module.new_round_first_turn = True
        self.round_module.squares = square
        self.ids.who_starts.text = ""
        self.ids.who_starts.disabled = False

        if self.round_module.round_winner == self.Player.player1_name:
            self.round_module.winning_score = self.Player.player1_score
        else:
            self.round_module.winning_score = self.Player.player2_score
        
        if self.Player.player1_first_turn:
            self.Player.player1_last_round_first_turn == True
            self.Player.player2_last_round_first_turn == False
        else:
            self.Player.player1_last_round_first_turn == False
            self.Player.player2_last_round_first_turn == True
        
        self.Player.player1_first_turn = False
        self.Player.player2_first_turn = False


    def end_game(self):
        '''
        Function Name: end_game
        Purpose: End the game and display the scores for both players
        Parameters: self
        Return Value:
        Algorithm:
                1) End the game and display winner and scores for both players
        Assistance Received: none
        '''
        self.ids.end_game.disabled = True
        self.ids.play_again9.disabled = True
        self.ids.play_again10.disabled = True
        self.ids.play_again11.disabled = True
        self.ids.play_again12.disabled = True
        #self.ids.play_again.disabled = True

        if self.Player.player1_last_round_score > self.Player.player2_last_round_score:
            message = "The winner of the game is: " + self.Player.player1_name + "\n"

        elif self.Player.player2_last_round_score > self.Player.player1_last_round_score:
            message = "The winner of the game is: " + self.Player.player2_name + "\n"

        else:
            message = "The overall game was a tie between both the players."

        message += self.Player.player1_name + " : " + str(self.Player.player1_last_round_score) + "\n"
        message += self.Player.player2_name + " : " + str(self.Player.player2_last_round_score) + "\n"
        self.ids.winner.text = message
        self.ids.winner.disabled = False

    def re_roll(self):
        '''
        Function Name: re_roll
        Purpose: To re_roll the dice for both players until one of them wins
        Parameters: self
        Return Value:
        Algorithm: Reset default values for rolls
        Assistance Received: none
        '''
        self.ids.re_roll.disabled = True
        self.ids.player1_roll.disabled = False
        self.ids.player2_roll.disabled = False
        self.ids.who_starts.text = ""
        self.ids.who_starts.disabled = True

    def checkIfAllCovered(self):

        '''Function Name: checkIfAllCovered
        Purpose: To check if all squares are covered for a given player
        Parameters: self
        Return Value: None 
        Algorithm: If all squares covered for a player, the player wins
        Assistance Received: None
        '''

        if self.round_module.current_player == self.Player.player1_name:
            if self.Player.isCovered_player1(self):
                self.ids.winner.text = str(self.Player.player1_name) + " covered all its square and is declared the winner of this round. \n Current score is:" + " Human:  " + str(self.Player.player1_score) + "  Computer:  "+ str(self.Player.player2_score) +  " Play again? \n If yes, select a square."
                self.ids.winner.disabled = False
                self.resetWidgetsAfterGame()


        elif self.round_module.current_player == self.Player.player2_name:
            if self.Player.isCovered_player2(self):
                self.ids.winner.text = str(self.Player.player2_name) + " covered all its square and is declared the winner of this round. \n Current score is:" + " Human:  " + str(self.Player.player1_score) + "  Computer:  "+ str(self.Player.player2_score) +  " Play again? \n If yes, select a square."
                self.ids.winner.disabled = False
                self.resetWidgetsAfterGame()


    def resetWidgetsAfterGame(self):
        '''
        Function Name: resetWidgetsAfterGame
        Purpose: enable widgets after a round has a winner
        Parameters: self
        Return Value:
        Algorithm:
                disables roll,roll1,turn, dice_image1, dice_image2,save,
                handicapped,end_game, play_again9, play_again10, play_again11, and play_again12 widgets 
        Assistance Received: none
        '''

        self.ids.roll1.disabled = True
        self.ids.roll.disabled = True
        self.ids.turn.disabled = True
        self.ids.dice_image1.opacity = 0
        self.ids.dice_image2.opacity = 0
        self.ids.save.disabled = True
        self.ids.play_again9.disabled = False
        self.ids.play_again10.disabled = False
        self.ids.play_again11.disabled = False
        self.ids.play_again12.disabled = False
        self.ids.end_game.disabled = False
        

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("kvfile.kv")

class STBCanoga(App):
    def build(self):
        return kv


if __name__ == "__main__":
    STBCanoga().run()

