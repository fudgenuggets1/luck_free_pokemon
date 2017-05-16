import pygame, random
from moves import movedex
from typechart import BattleTypeChart
from abilities import *


class Pokemon():

	def __init__(self, pokemon):
		self.name = pokemon
		self.type_names = set(pokedex[pokemon]["types"])
		self.types = []
		for t in self.type_names:
			entry = BattleTypeChart[t]
			self.types.append(entry)
		self.base_stats = pokedex[pokemon]["baseStats"]
		self.abilities = pokedex[pokemon]["abilities"]
		self.ability = self.abilities[0]
		self.images = [pygame.image.load("images/" + self.name.lower() + "_front.png"), pygame.image.load("images/" + self.name.lower() + "_back.png")]
		self.pokecenter()
		self.update_moves(pokedex[pokemon]["learnset"])

	def update_stats(self):

		self.stats = {
			"hp": self.base_stats["hp"],
			"atk": self.base_stats["atk"],
			"def": self.base_stats["def"],
			"spa": self.base_stats["spa"],
			"spd": self.base_stats["spd"],
			"spe": self.base_stats["spe"],
		}

	def update_moves(self, learnset):

		self.learnset = []
		self.learnset[:] = []
		for move in learnset:
			new_move = movedex[move]
			self.learnset.append(new_move)

	def clear_stat_changes(self):
		self.stat_stages = {
			"hp": 0,
			"atk": 0,
			"def": 0,
			"spa": 0,
			"spd": 0,
			"spe": 0,
		}

	def apply_stat_changes(self):

		for key, var in self.stat_stages.iteritems():
			if var > 0:
				self.stats[key] = self.base_stats[key] * ((2 + var) / 2)
			elif var < 0:
				self.stats[key] = self.base_stats[key] * (2 / (2 - var))
		self.stat_status()

	def pokecenter(self):
		self.update_stats()
		self.clear_stat_changes()
		self.cureStatus()

	def cureStatus(self):
		self.status = None
		self.sleep_turns = 0
		self.toxic_turns = 0

	def stat_status(self):
		if self.status:
			self.stats["spe"] = int(int(self.base_stats["spe"] * self.status["spe"]))

			if self.ability in statusBoostAbilities:
				self.stats[statusBoostAbilities[self.ability]] = int(int(self.base_stats[statusBoostAbilities[self.ability]] * 1.5))
	

pokedex = {
	"Bulbasaur": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 21, "atk": 23, "def": 23, "spa": 31, "spd": 31, "spe": 21},
		"abilities": ["Overgrow", "Chlorophyll"],
		"learnset": ["sludgebomb", "gigadrain", "ancientpower", "leechseed"],
	},
	"Ivysaur": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 22, "atk": 23, "def": 23, "spa": 30, "spd": 30, "spe": 22},
		"abilities": ["Overgrow", "Chlorophyll"],
		"learnset": ["sludgebomb", "gigadrain", "ancientpower", "leechseed"],
	},
	"Venusaur": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 23, "atk": 23, "def": 23, "spa": 29, "spd": 29, "spe": 23},
		"abilities": ["Overgrow", "Chlorophyll"],
		"learnset": ["sludgebomb", "gigadrain", "ancientpower", "leechseed"],
	},
	"Charmander": {
		"types": ["Fire"],
		"baseStats": {"hp": 19, "atk": 25, "def": 21, "spa": 29, "spd": 24, "spe": 32},
		"abilities": ["Blaze", "Solar Power"],
		"learnset": ["flamethrower", "ancientpower", "thunderpunch", "willowisp"],
	},
	"Charmeleon": {
		"types": ["Fire"],
		"baseStats": {"hp": 21, "atk": 24, "def": 21, "spa": 30, "spd": 24, "spe": 30},
		"abilities": ["Blaze", "Solar Power"],
		"learnset": ["flamethrower", "ancientpower", "thunderpunch", "willowisp"],
	},
	"Charizard": {
		"types": ["Fire", "Flying"],
		"baseStats": {"hp": 22, "atk": 23, "def": 22, "spa": 31, "spd": 24, "spe": 28},
		"abilities": ["Blaze", "Solar Power"],
		"learnset": ["flamethrower", "earthquake", "thunderpunch", "willowisp"],
	},
	"Squirtle": {
		"types": ["Water"],
		"baseStats": {"hp": 21, "atk": 23, "def": 31, "spa": 24, "spd": 30, "spe": 21},
		"abilities": ["Torrent", "Rain Dish"],
		"learnset": ["aquajet", "surf", "icebeam", "toxic"],
	},
	"Wartortle": {
		"types": ["Water"],
		"baseStats": {"hp": 22, "atk": 23, "def": 30, "spa": 24, "spd": 30, "spe": 21},
		"abilities": ["Torrent", "Rain Dish"],
		"learnset": ["aquajet", "surf", "icebeam", "toxic"],
	},
	"Blastoise": {
		"types": ["Water"],
		"baseStats": {"hp": 22, "atk": 24, "def": 28, "spa": 24, "spd": 30, "spe": 22},
		"abilities": ["Torrent", "Rain Dish"],
		"learnset": ["aquajet", "surf", "icebeam", "toxic"],
	},
	"Butterfree": {
		"types": ["Bug", "Flying"],
		"baseStats": {"hp": 23, "atk": 17, "def": 19, "spa": 34, "spd": 30, "spe": 27},
		"abilities": ["Tinted Lens"],
		"learnset": ["bugbuzz", "energyball", "psychic", "uturn"],
	},
	"Beedrill": {
		"types": ["Bug", "Poison"],
		"baseStats": {"hp": 25, "atk": 34, "def": 15, "spa": 17, "spd": 30, "spe": 29},
		"abilities": ["Swarm"],
		"learnset": ["poisonjab", "xscissor", "brickbreak", "uturn"],
	},
	"Pidgey": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 24, "atk": 27, "def": 24, "spa": 21, "spd": 21, "spe": 33},
		"abilities": ["Big Pecks"],
		"learnset": ["bravebird", "doubleedge", "steelwing", "uturn"],
	},
	"Pidgeotto": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 27, "atk": 26, "def": 24, "spa": 21, "spd": 21, "spe": 31},
		"abilities": ["Big Pecks"],
		"learnset": ["bravebird", "doubleedge", "steelwing", "uturn"],
	},
	"Pidgeot": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 26, "atk": 25, "def": 23, "spa": 22, "spd": 22, "spe": 32},
		"abilities": ["Big Pecks"],
		"learnset": ["bravebird", "doubleedge", "steelwing", "uturn"],
	},
	"Rattata": {
		"types": ["Normal"],
		"baseStats": {"hp": 18, "atk": 33, "def": 21, "spa": 15, "spd": 21, "spe": 42},
		"abilities": ["Guts"],
		"learnset": ["doubleedge", "suckerpunch", "flamewheel", "uturn"],
	},
	"Raticate": {
		"types": ["Normal"],
		"baseStats": {"hp": 20, "atk": 29, "def": 22, "spa": 18, "spd": 25, "spe": 35},
		"abilities": ["Guts"],
		"learnset": ["doubleedge", "suckerpunch", "flamewheel", "uturn"],
	},
	"Spearow": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 23, "atk": 34, "def": 17, "spa": 18, "spd": 18, "spe": 40},
		"abilities": ["Sniper"],
		"learnset": ["doubleedge", "drillpeck", "drillrun", "uturn"],
	},
	"Fearow": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 22, "atk": 30, "def": 22, "spa": 21, "spd": 21, "spe": 34},
		"abilities": ["Sniper"],
		"learnset": ["doubleedge", "drillpeck", "drillrun", "uturn"],
	},
	"Ekans": {
		"types": ["Poison"],
		"baseStats": {"hp": 18, "atk": 31, "def": 23, "spa": 21, "spd": 28, "spe": 29},
		"abilities": ["Intimidate"],
		"learnset": ["poisonjab", "earthquake", "suckerpunch", "aquatail"],
	},
	"Arbok": {
		"types": ["Poison"],
		"baseStats": {"hp": 20, "atk": 32, "def": 23, "spa": 22, "spd": 26, "spe": 27},
		"abilities": ["Intimidate"],
		"learnset": ["poisonjab", "earthquake", "suckerpunch", "aquatail"],
	},
	"Pichu": {
		"types": ["Electric"],
		"baseStats": {"hp": 14, "atk": 29, "def": 11, "spa": 26, "spd": 26, "spe": 44},
		"abilities": ["Lightning Rod"],
		"learnset": ["volttackle", "surf", "irontail", "voltswitch"],
	},
	"Pikachu": {
		"types": ["Electric"],
		"baseStats": {"hp": 17, "atk": 26, "def": 19, "spa": 23, "spd": 23, "spe": 42},
		"abilities": ["Lightning Rod"],
		"learnset": ["volttackle", "surf", "irontail", "voltswitch"],
	},
	"Raichu": {
		"types": ["Electric"],
		"baseStats": {"hp": 18, "atk": 28, "def": 17, "spa": 28, "spd": 25, "spe": 34},
		"abilities": ["Lightning Rod"],
		"learnset": ["volttackle", "surf", "irontail", "voltswitch"],
	},
	"Sandshrew": {
		"types": ["Ground"],
		"baseStats": {"hp": 25, "atk": 38, "def": 43, "spa": 9, "spd": 15, "spe": 20},
		"abilities": ["Sand Rush"],
		"learnset": ["earthquake", "rockslide", "rapidspin", "stealthrock"],
	},
	"Sandslash": {
		"types": ["Ground"],
		"baseStats": {"hp": 25, "atk": 33, "def": 37, "spa": 15, "spd": 18, "spe": 22},
		"abilities": ["Sand Rush"],
		"learnset": ["earthquake", "rockslide", "rapidspin", "stealthrock"],
	},
	"Nidoranf": {
		"types": ["Poison"],
		"baseStats": {"hp": 30, "atk": 26, "def": 28, "spa": 22, "spd": 22, "spe": 22},
		"abilities": ["Poison Point"],
		"learnset": ["poisonjab", "suckerpunch", "irontail", "doubleedge"],
	},
	"Nidorina": {
		"types": ["Poison"],
		"baseStats": {"hp": 29, "atk": 25, "def": 27, "spa": 23, "spd": 23, "spe": 23},
		"abilities": ["Poison Point"],
		"learnset": ["poisonjab", "suckerpunch", "irontail", "doubleedge"],
	},
	"Nidoqueen": {
		"types": ["Poison", "Ground"],
		"baseStats": {"hp": 27, "atk": 27, "def": 26, "spa": 22, "spd": 25, "spe": 23},
		"abilities": ["Poison Point"],
		"learnset": ["poisonjab", "suckerpunch", "earthquake", "icepunch"],
	},
	"Nidoranm": {
		"types": ["Poison"],
		"baseStats": {"hp": 25, "atk": 31, "def": 22, "spa": 22, "spd": 22, "spe": 28},
		"abilities": ["Poison Point"],
		"learnset": ["poisonjab", "suckerpunch", "irontail", "drillrun"],
	},
	"Nidorino": {
		"types": ["Poison"],
		"baseStats": {"hp": 25, "atk": 29, "def": 23, "spa": 23, "spd": 23, "spe": 27},
		"abilities": ["Poison Point"],
		"learnset": ["poisonjab", "suckerpunch", "irontail", "drillrun"],
	},
	"Nidoking": {
		"types": ["Poison", "Ground"],
		"baseStats": {"hp": 24, "atk": 30, "def": 23, "spa": 25, "spd": 22, "spe": 25},
		"abilities": ["Poison Point"],
		"learnset": ["poisonjab", "suckerpunch", "earthquake", "icepunch"],
	},
	"Cleffa": {
		"types": ["Fairy"],
		"baseStats": {"hp": 35, "atk": 17, "def": 19, "spa": 31, "spd": 38, "spe": 10},
		"abilities": ["Magic Guard"],
		"learnset": ["psychic", "flamethrower", "toxic", "wish"],
	},
	"Clefairy": {
		"types": ["Fairy"],
		"baseStats": {"hp": 33, "atk": 21, "def": 22, "spa": 28, "spd": 30, "spe": 16},
		"abilities": ["Magic Guard"],
		"learnset": ["moonblast", "icebeam", "thunderbolt", "wish"],
	},
	"Clefable": {
		"types": ["Fairy"],
		"baseStats": {"hp": 28, "atk": 22, "def": 23, "spa": 30, "spd": 28, "spe": 19},
		"abilities": ["Magic Guard"],
		"learnset": ["moonblast", "flamethrower", "stealthrock", "wish"],
	},
	"Vulpix": {
		"types": ["Fire"],
		"baseStats": {"hp": 19, "atk": 20, "def": 20, "spa": 25, "spd": 33, "spe": 33},
		"abilities": ["Drought", "Flash Fire"],
		"learnset": ["flamethrower", "energyball", "willowisp", "quickattack"],
	},
	"Ninetails": {
		"types": ["Fire"],
		"baseStats": {"hp": 22, "atk": 22, "def": 22, "spa": 24, "spd": 30, "spe": 30},
		"abilities": ["Drought", "Flash Fire"],
		"learnset": ["flamethrower", "energyball", "willowisp", "quickattack"],
	},
	"Jigglypuff": {
		"types": ["Normal", "Fairy"],
		"baseStats": {"hp": 64, "atk": 25, "def": 11, "spa": 25, "spd": 14, "spe": 11},
		"abilities": ["Competitive"],
		"learnset": ["moonblast", "doubleedge", "flamethrower", "wish"],
	},
	"Wigglytuff": {
		"types": ["Normal", "Fairy"],
		"baseStats": {"hp": 48, "atk": 24, "def": 16, "spa": 29, "spd": 17, "spe": 16},
		"abilities": ["Competitive"],
		"learnset": ["moonblast", "doubleedge", "flamethrower", "wish"],
	},
	"Zubat": {
		"types": ["Flying", "Poison"],
		"baseStats": {"hp": 24, "atk": 28, "def": 22, "spa": 18, "spd": 24, "spe": 34},
		"abilities": ["Infiltrator"],
		"learnset": ["bravebird", "poisonjab", "steelwing", "uturn"],
	},
	"Golbat": {
		"types": ["Flying", "Poison"],
		"baseStats": {"hp": 25, "atk": 26, "def": 23, "spa": 21, "spd": 25, "spe": 30},
		"abilities": ["Infiltrator"],
		"learnset": ["bravebird", "poisonjab", "steelwing", "uturn"],
	},
	"Crobat": {
		"types": ["Flying", "Poison"],
		"baseStats": {"hp": 24, "atk": 25, "def": 22, "spa": 20, "spd": 22, "spe": 37},
		"abilities": ["Infiltrator"],
		"learnset": ["bravebird", "poisonjab", "steelwing", "uturn"],
	},
	"Oddish": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 21, "atk": 23, "def": 26, "spa": 35, "spd": 31, "spe": 14},
		"abilities": ["Chlorophyll"],
		"learnset": ["sludgebomb", "gigadrain", "leechseed", "sleeppowder"],
	},
	"Gloom": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 23, "atk": 25, "def": 27, "spa": 32, "spd": 28, "spe": 15},
		"abilities": ["Chlorophyll"],
		"learnset": ["sludgebomb", "gigadrain", "leechseed", "sleeppowder"],
	},
	"Vileplume": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 23, "atk": 24, "def": 26, "spa": 34, "spd": 28, "spe": 15},
		"abilities": ["Chlorophyll"],
		"learnset": ["sludgebomb", "gigadrain", "leechseed", "sleeppowder"],
	},
	"Paras": {
		"types": ["Grass", "Bug"],
		"baseStats": {"hp": 18, "atk": 37, "def": 29, "spa": 24, "spd": 29, "spe": 13},
		"abilities": ["Dry Skin"],
		"learnset": ["leechlife", "seedbomb", "leechseed", "spore"],
	},
	"Parasect": {
		"types": ["Grass", "Bug"],
		"baseStats": {"hp": 22, "atk": 35, "def": 30, "spa": 22, "spd": 30, "spe": 11},
		"abilities": ["Dry Skin"],
		"learnset": ["leechlife", "seedbomb", "leechseed", "spore"],
	},
	"Venonat": {
		"types": ["Poison", "Bug"],
		"baseStats": {"hp": 30, "atk": 27, "def": 25, "spa": 20, "spd": 25, "spe": 23},
		"abilities": ["Tinted Lens"],
		"learnset": ["leechlife", "sludgebomb", "toxicspikes", "sleeppowder"],
	},
	"Venomoth": {
		"types": ["Poison", "Bug"],
		"baseStats": {"hp": 23, "atk": 22, "def": 20, "spa": 30, "spd": 25, "spe": 30},
		"abilities": ["Tinted Lens"],
		"learnset": ["bugbuzz", "sludgebomb", "psychic", "sleeppowder"],
	},
	"Diglett": {
		"types": ["Ground"],
		"baseStats": {"hp": 6, "atk": 31, "def": 14, "spa": 20, "spd": 25, "spe": 54},
		"abilities": ["Arena Trap"],
		"learnset": ["earthquake", "rockslide", "suckerpunch", "aerialace"],
	},
	"Dugtrio": {
		"types": ["Ground"],
		"baseStats": {"hp": 12, "atk": 35, "def": 18, "spa": 18, "spd": 25, "spe": 42},
		"abilities": ["Arena Trap"],
		"learnset": ["earthquake", "rockslide", "suckerpunch", "aerialace"],
	},
	"Meowth": {
		"types": ["Normal"],
		"baseStats": {"hp": 20, "atk": 23, "def": 18, "spa": 21, "spd": 21, "spe": 47},
		"abilities": ["Technician"],
		"learnset": ["fakeout", "doubleedge", "bite", "uturn"],
	},
	"Persian": {
		"types": ["Normal"],
		"baseStats": {"hp": 22, "atk": 24, "def": 21, "spa": 22, "spd": 22, "spe": 39},
		"abilities": ["Technician"],
		"learnset": ["fakeout", "doubleedge", "bite", "uturn"],
	},
	"Psyduck": {
		"types": ["Water"],
		"baseStats": {"hp": 23, "atk": 24, "def": 23, "spa": 31, "spd": 23, "spe": 26},
		"abilities": ["Cloud Nine", "Swift Swim"],
		"learnset": ["surf", "icebeam", "psychic", "yawn"],
	},
	"Golduck": {
		"types": ["Water"],
		"baseStats": {"hp": 24, "atk": 24, "def": 23, "spa": 29, "spd": 24, "spe": 26},
		"abilities": ["Cloud Nine", "Swift Swim"],
		"learnset": ["surf", "icebeam", "psychic", "encore"],
	},
	"Mankey": {
		"types": ["Fighting"],
		"baseStats": {"hp": 20, "atk": 39, "def": 17, "spa": 17, "spd": 22, "spe": 35},
		"abilities": ["Vital Spirit", "Defiant"],
		"learnset": ["closecombat", "uturn", "thunderpunch", "icepunch"],
	},
	"Primeape": {
		"types": ["Fighting"],
		"baseStats": {"hp": 21, "atk": 35, "def": 20, "spa": 20, "spd": 23, "spe": 31},
		"abilities": ["Vital Spirit", "Defiant"],
		"learnset": ["closecombat", "uturn", "earthquake", "rockslide"],
	},
	"Growlithe": {
		"types": ["Fire"],
		"baseStats": {"hp": 24, "atk": 30, "def": 19, "spa": 30, "spd": 21, "spe": 26},
		"abilities": ["Intimidate", "Flash Fire", "Justified"],
		"learnset": ["flareblitz", "wildcharge", "closecombat", "willowisp"],
	},
	"Arcanine": {
		"types": ["Fire"],
		"baseStats": {"hp": 24, "atk": 30, "def": 22, "spa": 26, "spd": 22, "spe": 26},
		"abilities": ["Intimidate", "Flash Fire", "Justified"],
		"learnset": ["flareblitz", "wildcharge", "closecombat", "extremespeed"],
	},
	"Poliwag": {
		"types": ["Water"],
		"baseStats": {"hp": 20, "atk": 25, "def": 20, "spa": 20, "spd": 20, "spe": 45},
		"abilities": ["Water Absorb", "Swift Swim"],
		"learnset": ["waterfall", "return", "icebeam", "hypnosis"],
	},
	"Poliwhirl": {
		"types": ["Water"],
		"baseStats": {"hp": 25, "atk": 25, "def": 25, "spa": 20, "spd": 20, "spe": 35},
		"abilities": ["Water Absorb", "Swift Swim"],
		"learnset": ["waterfall", "return", "icebeam", "hypnosis"],
	},
	"Poliwrath": {
		"types": ["Water", "Fighting"],
		"baseStats": {"hp": 27, "atk": 25, "def": 29, "spa": 21, "spd": 27, "spe": 21},
		"abilities": ["Water Absorb", "Swift Swim"],
		"learnset": ["waterfall", "brickbreak", "icebeam", "hypnosis"],
	},
	"Abra": {
		"types": ["Psychic"],
		"baseStats": {"hp": 12, "atk": 9, "def": 7, "spa": 51, "spd": 27, "spe": 44},
		"abilities": ["Magic Guard"],
		"learnset": ["psychic", "dazzlinggleam", "energyball", "signalbeam"],
	},
	"Kadabra": {
		"types": ["Psychic"],
		"baseStats": {"hp": 15, "atk": 12, "def": 11, "spa": 45, "spd": 26, "spe": 40},
		"abilities": ["Magic Guard"],
		"learnset": ["psychic", "dazzlinggleam", "energyball", "encore"],
	},
	"Alakazam": {
		"types": ["Psychic"],
		"baseStats": {"hp": 17, "atk": 13, "def": 14, "spa": 41, "spd": 29, "spe": 36},
		"abilities": ["Magic Guard"],
		"learnset": ["psychic", "dazzlinggleam", "energyball", "encore"],
	},
	"Machop": {
		"types": ["Fighting"],
		"baseStats": {"hp": 35, "atk": 39, "def": 25, "spa": 17, "spd": 17, "spe": 17},
		"abilities": ["Guts"],
		"learnset": ["crosschop", "knockoff", "rockslide", "poisonjab"],
	},
	"Machoke": {
		"types": ["Fighting"],
		"baseStats": {"hp": 30, "atk": 37, "def": 26, "spa": 18, "spd": 22, "spe": 17},
		"abilities": ["Guts"],
		"learnset": ["crosschop", "knockoff", "rockslide", "poisonjab"],
	},
	"Machamp": {
		"types": ["Fighting"],
		"baseStats": {"hp": 27, "atk": 39, "def": 24, "spa": 19, "spd": 25, "spe": 16},
		"abilities": ["Guts"],
		"learnset": ["crosschop", "knockoff", "rockslide", "poisonjab"],
	},
	"Bellsprout": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 25, "atk": 38, "def": 17, "spa": 35, "spd": 15, "spe": 20},
		"abilities": ["Chlorophyll", "Gluttony"],
		"learnset": ["poisonjab", "powerwhip", "gigadrain", "suckerpunch"],
	},
	"Weepinbell": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 25, "atk": 35, "def": 19, "spa": 33, "spd": 17, "spe": 21},
		"abilities": ["Chlorophyll", "Gluttony"],
		"learnset": ["poisonjab", "powerwhip", "gigadrain", "suckerpunch"],
	},
	"Victreebel": {
		"types": ["Grass", "Poison"],
		"baseStats": {"hp": 25, "atk": 32, "def": 20, "spa": 31, "spd": 21, "spe": 21},
		"abilities": ["Chlorophyll", "Gluttony"],
		"learnset": ["poisonjab", "powerwhip", "gigadrain", "suckerpunch"],
	},
	"Tentacool": {
		"types": ["Water", "Poison"],
		"baseStats": {"hp": 18, "atk": 18, "def": 16, "spa": 22, "spd": 45, "spe": 31},
		"abilities": ["Liquid Ooze", "Clear Body", "Rain Dish"],
		"learnset": ["sludgewave", "surf", "rapidspin", "toxicspikes"],
	},
	"Tentacruel": {
		"types": ["Water", "Poison"],
		"baseStats": {"hp": 23, "atk": 20, "def": 19, "spa": 23, "spd": 35, "spe": 30},
		"abilities": ["Liquid Ooze", "Clear Body", "Rain Dish"],
		"learnset": ["sludgewave", "surf", "rapidspin", "toxicspikes"],
	},
	"Geodude": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 20, "atk": 40, "def": 50, "spa": 15, "spd": 15, "spe": 10},
		"abilities": ["Sturdy", "Rock Head"],
		"learnset": ["earthquake", "stoneedge", "suckerpunch", "stealthrock"],
	},
	"Graveler": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 21, "atk": 37, "def": 44, "spa": 17, "spd": 17, "spe": 14},
		"abilities": ["Sturdy", "Rock Head"],
		"learnset": ["earthquake", "stoneedge", "suckerpunch", "stealthrock"],
	},
	"Golem": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 24, "atk": 36, "def": 39, "spa": 17, "spd": 20, "spe": 14},
		"abilities": ["Sturdy", "Rock Head"],
		"learnset": ["earthquake", "stoneedge", "suckerpunch", "stealthrock"],
	},
	"Ponyta": {
		"types": ["Fire"],
		"baseStats": {"hp": 18, "atk": 31, "def": 20, "spa": 24, "spd": 24, "spe": 33},
		"abilities": ["Flash Fire", "Flame Body"],
		"learnset": ["flareblitz", "wildcharge", "irontail", "willowisp"],
	},
	"Rapidash": {
		"types": ["Fire"],
		"baseStats": {"hp": 19, "atk": 30, "def": 21, "spa": 24, "spd": 24, "spe": 32},
		"abilities": ["Flash Fire", "Flame Body"],
		"learnset": ["flareblitz", "wildcharge", "irontail", "willowisp"],
	},
	"Slowpoke": {
		"types": ["Water", "Psychic"],
		"baseStats": {"hp": 43, "atk": 31, "def": 31, "spa": 19, "spd": 19, "spe": 7},
		"abilities": ["Regenerator", "Oblivious"],
		"learnset": ["aquatail", "zenheadbutt", "flamethrower", "thunderwave"],
	},
	"Slowbro": {
		"types": ["Water", "Psychic"],
		"baseStats": {"hp": 29, "atk": 23, "def": 34, "spa": 31, "spd": 24, "spe": 9},
		"abilities": ["Regenerator", "Oblivious"],
		"learnset": ["surf", "psychic", "flamethrower", "thunderwave"],
	},
	"Slowking": {
		"types": ["Water", "Psychic"],
		"baseStats": {"hp": 29, "atk": 23, "def": 24, "spa": 31, "spd": 34, "spe": 9},
		"abilities": ["Regenerator", "Oblivious"],
		"learnset": ["surf", "psychic", "flamethrower", "thunderwave"],
	},
	"Magnemite": {
		"types": ["Electric", "Steel"],
		"baseStats": {"hp": 12, "atk": 16, "def": 32, "spa": 44, "spd": 25, "spe": 21},
		"abilities": ["Sturdy", "Analytic", "Magnet Pull"],
		"learnset": ["thunderbolt", "flashcannon", "voltswitch", "signalbeam"],
	},
	"Magneton": {
		"types": ["Electric", "Steel"],
		"baseStats": {"hp": 16, "atk": 19, "def": 31, "spa": 39, "spd": 23, "spe": 23},
		"abilities": ["Sturdy", "Analytic", "Magnet Pull"],
		"learnset": ["thunderbolt", "flashcannon", "voltswitch", "signalbeam"],
	},
	"Magnezone": {
		"types": ["Electric", "Steel"],
		"baseStats": {"hp": 20, "atk": 20, "def": 32, "spa": 36, "spd": 25, "spe": 17},
		"abilities": ["Sturdy", "Analytic", "Magnet Pull"],
		"learnset": ["thunderbolt", "flashcannon", "voltswitch", "signalbeam"],
	},
	"Farfetchd": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 21, "atk": 36, "def": 22, "spa": 23, "spd": 24, "spe": 24},
		"abilities": ["Defiant", "Inner Focus"],
		"learnset": ["bravebird", "leafblade", "quickattack", "uturn"],
	},
	"Doduo": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 17, "atk": 41, "def": 22, "spa": 17, "spd": 17, "spe": 36},
		"abilities": ["Early Bird"],
		"learnset": ["bravebird", "knockoff", "quickattack", "jumpkick"],
	},
	"Dodrio": {
		"types": ["Normal", "Flying"],
		"baseStats": {"hp": 19, "atk": 35, "def": 23, "spa": 19, "spd": 19, "spe": 35},
		"abilities": ["Early Bird"],
		"learnset": ["bravebird", "knockoff", "quickattack", "jumpkick"],
	},
	"Seel": {
		"types": ["Water"],
		"baseStats": {"hp": 30, "atk": 21, "def": 25, "spa": 21, "spd": 32, "spe": 21},
		"abilities": ["Thick Fat", "Hydration", "Ice Body"],
		"learnset": ["fakeout", "aquajet", "aquatail", "drillrun"],
	},
	"Dewgong": {
		"types": ["Water", "Ice"],
		"baseStats": {"hp": 29, "atk": 22, "def": 25, "spa": 22, "spd": 30, "spe": 22},
		"abilities": ["Thick Fat", "Hydration", "Ice Body"],
		"learnset": ["fakeout", "aquajet", "iceshard", "toxic"],
	},
	"Grimer": {
		"types": ["Poison"],
		"baseStats": {"hp": 37, "atk": 37, "def": 23, "spa": 18, "spd": 23, "spe": 12},
		"abilities": ["Poison Touch"],
		"learnset": ["poisonjab", "firepunch", "shadowsneak", "icepunch"],
	},
	"Muk": {
		"types": ["Poison"],
		"baseStats": {"hp": 32, "atk": 32, "def": 23, "spa": 19, "spd": 30, "spe": 14},
		"abilities": ["Poison Touch"],
		"learnset": ["poisonjab", "firepunch", "shadowsneak", "icepunch"],
	},
	"Shellder": {
		"types": ["Water"],
		"baseStats": {"hp": 15, "atk": 32, "def": 49, "spa": 22, "spd": 12, "spe": 20},
		"abilities": ["Overcoat"],
		"learnset": ["razorshell", "avalanche", "iceshard", "rapidspin"],
	},
	"Cloyster": {
		"types": ["Water", "Ice"],
		"baseStats": {"hp": 14, "atk": 27, "def": 52, "spa": 24, "spd": 13, "spe": 20},
		"abilities": ["Overcoat"],
		"learnset": ["razorshell", "iceshard", "spikes", "toxicspikes"],
	},
	"Gastly": {
		"types": ["Ghost", "Poison"],
		"baseStats": {"hp": 15, "atk": 16, "def": 15, "spa": 48, "spd": 17, "spe": 39},
		"abilities": ["Levitate"],
		"learnset": ["sludgewave", "shadowball", "thunderbolt", "dazzlinggleam"],
	},
	"Haunter": {
		"types": ["Ghost", "Poison"],
		"baseStats": {"hp": 17, "atk": 18, "def": 17, "spa": 43, "spd": 20, "spe": 35},
		"abilities": ["Levitate"],
		"learnset": ["sludgewave", "shadowball", "thunderbolt", "dazzlinggleam"],
	},
	"Gengar": {
		"types": ["Ghost", "Poison"],
		"baseStats": {"hp": 18, "atk": 19, "def": 18, "spa": 39, "spd": 23, "spe": 33},
		"abilities": ["Levitate"],
		"learnset": ["sludgewave", "shadowball", "thunderbolt", "dazzlinggleam"],
	},
	"Onix": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 14, "atk": 18, "def": 62, "spa": 11, "spd": 18, "spe": 27},
		"abilities": ["Sturdy", "Rock Head", "Weak Armor"],
		"learnset": ["earthquake", "stoneedge", "stealthrock", "taunt"],
	},
	"Steelix": {
		"types": ["Ground", "Steel"],
		"baseStats": {"hp": 22, "atk": 25, "def": 59, "spa": 16, "spd": 19, "spe": 9},
		"abilities": ["Sturdy", "Rock Head", "Sheer Force"],
		"learnset": ["earthquake", "ironhead", "stealthrock", "toxic"],
	},
	"Drowzee": {
		"types": ["Psychic"],
		"baseStats": {"hp": 27, "atk": 22, "def": 21, "spa": 20, "spd": 41, "spe": 19},
		"abilities": ["Forewarn", "Inner Focus", "Insomnia"],
		"learnset": ["zenheadbutt", "thunderpunch", "icepunch", "drainpunch"],
	},
	"Hypno": {
		"types": ["Psychic"],
		"baseStats": {"hp": 26, "atk": 23, "def": 22, "spa": 23, "spd": 35, "spe": 21},
		"abilities": ["Forewarn", "Inner Focus", "Insomnia"],
		"learnset": ["zenheadbutt", "thunderpunch", "icepunch", "drainpunch"],
	},
	"Krabby": {
		"types": ["Water"],
		"baseStats": {"hp": 14, "atk": 48, "def": 42, "spa": 11, "spd": 12, "spe": 23},
		"abilities": ["Sheer Force", "Hyper Cutter"],
		"learnset": ["crabhammer", "knockoff", "superpower", "return"],
	},
	"Kingler": {
		"types": ["Water"],
		"baseStats": {"hp": 17, "atk": 41, "def": 36, "spa": 16, "spd": 16, "spe": 24},
		"abilities": ["Sheer Force", "Hyper Cutter"],
		"learnset": ["crabhammer", "knockoff", "superpower", "return"],
	},
	"Voltorb": {
		"types": ["Electric"],
		"baseStats": {"hp": 18, "atk": 14, "def": 23, "spa": 25, "spd": 25, "spe": 45},
		"abilities": ["Static", "Soundproof"],
		"learnset": ["taunt", "thunderbolt", "voltswitch", "signalbeam"],
	},
	"Electrode": {
		"types": ["Electric"],
		"baseStats": {"hp": 18, "atk": 15, "def": 21, "spa": 25, "spd": 25, "spe": 46},
		"abilities": ["Static", "Soundproof"],
		"learnset": ["taunt", "thunderbolt", "voltswitch", "signalbeam"],
	},
	"Exeggcute": {
		"types": ["Grass", "Psychic"],
		"baseStats": {"hp": 28, "atk": 18, "def": 37, "spa": 28, "spd": 21, "spe": 18},
		"abilities": ["Chlorophyll", "Harvest"],
		"learnset": ["psychic", "gigadrain", "leechseed", "toxic"],
	},
	"Exeggutor": {
		"types": ["Grass", "Psychic"],
		"baseStats": {"hp": 27, "atk": 27, "def": 24, "spa": 35, "spd": 21, "spe": 16},
		"abilities": ["Chlorophyll", "Harvest"],
		"learnset": ["psychic", "gigadrain", "leechseed", "toxic"],
	},
	"Cubone": {
		"types": ["Ground"],
		"baseStats": {"hp": 23, "atk": 23, "def": 45, "spa": 19, "spd": 23, "spe": 17},
		"abilities": ["Rock Head"],
		"learnset": ["bonemerang", "stealthrock", "firepunch", "doubleedge"],
	},
	"Marowak": {
		"types": ["Ground"],
		"baseStats": {"hp": 21, "atk": 28, "def": 39, "spa": 18, "spd": 28, "spe": 16},
		"abilities": ["Rock Head"],
		"learnset": ["bonemerang", "stealthrock", "firepunch", "doubleedge"],
	},
	"Hitmonlee": {
		"types": ["Fighting"],
		"baseStats": {"hp": 16, "atk": 40, "def": 17, "spa": 12, "spd": 36, "spe": 29},
		"abilities": ["Limber", "Reckless", "Unburden"],
		"learnset": ["closecombat", "stoneedge", "suckerpunch", "earthquake"],
	},
	"Hitmonchan": {
		"types": ["Fighting"],
		"baseStats": {"hp": 16, "atk": 35, "def": 26, "spa": 12, "spd": 36, "spe": 25},
		"abilities": ["Iron Fist", "Inner Focus"],
		"learnset": ["drainpunch", "stoneedge", "machpunch", "rapidspin"],
	},
	"Hitmontop": {
		"types": ["Fighting"],
		"baseStats": {"hp": 16, "atk": 31, "def": 31, "spa": 12, "spd": 36, "spe": 24},
		"abilities": ["Intimidate", "Technician"],
		"learnset": ["closecombat", "stoneedge", "suckerpunch", "rapidspin"],
	},
	"Lickitung": {
		"types": ["Normal"],
		"baseStats": {"hp": 35, "atk": 22, "def": 29, "spa": 23, "spd": 29, "spe": 12},
		"abilities": ["Cloud Nine", "Oblivious"],
		"learnset": ["return", "earthquake", "thunderbolt", "icebeam"],
	},
	"Lickilicky": {
		"types": ["Normal"],
		"baseStats": {"hp": 32, "atk": 25, "def": 28, "spa": 23, "spd": 28, "spe": 14},
		"abilities": ["Cloud Nine"],
		"learnset": ["return", "earthquake", "thunderbolt", "icebeam"],
	},
	"Koffing": {
		"types": ["Poison"],
		"baseStats": {"hp": 18, "atk": 29, "def": 42, "spa": 27, "spd": 20, "spe": 15},
		"abilities": ["Levitate"],
		"learnset": ["sludgewave", "flamethrower", "willowisp", "painsplit"],
	},
	"Weezing": {
		"types": ["Poison"],
		"baseStats": {"hp": 20, "atk": 28, "def": 37, "spa": 26, "spd": 21, "spe": 18},
		"abilities": ["Levitate"],
		"learnset": ["sludgewave", "flamethrower", "willowisp", "painsplit"],
	},
	"Rhyhorn": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 35, "atk": 37, "def": 41, "spa": 13, "spd": 13, "spe": 11},
		"abilities": ["Reckless", "Rock Head"],
		"learnset": ["earthquake", "stoneedge", "megahorn", "stealthrock"],
	},
	"Rhydon": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 33, "atk": 40, "def": 37, "spa": 14, "spd": 14, "spe": 12},
		"abilities": ["Reckless", "Rock Head"],
		"learnset": ["earthquake", "stoneedge", "megahorn", "stealthrock"],
	},
	"Rhyperior": {
		"types": ["Ground", "Rock"],
		"baseStats": {"hp": 32, "atk": 39, "def": 36, "spa": 16, "spd": 16, "spe": 11},
		"abilities": ["Solid Rock", "Reckless", "Rock Head"],
		"learnset": ["earthquake", "stoneedge", "megahorn", "stealthrock"],
	},
	"Chansey": {
		"types": ["Normal"],
		"baseStats": {"hp": 83, "atk": 2, "def": 2, "spa": 11, "spd": 35, "spe": 17},
		"abilities": ["Natural Cure"],
		"learnset": ["hypervoice", "icebeam", "thunderwave", "stealthrock"],
	},
	"Tangela": {
		"types": ["Grass"],
		"baseStats": {"hp": 22, "atk": 19, "def": 40, "spa": 34, "spd": 14, "spe": 21},
		"abilities": ["Regenerator", "Chlorophyll"],
		"learnset": ["gigadrain", "sludgebomb", "ancientpower", "sleeppowder"],
	},
	"Tangrowth": {
		"types": ["Grass"],
		"baseStats": {"hp": 28, "atk": 28, "def": 35, "spa": 31, "spd": 14, "spe": 14},
		"abilities": ["Regenerator", "Chlorophyll"],
		"learnset": ["gigadrain", "earthquake", "knockoff", "sleeppowder"],
	},
	"Kangaskhan": {
		"types": ["Normal"],
		"baseStats": {"hp": 32, "atk": 29, "def": 24, "spa": 13, "spd": 24, "spe": 28},
		"abilities": ["Scrappy"],
		"learnset": ["fakeout", "doubleedge", "earthquake", "suckerpunch"],
	},
	"Horsea": {
		"types": ["Water"],
		"baseStats": {"hp": 15, "atk": 19, "def": 36, "spa": 36, "spd": 13, "spe": 31},
		"abilities": ["Swift Swim"],
		"learnset": ["surf", "icebeam", "toxic", "raindance"],
	},
	"Seadra": {
		"types": ["Water"],
		"baseStats": {"hp": 19, "atk": 22, "def": 32, "spa": 32, "spd": 16, "spe": 29},
		"abilities": ["Poison Point","Swift Swim"],
		"learnset": ["surf", "icebeam", "toxic", "raindance"],
	},
	"Kingdra": {
		"types": ["Water", "Dragon"],
		"baseStats": {"hp": 22, "atk": 26, "def": 26, "spa": 26, "spd": 26, "spe": 24},
		"abilities": ["Swift Swim"],
		"learnset": ["surf", "icebeam", "dragonpulse", "ironhead"],
	},
	"Goldeen": {
		"types": ["Water"],
		"baseStats": {"hp": 21, "atk": 31, "def": 28, "spa": 16, "spd": 24, "spe": 30},
		"abilities": ["Lightning Rod" ,"Swift Swim"],
		"learnset": ["aquatail", "drillrun", "knockoff", "megahorn"],
	},
	"Seaking": {
		"types": ["Water"],
		"baseStats": {"hp": 27, "atk": 31, "def": 21, "spa": 21, "spd": 26, "spe": 23},
		"abilities": ["Lightning Rod" ,"Swift Swim"],
		"learnset": ["aquatail", "drillrun", "knockoff", "megahorn"],
	},
	"Staryu": {
		"types": ["Water"],
		"baseStats": {"hp": 13, "atk": 20, "def": 24, "spa": 31, "spd": 24, "spe": 38},
		"abilities": ["Natural Cure", "Analytic"],
		"learnset": ["surf", "icebeam", "psychic", "thunderbolt"],
	},
	"Starmie": {
		"types": ["Water", "Psychic"],
		"baseStats": {"hp": 17, "atk": 21, "def": 25, "spa": 29, "spd": 25, "spe": 33},
		"abilities": ["Natural Cure", "Analytic"],
		"learnset": ["surf", "icebeam", "psychic", "thunderbolt"],
	},
	"MimeJr": {
		"types": ["Fairy", "Psychic"],
		"baseStats": {"hp": 10, "atk": 12, "def": 22, "spa": 34, "spd": 43, "spe": 29},
		"abilities": ["Filter", "Soundproof", "Technician"],
		"learnset": ["psychic", "signalbeam", "shadowball", "thunderbolt"],
	},
	"MrMime": {
		"types": ["Fairy", "Psychic"],
		"baseStats": {"hp": 13, "atk": 15, "def": 21, "spa": 33, "spd": 39, "spe": 29},
		"abilities": ["Filter", "Soundproof", "Technician"],
		"learnset": ["psychic", "dazzlinggleam", "shadowball", "thunderbolt"],
	},
	"Scyther": {
		"types": ["Bug", "Flying"],
		"baseStats": {"hp": 21, "atk": 33, "def": 24, "spa": 16, "spd": 24, "spe": 32},
		"abilities": ["Technician", "Swarm"],
		"learnset": ["uturn", "aerialace", "knockoff", "quickattack"],
	},
	"Scizor": {
		"types": ["Bug", "Steel"],
		"baseStats": {"hp": 21, "atk": 39, "def": 30, "spa": 16, "spd": 24, "spe": 20},
		"abilities": ["Technician", "Swarm"],
		"learnset": ["uturn", "bulletpunch", "knockoff", "superpower"],
	},
	"Smoochum": {
		"types": ["Ice", "Psychic"],
		"baseStats": {"hp": 22, "atk": 15, "def": 7, "spa": 42, "spd": 32, "spe": 32},
		"abilities": ["Forewarn", "Oblivious"],
		"learnset": ["icebeam", "psychic", "signalbeam", "shadowball"],
	},
	"Jynx": {
		"types": ["Ice", "Psychic"],
		"baseStats": {"hp": 21, "atk": 16, "def": 12, "spa": 38, "spd": 31, "spe": 31},
		"abilities": ["Dry Skin", "Forewarn", "Oblivious"],
		"learnset": ["icebeam", "psychic", "energyball", "lovelykiss"],
	},
	"Elekid": {
		"types": ["Electric"],
		"baseStats": {"hp": 19, "atk": 26, "def": 15, "spa": 27, "spd": 23, "spe": 40},
		"abilities": ["Static", "Vital Spirit"],
		"learnset": ["thunderbolt", "voltswitch", "psychic", "crosschop"],
	},
	"Electabuzz": {
		"types": ["Electric"],
		"baseStats": {"hp": 20, "atk": 25, "def": 18, "spa": 29, "spd": 26, "spe": 32},
		"abilities": ["Static", "Vital Spirit"],
		"learnset": ["thunderbolt", "voltswitch", "psychic", "crosschop"],
	},
	"Electivire": {
		"types": ["Electric"],
		"baseStats": {"hp": 21, "atk": 34, "def": 19, "spa": 26, "spd": 24, "spe": 26},
		"abilities": ["Motor Drive", "Vital Spirit"],
		"learnset": ["wildcharge", "voltswitch", "flamethrower", "earthquake"],
	},
	"Magby": {
		"types": ["Fire"],
		"baseStats": {"hp": 18, "atk": 31, "def": 15, "spa": 29, "spd": 23, "spe": 34},
		"abilities": ["Flame Body", "Vital Spirit"],
		"learnset": ["flareblitz", "crosschop", "machpunch", "thunderpunch"],
	},
	"Magmar": {
		"types": ["Fire"],
		"baseStats": {"hp": 20, "atk": 29, "def": 17, "spa": 30, "spd": 26, "spe": 28},
		"abilities": ["Flame Body", "Vital Spirit"],
		"learnset": ["heatwave", "crosschop", "machpunch", "thunderpunch"],
	},
	"Magmortar": {
		"types": ["Fire"],
		"baseStats": {"hp": 21, "atk": 26, "def": 19, "spa": 35, "spd": 26, "spe": 23},
		"abilities": ["Flame Body", "Vital Spirit"],
		"learnset": ["heatwave", "thunderbolt", "machpunch", "earthquake"],
	},
	"Pinsir": {
		"types": ["Bug"],
		"baseStats": {"hp": 19, "atk": 38, "def": 30, "spa": 16, "spd": 21, "spe": 26},
		"abilities": ["Mold Breaker", "Moxie"],
		"learnset": ["xscissor", "earthquake", "stoneedge", "closecombat"],
	},
	"Tauros": {
		"types": ["Normal"],
		"baseStats": {"hp": 23, "atk": 31, "def": 29, "spa": 12, "spd": 21, "spe": 34},
		"abilities": ["Intimidate", "Sheer Force"],
		"learnset": ["doubleedge", "earthquake", "stoneedge", "zenheadbutt"],
	},
	"Magikarp": {
		"types": ["Water"],
		"baseStats": {"hp": 15, "atk": 8, "def": 41, "spa": 11, "spd": 15, "spe": 60},
		"abilities": ["Swift Swim"],
		"learnset": ["hydropump", "return", "splash", "magikarpsrevenge"],
	},
	"Gyarados": {
		"types": ["Water", "Flying"],
		"baseStats": {"hp": 26, "atk": 35, "def": 22, "spa": 16, "spd": 28, "spe": 23},
		"abilities": ["Intimidate", "Moxie"],
		"learnset": ["aquatail", "earthquake", "stoneedge", "icefang"],
	},
	"Lapras": {
		"types": ["Water", "Ice"],
		"baseStats": {"hp": 36, "atk": 24, "def": 22, "spa": 24, "spd": 27, "spe": 17},
		"abilities": ["Water Absorb"],
		"learnset": ["aquatail", "freezedry", "thunderbolt", "icebeam"],
	},
	"Vaporeon": {
		"types": ["Water"],
		"baseStats": {"hp": 37, "atk": 19, "def": 17, "spa": 31, "spd": 27, "spe": 19},
		"abilities": ["Water Absorb"],
		"learnset": ["surf", "icebeam", "toxic", "wish"],
	},
	"Jolteon": {
		"types": ["Electric"],
		"baseStats": {"hp": 19, "atk": 19, "def": 17, "spa": 31, "spd": 27, "spe": 37},
		"abilities": ["Volt Absorb"],
		"learnset": ["thunderbolt", "voltswitch", "signalbeam", "irontail"],
	},
	"Flareon": {
		"types": ["Fire"],
		"baseStats": {"hp": 19, "atk": 37, "def": 17, "spa": 27, "spd": 31, "spe": 19},
		"abilities": ["Flash Fire", "Guts"],
		"learnset": ["flareblitz", "superpower", "quickattack", "irontail"],
	},
	"Espeon": {
		"types": ["Psychic"],
		"baseStats": {"hp": 19, "atk": 19, "def": 17, "spa": 37, "spd": 27, "spe": 31},
		"abilities": ["Magic Bounce"],
		"learnset": ["psychic", "shadowball", "dazzlinggleam", "psyshock"],
	},
	"Umbreon": {
		"types": ["Dark"],
		"baseStats": {"hp": 27, "atk": 19, "def": 31, "spa": 17, "spd": 37, "spe": 19},
		"abilities": ["Synchronize"],
		"learnset": ["foulplay", "toxic", "taunt", "wish"],
	},
	"Leafeon": {
		"types": ["Grass"],
		"baseStats": {"hp": 19, "atk": 31, "def": 37, "spa": 17, "spd": 19, "spe": 27},
		"abilities": ["Chlorophyll"],
		"learnset": ["leafblade", "knockoff", "doubleedge", "xscissor"],
	},
	"Glaceon": {
		"types": ["Ice"],
		"baseStats": {"hp": 19, "atk": 17, "def": 31, "spa": 37, "spd": 27, "spe": 19},
		"abilities": ["Ice Body"],
		"learnset": ["icebeam", "shadowball", "signalbeam", "toxic"],
	},
	"Porygon": {
		"types": ["Normal"],
		"baseStats": {"hp": 25, "atk": 23, "def": 27, "spa": 32, "spd": 28, "spe": 15},
		"abilities": ["Trace", "Analytic"],
		"learnset": ["triattack", "psychic", "icebeam", "thunderbolt"],
	},
	"Porygon2": {
		"types": ["Normal"],
		"baseStats": {"hp": 25, "atk": 23, "def": 26, "spa": 31, "spd": 28, "spe": 17},
		"abilities": ["Trace", "Analytic"],
		"learnset": ["triattack", "psychic", "icebeam", "thunderbolt"],
	},
	"Porygon-Z": {
		"types": ["Normal"],
		"baseStats": {"hp": 24, "atk": 22, "def": 20, "spa": 38, "spd": 21, "spe": 25},
		"abilities": ["Adaptability", "Analytic"],
		"learnset": ["triattack", "psychic", "icebeam", "thunderbolt"],
	},
	"Omanyte": {
		"types": ["Water", "Rock"],
		"baseStats": {"hp": 15, "atk": 17, "def": 42, "spa": 38, "spd": 23, "spe": 15},
		"abilities": ["Swift Swim", "Weak Armor"],
		"learnset": ["surf", "earthpower", "icebeam", "stealthrock"],
	},
	"Omastar": {
		"types": ["Water", "Rock"],
		"baseStats": {"hp": 21, "atk": 18, "def": 38, "spa": 35, "spd": 21, "spe": 17},
		"abilities": ["Swift Swim", "Weak Armor"],
		"learnset": ["surf", "ancientpower", "icebeam", "stealthrock"],
	},
	"Kabuto": {
		"types": ["Water", "Rock"],
		"baseStats": {"hp": 13, "atk": 34, "def": 38, "spa": 23, "spd": 19, "spe": 23},
		"abilities": ["Swift Swim", "Weak Armor"],
		"learnset": ["rockslide", "waterfall", "aquajet", "rapidspin"],
	},
	"Kabutops": {
		"types": ["Water", "Rock"],
		"baseStats": {"hp": 18, "atk": 35, "def": 32, "spa": 20, "spd": 21, "spe": 24},
		"abilities": ["Swift Swim", "Weak Armor"],
		"learnset": ["stoneedge", "aquatail", "aquajet", "rapidspin"],
	},
	"Aerodactyl": {
		"types": ["Flying", "Rock"],
		"baseStats": {"hp": 23, "atk": 31, "def": 19, "spa": 17, "spd": 22, "spe": 38},
		"abilities": ["Rock Head", "Unnerve"],
		"learnset": ["stoneedge", "aquatail", "earthquake", "aerialace"],
	},
	"Munchlax": {
		"types": ["Normal"],
		"baseStats": {"hp": 52, "atk": 33, "def": 15, "spa": 15, "spd": 33, "spe": 2},
		"abilities": ["Thick Fat", "Gluttony"],
		"learnset": ["return", "earthquake", "firepunch", "toxic"],
	},
	"Snorlax": {
		"types": ["Normal"],
		"baseStats": {"hp": 44, "atk": 31, "def": 18, "spa": 18, "spd": 31, "spe": 8},
		"abilities": ["Thick Fat", "Gluttony", "Immunity"],
		"learnset": ["return", "earthquake", "firepunch", "toxic"],
	},
	"Articuno": {
		"types": ["Flying", "Ice"],
		"baseStats": {"hp": 23, "atk": 22, "def": 26, "spa": 25, "spd": 32, "spe": 22},
		"abilities": ["Ice Body"],
		"learnset": ["hurricane", "icebeam", "freezedry", "uturn"],
	},
	"Zapdos": {
		"types": ["Flying", "Electric"],
		"baseStats": {"hp": 23, "atk": 23, "def": 22, "spa": 33, "spd": 23, "spe": 26},
		"abilities": ["Static"],
		"learnset": ["thunderbolt", "voltswitch", "heatwave", "uturn"],
	},
	"Moltres": {
		"types": ["Flying", "Fire"],
		"baseStats": {"hp": 23, "atk": 26, "def": 23, "spa": 33, "spd": 22, "spe": 23},
		"abilities": ["Flame Body"],
		"learnset": ["heatwave", "hurricane", "roost", "uturn"],
	},
	"Dratini": {
		"types": ["Dragon"],
		"baseStats": {"hp": 21, "atk": 32, "def": 22, "spa": 25, "spd": 25, "spe": 25},
		"abilities": ["Marvel Scale"],
		"learnset": ["dragonrush", "extremespeed", "flamethrower", "irontail"],
	},
	"Dragonair": {
		"types": ["Dragon"],
		"baseStats": {"hp": 22, "atk": 30, "def": 23, "spa": 25, "spd": 25, "spe": 25},
		"abilities": ["Marvel Scale"],
		"learnset": ["dragonrush", "extremespeed", "flamethrower", "irontail"],
	},
	"Dragonite": {
		"types": ["Dragon", "Flying"],
		"baseStats": {"hp": 23, "atk": 33, "def": 24, "spa": 25, "spd": 25, "spe": 20},
		"abilities": ["Multiscale"],
		"learnset": ["dragonrush", "extremespeed", "firepunch", "earthquake"],
	},
	"Mewtwo": {
		"types": ["Psychic"],
		"baseStats": {"hp": 23, "atk": 24, "def": 20, "spa": 34, "spd": 20, "spe": 29},
		"abilities": ["Unnerve"],
		"learnset": ["psystrike", "aurasphere", "icebeam", "flamethrower"],
	},
	"Mew": {
		"types": ["Psychic"],
		"baseStats": {"hp": 25, "atk": 25, "def": 25, "spa": 25, "spd": 25, "spe": 25},
		"abilities": ["Synchronize"],
		"learnset": ["psychic", "uturn", "willowisp", "stealthrock"],
	},


}

# Checking all the moves are in the moves.movedex

letters = set(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
for letter in letters:
	letter = letter.lower()
pokemon_list = []
pokemon_names = []
for pokemon in pokedex:
	pokemon_names.append(pokemon)
	poke = Pokemon(pokemon)
	pokemon_list.append(poke)
for pokemon in pokemon_list:
	for move in pokemon.learnset:
		try:
			if move[0] in letters:
				x = move["name"]
		except:
			pass
			#print move["name"]
	try:
		BattleAbilities[pokemon.ability.lower()]
	except:
		print pokemon.ability.lower()

def pokemon_team_to_names(team):
	names = []
	for pokemon in team:
		names.append(pokemon.name)
	return names

def duplicate_pokemon_team(team):
	return make_team(pokemon_team_to_names(team))

def make_team(team_names):
	team = []
	for name in team_names:
		mon = Pokemon(name)
		team.append(mon)
	return team

def random_team():
	team_names = set([])
	while len(team_names) < 6:
		name = random.choice(pokemon_names)
		team_names.add(name)
	team = make_team(team_names)
	return team

def player_team():
	team_names = ["Articuno", "Alakazam", "Doduo", "Beedrill", "Graveler", "Dragonite"]
	return make_team(team_names)

def opponent_team():
	#return opponent
	team_names = ["Diglett", "Cloyster", "Munchlax", "Moltres", "Dragonite", "Leafeon"]
	return make_team(team_names)

# RBY ELITE 4
Lorelei = make_team(["Dewgong", "Cloyster", "Slowbro", "Jynx", "Lapras", "Seaking"])
Bruno = make_team(["Onix", "Hitmonchan", "Hitmonlee", "Steelix", "Machamp", "Kabutops"])
Agatha = make_team(["Gengar", "Golbat", "Haunter", "Arbok", "Gastly", "Muk"])
Lance = make_team(["Gyarados", "Dratini", "Dragonair", "Aerodactyl", "Dragonite", "Farfetchd"])
squirtle_chosen = make_team(["Pidgeot", "Alakazam", "Rhydon", "Arcanine", "Gyarados", "Venusaur"])
bulbasaur_chosen = make_team(["Pidgeot", "Alakazam", "Rhydon", "Gyarados", "Exeggutor", "Charizard"])
charmander_chosen = make_team(["Pidgeot", "Alakazam", "Rhydon", "Exeggutor", "Arcanine", "Blastoise"])

TrumpCard = make_team(["Starmie", "Rhydon", "Alakazam", "Dragonite", "Zapdos", "Tauros"])
rby_stars = make_team(["Rhydon", "Tauros", "Snorlax", "Exeggutor", "Starmie", "Alakazam"])
Giovanni = make_team(["Rhyhorn", "Dugtrio", "Nidoqueen", "Nidoking", "Rhydon", "Marowak"])

# Pokemon with the highest stats
superlatives = make_team(["Chansey", "Krabby", "Onix", "Abra", "Tentacool", "Magikarp"])
second_best = make_team(["Jigglypuff", "Doduo", "Steelix", "Gastly", "MimeJr", "Diglett"])
colettes_cuties = make_team(["Pichu", "Cleffa", "Oddish", "Squirtle", "Horsea", "Pikachu"])

elite_four = [Lorelei, Bruno, Agatha, Lance, squirtle_chosen, bulbasaur_chosen, charmander_chosen, TrumpCard, rby_stars, Giovanni, superlatives, second_best]


opponent = Lorelei


