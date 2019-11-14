DictionaryPath = "./Dictionary.txt"
Version = "Submission 2"

import sys
import time
import random

import Text
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

def Game():
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
	def GetGuesses() -> int:
		base = len(Text.ArtStages) - len(unsuccessfulGuesses)
		for char in unsuccessfulGuesses:
			if char in "AEIOU":
				base -= 1
		return base

	while GetGuesses() > 0:
		ConsoleTools.Clear()
		
		# Write the ASCII art
		ConsoleTools.WriteFromPosition(Text.ArtStages[len(unsuccessfulGuesses)], XOffset + 50, YOffset + 2)

		# Write the word
		ConsoleTools.WriteFromPosition("Word:", XOffset + 4, YOffset + 2)
		ConsoleTools.WriteFromPosition(Text.GetPrintableWord(word, successfulGuesses), XOffset + 12, YOffset + 2)

		# Write unsuccessful guesses
		ConsoleTools.WriteErrorFromPosition("Unsuccessful Guesses:", XOffset, YOffset + 4)
		ConsoleTools.WriteErrorFromPosition(Text.FormatArray(unsuccessfulGuesses), XOffset + 5, YOffset + 5)

		# Write the guesses left
		ConsoleTools.WriteFromPosition("You have " + str(GetGuesses()) + " guesses left.", XOffset, YOffset + 7)
		
		# Set cursor position to correct spot for input, then get the letter.
		ConsoleTools.SetCursor(XOffset, YOffset + 8)
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

		# Get the score
		
	else:
		# Failed
		ConsoleTools.DialogError("You have failed to guess the word.")
		ConsoleTools.WriteErrorFromPosition(
			"The word was: " + word + ".",
			ConsoleTools.XOffset + ConsoleTools.DialogOffsetX,
			ConsoleTools.YOffset + ConsoleTools.DialogOffsetY + 1
		)
	time.sleep(5.0)
	Menu()

def ExitProgram():
	ConsoleTools.Clear()
	exit(1)

def Menu():
	def PrintTitleScreen():
		# Title
		ConsoleTools.Clear()
		ConsoleTools.WriteFromPosition(Text.Title, 5, 1)

		# Version
		versionStr = "Version: " + Version
		ConsoleTools.WriteFromPosition(versionStr, 12, 10)

	# Menu
	selected = None

	selection = 0
	MaxOption = 1

	while selected == None:
		# Title
		PrintTitleScreen()

		# Play button
		playString = "Play Hangman"
		ConsoleTools.WriteFromPosition("> " + playString + " <" if selection == 0 else "  " + playString, 35, YOffset + 8)
		
		# Exit button
		exitString = "Exit Program"
		ConsoleTools.WriteFromPosition("> " + exitString + " <" if selection == 1 else "  " + exitString, 35, YOffset + 10)
		
		# Read input and move cursor, or set & execute the pointer
		ConsoleTools.SetCursor(0, 0)
		key = ConsoleTools.GetInput()
		if key.upper() == "W":
			if selection > 0:
				selection -= 1
		elif key.upper() == "S":
			if selection < MaxOption:
				selection += 1
		elif key == chr(13):
			# Set selection to the method when enter is pressed
			if selection == 0: selected = Game
			if selection == 1: selected = ExitProgram
	
	# Run the selected method through its pointer
	selected()

def Hangman():
	Menu()

if __name__ == "__main__": Hangman()
