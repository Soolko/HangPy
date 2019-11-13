DictionaryPath = "./Dictionary.txt"

import random

import Art

def LoadDictionary(path: str) -> list:
	# Load file
	file = None
	try:
		file = open(path)
	except FileNotFoundError:
		print("Could not find Dictionary file \"" + path + "\".")
		exit(0)
	assert file != None

	# Load into single string.
	contents = ""
	for line in file: contents += line + "\n"
	
	# Format newlines into spaces
	formatted = ""
	for character in contents: formatted += character if character != '\n' else ' '

	# Split up into dictionary
	dictionary = []
	current = ""
	for character in formatted:
		if character == ' ':
			if current == "": continue
			dictionary.append(current)
			current = ""
		else: current += character
	
	# Return that dictionary
	return dictionary

def Hangman():
	dictionary = LoadDictionary(DictionaryPath)
	word = random.choice(dictionary)
	word = word.upper()
	guesses = []

if __name__ == "__main__":
	Hangman()
