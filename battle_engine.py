from __future__ import division
import pygame, math, Functions, computer_move, random
from pokedex import *
from colors import *
from display import *
from buttons import Button
from pokemon_statuses import BattleStatuses
from damage_calc import *
from typechart import BattleTypeChart
from moves import contactImages
from abilities import *

opponent_x = 10
opponent_y = 10
player_x = opponent_x + 390
player_y = opponent_y + 238
health_bar_x = opponent_x + 50
health_bar_y = opponent_y + 40
health_bar_l = 150
health_bar_w = 20
player_sprite_x = 120
player_sprite_y = 284
opponent_sprite_x = 460
opponent_sprite_y = 76
player_team = player_team()
opponent_team = opponent_team()

# sound
pygame.mixer.init()

pygame.mixer.music.load("sounds/battle_factory_music.mp3")
pygame.mixer.music.play(-1)

# images
stealth_rock_image = pygame.image.load('images/stealth_rock.png')
spikes_image = pygame.image.load('images/spike.png')
toxic_spikes_image = pygame.image.load('images/toxic_spike.png')
pokeball = pygame.image.load('images/pokeball.png')
x_icon = pygame.image.load('images/icon_x.png')

def update_display(screen):
	current_display_screen.Block_List.draw(screen)
	current_display_screen.update(screen)

def get_percent(numerator, denominator):
	number = int(round((numerator/denominator)*100))
	percent = "%s%%" % number
	return percent



class Sound_Button(Button):
	def __init__(self, msg, x, y, w, h, color, highlight, action):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)
		self.sound_on = True

	def do_action(self):
		if self.sound_on:
			self.sound_on = False
			pygame.mixer.music.pause()
		else:
			self.sound_on = True
			pygame.mixer.music.unpause()


class Invisible_Button(Button):

	def __init__(self, msg, x, y, w, h, color, highlight, action, x_offset=2, y_offset=20):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)
		self.x_offset = x_offset
		self.y_offset = y_offset

	@staticmethod
	def update(screen, List):
		for button in List:
			button.update(screen)
		


class Stat_Button(Invisible_Button):

	def __init__(self, msg, x, y, action, w=125, h=216, color=RED, highlight=BRIGHT_RED, x_offset=2, y_offset=20):
		Invisible_Button.__init__(self, msg, x, y, w, h, color, highlight, action, x_offset, y_offset)

	def get_stats(self):
		stat_text = []
		stats = ["Hp:", "Atk:", "Def:", "spA:", "spD:", "Spe:"]
		order = ["hp", "atk", "def", "spa", "spd", "spe"]
		if self.action == "player":
			pokemon = current_battle.player.current_pokemon
		elif self.action == "opponent":
			pokemon = current_battle.opponent.current_pokemon
		else:
			pokemon = self.action
		for stat in order:
			text = "%s %s" % (stats.pop(stats.index(stats[0])), pokemon.base_stats[stat])
			if pokemon.base_stats[stat] != pokemon.stats[stat]:
				text += " / %s" % pokemon.stats[stat]
			stat_text.append(text)
		stat_text.append("%s" % pokemon.ability)
		return stat_text

	def update(self, screen):
		
		if self.mouse_on:
			y = self.y - 20 + self.y_offset
			pygame.draw.rect(screen, self.color, (self.x, y, self.w, self.h))
			pygame.draw.rect(screen, BLACK, (self.x, y, self.w, self.h), 2)        
			x = self.w / self.x_offset
			y = self.y_offset
			Functions.text_to_screen(screen, self.msg, self.x+x, self.y+y, 20)
			
			var = self.y+24+self.y_offset
			for stat in self.get_stats():
				Functions.text_to_screen(screen, stat, self.x+x, var, 20)
				var += 24

class Damage_Button(Invisible_Button):

	def __init__(self, msg, x, y, action, w=159, h=110, color=BLUE, highlight=BRIGHT_BLUE, x_offset=2, y_offset=20):
		Invisible_Button.__init__(self, msg, x, y, w, h, color, highlight, action, x_offset, y_offset)	

	def get_stats(self):
		stat_text = []
		attacker = current_battle.player.current_pokemon
		defender = current_battle.opponent.current_pokemon
		if self.action["category"] != "Status":
			power = damage_calc(attacker, defender, self.action)
			stat_text.append("Damage:")
			stat_text.append("Hp: %s / %s" % (int(power), get_percent(power, defender.base_stats["hp"])))
		if "shortDesc" in self.action:
			stat_text.append(self.action["shortDesc"])
		
		return stat_text

	def update(self, screen):
		if self.mouse_on:        
			
			my_rect = pygame.Rect((self.x, self.y, self.w, self.h+50))

			var = self.y-100
			h = 20
			for stat in self.get_stats():

				rendered_text, height = Functions.render_textrect(stat, my_rect, WHITE, BRIGHT_BLUE, justification=1)
				screen.blit(rendered_text, (self.x, var))
				var += 30
				h+=30

			pygame.draw.rect(screen, BLACK, (self.x, self.y-100, self.w, self.h+h), 2)

class Change_Screen_Button(Button):

	def __init__(self, msg, x, y, w, h, color, highlight, action):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)

	def do_action(self):
		global screen_number, current_display_screen, current_battle
		screen_number = self.action
		current_display_screen = screens[screen_number]

		if self.action == 1:	
			current_battle = create_battle(player_team, opponent_team)
		Animation.clear_animations()
		

class Change_Team_Button(Button):

	def __init__(self, msg, x, y, w, h, color, highlight, action):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)

	def do_action(self):
		global player_team, opponent_team
		randies = random_team()
		if self.action == "player":
			player_team = randies
		else:
			opponent_team = randies


class Challenge_Button(Button):

	def __init__(self, msg, x, y, w, h, color, highlight, action):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)

	def do_action(self):
		global player_team, opponent_team, screen_number, current_display_screen, current_battle
		
		if current_display_screen == team_builder_screen:
			player_team = duplicate_pokemon_team(team_builder_screen.pokemon_team)
		screen_number = 1
		current_display_screen = screens[screen_number]
		new = opponent_team
		while new == opponent_team:
			new = random.choice(elite_four)
		opponent_team = new
		current_battle = create_battle(player_team, opponent_team)


class Sort_Button(Button):

	current_stat = None
	current_index = 0

	def __init__(self, msg, x, y, action, w=100, h=30, color=BLUE, highlight=BRIGHT_BLUE):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)
		

	def do_action(self):
		global pokemon_list
		
		if self.msg == "Up" or self.msg == "Down":
			if self.msg == "Up":
				Sort_Button.current_index -= 1
			else:
				Sort_Button.current_index += 1
		
		else:
			Sort_Button.current_stat = self.msg.lower()
			Sort_Button.current_index = 0
			pokemon_list = sorted(pokemon_list, key=lambda x: x.base_stats[Sort_Button.current_stat], reverse=True)
		
		max_index = 163
		if abs(Sort_Button.current_index) >= max_index:
			Sort_Button.current_index = 0		
		self.action[:] = []
		for i in range(Sort_Button.current_index, Sort_Button.current_index+7):
			if i > Sort_Button.current_index+6:
				break
			self.action.append(pokemon_list[i])
			
class Select_Pokemon_Button(Button):

	def __init__(self, x, y, action, source=None, index=0, msg="", w=580, h=70, color=BLUE, highlight=BRIGHT_BLUE):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)
		self.source = source
		self.index = index

	def do_action(self):
		if self.msg == "Use This!" and len(self.action) < 6:
			self.action.append(self.source)
		elif self.msg == "" and len(self.source) > self.index:
			self.action[0] = (self.source[self.index])
		elif self.msg == "X" and len(self.source) > self.index:
			del self.source[self.index]
		elif self.msg == "<" and len(self.source) > self.index and self.index > 0:
			first = self.source[0]
			second = self.source[self.index]
			self.source[0] = second
			self.source[self.index] = first
		

class Home_Screen(Display_Screen):

	def __init__(self):

		Display_Screen.__init__(self)
		self.background_image = pygame.image.load('images/home_background.jpg')

		buttons = [
		["Play", 500, 300, 100, 30, GREEN, BRIGHT_GREEN, 1],
		["Chart Room", 500, 400, 150, 30, YELLOW, BRIGHT_GREEN, 2],
		["Team Builder", 200, 300, 150, 30, BLUE, BRIGHT_GREEN, 3],
		]

		for item in buttons:
			button = Change_Screen_Button(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])

			self.Button_List.append(button)

		random_buttons = [
		["Random Team", 250, 250, 150, 30, WHITE, GRAY, "player"],
		["Random Team", 750, 250, 150, 30, YELLOW, PURPLE, "opponent"],
		]

		for item in random_buttons:
			button = Change_Team_Button(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])

			self.Button_List.append(button)

		challenge_buttons = [
		["Challenge", 500, 500, 150, 30, ORANGE, RED, "Challenge"],
		]

		for item in challenge_buttons:
			button = Challenge_Button(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])

			self.Button_List.append(button)

		music = Sound_Button("Music", 800, 575, 75, 30, GRAY, SNOW_WHITE, 0)
		self.Button_List.append(music)


	def update(self, screen):
		
		screen.blit(self.background_image, (0, 0))
		Button.update(screen, self.Button_List)
		x = 24
		for pokemon in player_team:
			screen.blit(pokemon.images[0], (x, 100))
			x += 72
		x = 520
		for pokemon in opponent_team:
			screen.blit(pokemon.images[0], (x, 100))
			x += 72


class Battle_Screen(Display_Screen):

	def __init__(self):

		Display_Screen.__init__(self)

		c = BLUE
		w = 640
		blocks = [
			[w, 0, 2, 625, c],
			[0, 400, w, 2, c],
		]

		for item in blocks:
			block = Block(item[0], item[1], item[2], item[3], item[4])
			self.Block_List.add(block)

	def update(self, screen):
		Button.update(screen, self.Button_List)
		current_battle.update(screen)
		Animation.update_animations(screen)
		Invisible_Button.update(screen, self.Invisible_Button_List)
		
	def update_buttons(self):
		self.Button_List[:] = []
		exit = Change_Screen_Button("EXIT", 900, 575, 75, 30, RED, BRIGHT_RED, 0)
		music = Sound_Button("Music", 800, 575, 75, 30, GRAY, SNOW_WHITE, 0)
		self.Button_List = [exit, music]
		self.Invisible_Button_List[:] = []
		stats = [
			["Base Stats", player_sprite_x, player_sprite_y-100, "player"],
			["Base Stats", opponent_sprite_x, opponent_sprite_y-75, "opponent"],
		]
		
		for stat in stats:
			button = Stat_Button(stat[0], stat[1], stat[2], stat[3])
			self.Invisible_Button_List.append(button)


class Pokedex_Screen(Display_Screen):

	def __init__(self):
		Display_Screen.__init__(self)
		
		self.display_pokemon = []
		self.stats = ["Hp", "Atk", "Def", "spA", "spD", "Spe"]

		exit = Change_Screen_Button("EXIT", 900, 575, 75, 30, RED, BRIGHT_RED, 0)
		music = Sound_Button("Music", 800, 575, 75, 30, GRAY, SNOW_WHITE, 0)
		up = Sort_Button("Up", 888, 290, self.display_pokemon)
		down = Sort_Button("Down", 888, 320, self.display_pokemon)
		self.Button_List = [exit, music, up, down]

		# Sort Buttons
		x, y = 200, 8
		for stat in self.stats:
			button = Sort_Button(stat, x, y, self.display_pokemon)
			self.Button_List.append(button)
			x += 120

		# Grid lines
		y = 2
		for x in range(190, 1000, 120):
			block = Block(x, y, 2, 542, DODGER_BLUE)
			self.Block_List.add(block)
		x = 190
		for y in range(110, 600, 72):
			block = Block(x, y, 720, 2, DODGER_BLUE)
			self.Block_List.add(block)

	def update(self, screen):

		x, y = 50, 24
		
		Button.update(screen, self.Button_List)

		for pokemon in self.display_pokemon:
			screen.blit(pokemon.images[0], (x,y))
			y += 72
			text_x = x+200
			for stat in self.stats:
				Functions.text_to_screen(screen, str(pokemon.base_stats[stat.lower()]), text_x, y-20, color=BLACK)
				text_x += 120


class Team_Builder_Screen(Display_Screen):

	def __init__(self):
		Display_Screen.__init__(self)

		self.display_pokemon = []
		self.pokemon_team = []
		self.focus_pokemon = [False]
		self.stats = ["Hp", "Atk", "Def", "spA", "spD", "Spe"]

		exit = Change_Screen_Button("EXIT", 900, 575, 75, 30, RED, BRIGHT_RED, 0)
		music = Sound_Button("Music", 800, 575, 75, 30, GRAY, SNOW_WHITE, 0)
		up = Sort_Button("Up", 600, 550, self.display_pokemon)
		down = Sort_Button("Down", 600, 580, self.display_pokemon)
		use = Select_Pokemon_Button(612, 400, self.pokemon_team, self.focus_pokemon[0], msg="Use This!", w=125, h=30)
		challenge = Challenge_Button("PLAY!", 700, 100, 150, 30, RED, BRIGHT_RED, 1)
		self.Button_List = [exit, music, up, down, use, challenge]

		# Sort Buttons
		x, y = 116, 232
		for stat in self.stats:
			button = Sort_Button(stat, x, y, self.display_pokemon, w=75, h=25)
			self.Button_List.append(button)
			x += 80
			button.do_action()
		# Focus Pokemon Buttons
		x, y = 14, 260
		for i in range(len(self.display_pokemon)-2):
			button = Select_Pokemon_Button(x, y, self.focus_pokemon, self.display_pokemon, i)
			self.Button_List.append(button)
			y += 72
			button.do_action()
		# Pokemon Team Buttons
		x, y = 75, 150
		for i in range(6):
			button = Select_Pokemon_Button(x, y, 0, self.pokemon_team, i, msg="X", w=30, h=30)
			self.Button_List.append(button)
			back = Select_Pokemon_Button(x, y-130, 0, self.pokemon_team, i, msg="<", w=30, h=30)
			self.Button_List.append(back)
			info = Select_Pokemon_Button(x-30, y-100, self.focus_pokemon, self.pokemon_team, i, w=100, h=100)
			self.Button_List.append(info)
			x += 96
		self.text_list, self.sprite_list = [], []
		self.update_info()

	def update(self, screen):
		
		Button.update(screen, self.Button_List)

		# Sorted Pokemon
		x, y = 6, 248
		for pokemon in self.display_pokemon:
			if pokemon == self.display_pokemon[5]:
				break
			screen.blit(pokemon.images[0], (x,y))
			y += 72
			text_x = x+148
			for stat in self.stats:
				Functions.text_to_screen(screen, str(pokemon.base_stats[stat.lower()]), text_x, y-20)
				text_x += 80

		# Pokemon Team
		x,y = 50, 50
		for pokemon in self.pokemon_team:
			screen.blit(pokemon.images[0], (x,y))
			x+=96

		# Focus Pokemon
		screen.blit(self.focus_pokemon[0].images[0], (600, 250))
		for item in self.text_list:
			Functions.text_to_screen(screen, item[0], item[1], item[2], 20, BLACK)
		for item in self.sprite_list:
			screen.blit(item[0], item[1])
		if self.text_list[0][0] != self.focus_pokemon[0].name:
			self.update_info()

	def update_info(self):
		self.text_list[:] = []
		self.sprite_list[:] = []
		self.text_list, self.sprite_list[:] = self.get_info(self.focus_pokemon[0])
		self.Button_List[4].source = self.focus_pokemon[0]

	def get_info(self, pokemon):
		y = 300
		text = [[pokemon.name, 650, 248]]
		for stat in self.stats:
			text.append(["%s: %s" % (stat, pokemon.base_stats[stat.lower()]), 936, y])
			y += 30 
		
		sprites = []
		x = 625
		for t in pokemon.types:
			sprites.append([t["image"], (x, 350)])
			x+=33
		x,y = 800, 300
		for move in pokemon.learnset:
			text.append([move["name"], x, y-30])
			sprites.append([BattleTypeChart[move["type"]]["image"], (x, y)])
			sprites.append([contactImages[move["category"]], (x+33, y)])
			y+=60
		return text, sprites


home_screen = Home_Screen()
battle_screen = Battle_Screen()
pokedex_screen = Pokedex_Screen()
team_builder_screen = Team_Builder_Screen()
screens = [home_screen, battle_screen, pokedex_screen, team_builder_screen]
screen_number = 0
current_display_screen = screens[screen_number]


class Animation():
	opponent_box = [opponent_x, opponent_y, 144, 144]
	player_box = [player_x, player_y, 144, 144]
	active_list = []
	player_sprites = []
	change_x = 10
	change_y = 7

	def __init__(self, move, player):
			
		if player == current_battle.player:
			self.x = 200
			self.y = 274
			self.change_x = Animation.change_x
			self.change_y = Animation.change_y * -1
			self.image_number = 0

		elif player == current_battle.opponent:
			self.x = 424
			self.y = 124
			self.change_x = Animation.change_x * -1
			self.change_y = Animation.change_y
			self.image_number = 1

		if move["category"] == "Physical":
			self.image = Animation.player_sprites.pop(self.image_number).image
		else:
			self.image = pygame.image.load('images/special_' + move["type"] + '.png')

		Animation.active_list.append(self)
	
	def update(self, screen):
		self.x += self.change_x
		self.y += self.change_y
		screen.blit(self.image, (self.x, self.y))
		if 176 <= self.x <= 448:
			pass
		else:
			Animation.active_list.remove(self)

	@staticmethod
	def update_animations(screen):
		for sprite in Animation.player_sprites:
			screen.blit(sprite.image, (sprite.x, sprite.y))
		if len(Animation.active_list):
			Animation.active_list[0].update(screen)

	@staticmethod
	def clear_animations():
		Animation.active_list[:] = []


class Player():
	def __init__(self, pokemon_list):
		self.pokemon_list = pokemon_list
		for pokemon in pokemon_list:
			pokemon.pokecenter()
		self.current_pokemon = self.pokemon_list[0]
		self.pokemon_party = self.pokemon_list[1:]
		self.update()
		self.text_color = BLACK
		self.pokemon_fainted = False
		self.whiteout = False
		self.set_status_effects()
		self.set_empty_field()
		# fake out, toxic damage
		self.active_turns = 0
		# sleep clause
		self.sleep = False

	def update(self):
		self.update_party()
		self.pokemon_fainted = self.fainted_pokemon()

	def update_party(self):
		self.pokemon_party[:] = []
		for pokemon in self.pokemon_list:
			if pokemon != self.current_pokemon:
				self.pokemon_party.append(pokemon)
			pokemon.stats["hp"] = int(pokemon.stats["hp"])

	def switch_pokemon(self, pokemon):
		self.current_pokemon = pokemon
		self.active_turns = 0
		self.update()
		self.set_status_effects()

	def check_pokemon(self):
		total_pokemon = []
		sleep = False
		for pokemon in self.pokemon_list:
			total_pokemon.append(pokemon)
			if pokemon.status and pokemon.status["name"] == "Sleep":
				sleep = True
		self.sleep = sleep
		return total_pokemon

	def fainted_pokemon(self):
		fainted = False
		if self.current_pokemon.stats["hp"] <= 0:
			fainted = True

		return fainted

	def total_faint(self):
		l = len(self.pokemon_list)
		total = 0
		whiteout = False
		for pokemon in self.pokemon_list:
			if pokemon.stats["hp"] == 0:
				total += 1
				pokemon.status = None
			else:
				pass
		if l == total:
			self.whiteout = True
	
	def set_status_effects(self):
		self.status_effects = {
			"Disable": {
				"turns": 0,
				"move": None,
			},
			"Encore": {
				"turns": 0,
				"move": None,
			},
			"Leech Seed": False,
			"Wish": {
				"turns": 0,
				"health": 0,
			}
		}

	def set_empty_field(self):
		self.field = {
			"Stealth Rock": False,
			"Spikes": 0,
			"Toxic Spikes": 0,
			"Sticky Web": False,
			"Trapped": False,
		}


class Turn():
	number = 0
	List = []
	def __init__(self):

		self.number = Turn.number
		self.text = [["Turn: %s" % self.number, BLACK]]
		Turn.List.append(self)
		Turn.number += 1

	def add_text(self, text, color=BLACK):
		Functions.text_to_list((text, color), self.text)

	@staticmethod
	def reset_turns():
		Turn.number = 0
		Turn.List[:] = []


class Attack_Button(Button):

	def __init__(self, msg, x, y, w, h, color, highlight, action):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)

	def do_action(self):
		if not current_battle.fainted and not current_battle.animation_flag and (not current_battle.switch_flag and not current_battle.move):
			
			attack = Attack_Move(self.action, current_battle.player.current_pokemon, current_battle.player, current_battle.opponent)
			current_battle.turn(attack)


class Switch_Button(Button):

	def __init__(self, msg, x, y, w, h, color, highlight, action):
		Button.__init__(self, msg, x, y, w, h, color, highlight, action)

	def do_action(self):
		if self.action.stats["hp"] > 0 and not current_battle.animation_flag and not current_battle.player.field["Trapped"]:	
			switch = Switch_Move(self.action, current_battle.player)
			current_battle.process_switch(switch)


class Move():

	def __init__(self):
		self.text = []
		self.priority = 0


class Attack_Move(Move):

	def __init__(self, move, attacker, attacking_player, defending_player):

		Move.__init__(self)
		self.move = move
		self.priority = self.move["priority"]
		self.pokemon = attacker
		self.player = attacking_player
		self.defending_player = defending_player

	def do_move(self):

		defender = self.defending_player.current_pokemon
		if not self.player.pokemon_fainted:
				
			current_battle.process_attack(self.player, self.defending_player, self.pokemon, defender, self.move)
			if self.pokemon.status and self.pokemon.status["name"] == "Sleep":
				return
			Animation(self.move, self.player)
			

class Switch_Move(Move):

	def __init__(self, move, player):

		Move.__init__(self)
		self.move = move
		self.priority = 6
		self.player = player
		self.pokemon = player.current_pokemon

	def do_move(self):
		if self.move.stats["hp"] > 0: 
			current_battle.switch_pokemon(self.player, self.move)

class Battle():

	def __init__(self, player_team, opponent_team):

		self.player = Player(player_team)
		self.opponent = Player(opponent_team)
		self.battle_scene = pygame.image.load('images/my_background2.png')
		self.text_list = []
		self.current_turn = Turn()
		self.player.text_color = BLUE
		self.opponent.text_color = RED
		self.fainted = False
		self.playing = True
		self.switch_flag = None
		self.flinch_flag = None
		self.animation_flag = None
		self.flags = [self.switch_flag, self.animation_flag]
		self.move = None
		self.update_screen()

	def update(self, screen):

		self.check_flags()
		self.draw_sprites(screen)
		self.draw_text(screen)
		self.update_players()
		self.logic()

	def update_players(self):

		self.player.update()
		self.opponent.update()
		if self.playing:	
			self.check_players()
		else:
			self.update_buttons()

	def update_screen(self):
		self.update_players()
		self.update_moves()
		self.update_health_bars()
		self.update_sprites()
		self.update_text()
		self.update_pokeballs()

	def draw_sprites(self, screen):

		for sprite in self.sprites:
			screen.blit(sprite[0], sprite[1])

		#### Health Bars ###
		# Separate block_lists because of bugs
		block_list = pygame.sprite.Group()
		health_bars = [
			[health_bar_x, health_bar_y],
			[health_bar_x+390, health_bar_y+238],
		]
		for block in health_bars:
			new_block = Block(block[0], block[1], health_bar_l, health_bar_w, RED)
			block_list.add(new_block)

		block_list.draw(screen)
		self.block_list.draw(screen)

	def draw_text(self, screen):

		for item in self.info_text:
			Functions.text_to_screen(screen, item[0], item[1], item[2], item[3], item[4], False)	

		self.draw_text_list(screen)

	def draw_text_list(self, screen):
		x, y = 640 + 12, 12
		l, w = 336, 100
		for item in self.current_turn.text:
			my_rect = pygame.Rect((x, y, l, w))
			rendered_text, height = Functions.render_textrect(item[0], my_rect, item[1])
			screen.blit(rendered_text, (x, y))
			y += height

	def update_sprites(self):
		self.sprites = [
			[self.battle_scene, (1, 2)],
			[self.player.current_pokemon.types[0]["image"], (player_x+175, player_y+7)],
			[self.opponent.current_pokemon.types[0]["image"], (opponent_x+175, opponent_y+7)],
		]
			
		if len(self.player.current_pokemon.types) > 1:
			self.sprites.append([self.player.current_pokemon.types[1]["image"], (player_x+175, player_y+22)])
		if len(self.opponent.current_pokemon.types) > 1:
			self.sprites.append([self.opponent.current_pokemon.types[1]["image"], (opponent_x+175, opponent_y+22)])
		
		if self.player.current_pokemon.status:
			self.sprites.append([self.player.current_pokemon.status['image'], (player_x+25, player_y+75)])
		if self.opponent.current_pokemon.status:
			self.sprites.append([self.opponent.current_pokemon.status['image'], (opponent_x+25, opponent_y+75)])

		self.update_field_sprites()

		x, y = 40, 475
		for move in self.player.current_pokemon.learnset:
			self.sprites.append([BattleTypeChart[move["type"]]["image"], (x, y)])
			self.sprites.append([contactImages[move["category"]], (x+33, y)])
			x += 160

		# Spaghetti code for team of one pokemon
		if len(self.player.pokemon_party):	
			l = math.floor(640 / len(self.player.pokemon_party))
			x, y = l/4, 580
			for pokemon in self.player.pokemon_party:
				self.sprites.append([pokemon.types[0]["image"], (x, y)])
				if len(pokemon.types) > 1:
					self.sprites.append([pokemon.types[1]["image"], (x+33, y)])
				x += l

		Animation.player_sprites[:] = []
		player_sprites = [
			[self.player.current_pokemon.images[1], player_sprite_x, player_sprite_y],
			[self.opponent.current_pokemon.images[0], opponent_sprite_x, opponent_sprite_y],
		]
		for sprite in player_sprites:
			image = Sprite_Image(sprite[1], sprite[2], sprite[0])
			Animation.player_sprites.append(image)

	def update_field_sprites(self):
		players = [self.player, self.opponent]
		for player in players:
			if player == self.player:
				x, y = player_x-300, player_y+50
			else:
				x, y = opponent_x+400, opponent_y+100
			for key in player.field:
				if player.field[key]:
					if key == "Stealth Rock":
						self.sprites.append([stealth_rock_image, (x, y)])
					elif key == "Spikes":
						spike_x, spike_y = x+24, y+72
						for spike in range(1, player.field[key]+1):
							self.sprites.append([spikes_image, (spike_x, spike_y)])
							spike_x += 24
					elif key == "Toxic Spikes":
						spike_x, spike_y = x+96, y+72
						for spike in range(1, player.field[key]+1):
							self.sprites.append([toxic_spikes_image, (spike_x, spike_y)])
							spike_x += 24

	def update_pokeballs(self):

		total_pokemon = self.player.check_pokemon()
		x = player_x + 124
		y = player_y + 85
		for pokemon in total_pokemon:
			self.sprites.append([pokeball, (x, y)])
			if pokemon.stats["hp"] <= 0:
				self.sprites.append([x_icon, (x, y)])
			x += 14

		x = opponent_x + 124
		y = opponent_y + 85
		total_pokemon = self.opponent.check_pokemon()
		for pokemon in total_pokemon:
			self.sprites.append([pokeball, (x, y)])
			if pokemon.stats["hp"] <= 0:
				self.sprites.append([x_icon, (x, y)])
			x += 14

	def update_health_bars(self):

		pokemon_health = self.player.current_pokemon.stats["hp"]
		opponent_health = self.opponent.current_pokemon.stats["hp"]
		pokemon_hp = math.floor((pokemon_health / self.player.current_pokemon.base_stats["hp"]) * health_bar_l)
		opponent_hp = math.floor((opponent_health / self.opponent.current_pokemon.base_stats["hp"]) * health_bar_l)
		
		self.block_list = pygame.sprite.Group()
		# Health Bar Colors
		if health_bar_l/4 < pokemon_hp <= health_bar_l/2:
			pokemon_color = YELLOW
		elif 0 < pokemon_hp <= health_bar_l/4:
			pokemon_color = DARK_RED
		else:
			pokemon_color = BLUE
		if health_bar_l/4 < opponent_hp <= health_bar_l/2:
			opponent_color = YELLOW
		elif 0 < opponent_hp <= health_bar_l/4:
			opponent_color = DARK_RED
		else:
			opponent_color = BLUE
		health_bar_color = (25,25,25)
		blocks = [
			[health_bar_x+390, health_bar_y+238, pokemon_hp, pokemon_color],
			[health_bar_x, health_bar_y, opponent_hp, opponent_color],
		]
		for block in blocks:          
			new_block = Block(block[0], block[1], block[2], health_bar_w, block[3])
			self.block_list.add(new_block)

	def update_text(self):
		text_size = 20
		text_color = BLACK
		y = 35
		self.info_text = [
			["%s" % self.player.current_pokemon.name, player_x+10, player_y+10, text_size, text_color],
			["%s" % self.opponent.current_pokemon.name, opponent_x+10, opponent_y+7, text_size, text_color],
			["hp", opponent_x+25, opponent_y+y, text_size, text_color],
			["hp", player_x+25, player_y+y, text_size, text_color],
			["%s" % get_percent(self.opponent.current_pokemon.stats["hp"], self.opponent.current_pokemon.base_stats["hp"]), opponent_x+100, health_bar_y-2, text_size, WHITE],
			["%s" % get_percent(self.player.current_pokemon.stats["hp"], self.player.current_pokemon.base_stats["hp"]), player_x+100, health_bar_y+236, text_size, WHITE],
			["%s/%s" % (self.player.current_pokemon.stats["hp"], self.player.current_pokemon.base_stats["hp"]), player_x+100, player_y+60, text_size, text_color],
		]

		x = 112
		for move in self.player.current_pokemon.learnset:
			self.info_text.append(["%s" % move["basePower"], x, 470, 18, WHITE])
			x += 160

		# More Spaghetti
		if len(self.player.pokemon_party):
			x = 42
			l = math.floor(640 / len(self.player.pokemon_party))
			for pokemon in self.player.pokemon_party:
				self.info_text.append(["%s/%s" % (pokemon.stats["hp"], pokemon.base_stats["hp"]), x, 596, 18, WHITE])
				x += l

	def update_buttons(self):
		self.update_moves()

	def update_moves(self):
		x, y = 0, 0
		battle_screen.update_buttons()
		color = BLUE
		highlight = BRIGHT_BLUE
		if self.player.pokemon_fainted or self.switch_flag == self.player:
			color = GRAY
			highlight = (150, 150, 150)
		for move in self.player.current_pokemon.learnset:
			button = Attack_Button("%s" % move["name"], x, y+402, 159, 110, color, highlight, move)
			battle_screen.Button_List.append(button)
			damage_button = Damage_Button("Damage", x, y+402, move)
			battle_screen.Invisible_Button_List.append(damage_button)
			if "shortDesc" in move:
				pass
			x += 160
		
		# If there is only one pokemon on players team
		if self.player.field["Trapped"]:
			color, highlight = GRAY, (150, 150, 150)
		else:
			color, highlight = GREEN, BRIGHT_GREEN
		if len(self.player.pokemon_party):
			x = 0
			l = math.floor(640 / len(self.player.pokemon_party))
			for pokemon in self.player.pokemon_party:
				button = Switch_Button("%s" % pokemon.name, x, 512, l, 110, color, highlight, pokemon)
				battle_screen.Button_List.append(button)
				invisible_button = Stat_Button("Base Stats", x, 512, pokemon, y_offset=-75)
				battle_screen.Invisible_Button_List.append(invisible_button)
				x += l

	def turn(self, move):
		
		self.current_turn = Turn()
		self.process_moves(move)
		self.process_status_effects()
		self.update_screen()
		self.reset_flags()

	def process_moves(self, move):
		
		opponent_attack = self.computer_move()
		
		moves = [opponent_attack, move]
		moves = sorted(moves, key=lambda x: x.pokemon.stats["spe"], reverse = True)
		self.moves = sorted(moves, key=lambda x: x.priority, reverse = True)
		for move in self.moves:
			if self.switch_flag and self.switch_flag != "double-down" and not self.fainted:
				self.move = move
				self.check_players()
			elif self.flinch_flag:
				self.pokemon_flinched()
			else:	
				move.do_move()
			self.check_players()
			self.update_screen()

	def process_switch(self, switch):
		if not self.fainted and not self.switch_flag:
			
			self.turn(switch)
		if self.switch_flag and self.playing:
			# U-turn/Volt-switch
			switch.do_move()
			if self.move:
				self.move.do_move()
				self.move = None
			self.check_players()
			self.update_screen()

		elif switch.player.pokemon_fainted:
			switch.do_move()
			self.update_screen()

	def process_attack(self, attacking_player, defending_player, attacker, defender, move):
		if self.sleep_turn(attacking_player, attacker):
			return
		self.current_turn.add_text("%s used %s!" % (attacker.name, move["name"]), attacking_player.text_color)
		if defender.stats["hp"] == 0 and "sideCondition" not in move:
			self.but_it_failed()
			return
		elif move["name"] == "Fake Out":
			if attacking_player.active_turns > 0:
				self.but_it_failed()
				return
		elif move["name"] == "Sucker Punch" and (move == self.moves[1].move or self.moves[1].move["category"] == "Status"):
			self.but_it_failed()
			return
		elif "multihit" in move:
			self.multihit_move(attacking_player, defending_player, attacker, defender, move)
		if move["category"] != "Status":
			if attacker.ability != "Mold Breaker" and not damage_alter_ability(defender, move):
				self.damage_alter_ability(defender)
			else:
				self.attack(attacking_player, defending_player, attacker, defender, move)	
			return
		elif "sideCondition" in move:
			if move["name"] != "Wish":
				self.entry_hazard_move(attacking_player, defending_player, attacker, defender, move)
		elif move["category"] == "Status":
			self.status_move(attacking_player, defending_player, attacker, defender, move)
		else:
			self.but_it_failed()

	def process_status_effects(self):
		def leech_seed(players, seeded):
			if players[0].current_pokemon.stats["hp"] and players[1].current_pokemon.stats["hp"]:
				number = players.index(seeded)
				losing = players.pop(number)
				gaining = players[0]
				self.current_turn.add_text("%s's health is sapped by Leech Seed!" % player.current_pokemon.name, GREEN)
				self.drain_health(gaining.current_pokemon, losing.current_pokemon, 0.125)
				self.check_if_fainted(losing.current_pokemon)

		players = [self.player, self.opponent]
		text = []
		for player in players:
			if player.current_pokemon.stats["hp"] and player.current_pokemon.ability != "Magic Guard":
				for key in player.status_effects:
					if player.status_effects[key]:
						if key == "Leech Seed":
							if "Grass" not in player.current_pokemon.types:
								leech_seed(players, player)
		
				if player.current_pokemon.status and player.current_pokemon.status['damage']:	
					self.residual_damage(player, player.current_pokemon, player.current_pokemon.status)
	
	def attack(self, attacking_player, defending_player, attacker, defender, move):
		TA = type_advantage(defender, move)
		power = damage_calc(attacker, defender, move)
		power = self.sturdy_ability(defender, power)
		damage = power
		if defender.stats["hp"] - damage < 0:
			damage = defender.stats["hp"]
		if TA > 0:
			self.deduct_health(defender, power)
		
		color = attacking_player.text_color
		text = []
		
		if damage == 0:
			return
		elif TA > 1:
			text.append(("It's super effective!", color))
		elif 0 < TA < 1:
			text.append(("It's not very effective...", color))
		elif TA == 0:
			text.append(("It didn't do anything...", color))
		
		if TA > 0:
			text.append(("%s lost %s HP!" % (defender.name, get_percent(damage, defender.base_stats["hp"])), color))

		for line in text:
			self.current_turn.add_text(line[0], line[1])

		attacking_player.active_turns += 1

		self.check_if_fainted(defender)
		self.after_move_effects(attacking_player, defending_player, attacker, defender, move, TA, damage)

	def switch_pokemon(self, player, new_pokemon):
		pokemon = player.current_pokemon
		player.switch_pokemon(new_pokemon)

		color = player.text_color
		if not self.fainted:
			self.current_turn.add_text("%s come back!" % pokemon.name, color)
			self.switch_ability(pokemon)
		self.current_turn.add_text("Go %s!" % new_pokemon.name, color)

		self.entry_hazard_damage(player, new_pokemon)

		if self.switch_flag == "double-down":
			self.switch_flag = self.opponent
		else:	
			self.switch_flag = False

	def status_move(self, attacking_player, defending_player, attacker, defender, move):
		try:	
			if defending_player.status_effects[move["name"]] or get_stab(defender, move) == 1.5:
				self.but_it_failed()
				return
			elif move["name"] == "Leech Seed":
				defending_player.status_effects[move["name"]] = move
				self.current_turn.add_text("%s was seeded!" % defender.name, attacking_player.text_color)
		except:
			if defender.status:
				self.but_it_failed()
				return
			else:
				self.set_status(defending_player, defender, move, attacker, attacking_player)

	def entry_hazard_move(self, attacking_player, defending_player, attacker, defender, move):
		if defending_player.field[move["name"]]:
			if move["name"] == "Spikes" and defending_player.field[move["name"]] < 3:	
				pass
			elif move["name"] == "Toxic Spikes" and defending_player.field[move["name"]] < 2:
				pass
			else:	
				self.but_it_failed()
				return
		if move["name"] == "Stealth Rock":
			defending_player.field[move["name"]] = move
			self.current_turn.add_text("Pointed stones float in the air around %s!" % defender.name, attacking_player.text_color)
		elif move["name"] == "Spikes":
			defending_player.field[move["name"]] += 1
			self.current_turn.add_text("Spikes were scattered around %s's feet!" % defender.name, attacking_player.text_color)
		elif move["name"] == "Toxic Spikes":
			defending_player.field[move["name"]] += 1

	def after_move_effects(self, attacking_player, defending_player, attacker, defender, move, TA, damage):		
		if "selfSwitch" in move and TA:
			if len(attacking_player.pokemon_party):
				if damage:
					attacking_player.field["Trapped"] = False
				self.switch_flag = attacking_player
				if self.switch_flag == self.opponent:
					self.opponent_logic(True)
		
		elif "drain" in move:
			self.restore_drained_health(attacker, damage)

		elif "recoil" in move:
			n, d = move["recoil"][0], move["recoil"][1]
			self.recoil_damage(attacker, damage, n/d)

		elif move["secondary"]:
			if "volatileStatus" in move["secondary"]:
				if move["secondary"]["volatileStatus"] == 'flinch':
					self.flinch_flag = defender

		if (move["category"] == "Physical" and damage) and defender.ability in hitByContactAbilities and TA:
			self.hit_by_contact_ability(attacking_player, defending_player, attacker, defender, move)

	def switch_ability(self, pokemon):
		if pokemon.ability == "Regenerator":
			health = int(pokemon.base_stats["hp"] / 3)
			self.restore_health(pokemon, health)
		elif pokemon.ability == "Natural Cure":
			pokemon.cureStatus()

	def set_status(self, player, pokemon, move, synced=None, synced_player=None):
		
		if move["status"] == 'brn':
			status = "burned"
		elif move["status"] == "par":
			status = "paralyzed"
		elif move["status"] == "psn":
			status = "poisoned"
		elif move["status"] == "tox":
			status = "badly poisoned"
		elif move["status"] == "slp":		
			if player.sleep:
				self.sleep_clause()
				return
			status = "put to sleep"
		if self.check_status_prevention(pokemon, move):
			return

		if (get_stab(pokemon, move) == 1.5 and move["type"] != "Psychic") or type_advantage(pokemon, move) == 0:
			self.but_it_failed()
		
		else:
			pokemon.status = BattleStatuses[move["status"]]
			self.current_turn.add_text("%s was %s!" % (pokemon.name, status), pokemon.status["color"])
			if synced and status != "put to sleep":
				if pokemon.ability == "Synchronize" and not synced.status:
					self.add_ability_text(pokemon)
					self.set_status(synced_player, synced, move)
		pokemon.apply_stat_changes()

	def deduct_health(self, pokemon, health):
		if pokemon.stats["hp"] - health < 0:	
			pokemon.stats["hp"] = 0
		else:
			pokemon.stats["hp"] -= int(health)

	def check_status_prevention(self, pokemon, move):
		if pokemon.ability in statusProtectedAbilities:
			if move["status"] == statusProtectedAbilities[pokemon.ability] or move["type"] == statusProtectedAbilities[pokemon.ability]:
				self.add_ability_text(pokemon)
				return True
		return False

	def sleep_clause(self):
		self.but_it_failed()
		self.current_turn.add_text("(Sleep Clause)", WHITE)

	def sleep_turn(self, player, pokemon):

		if not pokemon.status:
			return False
		elif pokemon.status["name"] != "Sleep":
			return False

		if pokemon.sleep_turns < 2:
			sleep_text = "is fast asleep..."
			if pokemon.ability == "Early Bird":
				pokemon.sleep_turns += 2
			else:	
				pokemon.sleep_turns += 1
			asleep = True
		else:
			sleep_text = "woke up!"
			pokemon.cureStatus()
			asleep = False
			
		self.current_turn.add_text("%s %s" % (pokemon.name, sleep_text), player.text_color)
		return asleep

	def drain_health(self, gaining, losing, percent):
		
		health = int(percent * losing.base_stats["hp"])
		self.deduct_health(losing, health)
		self.restore_drained_health(gaining, health)

	def restore_drained_health(self, pokemon, health):
		health = int(health / 2)
		self.restore_health(pokemon, health)

	def absorb_damage(self, pokemon, percent):
		health = pokemon.base_stats["hp"] * percent
		self.restore_health(pokemon, health)

	def restore_health(self, pokemon, health):
		if pokemon.stats["hp"] == pokemon.base_stats["hp"]:
			return	
		elif pokemon.stats["hp"] + health > pokemon.base_stats["hp"]:
			health = pokemon.base_stats["hp"] - pokemon.stats["hp"]
		pokemon.stats["hp"] += int(health)
		self.current_turn.add_text("%s restored some hp!" % pokemon.name, GREEN)

	def recoil_damage(self, pokemon, damage, percent):
		if not damage:
			print "no recoil"
			return
		health = int(percent * damage)
		if health == 0:
			health = 1
		self.deduct_health(pokemon, health)
		self.current_turn.add_text("%s was hurt by recoil!" % pokemon.name, DARK_RED)
		self.check_if_fainted(pokemon)

	def residual_damage(self, player, pokemon, info):
		if info['name'] == "Toxic":
			pokemon.toxic_turns+=1
			damage = info['damage'] * pokemon.toxic_turns
		else:
			damage = info['damage']
		health = damage * pokemon.base_stats["hp"]
		if health < 1:
			health = 1
		self.deduct_health(pokemon, health)
		self.current_turn.add_text("%s was hurt by its %s!" % (pokemon.name, info['name']), info['color'])
		self.check_if_fainted(pokemon)

	def pokemon_flinched(self):
		pokemon = self.flinch_flag
		if pokemon.stats["hp"]:	
			self.current_turn.add_text("%s flinched!" % pokemon.name, WHITE)
		self.flinch_flag = None

	def sturdy_ability(self, pokemon, damage):
		new_damage = damage
		if pokemon.ability == "Sturdy":
			if pokemon.stats["hp"] == pokemon.base_stats["hp"] and pokemon.stats["hp"] - damage <= 0:
				new_damage = pokemon.base_stats["hp"] - 1
				self.current_turn.add_text("%s endured the hit!" % pokemon.name, PERU)
		return new_damage

	def add_ability_text(self, pokemon):
		self.current_turn.add_text("%s's %s!" % (pokemon.name, pokemon.ability), DODGER_BLUE)

	def damage_alter_ability(self, pokemon):
		self.add_ability_text(pokemon)
		if "absorb" in damageAlterAbilities[pokemon.ability]["effect"]:
			n = damageAlterAbilities[pokemon.ability]["effect"]["absorb"]
			self.absorb_damage(pokemon, n)

	def entry_hazard_damage(self, player, pokemon):
		for key in player.field:
			if player.field[key]:
				spikes = {"type": "Ground"}
				grounded = damage_alter_ability(pokemon, spikes)
				if not grounded:
					pass	
				else:
					grounded = type_advantage(pokemon, spikes)
				if key == "Stealth Rock":
					stealth_rock = {"type": "Rock"}
					TA = type_advantage(pokemon, stealth_rock)
					percent = (TA * 12.5) / 100
					self.deduct_entry_hazard_damage(player, pokemon, percent, key)
				elif key == "Spikes" and grounded:
					if player.field[key] == 1:
						percent = 0.125
					elif player.field[key] == 2:
						percent = 0.167
					else:
						percent = 0.25
					self.deduct_entry_hazard_damage(player, pokemon, percent, key)
				elif key == "Toxic Spikes" and grounded:
					poison = {"status": "psn", "type": "Poison"}
					self.set_status(player, pokemon, poison)

	def deduct_entry_hazard_damage(self, player, pokemon, percent, hazard):
		if pokemon.ability == "Magic Guard":
			return
		damage = math.floor(percent * pokemon.base_stats["hp"])
		self.deduct_health(pokemon, damage)
		self.current_turn.add_text("%s was hurt by %s!" % (pokemon.name, hazard), player.text_color)
		self.check_if_fainted(pokemon)

	def multihit_move(self, attacking_player, defending_player, attacker, defender, move):
		if type_advantage(defender, move):
			for hit in range(move["multihit"]):
				if not self.fainted:
					self.attack(attacking_player, defending_player, attacker, defender, move)
			self.current_turn.add_text("Hit %s times!" % move["multihit"])

	def hit_by_contact_ability(self, attacking_player, defending_player, attacker, defender, move):
		status = hitByContactAbilities[defender.ability]
		if attacker.status:
			return
		elif get_stab(attacker, status) == 1.5 or type_advantage(pokemon, status) == 0:
			return
		else:
			self.add_ability_text(defender)
			self.set_status(attacking_player, attacker, status)

	def but_it_failed(self):
		self.current_turn.add_text("But it failed!", WHITE)

	def check_if_fainted(self, pokemon):
		if pokemon.stats["hp"] <= 0:
			pokemon.stats["hp"] = 0
			self.current_turn.add_text("%s fainted!" % pokemon.name, DARK_RED)
			self.check_players()

	def check_players(self):
		players = [self.player, self.opponent]
		self.fainted = False
		for player in players:
			if player.current_pokemon.stats["hp"] <= 0:
				self.fainted = True
				player.pokemon_fainted = True
			player.total_faint()
			if player.whiteout and self.playing:
				self.game_over(player)
				self.update_buttons()
				break
		if self.player.current_pokemon.ability == "Arena Trap" and not self.player.pokemon_fainted and self.switch_flag != self.opponent:
			self.opponent.field["Trapped"] = True
		else:
			self.opponent.field["Trapped"] = False
		if self.opponent.current_pokemon.ability == "Arena Trap" and not self.opponent.pokemon_fainted and self.switch_flag != self.player:
			self.player.field["Trapped"] = True
		else:
			self.player.field["Trapped"] = False


	def game_over(self, player):
	
		if player == self.player:
			text = "You lose!"
			text_color = DARK_RED
		else:
			text = "You win!"
			text_color = BRIGHT_BLUE
		self.current_turn.add_text(text, text_color)
			
		self.playing = False

	def logic(self):
		self.opponent_logic()

	def opponent_logic(self, selfswitch=False):
		if len(Animation.active_list) and not selfswitch:
			return
		if self.switch_flag == self.opponent:
			try:	
				switch = False
				best_switch = computer_move.best_switch(self.player.current_pokemon, self.opponent.pokemon_list, True)
				if best_switch.stats["hp"] > 0 and best_switch != self.opponent.current_pokemon:
					switch = Switch_Move(best_switch, self.opponent)
				else:
					best_switch = computer_move.send_in_pokemon(self.opponent.pokemon_party)
					if best_switch.stats["hp"] > 0:
						switch = Switch_Move(best_switch, self.opponent)
				if switch:
					self.process_switch(switch)
			except:
				print "Last Alive"
			self.switch_flag = False
			

	def computer_move(self):
		choice = computer_move.best_move(self.player, self.opponent)
		try:
			move = Attack_Move(choice, self.opponent.current_pokemon, self.opponent, self.player)
		except:
			move = Switch_Move(choice, self.opponent)
		
		return move

	def reset_flags(self):
		self.flinch_flag = None

	def check_flags(self):
		
		# Wait until animations are done
		if len(Animation.active_list):
			self.animation_flag = True
		else:
			self.animation_flag = False

		if (self.opponent.pokemon_fainted and not self.opponent.whiteout) and not self.switch_flag:
			self.switch_flag = self.opponent
		if (self.opponent.pokemon_fainted and self.player.pokemon_fainted) and self.playing:
			self.switch_flag = "double-down"

def create_battle(player_team, opponent_team):

	Turn.reset_turns()
	battle = Battle(player_team, opponent_team)
	return battle





