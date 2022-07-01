
''' round_module'''
class round_module:
    '''
    Function Name: __init__
    Purpose: Initialize a Round Class
    Paramenters: self, squares, dice_rolls, next_turn,
                 current_player, next_player,first_round,
                 round_winner, winner_score, first_player,filename,
                 player1_squares, player2_squares, player1_roll1, player2_roll2, haveFirstPlayer
    Return Value: None
    Algotithm: Initialize the members
    Assistance Received: None
    '''
    def __init__(self, squares, dice_rolls, next_turn,
                 current_player, next_player,first_round, round_num,
                 round_winner,filename,new_round,
                 player1_squares, player2_squares, player1_roll1, player2_roll2, haveFirstPlayer = False , winning_score = 0
                 ):
        self.squares = squares
        self.dice_rolls = dice_rolls
        self.next_turn = next_turn
        self.current_player = current_player
        self.next_player = next_player
        self.round_winner = round_winner
        self.winning_score = winning_score
        self.player1_squares = player1_squares
        self.player2_squares = player2_squares
        self.haveFirstPlayer = haveFirstPlayer
        self.first_round = first_round
        self.player1_roll1 = player1_roll1
        self.player2_roll1 = player2_roll2
        self.resume = False
        self.filename = filename
        self.coverables = []
        self.uncoverables = []
        self.restart = False
        self.round_num = round_num
        self.new_round_first_turn = False
        self.new_round = new_round
        self.last_round_player1_first_turn = False
        self.last_round_player2_first_turn = False
