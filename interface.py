# coding=UTF-8
from os import system
import curses
import locale
import json
import sys

locale.setlocale(locale.LC_ALL,"")

def interface(dictionary):
	x = 0
	lastAwardPress = 0

	hosts = ["Tina Fey", "Amy Poehler"]
	awards = [x for x in dictionary.keys() if x not in ["hosts"]]
	screen = curses.initscr()

	curses.noecho()

	screen.clear()
	screen.border(0)
	screen.addstr(2, 2, "Please enter a number...")
	screen.addstr(4, 4, "1 - Hosts")
	screen.addstr(5, 4, "2 - Awards, Page 1")
	screen.addstr(6, 4, "3 - Awards, Page 2")
	screen.addstr(7, 4, "4 - Exit")
	screen.refresh()

	while x != ord('4'):
		if x not in ["hosts", "awards1", "awards2"]:
			x = screen.getch()

		if x == ord('1') or x == "hosts":
			screen.clear()
			screen.border(0)
			for y in range(0, len(hosts)):
				screen.addstr(y + 1, 2, hosts[y])
			screen.addstr(22, 2, "2 - Awards, Page 1    3 - Awards, Page 2    4 - Exit")
			screen.refresh()
			x = 0
		if x == ord('2') or x == "awards1":
			screen.clear()
			screen.border(0)
			for z in range(0, 14):
				screen.addstr(z + 1, 2, str(chr(ord('a') + z)) + " - " + awards[z])
			screen.addstr(22, 2, "1 - Hosts    3 - Awards, Page 2    4 - Exit")
			screen.refresh()
			lastAwardPress = 2
		if x == ord('3') or x == "awards2":
			screen.clear()
			screen.border(0)
			for z in range(14, len(awards)):
				screen.addstr(z - 13, 2, str(chr(ord('a') + z)) + " - " + awards[z])
			screen.addstr(22, 2, "1 - Hosts    2 - Awards, Page 1    4 - Exit")
			screen.refresh()
			lastAwardPress = 3
		if x == ord('2') or x == ord('3') or x == "awards1" or x == "awards2":
			x = screen.getch()
			if x == ord('1'):
				x = "hosts"
			if x == ord('2'):
				x = "awards1"
			if x == ord('3'):
				x = "awards2"
			if (lastAwardPress == 2 and x >= ord('a') and x <= ord('n')) or (lastAwardPress == 3 and x >= ord('o') and x <= ord('y')):
				screen.clear()
				screen.border(0)
				screen.addstr(1, 2, "Winner:")
				if dictionary[awards[x-ord('a')]]["Winner"] == None:
					screen.addstr(2, 5, "None")
				else:
					screen.addstr(2, 5, dictionary[awards[x-ord('a')]]["Winner"])
				screen.addstr(4, 2, "Presenter(s):")
				for y in range(0, len(dictionary[awards[x-ord('a')]]["Presenters"])):
					screen.addstr(y + 5, 5, dictionary[awards[x-ord('a')]]["Presenters"][y])
				screen.addstr(8, 2, "Nominees:")
				for z in range(0, len(dictionary[awards[x-ord('a')]]["Nominees"])):
					screen.addstr(z + 9, 5, dictionary[awards[x-ord('a')]]["Nominees"][z])
				screen.addstr(15, 2, "Sentiment:")
				screen.addstr(16, 5, "Positive:Negative -- " + str(dictionary[awards[x-ord('a')]]["Sentiment"]["Positivity score"]))
				screen.addstr(17, 5, "Dominant Emotion: " + str(dictionary[awards[x-ord('a')]]["Sentiment"]["Dominant emotion"]["Name"]))
				arr = []
				for w in range(0, min(len(dictionary[awards[x-ord('a')]]["Sentiment"]["Dominant emotion"]["Emojis"]), 5)):
					arr.append(dictionary[awards[x-ord('a')]]["Sentiment"]["Dominant emotion"]["Emojis"][w])
				screen.addstr(18, 5, "Most Popular Emojis: " + " ".join(arr).encode("utf-8"))
				screen.addstr(22, 2, "1 - Hosts   2 - Awards, Page 1   3 - Awards, Page 2   4 - Exit")
				screen.refresh()




	curses.endwin()

def main():
	jsonfile = sys.argv[1]
	with open(jsonfile) as f:
		interface(json.loads(f.read()))

if __name__ == "__main__":
	main()
