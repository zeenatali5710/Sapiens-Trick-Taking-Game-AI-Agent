import random

class Player(object):

	def __init__(self):
		self.sAgentName = "Sapiens"
		self.hand       = []
		self.cards      = []
		self.players    = []
		self.pastTricks = []
		self.scoreMap   = { }	# dictionary to maintain mapping of player name and his/her score 

	def get_name(self):
		"""
		Returns a string of the agent's name
		"""
		return self.sAgentName

	def get_hand(self):
		"""
		Returns a list of two character strings reprsenting cards in the agent's hand
		"""
		return self.hand

	def new_hand(self, names):
		"""
		Takes a list of names of all agents in the game in clockwise playing order
		and returns nothing. This method is also responsible for clearing any data
		necessary for your agent to start a new round.
		"""
		self.players = names
		self.scoreMap = { key: 0 for key in self.players } 

	def add_cards_to_hand(self, cards):
		"""
		Takes a list of two character strings representing cards as an argument
		and returns nothing.
		This list can be any length.
		"""
		self.hand = cards

	def play_card(self, lead, trick):
		"""
		Takes a a string of the name of the player who lead the trick and
		a list of cards in the trick so far as arguments.

		Returns a two character string from the agents hand of the card to be played
		into the trick.
		"""
		suit = ""
		playCard = random.choice(self.hand)
		if (len(trick) > 0):
			suit = trick[0][0]
			res = [card for card in self.hand if card[0].lower() == suit.lower()]
			if (len(res) == 0):
				playCard = random.choice(self.hand)
			else:
				playCard = random.choice(res)
		else:
			ace = [card for card in self.hand if card[1] == 'A']
			if (len(ace) == 0):
				playCard = random.choice(self.hand)
			else:
				playCard = random.choice(ace)

		return playCard
		

	def collect_trick(self, lead, winner, trick):
		"""
		Takes three arguements. Lead is the name of the player who led the trick.
		Winner is the name of the player who won the trick. And trick is a four card
		list of the trick that was played. Should return nothing.
		"""
		trickHistoryData = (lead, winner, trick)
		self.pastTricks.append(trickHistoryData)
		self.scoreMap[winner] += 1

	def score(self):
		"""
		Calculates and returns the score for the game being played.
		"""
		return self.scoreMap[self.sAgentName]


def main():
	p = Player();
	print(p.get_name())
	p.new_hand(["player1", "player2", "player3", p.get_name()])
	p.add_cards_to_hand(["C9", "C8", "DQ", "H10", "HJ", "HK", "C5", "D5", "H5", "D2", "H9", "C10", "CQ"])
	#print(p.play_card("player1", ['SQ', 'C2', 'DA']))
	print(p.play_card("player1", ["HA"]))
	#p.play_card("player1", ['SA', "C6", "SQ"])

if __name__ == '__main__':
	main()