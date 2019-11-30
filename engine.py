import random
import more_itertools as mit
import operator

# Build a Deck
suits = "CDHS"
ranks = list(range(2, 11)) + list("JQKA")
for i in range(0, len(ranks)):
    ranks[i] = str(ranks[i])
DeckCard = [j + i for j in suits for i in ranks]

# Shuffle and Distribute
players = 4
random.shuffle(DeckCard)
hands = [list(hand) for hand in list(mit.distribute(players, DeckCard))]
#return all 4 hands to each player
print("player1:", hands[0])
print("player2:", hands[1])
print("player3:", hands[2])
print("AgentHand:", hands[3])

playcard1 = 'SA'
playcard2 = 'SK'
playcard3 = 'SQ'
playcard4 = 'S10'
trick = [playcard1, playcard2, playcard3, playcard4]
print(len(trick))
if len(trick) == 4:
    leadSuit = trick[0][1]
    print(leadSuit)
    cards_value = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14 }
    # CardValue =  [(map(lambda x: cards_value[x[1]], hand)) for hand in trick]
    print(trick)
    stats = {'a': 1000, 'b': 3000, 'c': 100}
    print(max(cards_value.items(), key=operator.itemgetter(1))[0])


Trick = []
