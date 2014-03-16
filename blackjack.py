from random import shuffle

default_deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
        6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
deck = []
hands = []
dealer = []

LOWER_LIMIT = 5
UPPER_LIMIT = 300
PROFIT = 5
INITIAL_CASH = 10000

def main():
    results = 0
    for i in range(1000):
        if i % 100 == 0:
            print i
        hands = 0
        wins = 0
        pushes = 0
        losses = 0
        total_bet = 0
        cash = INITIAL_CASH
        bet = LOWER_LIMIT

        while hands < 100:
            initialize()
            res, bets = play_hand(bet) # should be two arrays of the same length
            starting_cash = cash
            for i in range(len(res)):
                if res[i] == "BLACKJACK":
                    cash += (bets[i] * 6) / 5 # most casinos do a 3:2 payout
                    wins += 1
                elif res[i] == "WIN":
                    cash += bets[i]
                    wins += 1
                elif res[i] == "PUSH":
                    pushes += 1
                elif res[i] == "LOSE":
                    cash -= bets[i]
                    losses += 1
                total_bet += bets[i]
            hands += len(res)

            if cash - starting_cash > 0:
                bet = LOWER_LIMIT
            elif bet + starting_cash - cash <= UPPER_LIMIT:
                bet += starting_cash - cash
            else:
                bet = UPPER_LIMIT

        #print hands
        #print wins
        #print losses
        #print pushes
        #print cash - INITIAL_CASH

        results += float(cash - INITIAL_CASH) / total_bet
    print float(results / 1000)

def initialize():
    # clear the deck and hands
    while len(deck) > 0:
        deck.pop()

    while len(hands) > 0:
        hands.pop()

    while len(dealer) > 0:
        dealer.pop()

    # turn a single deck of cards into eight decks
    for i in range(8):
        for card in default_deck:
            deck.append(card)
    
    # shuffle cards
    shuffle(deck)

def play_hand(bet):
    bets = [bet]
    hands.append([])

    # deal cards to dealer and player
    for hand in hands:
        hit(hand)
    hit(dealer)
    for hand in hands:
        hit(hand)
    hit(dealer)

    if bsum(dealer) == 21:
        # print hands
        # print dealer
        # print evaluate_hands(hands, dealer)
        return evaluate_hands(hands, dealer), bets
    
    # This is the meat of our program. We must dynamically update the number
    # of hands that the player keeps due to splitting.

    i = 0 # what hand are we currently on?
    while i < len(hands):
        strat = invoke_strategy(hands[i])
        if strat == "DOUBLE":
            bets[i] *= 2
        while eval_strat(strat):
            if strat == "DOUBLE":
                bets[i] *= 2
            elif strat == "SPLIT":
                old_bet = bets.pop(i)
                bets.insert(i, old_bet)
                bets.insert(i+1, old_bet)

            strat = invoke_strategy(hands[i])

        i += 1

    dealer_action(dealer)
    # print hands
    # print dealer
    # print evaluate_hands(hands, dealer)
    return evaluate_hands(hands, dealer), bets

# precondition: hand must be a two-element or larger array of integers 1 through
# 10
def invoke_strategy(hand):
    ############
    # Ax hands #
    ############
    if soft(hand) and len(hand) == 2:
        # AA
        if bsum(hand) == 12:
            split(hand)
            return "SPLIT"

        # A2
        elif bsum(hand) == 13:
            hit(hand)
            if 5 <= dealer[0] <= 6:
                return "DOUBLE"
            else:
                return "HIT"

        # A3
        elif bsum(hand) == 14:
            hit(hand)
            if 5 <= dealer[0] <= 6:
                return "DOUBLE"
            else:
                return "HIT"

        # A4
        elif bsum(hand) == 15:
            hit(hand)
            if 4 <= dealer[0] <= 6:
                return "DOUBLE"
            else:
                return "HIT"

        # A5
        elif bsum(hand) == 16:
            hit(hand)
            if 4 <= dealer[0] <= 6:
                return "DOUBLE"
            else:
                return "HIT"

        # A6
        elif bsum(hand) == 17:
            hit(hand)
            if 3 <= dealer[0] <= 6:
                return "DOUBLE"
            else:
                return "HIT"

        # A7
        elif bsum(hand) == 18:
            if 3 <= dealer[0] <= 6:
                hit(hand)
                return "DOUBLE"
            elif dealer[0] == 2 or 7 <= dealer[0] <= 8:
                return "STAND"
            else:
                hit(hand)
                return "HIT"

        # A8
        elif bsum(hand) == 19:
            return "STAND"

        # A9
        elif bsum(hand) == 20:
            return "STAND"

        # A10 - blackjack!
        elif bsum(hand) == 21:
            return "STAND"

        else:
            return "ERROR"

    ################################
    # splittable hands, besides AA #
    ################################
    elif splittable(hand):
        # 22
        if bsum(hand) == 4:
            if 2 <= dealer[0] <= 7:
                split(hand)
                return "SPLIT"
            else:
                hit(hand)
                return "HIT"

        # 33
        elif bsum(hand) == 6:
            if 2 <= dealer[0] <= 7:
                split(hand)
                return "SPLIT"
            else:
                hit(hand)
                return "HIT"

        # 44
        elif bsum(hand) == 8:
            if 5 <= dealer[0] <= 6:
                split(hand)
                return "SPLIT"
            else:
                hit(hand)
                return "HIT"

        # 55
        elif bsum(hand) == 10:
            hit(hand)
            if 2 <= dealer[0] <= 9:
                return "DOUBLE"
            else:
                return "HIT"

        # 66
        elif bsum(hand) == 12:
            if 2 <= dealer[0] <= 6:
                split(hand)
                return "SPLIT"
            else:
                hit(hand)
                return "HIT"

        # 77
        elif bsum(hand) == 14:
            if 2 <= dealer[0] <= 7:
                split(hand)
                return "SPLIT"
            else:
                hit(hand)
                return "HIT"

        # 88
        elif bsum(hand) == 16:
            split(hand)
            return "SPLIT"

        # 99
        elif bsum(hand) == 18:
            if 2 <= dealer[0] <= 6 or 8 <= dealer[0] <= 9:
                split(hand)
                return "SPLIT"
            else:
                return "STAND"

        # 1010
        elif bsum(hand) == 20:
            return "STAND"

        else:
            return "ERROR"

    ###################
    # all other hands #
    ###################
    # 5 through 8 -- 4 is only possible via the 22 split
    elif bsum(hand) <= 8:
        hit(hand)
        return "HIT"
    
    # 9
    elif bsum(hand) == 9:
        hit(hand)
        if len(hand) == 2 and 3 <= dealer[0] <= 6:
            return "DOUBLE"
        else:
            return "HIT"

    # 10
    elif bsum(hand) == 10:
        hit(hand)
        if len(hand) == 2 and 2 <= dealer[0] <= 9:
            return "DOUBLE"
        else:
            return "HIT"

    # 11
    elif bsum(hand) == 11:
        hit(hand)
        if len(hand) == 2 and 2 <= dealer[0] <= 10:
            return "DOUBLE"
        else:
            return "HIT"

    # 12
    elif bsum(hand) == 12:
        if 4 <= dealer[0] <= 6:
            return "STAND"
        else:
            hit(hand)
            return "HIT"

    # 13
    elif bsum(hand) == 13:
        if 2 <= dealer[0] <= 6:
            return "STAND"
        else:
            hit(hand)
            return "HIT"

    # 14
    elif bsum(hand) == 14:
        if 2 <= dealer[0] <= 6:
            return "STAND"
        else:
            hit(hand)
            return "HIT"

    # 15
    elif bsum(hand) == 15:
        if 2 <= dealer[0] <= 6:
            return "STAND"
        else:
            hit(hand)
            return "HIT"

    # 16
    elif bsum(hand) == 16:
        if 2 <= dealer[0] <= 6:
            return "STAND"
        else:
            hit(hand)
            return "HIT"

    # 17 and up
    else:
        return "STAND"

def dealer_action(hand):
    # dealer draws until he gets 17 or higher, excluding soft 17
    while bsum(hand) < 17 or (bsum(hand) <= 17 and soft(hand)):
        hit(hand)
    return hand

def evaluate_hands(hands, dealer):
    results = []
    for i in range(len(hands)):
        results.append("LOSE") # assume that all hands bust or lose by default

    for i in range(len(hands)):
        if bsum(hands[i]) > 21:
            results[i] = "LOSE"
        elif bsum(hands[i]) == 21 and len(hands[i]) == 2:
            if bsum(dealer) == 21 and len(dealer) == 2:
                results[i] = "PUSH"
            else:
                results[i] = "BLACKJACK"
        elif bsum(dealer) > 21:
            results[i] = "WIN"
        elif bsum(hands[i]) == bsum(dealer):
            results[i] = "PUSH"
        elif bsum(hands[i]) > bsum(dealer):
            results[i] = "WIN"
        elif bsum(hands[i]) < bsum(dealer):
            results[i] = "LOSE"

    return results

####################
# HELPER FUNCTIONS #
####################

# compute the blackjack hand, with consideration of an ace in the hand
def bsum(hand):
    total = sum(hand)
    if soft(hand) and total <= 11:
        return total + 10
    else:
        return total

# return true if the hand has an ace
def soft(hand):
    return hand.__contains__(1)

def hit(hand):
    hand.append(deck.pop(0))
    return hand

def split(hand):
    if not splittable(hand):
        return
    
    i = hands.index(hand)
    hands.pop(i)
    hand_one = [hand[0]]
    hand_two = [hand[0]]
    hit(hand_one)
    hit(hand_two)
    hands.insert(i, hand_one)
    hands.insert(i+1, hand_two)

def splittable(hand):
    return len(hand) == 2 and hand[0] == hand[1]

# do we get another opportunity to act after this current action?
def eval_strat(res):
    if res == "HIT" or res == "SPLIT":
        return True
    else:
        return False

########
# BODY #
########

main()