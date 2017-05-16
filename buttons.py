import pygame, Functions, random, time
from colors import *

class Button():

    def __init__(self, msg, x, y, w, h, color, highlight, action):

        self.msg = msg
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.regular_color, self.highlight_color = color, highlight
        self.action = action
        self.color = self.regular_color
        self.mouse_on = False

    @staticmethod
    def update(screen, list):

        for button in list:
            pygame.draw.rect(screen, button.color, (button.x, button.y, button.w, button.h))
            pygame.draw.rect(screen, BLACK, (button.x, button.y, button.w, button.h), 2)        
            x = button.w / 2
            y = button.h / 2
            Functions.text_to_screen(screen, button.msg, button.x+x, button.y+y, 20)

    def mouse_over(self):
        self.color = self.highlight_color
        self.mouse_on = True
    def mouse_off(self):
        self.color = self.regular_color
        self.mouse_on = False
    def do_action(self):
        pass
