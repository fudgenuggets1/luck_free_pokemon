import pygame
from colors import *
from buttons import Button


class Block(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color=BLUE):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a block, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.width = width
        self.height = height

        # Make top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.x = x
        self.y = y


class Display_Screen(object):

    def __init__(self):

        self.Button_List = []
        self.Invisible_Button_List = []
        self.Block_List = pygame.sprite.Group()
        blocks = [
            [0, 0, 2, 625],
            [0, 0, 1000, 2],
            [998, 0, 2, 625],
            [0, 623, 1000, 2],
            ]

        for item in blocks:
            block = Block(item[0], item[1], item[2], item[3])
            self.Block_List.add(block)


class Sprite_Image(pygame.sprite.Sprite):

    def __init__(self, x, y, pic):

        pygame.sprite.Sprite.__init__(self)

        self.image = pic
        #self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    




        
