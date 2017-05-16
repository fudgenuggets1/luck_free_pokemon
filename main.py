import pygame, battle_engine
from interaction import interaction
from colors import *
from pokedex import *
from moves import *

pygame.init()

screen = pygame.display.set_mode((1000, 625))

clock = pygame.time.Clock()
FPS = 20
total_frames = 0

while True:

	screen = pygame.display.get_surface()

	screen.fill((200, 200, 200))

	interaction(screen)

	battle_engine.update_display(screen)
	
	pygame.display.set_caption("Hax Free Pokemon     FPS: %s" % int(clock.get_fps()))
	pygame.display.flip()
	clock.tick(FPS)
	total_frames += 1
