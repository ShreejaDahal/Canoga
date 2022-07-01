''' Human module'''

from player_module import Player


class Human(Player):
    '''
        Function Name: __init__
        Purpose: Initialize a Human Class
        Parameters: self, name
        Return Value: None
        Algorithm: Initialize name with default value
    '''
    def __init__(self, name):
        self.name = name
