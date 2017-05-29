# -*- coding: utf-8 -*-
import blackjack
import sys
import os
import platform


def write(s):
	sys.stdout.write(s)
	sys.stdout.flush()


def clear():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

print('''
♠♣BLACKJACK♥♦ v. 1.0
By Jake Henderson
''')
while True:
	try:
		score = int(input("Enter starting score for players: "))
		game = blackjack.Blackjack(score)
		break
	except ValueError as e:
		print("Please enter a valid number.")

while True:
	player_name = input("Enter player name: ")
	if not player_name:
		if len(game.get_players()) == 1:
			print("Please enter at least one player.")
		else:
			break
	else:
		if player_name[-3:] == " -r":
			game.add_player(player_name[:-3], score, True)
		else:
			game.add_player(player_name, score)
		if len(game.get_players()) == 10:
			break

while True:
	try:
		bet = float(input("Enter bet: "))
		game.deal(bet)
		clear()
		for p in game.get_players():
			while True:
				if not p.is_robot():
					write("\n")
					for key, value in game.get_hands().items():
						write(game.get_player(key).get_name() + ": ")
						for card in value:
							write(str(card[0]) + card[1] + " ")
						write("\n")
					write("\nYour score: ")
					idx = game.get_players().index(p)
					score = game.get_score(idx)
					if len(score) == 1:
						write(str(score[0]) + "\n\n")
					else:
						write(str(score[0]) + " or " + str(score[1]) + "\n\n")
					while True:
						cmd = input(game.get_player(idx).get_name() + ", what do you want to do?: ")
						if not cmd:
							print("Please enter a command:")
						else:
							break
					if (cmd == "h") or (cmd == "d"):
						clear()
						if cmd == "d":
							try:
								game.double_down(idx)
							except ValueError as e:
								print("Error! " + str(e))
						if game.hit(idx):
							print(game.get_player(idx).get_name() + " busted! :(")
							for card in game.get_hand(idx):
								write(str(card[0]) + card[1] + " ")
							write("= " + str(game.get_score(idx)[0]) + "\n")
							print("------------")
							game.remove_hand(idx)
							break
						if cmd == "d":
							break
					elif cmd == "s":
						clear()
						break
					else:
						print("Please enter a valid command.")
				else:
					break
		if len(game.get_hands()) > 1:
			for p in game.get_players():
				if p.is_robot():
					idx = game.get_players().index(p)
					if game.robo(idx):
						print(game.get_player(idx).get_name() + " busted!")
						for card in game.get_hand(idx):
							write(str(card[0]) + card[1] + " ")
						write("= " + str(game.get_score(idx)[0]) + "\n")
						write("------------\n\n")
						game.remove_hand(idx)
		for key, value in game.get_hands(True).items():
			write(game.get_player(key).get_name() + ": ")
			for card in value:
				write(str(card[0]) + card[1] + " ")
			score = game.get_score(key)
			if len(score) == 2:
				write("= " + str(score[1]) + "\n")
			else:
				write("= " + str(score[0]) + "\n")
		winner = game.check_winner()
		if len(winner['winner']) > 1:
			print("\nTie!")
		else:
			print("\n" + game.get_player(winner['winner'][0]).get_name() + " had a score of " + str(winner['score']) + " and won " + str(winner['total']) + " chips!")
		print("\nCurrent score")
		print("-------------")
		for p in game.get_players():
			score = p.get_score()
			print(p.get_name() + ": " + str(round(score, 2)))
			if score < 1:
				print(p.get_name() + " is out of the game!")
				game.remove_player(game.get_players().index(p))
		write("\n")
		if len(game.get_players()) == 1:
			print("GAME OVER!")
			print(game.get_player(0).get_name() + " wins the game with " + str(game.get_player(0).get_score()) + " chips!")
			break
	except ValueError as e:
		print("Error! " + str(e))
