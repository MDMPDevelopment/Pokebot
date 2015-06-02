import praw
import requests
import json
import re
import time
import sys

names = [
			'bulbasaur', 
			'ivysaur', 
			'venusaur', 
			'charmander', 
			'charmeleon', 
			'charizard', 
			'squirtle', 
			'wartortle', 
			'blastoise', 
			'caterpie', 
			'metapod', 
			'butterfree', 
			'weedle', 
			'kakuna', 
			'beedrill', 
			'pidgey', 
			'pidgeotto', 
			'pidgeot', 
			'rattata', 
			'raticate', 
			'spearow', 
			'fearow', 
			'ekans', 
			'arbok', 
			'pikachu', 
			'raichu', 
			'sandshrew', 
			'sandslash', 
			'nidoranf', 
			'nidorina', 
			'nidoqueen', 
			'nidoranm', 
			'nidorino', 
			'nidoking', 
			'clefairy', 
			'clefable', 
			'vulpix', 
			'ninetales', 
			'jigglypuff', 
			'wigglytuff', 
			'zubat', 
			'golbat', 
			'oddish', 
			'gloom', 
			'vileplume', 
			'paras', 
			'parasect', 
			'venonat', 
			'venomoth', 
			'diglett', 
			'dugtrio', 
			'meowth', 
			'persian', 
			'psyduck', 
			'golduck', 
			'mankey', 
			'primeape', 
			'growlithe', 
			'arcanine', 
			'poliwag', 
			'poliwhirl', 
			'poliwrath', 
			'abra', 
			'kadabra', 
			'alakazam', 
			'machop', 
			'machoke', 
			'machamp', 
			'bellsprout', 
			'weepinbell', 
			'victreebel', 
			'tentacool', 
			'tentacruel', 
			'geodude', 
			'graveler', 
			'golem', 
			'ponyta', 
			'rapidash', 
			'slowpoke', 
			'slowbro', 
			'magnemite', 
			'magneton', 
			"farfetchd", 
			'doduo', 
			'dodrio', 
			'seel', 
			'dewgong', 
			'grimer', 
			'muk', 
			'shellder', 
			'cloyster', 
			'gastly', 
			'haunter', 
			'gengar', 
			'onix', 
			'drowzee', 
			'hypno', 
			'kingler', 
			'voltorb', 
			'electrode', 
			'exeggcute', 
			'exeggutor', 
			'cubone', 
			'marowak', 
			'hitmonlee', 
			'hitmonchan', 
			'lickitung', 
			'koffing', 
			'weezing', 
			'rhyhorn', 
			'rhydon', 
			'chansey', 
			'tangela', 
			'kangaskhan', 
			'horsea', 
			'seadra', 
			'goldeen', 
			'seaking', 
			'staryu', 
			'starmie', 
			'mr. mime', 
			'scyther', 
			'jynx', 
			'electabuzz', 
			'magmar', 
			'pinsir', 
			'tauros', 
			'magikarp', 
			'gyarados', 
			'lapras', 
			'ditto', 
			'eevee', 
			'vaporeon', 
			'jolteon', 
			'flareon', 
			'porygon', 
			'omanyte', 
			'omastar', 
			'kabuto', 
			'kabutops', 
			'aerodactyl', 
			'snorlax', 
			'articuno', 
			'zapdos', 
			'moltres', 
			'dratini', 
			'dragonair', 
			'dragonite', 
			'mewtwo', 
			'mew'
		]

base = 'http://www.pokeapi.co'

user_agent = "any:autopokedex:v1.0.2"

def get_pokemon(poke_id, base):					# Retreives Pokedex
	entry = '/api/v1/pokemon/' + str(poke_id)	# information for the
											    # specified Pokemon
	data = requests.get(base + entry)		    # from the pokeapi.
	dex = json.loads(data.text)
	data.close()
	
	return dex

def get_posts(reddit, name, num=10):		# Returns list of 
	sub = reddit.get_subreddit(name)		# PRAW post objects
	gen = sub.get_new(limit=num)			# from specified sub.
	
	return list(gen)

def mentor(comment, matches, base):
	# Ensure id is valid integer.
	try:
		num = int(matches[0])
	except ValueError as e:
		num = names.index(matches[0].lower()) + 1
	
	dex = get_pokemon(num, base)
	
	name = dex['name']
	description = json.loads(requests.get(base + dex['descriptions'][0]['resource_uri']).text)['description']
	
	response = name + ': \n' + description
	
	# Prevent program crash if bot replies too frequently.
	try:
		comment.reply(response)
	except:
		print("Comment not handled")

def parse_posts(posts, base):				# Checks for Pokedex
	for post in posts:						# request, then 
		for comment in post.comments:		# serves requests via mentor function.
			matches = re.findall(r'^Pokedex ([A-Za-z]+|\d{1,3})$', comment.body)
			
			if len(matches) > 0:
				responders = [rep.author.name for rep in comment.replies]
				
				if 'pokebot5000' not in responders:
					mentor(comment, matches, base)
		
		time.sleep(3)

def main(base, user_agent, cons_args):					# Console arguments
	r = praw.Reddit(user_agent=user_agent)	# passed include:
	r.login(cons_args[0], cons_args[1])		# username, password,
											# all watched subs.
	while True:
		for sub in cons_args[2:]:
			posts = get_posts(r, sub)
			parse_posts(posts, base)
		
		time.sleep(180)

if __name__ == '__main__':
	main(base, user_agent, sys.argv[1:])