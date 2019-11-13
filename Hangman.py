DictionaryPath = "./Dictionary.txt"

import sys
import time
import random

import Art
import ConsoleTools
from ConsoleTools import XOffset
from ConsoleTools import YOffset

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

TimeoutTime = 1.5
ConsoleTools.DialogTime = TimeoutTime

def Hangman():
	dictionary = LoadDictionary(DictionaryPath)
	word = random.choice(dictionary)
	word = word.upper()
	
	# Get individual characters of the word to compare length to guesses.
	# This will find whether it's been guessed properly or not.
	wordCharacters = []
	for character in word:
		if character not in wordCharacters:
			wordCharacters.append(character)
	
	unsuccessfulGuesses = []
	successfulGuesses = []
	
	# While guesses are less than the max amount of stages
	guessesLeft = len(Art.ArtStages) - len(unsuccessfulGuesses)
	while guessesLeft > 0:
		ConsoleTools.Clear()
		
		# Write the ASCII art
		ConsoleTools.WriteFromPosition(Art.ArtStages[len(unsuccessfulGuesses)], XOffset + 40, YOffset)

		# Write the word
		ConsoleTools.WriteFromPosition("Word:", XOffset + 4, YOffset + 1)
		ConsoleTools.WriteFromPosition(Art.GetPrintableWord(word, successfulGuesses), XOffset + 12, YOffset + 1)
		ConsoleTools.WriteFromPosition("=" * (len(word) + 2), XOffset + 11, YOffset + 2)

		# Write the guesses left
		ConsoleTools.WriteFromPosition("You have " + str(guessesLeft) + " guesses left.", XOffset, YOffset + 4)
		
		# Set cursor position to correct spot for input, then get the letter.
		ConsoleTools.SetCursor(XOffset, YOffset + 5)
		guess = input("Enter a letter: ")
		guess = guess.upper()

		# Check if it is one letter.
		if len(guess) != 1:
			ConsoleTools.DialogError("You must enter one letter.")
			continue
		
		# Check if already guessed this letter
		if guess in unsuccessfulGuesses or guess in successfulGuesses:
			ConsoleTools.DialogError("You have already guessed this letter.")
			continue
		
		if guess not in word:
			# Add to bad guesses
			unsuccessfulGuesses.append(guess)
			ConsoleTools.DialogError("Incorrect guess.")
		else:
			# Add to successful guesses
			successfulGuesses.append(guess)
			ConsoleTools.Dialog("Successful Guess!")

		# Set current guesses left
		guessesLeft = len(Art.ArtStages) - len(unsuccessfulGuesses)
		
		# Check if word is fully guessed
		if len(wordCharacters) == len(successfulGuesses): break
			
	
	# Success / Game Over
	ConsoleTools.TimeoutTime = 0.5
	if len(wordCharacters) == len(successfulGuesses):
		# Success
		ConsoleTools.Dialog("You have guessed the word!")
		ConsoleTools.WriteFromPosition(
			"The word was: " + word + ".",
			ConsoleTools.XOffset + ConsoleTools.DialogOffsetX,
			ConsoleTools.YOffset + ConsoleTools.DialogOffsetY + 1
		)
	else:
		ConsoleTools.DialogError("You have failed to guess the word.")
		ConsoleTools.WriteErrorFromPosition(
			"The word was: " + word + ".",
			ConsoleTools.XOffset + ConsoleTools.DialogOffsetX,
			ConsoleTools.YOffset + ConsoleTools.DialogOffsetY + 1
		)
	time.sleep(5.0)
	print("\n")


if __name__ == "__main__": Hangman()
