import random
from gym import spaces
import numpy as np
import random
import pydealer
import json
import os
from itertools import groupby
from itertools import product
from pydealer import ( Card, Deck, Stack)

'''
Reference: https://github.com/nihalsoans91/Multi-Agent-Alternating-Turn-Board-and-Card-Games

Approach description:
Using the Q-learning algorithm, which uses the Bellman equation to choose the best card 
while playing the game of Spades.

For our agent, we define the following
environment: cards on the table i.e the current trick
state      : list of cards in hand
action_list: list of legal cards which can be played
action     : card played by the agent from action list

An 'action' causes a change in the agent 'environment' and 'state'.
When a card is played, it is removed from the current hand and hence state changes.

This is a model-free approach of reinforcement learning where agent updates its 
q-values and selects the best card which would make him win the trick.

We are using the sorting API provided by the pydealer module, cards are sorted according 
to the rank of their suit and card-value.

Q-dictionary:
key   : hand | action
value : qValue calculated using the Bellman equation

Q-Policy:
key   : trick | hand
value : action which is the card to be played

Parameters for Bellman equation:

1. reward : calculated based on action
   for each action in action list, 
    if that action causes agent to win the trick, then reward = 50
    else reward = -10

2. learning rate(alpha): 0.01

3. gamma               : 0.8

4. next Q-value for Bellman equation is taken from the Q-dictionary.


Policy:
The card having maximum q-Value is selected

'''

class Player(object):
    
    def __init__(self):
        self.sAgentName = "Sapiens"
        self.hand       = []
        self.players    = []
        self.pastTricks = []   # list of tuples 
        self.scoreMap   = { }  # dictionary to maintain mapping of player name and his/her score 
        self.deck       = pydealer.deck.Deck()
        self.stack      = pydealer.stack.Stack()
        self.reward     = 0
        self.q_value    = 0
        self.q_dict     = { }
        self.q_policy   = { }
        
        self.alpha      = 0.01
        self.gamma      = 0.9
        # self.epsilon    = 1.0
        # self.decay_rate = 0.001
        # self.EPISODES   = 1500000
        
        self.qfilename = 'dictionary/qVal.txt'
        if os.path.isfile(self.qfilename):
            self.q_dict = json.load(open(self.qfilename,'r'))
        else:
            self.q_dict = {}
            json.dump(self.q_dict, open(self.qfilename, 'w'))
        
        self.pfilename = 'dictionary/qPolicy.txt'
        if os.path.isfile(self.pfilename):
            self.q_policy = json.load(open(self.pfilename,'r'))
        else:
            self.q_policy = {}
            json.dump(self.q_policy, open(self.pfilename, 'w'))
        
        
        self.suit       = {
                            'D' : "Diamonds",
                            'H' : "Hearts",
                            'C' : "Clubs",
                            'S' : "Spades"
                        }
        self.rank       = {
                            'J' : "Jack",
                            'Q' : "Queen",
                            'K' : "King",
                            'A' : "Ace",
                            '2' : "2",
                            '3' : "3",
                            '4' : "4",
                            '5' : "5",
                            '6' : "6",
                            '7' : "7",
                            '8' : "8",
                            '9' : "9",
                            '1' : "10"
                        }
        
    def sortCards(self, cardsToSort):        
        terms = []
        for card in cardsToSort:
            c = self.rank[card[1]] + " of " + self.suit[card[0]]
            terms.append(c)
        cards = self.deck.get_list(terms)
        self.stack.insert_list(cards)
        pydealer.tools.sort_cards(cards)
        self.stack.sort()
        hand = []
        for card in self.stack:
            hand.append(list(self.suit.keys())[list(self.suit.values()).index(card.suit)]
            + list(self.rank.keys())[list(self.rank.values()).index(card.value)])
        cardsToSort = []
        cardsToSort = hand.copy()
        # print(cardsToSort)
        # print(hand)
            
    def get_name(self):
        return self.sAgentName

    def get_hand(self):
        return self.hand

    def new_hand(self, names):
        self.players = names
        self.scoreMap = { key: 0 for key in self.players }

    def add_cards_to_hand(self, cards):
        self.hand = cards
        self.sortCards(self.hand)
        
    def get_valid_actions(self, trick):
        valid_Actions = []
        suit     = ""
        if (len(trick) > 0):
            suit = trick[0][0]
            res = [card for card in self.hand if card[0].lower() == suit.lower()]
            if (len(res) == 0):
                valid_Actions = self.hand
            else:
                valid_Actions = res
        else:
            valid_Actions = self.hand
        return valid_Actions
    
    def serialize_state(self):
        state = ""
        allTricks = []
        for trick in self.pastTricks:
            sTrick = '-'.join(map(str, trick[2]))
            allTricks.append(sTrick)
        state = '|'.join(map(str, allTricks))
        return state
    
    def is_winner(self, trick, action):
        if action not in trick:
            trick.append(action)
        self.sortCards(trick)       
        if (trick[len(trick)-1] == action):
            return True
        else:
            return False
        
    def get_reward(self, trick, action):
        reward = 0
        if self.is_winner(trick, action):
            reward = 50
        else:
            reward = -10
        return reward
    
    def nextQvalue(self, hand, action):
        # print("action: ", action)
        # print("hand: ", hand)
        new_hand = hand.copy()
        new_hand.remove(action)
        key = '-'.join(hand) + "|" + action
        if key in self.q_dict.keys():
            q_value = self.q_dict[key]
        else:
            self.q_dict[key]  = 0
            q_value = 0
        return q_value

    def updatePolicy(self, trick):
        for key in self.q_dict.keys():
            k = key.split('|')
            #print("key: ", k)
            e = ('-').join(trick)
            h = k[0]
            a = k[1]
            hand  = h.split('-')
            Qs = {}
            for card in hand:
                k1 = h + '|' + card
                if k1 in self.q_dict.keys():
                    Qs[card] = self.q_dict[k1]
                else:
                    Qs[card] = 0
            c = list(Qs.keys())[list(Qs.values()).index(max(Qs.values()))]
            self.q_policy[e + "|" + h] = str(c)
    
            
    def play_card(self, lead, trick):
        actions  = self.get_valid_actions(trick)
        state    = self.hand
        env      = trick
                    
        for action in actions:
            key = '-'.join(self.hand) + "|" + action
            if key in self.q_dict.keys():
                self.q_value = self.q_dict[key]
            else:
                self.q_dict[key]  = 0
                self.q_value = 0

            reward = self.get_reward(trick,action) 
            self.q_value = self.q_value  + self.alpha*(reward + self.gamma * max(self.nextQvalue(self.hand,a) for a in actions) - self.q_value)
            #print("Qvalue: ", self.q_value)
            self.q_dict[key] = self.q_value

        #print("q_dict: ", self.q_dict)
        print()

        self.updatePolicy(trick)
        
        playCard = self.q_policy['-'.join(trick) + "|" + '-'.join(self.hand)]
        print("played card is: ", playCard)
        self.hand.remove(playCard)
        json.dump(self.q_dict, open(self.qfilename, 'w'))
        json.dump(self.q_policy, open(self.pfilename, 'w'))
        return playCard

    def collect_trick(self, lead, winner, trick):
        trickHistoryData = (lead, winner, trick)
        self.pastTricks.append(trickHistoryData)
        self.scoreMap[winner] += 1

    def score(self):
        return self.scoreMap[self.sAgentName]


def main():
    p = Player();
    p.new_hand(["player1", "player2", "player3", p.get_name()])
    p.add_cards_to_hand(["DJ", "DQ", "DK", "DA", "HJ", "HK", "HQ", "HA", "CJ", "SK", "SQ", "CA", "SA"])

    hand2 = p.get_hand().copy()
    #print(p.get_hand())
    #print(p.play_card("player1", ['SQ', 'C2', 'DA']))

    card = p.play_card("player1", ["H4"])
    l = ["H4", card, "H2", "H3"]
    p.collect_trick("player1", "player1", l)
    
    # print(p.deck)
    # print(p.deck.get_list(["Queen of Hearts"]))
    # print(p.deck[25])
    
    card = p.play_card("player3", ["H7", "C2", "D4"])
    l = ["D9", "C2", "D4", card]
    p.collect_trick("player3", "player1", l)
    
    print(p.play_card("player4", ["CQ", "C2"]))
    l = ["CQ", "C2", card, "C3"]
    p.collect_trick("player4", "Sapiens",  l)

    print("initial hand is: ", hand2)
    print("current hand is: ", p.get_hand())

if __name__ == '__main__':
    main()
