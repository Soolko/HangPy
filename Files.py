DictionaryPath = "./Dictionary.txt"
ScoreboardPath = "./Scoreboard.csv"

def LoadFile(path: str) -> str:
	# Load file
	file = open(path)

	# Load into single string.
	contents = ""
	for line in file: contents += line + "\n"

	file.close()
	return contents

def SaveFile(path: str, data: str):
	file = open(path, "w")
	file.write(data)
	file.close()

def LoadDictionary(path: str) -> list:
	# Load the dictionary file
	contents = None
	try:
		contents = LoadFile(path)
	except FileNotFoundError:
		print("Could not load dictionary \"" + path + "\" as the file doesn't exist.")
		exit(0)
	assert contents != None
	
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

def LoadScoreboard(path: str) -> list:
	# Load in base file
	contents = None
	try:
		contents = LoadFile(path)
	except FileNotFoundError:
		print("Scoreboard file not found.\nCreating new one at \"" + path + "\".")
		SaveScoreboard(path, [])
		return []
	# Sanity check
	assert contents != None

	lines = contents.split("\n")

	# Base error if needed
	BaseErr = "Error in scoreboard \"" + path + "\".\n"

	# Declare scoreboard array ready
	scoreboard = []

	# Iterate through CSV
	for line in lines:
		split = line.split(",")

		# Parts to the tuple
		name = None
		score = None

		if len(split) == 0: continue
		elif len(split) == 2:
			# Set the tuple values if possible
			name = split[0]
			try:
				score = int(split[1])
			except ValueError:
				print(BaseErr + "Score \"" + split[1] + "\" is not a valid integer.")
				continue
		else:
			print(BaseErr + "Line \"" + line + "\" must have 2 columns.")
			continue
		# Actually append this tuple
		scoreboard.append((name, score))
	return scoreboard

def SaveScoreboard(path: str, scoreboard: list):
	output = ""
	for entry in scoreboard:
		output += entry[0] + "," + str(entry[1]) + "\n"
	SaveFile(path, output)