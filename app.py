import os
import json
import time
import random
import requests

import colorama
from termcolor import colored

from bs4 import BeautifulSoup

import utils as u

colorama.init()


def p(key: str):
	return json.load(open("settings.json", encoding="utf-8"))[key]

def fetch_motsqui_word() -> str:
	try:
		r = requests.get(
			"https://motsqui.com/mots-aleatoires.php?Submit=Nouveau+mot",
			headers={
				"User-Agent": "ghrlt/hangman-game"
			}
		)
	except:
		print(colored("This program must be connected to internet if you want to use this wordlist.", "red"))
		input(); exit()

	soup = BeautifulSoup(r.content, "html.parser")
	w = soup.find("b").text
	if len(w) > 18: #Design limitation
		return fetch_motsqui_word()
	return w



class Rules:
	def __init__(self):
		for key,value in p("rules").items():
			exec(f"self.{key} = {value}")
		

	def update(self, key, new_value):
		settings = json.load(open("settings.json", encoding="utf-8"))
		settings['rules'][key] = new_value

		json.dump(settings, open("settings.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)

		self.reload()

	def reload(self):
		for key,value in p("rules").items():
			exec(f"self.{key} = {value}")



class Game:
	rules = Rules()
	
	banner = [
		r"    )                    *                                          ",
		r" ( /(                  (  `                (                        ",
		r" )\())   )       (  (  )\))(     )         )\ )      )    )     (   ",
		r"((_)\ ( /(  (    )\))(((_)()\ ( /(  (     (()/(   ( /(   (     ))\  ",
		r" _((_))(_)) )\ )((_))\(_()((_))(_)) )\ )   /(_))_ )(_))  )\  '/((_) ",
		r"| || ((_)_ _(_/( (()(_)  \/  ((_)_ _(_/(  (_)) __((_)_ _((_))(_))   ",
		r"| __ / _` | ' \)) _` || |\/| / _` | ' \))   | (_ / _` | '  \() -_)  ",
		r"|_||_\__,_|_||_|\__, ||_|  |_\__,_|_||_|     \___\__,_|_|_|_|\___|  ",
		r"                |___/                                               "
	]
	hangman_design = [
		r"                                    ",
		r"        ════════════════════        ",
		r"            ║║            ║         ",
		r"            ║║            ☺         ",
		r"            ║║           /│\        ",
		r"            ║║           /‾\        ",
		r"            ║║                      ",
		r"     ════════════════               "
	]
	hangman_parts = [
		r"",
		r""+"                                    \n"*5+r"     ════════════════               ",
		r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ",
		r"        ════════════════════        "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ",
		r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ",
		r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ",
		#r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│\        "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ",
		#r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│\        "+"\n"+r"            ║║           /‾\        "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               "
	]
	if rules.add_arms_to_hangedman:
		hangman_parts.append(r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║            │         "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ")
		if rules.separate_the_two_arms_of_hangedman:
			hangman_parts.append(r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│         "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ")
		hangman_parts.append(r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│\        "+"\n"+r"            ║║                      "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ")

	if rules.add_legs_to_hangedman:
		hangman_parts.append(r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│\        "+"\n"+r"            ║║            ‾         "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ")
		if rules.separate_the_two_legs_of_hangedman:
			hangman_parts.append(r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│\        "+"\n"+r"            ║║           /‾         "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ")
		hangman_parts.append(r"        ════════════════════        "+"\n"+r"            ║║            ║         "+"\n"+r"            ║║            ☺         "+"\n"+r"            ║║           /│\        "+"\n"+r"            ║║           /‾\        "+"\n"+r"            ║║                      "+"\n"+r"     ════════════════               ")


	def __init__(self):
		self.languages = p("languages")
		self.l_list = [l for l in self.languages.values()]
		self.language = p("preferences")['language']

		self.wordlists = p("wordlists")
		self.wordlist = self.wordlists[self.language][p("preferences")['wordlist']]


	def start(self):
		self.showBanner()
		self.showMenu()

	def showBanner(self, clear=True):
		os.system('cls||clear')


		for i,line in enumerate(self.banner):
			if i < round(len(self.banner)/2):
				for char in line:
					print(colored(char, random.choice(["red", "yellow"])), end="")
				print()

			elif i >= round(len(self.banner)/3):
				for char in line:
					print(colored(char, random.choice(["red", "red", "red", "yellow"]), attrs=random.choice([["dark"], [], []])), end="")
				print()

		print( colored("—"*len(self.banner[-1]), "grey", attrs=["bold"]), end="\n" )

	def showMenu(self):
		menu = [
			{"text": "Start playing!", "action": self.startPlaying},
			{"text": "Choose language", "action": self.defineLanguage},
			{"text": "Choose wordlist source", "action": self.defineWordlist},
			{"text": "Check and personnalize the rules", "action": self.defineRules}
		]

		for i,item in enumerate(menu):
			print( colored(f"\t{i+1}›", "green"), end=" ")
			print( colored(f"{item['text']}", "yellow") )


		print()
		action = u.get_input(t=int, r=range(1, len(menu)+1))

		menu[action-1]['action']()


	def defineLanguage(self):
		self.showBanner()

		for i in range(1, len(self.l_list), 2):
			print( colored(f"\t({self.l_list[i-1][:2].upper()})", "green"), end=" ")
			print( colored(f"{self.l_list[i-1]:<15}", "yellow"), end="")

			print( colored(f"\t({self.l_list[i][:2].upper()})", "green"), end=" ")
			print( colored(f"{self.l_list[i]:<15}", "yellow") )

		if len(self.l_list) % 2 != 0:
			print( colored(f"\t({self.l_list[-1][:2].upper()})", "green"), end=" ")
			print( colored(f"{self.l_list[-1]:<15}", "yellow") )

		choice = u.get_input(t=str, l=[l[:2].upper() for l in self.l_list])


		self.language = choice.upper()
		with open("settings.json", "r", encoding="utf-8") as f:
			j = json.load(f)
		j['preferences']['language'] = self.language
		with open("settings.json", "w", encoding="utf-8") as f:
			json.dump(j, f, indent=4, ensure_ascii=False)

		print( colored("Language successfully choosen.", "green") )
		time.sleep(1)

		self.start()

	def defineWordlist(self):
		self.showBanner()

		wl = self.wordlists[self.language]

		for i in range(1, len(wl), 2):
			print( colored(f"\t{i}›", "green"), end=" ")
			print( colored(f"{wl[i-1]['source']:<20}", "yellow"), end="")

			print( colored(f"\t{i+1}›", "green"), end=" ")
			print( colored(f"{wl[i]['source']:<20}", "yellow") )

		if len(wl) % 2 != 0:
			print( colored(f"\t{len(wl)}›", "green"), end=" ")
			print( colored(f"{wl[-1]['source']:<20}", "yellow") )

		choice = u.get_input(t=int, r=range(1,len(wl)+1))


		self.wordlist = self.wordlists[self.language][choice-1]
		with open("settings.json", "r", encoding="utf-8") as f:
			j = json.load(f)
		j['preferences']['wordlist'] = choice-1
		with open("settings.json", "w", encoding="utf-8") as f:
			json.dump(j, f, indent=2, ensure_ascii=False)

		print( colored("Wordlist successfully choosen.", "green") )
		time.sleep(1)

		self.start()

	def defineRules(self):
		i=0
		for rule,state in [(r, eval(f"Rules().{r}")) for r in self.rules.__dict__ if r[:2] != "__"]:
			i+=1
			rule = ' '.join(rule.split('_')).title()
			print(colored(f"    {i}›", "green"), colored(f"{rule}:", "yellow"), colored(f"{state}", "magenta"))

		print()
		print(colored(f"    99›", "green"), colored("Go back to menu", "yellow"))

		answer = u.get_input(t=int, r=range(1,i+1), r2=range(99,100))
		if answer == 99:
			return self.start()

		rule = list(p("rules").keys())[answer-1]
		return self.defineRule(rule)

	def defineRule(self, rule):
		r = rule
		rule = ' '.join(rule.split('_')).title()

		rp = p("rules")[r]

		print(f"Set the rule \"{colored(rule, 'grey', attrs=['bold'])}\" to:")
		if type(rp) is bool:
			print(colored("True (Yes) or False (No)", "white"), end="")
			answer = u.get_input(t=bool)

		elif type(rp) == str:
			print(colored("", "white", attrs=['bold']), end="")
			answer = u.get_input(t=str)

		elif type(rp) == int:
			print(colored("Input the wanted number", "white"), end="")
			answer = u.get_input(t=int)

		self.rules.update(r, answer)
		print(colored("Successfully updated the rule.", "green"))

		time.sleep(1.5)
		return self.start()



	def startPlaying(self):
		self.showBanner()
		
		self.failed = []
		self.succeeded = []
		self.word = self.getWord()
		self.word_hidden = "_"*len(self.word)

		self.play()

	def play(self):
		for i,letter in enumerate(self.word):
			if letter in self.succeeded:
				wh = list(self.word_hidden)
				wh[i] = letter
				self.word_hidden = ''.join(wh)

		if self.word_hidden == self.word:
			return self.playerWon()
		
		errors = len(self.failed)
		hangman = self.hangman_parts[errors].split("\n")

		for i,part in enumerate(hangman):
			hangman[i] = colored(part, "grey", attrs=["bold"])

		if errors > 0:
			hangman[0] += "         Letters you tried so far:"

			hangman[2] += f"          {''.join([colored('  '+l, 'red') for l in self.failed])}"
			hangman[3] += f"          {''.join([colored('  '+l, 'green') for l in self.succeeded[:7]])}"
			hangman[4] += f"          {''.join([colored('  '+l, 'green') for l in self.succeeded[7:16]])}"


		self.showBanner()
		print('\n'.join(hangman))

		print("Your objective is to find this word:", colored(self.word_hidden, "white", attrs=["bold"]))
		print("\n")
		print(colored(f"Propose a letter {'or a word ' if self.rules.allow_word_guessing else ''}", "white", attrs=['blink', 'dark']), end="")
		answer = u.get_input(t=str, l=u.alphabet, minlength=1, maxlength=None if self.rules.allow_word_guessing else 1)
		if len(answer) > 1:
			if answer == self.word:
				return self.playerWon()
			else:
				if self.rules.lose_if_wrong_word:
					return self.playerLose()

		else:
			if answer in self.word:
				print(colored("Letter found!", "green", attrs=['bold']), end="")
				if not answer in self.succeeded:
					self.succeeded.append(answer)

				else:
					if self.rules.fail_if_letter_already_guessed:
						self.failed.append(answer) #Not sure how to represent such fail case..
					print(colored("But you had already found it..", "green"))


			else:
				print(colored("Letter not in word..", "red", attrs=['bold']), end="")
				if not answer in self.failed:
					self.failed.append(answer)

				else:
					if self.rules.fail_even_if_letter_already_tried:
						self.failed.append(answer)
					print(colored("But you already knew that..", "red"))
				
				if len(self.failed) == len(self.hangman_parts[1:]):
					return self.playerLose()

		time.sleep(1.5)
		self.play()


	def playerWon(self):
		print(colored("YOU WON!", "green", attrs=['dark', 'blink']))
		print(
			colored("The word was", "yellow", attrs=['dark']),
			colored(self.word, "white", attrs=['bold']),
			colored("!", "yellow", attrs=['dark'])
		)
		time.sleep(1)

		self.showBanner()

		print(r"             _______________                 _______________         ")
		print(r"            |@@@@|     |####|               |@@@@|     |####|        ")
		print(r"            |@@@@|     |####|               |@@@@|     |####|        ")
		print(r"            |@@@@|     |####|               |@@@@|     |####|        ")
		print(r"            \@@@@|     |####/               \@@@@|     |####/        ")
		print(r"             \@@@|     |###/                 \@@@|     |###/         ")
		print(r"              `@@|_____|##'                   `@@|_____|##'          ")
		print(r"                   (O)                             (O)               ")
		print(r"                .-'''''-.                       .-'''''-.            ")
		print(r"              .'  * * *  `.                   .'  * * *  `.          ")
		print(r"             :  *       *  :                 :  *       *  :         ")
		print(r"            : ~   Y O U   ~ :               : ~   Y O U   ~ :        ")
		print(r"            : ~   W O N   ~ :               : ~   W O N   ~ :        ")
		print(r"             :  *       *  :                 :  *       *  :         ")
		print(r"        jgs   `.  * * *  .'             jgs   `.  * * *  .'          ")
		print(r"                `-.....-'                       `-.....-'            ")
		
		print("\n\n\nPress enter to leave", end=""); input(); exit()

	def playerLose(self):
		print(colored("YOU LOSE!", "red", attrs=['dark', 'blink']))
		print(
			colored("The word was", "yellow", attrs=['dark']),
			colored(self.word, "white", attrs=['bold']),
			colored("!", "yellow", attrs=['dark'])
		)


	def getWord(self):
		exec(f"self.word = {self.wordlist['access']}.lower()")

		if self.rules.remove_accent_from_letters:
			for i,accent in enumerate(u.accents_list):
				self.word = self.word.replace(accent, u.noaccents_list[i])
		else:
			u.alphabet += u.accents_list

		return self.word





g = Game()
g.start()