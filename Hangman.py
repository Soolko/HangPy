Version = "Submission 2"

import sys
import time
import random

import Text
import Files
import ConsoleTools
from ConsoleTools import XOffset
from ConsoleTools import YOffset

Dictionary = []
Scoreboard = []

def Game():
	global Dictionary
	Dictionary = Files.LoadDictionary(Files.DictionaryPath)
	word = random.choice(Dictionary)
	word = word.upper()

	global Scoreboard
	Scoreboard = Files.LoadScoreboard(Files.ScoreboardPath)
	
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
		if len(unsuccessfulGuesses) > 0:
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
		time.sleep(0.25)
		score = GetGuesses() * Text.UniqueLetters(word)
		ConsoleTools.WriteFromPosition(
			"Your score was: " + str(score),
			ConsoleTools.XOffset + ConsoleTools.DialogOffsetX + 2,
			ConsoleTools.YOffset + ConsoleTools.DialogOffsetY + 3
		)

		# Allow player to enter name
		ConsoleTools.SetCursor(
			ConsoleTools.XOffset + ConsoleTools.DialogOffsetX + 2,
			ConsoleTools.YOffset + ConsoleTools.DialogOffsetY + 5
		)
		name = input("Enter your name if you want to add it to the scoreboard: ")
		if len(name) > 0:
			Scoreboard.append((name, score))
			Files.SaveScoreboard(Files.ScoreboardPath, Scoreboard)
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

def DisplayScoreboard():
	ConsoleTools.Clear()

	# Scoreboard
	scoreboardTitle = "Scoreboard"
	ConsoleTools.WriteFromPosition(scoreboardTitle + "\n" + ("=" * len(scoreboardTitle)), 25, 1)

	# Construct table header (Messy, I know)
	ConsoleTools.WriteFromPosition("|", 5, 4)
	ConsoleTools.WriteFromPosition("Name", 16, 4)
	ConsoleTools.WriteFromPosition("|", 30, 4)
	ConsoleTools.WriteFromPosition("Score", 41, 4)
	ConsoleTools.WriteFromPosition("|", 55, 4)

	ConsoleTools.WriteFromPosition("-" * 51, 5, 5)

	# Generate table
	position = 6
	for entry in Scoreboard:
		# Name
		ConsoleTools.WriteFromPosition("|", 5, position)
		ConsoleTools.WriteFromPosition(entry[0], 18 - (len(entry[0]) // 2), position)
		
		ConsoleTools.WriteFromPosition("|", 30, position)

		# Score
		ConsoleTools.WriteFromPosition(str(entry[1]), 43 - (len(str(entry[1])) // 2), position)
		ConsoleTools.WriteFromPosition("|", 55, position)

		# Increment position
		position += 1
	
	# Reset cursor
	ConsoleTools.SetCursor(0, 0)

	# Wait for keypress
	ConsoleTools.GetInput()

	# Return to menu
	Menu()

def ExitProgram():
	# Save & Exit
	Files.SaveScoreboard(Files.ScoreboardPath, Scoreboard)
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
	MaxOption = 2

	while selected == None:
		# Title
		PrintTitleScreen()

		# Play button
		playString = "Play Hangman"
		ConsoleTools.WriteFromPosition("> " + playString + " <" if selection == 0 else "  " + playString, 28, YOffset + 8)
		
		# Scoreboard button
		scoreboardString = "Scoreboard"
		ConsoleTools.WriteFromPosition(">  " + scoreboardString + "  <" if selection == 1 else "   " + scoreboardString, 28, YOffset + 9)

		# Exit button
		exitString = "Exit Program"
		ConsoleTools.WriteFromPosition("> " + exitString + " <" if selection == 2 else "  " + exitString, 28, YOffset + 10)
		
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
			if selection == 1: selected = DisplayScoreboard
			if selection == 2: selected = ExitProgram
	
	# Run the selected method through its pointer
	selected()

# Manual Launch
def Hangman():
	Menu()

# Auto Launch
if __name__ == "__main__": Hangman()
