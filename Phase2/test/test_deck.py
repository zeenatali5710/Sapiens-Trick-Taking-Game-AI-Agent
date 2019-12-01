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
