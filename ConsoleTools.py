import sys

def Clear():
	# Escape sequence to clear the console window.
	sys.stdout.write(chr(27) + "[2J")

# Position starts at 1.
# Don't forget.
def SetCursor(x: int, y: int):
	# Escape sequence to set the cursor position in the console window.
	sys.stdout.write("\033[" + str(y) + ";" + str(x) + "H")

# Position starts at 1.
# Don't forget.
def WriteFromPosition(input: str, x: int, y: int):
	split = str.split(input, "\n")
	for line in split:
		SetCursor(x, y)
		sys.stdout.write(line)
		y += 1

if __name__ == "__main__":
	import time
	
	# Clear Test
	print("Test")
	
	time.sleep(1.0)
	
	Clear()
	
	time.sleep(0.25)
	
	print("If this is all you see, then the clear test was successful.")
	
	time.sleep(1.0)

	# Position test
	Clear()
	sys.stdout.write("Default position is here.")
	for i in range(1, 5):
		SetCursor(i, i)
		iStr = str(i)
		sys.stdout.write("This is position " + iStr + ", " + iStr + ".")
		time.sleep(0.5)
	sys.stdout.write("\nBack to where it should be.\n")
	
	time.sleep(1.0)

	# Write from position test
	Clear()
	print("Writing multi-line string.")

	time.sleep(0.5)
	
	Clear()
	WriteFromPosition("AAAAAAAAAAAAAAAAAAA\nBBBB\nC\nDDDDD", 25, 4)
	
	time.sleep(0.5)
	
	print("\nBack to normal.")
	
	time.sleep(1.0)
