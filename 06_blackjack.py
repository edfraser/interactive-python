# Mini-project #6 - Blackjack
# See readme for directions on how to execute this code...

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
            
    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
# define hand class
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        str_hand = ""
        for card in self.hand:
            str_hand += str(card) + " "
        return str_hand	# return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card) # add a card object to a hand
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
       
        # value of hand
        an_ace_in_hand = False
        value = 0
        
        for i in range(len(self.hand)):
            card = self.hand[i]
            rank = card.get_rank()
            value = value + VALUES.get(rank)
            if rank == "A":
                an_ace_in_hand = True
        
        # value if an ace in hand
        if not an_ace_in_hand:
            return value
        elif value + 10 <= 21:
            return value + 10
        else:
            return value
            
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand)):
            card = self.hand[i]
            pos[0] = 100 + i * CARD_SIZE[0]
            card.draw(canvas, pos)
    
    def draw_back(self, canvas, pos):
        card_back_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0]), (CARD_BACK_CENTER[1] + CARD_BACK_SIZE[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop(0)	# deal first card object from the deck
    
    def __str__(self):
        # return a string representing the deck
        str_deck = ""
        for card in self.deck:
            str_deck += str(card) + " "
        return str_deck	# return a string representation of a hand
    
    def count(self):
        # return a number representing count of cards in deck
        count = 0
        for card in self.deck:
            count += 1
        return count
    
    #define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, mydeck, score
    outcome = "Hit or Stand?"

    # begin game of blackjack...
    # create instance of card deck and shuffle
    mydeck = Deck()
    mydeck.shuffle()
    
    # create instance of player hand, and deal two cards
    player_hand = Hand()
    player_hand.add_card(mydeck.deal_card())
    player_hand.add_card(mydeck.deal_card())
    
    # create instance of dealer hand, and deal two cards
    dealer_hand = Hand()
    dealer_hand.add_card(mydeck.deal_card())
    dealer_hand.add_card(mydeck.deal_card())
    
    # if player re-deals hand while in-play, decrement score
    if in_play:
        score = score - 1
    else: in_play = True
    
#    print
#    print "Dealer: " + str(dealer_hand), str(dealer_hand.get_value())
#    print "Player: " + str(player_hand), str(player_hand.get_value()), outcome

def hit():
    global score, outcome, in_play, player_hand, mydeck

    # if the hand is in play, hit the player
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(mydeck.deal_card())      
        
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You have busted, new deal?"
            score = score - 1
            in_play = False
    
#    print "Player: " + str(player_hand), str(player_hand.get_value()), outcome
    
def stand():
    global score, outcome, in_play, player_hand, dealer_hand, mydeck
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if outcome.find("busted") != -1:
        outcome = "You already busted, new deal?"
        
    else:        
        while in_play and dealer_hand.get_value() < 17:
            dealer_hand.add_card(mydeck.deal_card())
            
            if dealer_hand.get_value() > 21:
                outcome = "Dealer busts, new deal?"
                score = score + 1
                in_play = False
                
        # assign a message to outcome, update in_play and score
        if in_play:
            in_play = False
            
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "Dealer wins, new deal?"
                score = score - 1

            else:
                outcome = "Player wins, new deal?"
                score = score + 1 
    
#    print "Dealer: " + str(dealer_hand), str(dealer_hand.get_value())
#    print "Player: " + str(player_hand), str(player_hand.get_value()), outcome
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand
    
    player_hand.draw(canvas, [100, 125])
    dealer_hand.draw(canvas, [100, 325])
    
    if in_play:
        canvas.draw_image(card_back, (72/2, 96/2), (72, 96), [100+72/2, 325+96/2], (72, 96))
        
    canvas.draw_text("Blackjack",[110, 60], 75, 'black')
    canvas.draw_text(outcome, [110, 100], 20, 'black')
    canvas.draw_text("Score: " + str(score), [110, 120], 20, 'black')
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
