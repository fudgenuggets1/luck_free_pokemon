from __future__ import division
import math
from abilities import *

def get_stab(pokemon, move):
	stab = 1
	if move["type"] in pokemon.type_names:
		stab = 1.5
		if pokemon.ability == "Adaptability":
			stab = 2
	else:
		stab = 1
	return stab

def damage_calc(attacker, defender, move):
	# Damage Calculation
	# Damage = (0.44*(attack/defense)*move power)*modifier
	if move["category"] == "Physical":
		if move["name"] == "Foul Play":
			attack = defender.stats["atk"]
		else:
			attack = attacker.stats["atk"]
		defense = defender.stats["def"]
	elif move["category"] == "Special":		
		attack = attacker.stats["spa"]
		if move["name"] == "Psyshock" or move["name"] == "Psystrike":
			defense = defender.stats["def"]
		else:	
			defense = defender.stats["spd"]

	power = move["basePower"]

	# STAB
	STAB = get_stab(attacker, move)
	# Type Advantage
	if attacker.ability != "Mold Breaker":
		alter_ability = damage_alter_ability(defender, move)
	else:
		alter_ability = 1	
	TA = type_advantage(defender, move)
	# Burn
	Burn = 1
	if attacker.status and attacker.ability != "Guts":
		if attacker.status["name"] == "Burn" and move["category"] == "Physical":
			Burn = 0.5
	# Modifier(Other)
	atk_ability, def_ability = process_both_abilities(attacker, defender, move)

	# Damage calculation 
	# Modifier = Weather * STAB * Type effectiveness * Burn * other(items, abilities)
	modifier = STAB * TA * Burn * atk_ability * def_ability * alter_ability

	level = (((2 * defender.base_stats["hp"]) / 5) + 2) / 50
	#level += 0.5

	damage = math.floor((((attack / defense) * (power / 10)) / (2-level)) * modifier)

	if damage < 1 and TA and alter_ability:
		damage = 1

	return damage

def type_advantage(defender, move):
	type_advantage = 1

	tas = {
		"0": 1,
		"1": 2,
		"2": 0.5,
		"3": 0,
	}

	numbers = []
	for typ in defender.types:	
		numbers.append(typ["damageTaken"][move["type"]])
	if len(numbers) == 1:
		type_advantage = tas[str(numbers[0])]
	elif numbers[0] == 3 or numbers[1] == 3:
		type_advantage = tas[str(3)]
	else:		
		type_advantage = tas[str(numbers[0])] * tas[str(numbers[1])]

	return type_advantage

def process_both_abilities(attacker, defender, move):
	return process_attacker_ability(attacker, defender, move), process_defender_ability(defender, attacker, move)

def process_attacker_ability(pokemon, defender, move):
	modifier = 1
	pinchAbilities = set(["Blaze", "Overgrow", "Torrent", "Swarm"])
	basepower = move["basePower"]
	TA = type_advantage(defender, move)

	if pokemon.ability in pinchAbilities:
		if pokemon.stats["hp"] < pokemon.base_stats["hp"] / 3 and get_stab(pokemon, move) > 1:
			modifier = 1.5
		else:
			return modifier

	elif pokemon.ability == "Technician" and basepower <= 60:
		modifier = 1.5
	elif pokemon.ability == "Iron Fist" and "punch" in move["flags"]:
		modifier = 1.2
	elif pokemon.ability == "Tinted Lens" and TA < 1:
		modifier = 2
	
	return modifier

def process_defender_ability(pokemon, attacker, move):
	TA = type_advantage(pokemon, move)
	modifier = 1
	if pokemon.ability == "Multiscale" and pokemon.stats["hp"] == pokemon.base_stats["hp"]:
		modifier = 0.5
	elif pokemon.ability == "Solid Rock" or pokemon.ability == "Filter":
		if TA > 1:
			modifier = 0.75

	return modifier

def damage_alter_ability(defender, move):
	if defender.ability in damageAlterAbilities:
		for t in damageAlterAbilities[defender.ability]["type"]:
			if move["type"] == t:
				if damageAlterAbilities[defender.ability]["effect"]["immune"]:
					return 0
				else:
					return 0.5
	return 1
	



