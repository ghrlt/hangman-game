from termcolor import colored

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

accents_list = ["é", "è", "ê", "ë", "ù", "û", "ü", "ô", "ö", "à", "â", "ä"]
noaccents_list = ["e", "e", "e", "e", "u", "u", "u", "o", "o", "a", "a", "a"]


def get_input(t: type, r: range=None, r2: range=None, l: list=[], minlength: int=1, maxlength: int=None, case_sensitive=False):
	i = input(colored("> ", "white", attrs=['blink']))

	if t == int or t == float:
		try:
			i = int(i)
			if not (r and i in r) and not (r2 and i in r2):
				print(r, r2, "a" if r2!=None else "b")
				print(colored(f"Invalid input. Should be in {r} {'or in '+str(r2) if r2!=None else ''}", "red"))
				return get_input(t=t, r=r, r2=r2)

		except ValueError:
			print(colored(f"Invalid input. Should be of type {t}", "red"))
			return get_input(t=t, r=r)

	elif t == str:
		if (maxlength and len(i) > maxlength) or (minlength and len(i) < minlength):
			print(colored(f"Invalid input. Input length shall be between {minlength if minlength else '0'} & {maxlength if maxlength else '∞'} characters", "red"))
			return get_input(t=t, minlength=minlength, maxlength=maxlength, case_sensitive=case_sensitive)

		if case_sensitive:
			if (l and not (i in l)):
				print(colored(f"Invalid input. /!\\ It is cAsE sEnsItiVe /!\\ Should be a value in {l}", "red"))
				return get_input(t=t, l=l, case_sensitive=case_sensitive)
		else:
			if (l and not (i.upper() in l or i.lower() in l)):
				print(colored(f"Invalid input. Should be a value in {l}", "red"))
				return get_input(t=t, l=l)

	elif t == bool:
		try:
			i = int(i)
		except ValueError:
			if i.lower() not in ["true", "false", "vrai", "faux", "yes", "no", "y", "n", "o"]:
				print(colored(f"Invalid input. You must input a boolean value", "red"))
				return get_input(t=t)

		if i in [0, "n", "no", "false", "faux"]:
			i = False
		else:
			i = True

	return i
