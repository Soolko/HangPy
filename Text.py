"""
	=======================
	  Hangman Art library
	=======================

	Prints off the hangman stages,
	or returns the strings to print off at least.

	=============
	  Full Set:
	=============
	/---\
	|/  |
	|   O
	|  /|\
	|  / \
	\------
"""

import sys
import ConsoleTools

#region Stage Definitions
Lines = 6
def Stage1() -> str: return ("\n" * (Lines - 1)) + "\\------\n"
def Stage2() -> str:
	return str(
		"       \n" +
		"|      \n" +
		"|      \n" +
		"|      \n" +
		"|      \n" +
		"\\------\n"
	)
def Stage3() -> str:
	return str(
		"/---\\  \n" +
		"|      \n" +
		"|      \n" +
		"|      \n" +
		"|      \n" +
		"\\------\n"
	)
def Stage4() -> str:
	return str(
		"/---\\  \n" +
		"|/     \n" +
		"|      \n" +
		"|      \n" +
		"|      \n" +
		"\\------\n"
	)
def Stage5() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|      \n" +
		"|      \n" +
		"|      \n" +
		"\\------\n"
	)
def Stage6() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|   O  \n" +
		"|      \n" +
		"|      \n" +
		"\\------\n"
	)
def Stage7() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|   O  \n" +
		"|   |  \n" +
		"|      \n" +
		"\\------\n"
	)
def Stage8() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|   O  \n" +
		"|   |  \n" +
		"|  /   \n" +
		"\\------\n"
	)
def Stage9() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|   O  \n" +
		"|   |  \n" +
		"|  / \\ \n" +
		"\\------\n"
	)
def Stage10() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|  \\O  \n" +
		"|   |  \n" +
		"|  / \\ \n" +
		"\\------\n"
	)
def Stage11() -> str:
	return str(
		"/---\\  \n" +
		"|/  |  \n" +
		"|  \\O/ \n" +
		"|   |  \n" +
		"|  / \\ \n" +
		"\\------\n"
	)
#endregion

ArtStages = [
	"\n" * Lines,
	Stage1(),
	Stage2(),
	Stage3(),
	Stage4(),
	Stage5(),
	Stage6(),
	Stage7(),
	Stage8(),
	Stage9(),
	Stage10(),
	Stage11()
]

def TestArt():
	for i in range(0, len(ArtStages)):
		output = "Stage " + str(i)
		sys.stdout.write("\n" + output + "\n")
		sys.stdout.write(("=" * len(output)) + "\n")
		sys.stdout.write(ArtStages[i] + "\n")

if __name__ == "__main__":
	sys.stdout.write(chr(27) + "[2J")
	TestArt()

def GetPrintableWord(word: str, guesses: list) -> str:
	output = ""
	for character in word: output += character if character in guesses else "-"
	return output

def FormatArray(input: list) -> str:
	output = ""
	first = True
	for element in input:
		if not first:
			output += ", "
		output += str(element)
		first = False
	return output
