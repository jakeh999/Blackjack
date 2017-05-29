from random import shuffle
# import os
import player


class Blackjack:

	# Game Vars
	__fresh_deck = []
	__deck = []
	__players = []
	# Round vars
	__pot = {}
	__hands = {}
	__totals = {}

	def __init__(self, starting_score):
		for i in range(1, 14):
			if i == 1:
				card = "A"
			elif i == 11:
				card = "J"
			elif i == 12:
				card = "Q"
			elif i == 13:
				card = "K"
			else:
				card = i
			self.__fresh_deck.append(tuple([card, "♠"]))
			self.__fresh_deck.append(tuple([card, "♣"]))
			self.__fresh_deck.append(tuple([card, "♥"]))
			self.__fresh_deck.append(tuple([card, "♦"]))
		self.shuffle_deck()
		self.add_player("Dealer", starting_score, True)

	def remove_player(self, i):
		del self.__players[i]

	def remove_hand(self, i):
		del self.__hands[i]

	def get_players(self):
		return self.__players

	def get_player(self, i):
		return self.__players[i]

	def shuffle_deck(self):
		self.__deck = list(self.__fresh_deck)
		shuffle(self.__deck)

	def get_deck(self):
		return self.__deck

	def add_player(self, name, starting_score, is_robot=False):
		self.__players.append(player.Player(name, starting_score, is_robot))

	def deal(self, bet):
		# print("Deck length before: " + str(len(self.__deck)))
		if len(self.__deck) < 21:
			# print("Shuffling deck...")
			self.shuffle_deck()
		# print("Deck length after: " + str(len(self.__deck)))
		# os.system("pause")
		for p in self.__players:
			if (p.get_score() - bet) < 0:
				raise ValueError("Not enough chips!")
		for p in self.__players:
			p.change_score(-bet)
			self.__pot[self.__players.index(p)] = bet
			self.__hands[self.__players.index(p)] = [self.__deck.pop(), self.__deck.pop()]

	def get_hands(self, get_all=False):
		helper = {}
		for key, value in self.__hands.items():
			if self.__players[key].is_robot():
				if get_all:
					helper[key] = value
				else:
					helper[key] = value[1:]
			else:
				helper[key] = value
		return helper

	def get_hand(self, i):
		return self.__hands[i]

	def get_score(self, h):
		score = [0]
		for card in self.__hands[h]:
			if card[0] in ("J", "Q", "K"):
				score[0] += 10
				if len(score) == 2:
					score[1] += 10
					if score[1] > 21:
						del score[1]
			elif card[0] == "A":
				if len(score) == 1:
					if (score[0] + 11) <= 21:
						score.append(score[0]+11)
				else:
					if (score[1] + 11) <= 21:
						score[1] += 11
					elif (score[1] + 1) <= 21:
						score[1] += 1
					else:
						del score[1]
				score[0] += 1
			else:
				score[0] += card[0]
				if len(score) == 2:
					score[1] += card[0]
					if score[1] > 21:
						del score[1]
		return score

	def hit(self, h):
		if len(self.__deck) == 0:
			self.shuffle_deck()
		self.__hands[h].append(self.__deck.pop())
		if self.get_score(h)[0] > 21:
			return True
		else:
			return False

	def robo(self, h):
		while True:
			score = self.get_score(h)
			# print(self.__players[h].get_name())
			# print(score)
			if len(score) == 2:
				if score[1] <= 16:
					self.hit(h)
				else:
					break
			elif score[0] <= 16:
				self.hit(h)
			else:
				break
		if self.get_score(h)[0] > 21:
			return True
		else:
			return False

	def double_down(self, idx):
		if ((self.__players[idx].get_score() - (self.__pot[idx])) < 0) or ((self.__players[0].get_score() - (self.__pot[idx])) < 0):
			raise ValueError("Not enough chips!")
		self.__players[idx].change_score(-(self.__pot[idx]*2))
		self.__players[0].change_score(-(self.__pot[idx] * 2))
		self.__pot[0] += self.__pot[idx]
		self.__pot[idx] *= 2

	def check_winner(self):
		winner = [[0], 0]
		for idx in self.__hands.keys():
			score = self.get_score(idx)
			if (len(score) == 2) and (score[1] <= 21):
				if score[1] == winner[1]:
					winner[0].append(idx)
				elif winner[1] < score[1]:
					winner[1] = score[1]
					winner[0] = [idx]
			elif score[0] <= 21:
				if score[0] == winner[1]:
					winner[0].append(idx)
				elif winner[1] < score[0]:
					winner[1] = score[0]
					winner[0] = [idx]
		total = 0
		for chips in self.__pot.values():
			total += chips
		if len(winner[0]) > 1:
			total = total/len(winner[0])
			for w in winner[0]:
				self.__players[w].change_score(round(total, 2))
		else:
			self.__players[winner[0][0]].change_score(round(total, 2))
		self.__pot = {}
		return {'winner': winner[0], 'score': winner[1], 'total': round(total, 2)}



