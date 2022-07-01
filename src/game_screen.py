''' Does something cool here'''
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.app import App
import random
import os

class game_screen(Screen):
    def __init__(self):
        ''' Something goes here'''
        self.rows = 9
        self.single_player = True

    
    