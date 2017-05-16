from __future__ import division
import pygame, math
from damage_calc import *


def stay_alive(pokemon, opponent, opponent_party):
	strongest_move = opponent_move(pokemon, opponent)
	pokemon_strongest_move = opponent_move(opponent, pokemon)
	safest_switch = best_switch(pokemon, opponent_party)
	safest_switch_best_move = opponent_move(pokemon, safest_switch)
	
	safest_switch_damage = damage_calc(safest_switch, pokemon, safest_switch_best_move)

	# If player's pokemon is faster and will kill the opponent
	# but the opponent has a pokemon that can take two hits and
	# kill the player's pokemon. 
	move = False
	#if pokemon.stats["spe"] > opponent.stats["spe"]:
	if not move:
		
		damage = damage_calc(pokemon, opponent, pokemon_strongest_move)
		
		if opponent.stats["hp"] - damage <= 0:
	
			
			damage = damage_calc(pokemon, safest_switch, pokemon_strongest_move)
			
			pokemon_strongest_move = opponent_move(safest_switch, pokemon)
			
			pokemon_damage = damage_calc(pokemon, safest_switch, pokemon_strongest_move)
	
			test_pokemon_health = pokemon.stats["hp"]
			test_safest_switch_health = safest_switch.stats["hp"] - damage
			if pokemon.stats["spe"] > safest_switch.stats["spe"]:
				
				while test_pokemon_health > 0 and test_safest_switch_health > 0:
					test_safest_switch_health -= pokemon_damage
					if test_safest_switch_health > 0:
						test_pokemon_health -= safest_switch_damage
			
			if pokemon.stats["spe"] <= safest_switch.stats["spe"]:

				while test_pokemon_health > 0 and test_safest_switch_health > 0:
					test_pokemon_health -= safest_switch_damage
					if test_pokemon_health > 0:
						test_safest_switch_health -= pokemon_damage
			
			if test_pokemon_health <= 0:
				return safest_switch
			# In case a pokemon is faster and can take a hit and kill.
			# I had Tangela vs the opponent's Slowpoke and the opponent
			# had a Munchlax and a Ghastly. Munchlax takes hits better
			# and is the safest_switch. Ghastly is the actual safest
			# switch (and best switch) but was not tested before this code. 
			elif test_pokemon_health > 0:
				safest_switch = best_switch(pokemon, opponent_party, True)
				safest_switch_best_move = opponent_move(pokemon, safest_switch)
				
				
				safest_switch_damage = damage_calc(safest_switch, pokemon, safest_switch_best_move)
				
				damage = damage_calc(pokemon, safest_switch, pokemon_strongest_move)
				
				pokemon_strongest_move = opponent_move(safest_switch, pokemon)
				
				pokemon_damage = damage_calc(pokemon, safest_switch, pokemon_strongest_move)
		
				test_pokemon_health = pokemon.stats["hp"]
				test_safest_switch_health = safest_switch.stats["hp"] - damage
				if pokemon.stats["spe"] > safest_switch.stats["spe"]:
				
					while test_pokemon_health > 0 and test_safest_switch_health > 0:
						test_safest_switch_health -= pokemon_damage
						if test_safest_switch_health > 0:
							test_pokemon_health -= safest_switch_damage
				
				if pokemon.stats["spe"] <= safest_switch.stats["spe"]:

					while test_pokemon_health > 0 and test_safest_switch_health > 0:
						test_pokemon_health -= safest_switch_damage
						if test_pokemon_health > 0:
							test_safest_switch_health -= pokemon_damage
			if test_pokemon_health <= 0:
				return safest_switch
	return move

def type_vs_type(type1, type2):
	ta = 1
	for resist in type1.resist_list:
		if type2.name == resist:
			ta = 1

def best_switch(pokemon, opponent_party, dead=False):
	
	damages = []
	faster_switches = []
	
	for choice in opponent_party:
		best_move = opponent_move(choice, pokemon)
		damage = damage_calc(pokemon, choice, best_move)
		damages.append([choice, damage])

		if choice.stats["spe"] > pokemon.stats["spe"]:
			move = opponent_move(pokemon, choice)			
			damage = damage_calc(choice, pokemon, move)
			if pokemon.stats["hp"] - damage <= 0:
				faster_switches.append(choice)

	damages = sorted(damages, key=lambda x: x[1], reverse=False)
	if len(faster_switches):
		return faster_switches[0]
	
	return damages[0][0]

def opponent_move(pokemon, opponent):

	def test_damage(move):
		return damage_calc(opponent, pokemon, move)
	moves = []	
	for move in opponent.learnset:
		if move["basePower"]:
			moves.append(move)
	while len(moves) > 1:
		if test_damage(moves[0]) > test_damage(moves[1]):
			moves.remove(moves[1])
		elif test_damage(moves[0]) < test_damage(moves[1]):
			moves.remove(moves[0])
		else:
			moves.remove(moves[1])
	return moves[0]

def who_wins(pokemon, opponent):
	test_pokemon_health = pokemon.stats["hp"]
	test_opponent_health = opponent.stats["hp"]
	move = opponent_move(opponent, pokemon)
	
	pokemon_damage = damage_calc(pokemon, opponent, move)
	move = opponent_move(pokemon, opponent)
	
	opponent_damage = damage_calc(opponent, pokemon, move)
	if pokemon.stats["spe"] > opponent.stats["spe"]:
				
		while test_pokemon_health > 0 and test_opponent_health > 0:
			test_opponent_health -= pokemon_damage
			if test_opponent_health > 0:
				test_pokemon_health -= opponent_damage
	
	else:

		while test_pokemon_health > 0 and test_opponent_health > 0:
			test_pokemon_health -= opponent_damage
			if test_pokemon_health > 0:
				test_opponent_health -= pokemon_damage
	info = "loses"
	if test_opponent_health > 0:
		info = "wins"
	return info

def test_party(pokemon, opponent, opponent_party):
	pass
 
def check_pokemon(pokemon, opponent, opponent_party):
	
	if opponent.stats["hp"] <= 0:
		pass

def send_in_pokemon(pokemon_party):
	switch = None
	for pokemon in pokemon_party:
		if pokemon.stats["hp"] > 0:
			switch = pokemon
			break

	return switch

def best_move(player, opponent):
	
	#return opponent.current_pokemon.learnset[2]
	strongest_move = opponent_move(player.current_pokemon, opponent.current_pokemon)
	#stongest_switch = best_switch(player.current_pokemon, opponent.pokemon_party)
	
	damage = damage_calc(opponent.current_pokemon, player.current_pokemon, strongest_move)
	wins = who_wins(player.current_pokemon, opponent.current_pokemon)

	stayin_alive = len(opponent.pokemon_party)
	if stayin_alive:
		stayin_alive = stay_alive(player.current_pokemon, opponent.current_pokemon, opponent.pokemon_party)

	if stayin_alive and opponent.active_turns:
		move = stayin_alive
	else:
		move = strongest_move
	return move











		