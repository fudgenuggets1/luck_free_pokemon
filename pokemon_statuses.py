import pygame
from colors import *

brn = pygame.image.load('images/burn.png')
par = pygame.image.load('images/paralyze.png')
psn = pygame.image.load('images/toxic.png')
slp = pygame.image.load('images/sleep.png')

BattleStatuses = {
	'brn': {
		'image': brn,
		'name': 'Burn',
		'color': ORANGE,
		'effectType': 'Status',
		'damage': 0.0625,
		'spe': 1,
	},
	'par': {
		'image': par,
		'name': 'Paralyze',
		'color': GOLD,
		'effectType': 'Status',
		'damage': 0,
		'spe': 0.5,
	},
	'psn': {
		'image': psn,
		'name': 'Poison',
		'color': PURPLE,
		'effectType': 'Status',
		'damage': 0.125,
		'spe': 1,
	},
	'tox': {
		'image': psn,
		'name': 'Toxic',
		'color': PURPLE,
		'effectType': 'Status',
		'damage': 0.0625,
		'spe': 1,
	},
	'slp': {
		'image': slp,
		'name': 'Sleep',
		'color': GRAY,
		'effectType': 'Status',
		'damage': 0,
		'spe': 1,
	},
}

