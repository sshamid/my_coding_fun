# blackjack game
'''
Game logic:
The game logic for our simplified version of Blackjack is as follows. 
The player and the dealer are each dealt two cards initially with one of the dealer's cards 
being dealt faced down (his hole card, marked XX in my text version). 
The player chooses to "hit" his hand by dealing him another card.
If, at any point, the value of the player's hand exceeds 21, the player is "busted" and 
loses immediately. At any point prior to busting, the player may "stand" and 
the dealer will then hit his hand until the value of his hand is 17 or more. 
(For the dealer, aces count as 11 unless it causes the dealer's hand to bust). 
If the dealer busts, the player wins. Otherwise, the player and dealer then compare the 
values of their hands and the hand with the higher value wins. 
The dealer wins ties in my version.
The player starts with 100 chips and must bet a listed amount in each game.
'''
import random
import string

# initialize some useful global variables
in_play = False
outcome = ""
player_message="Hit or Stand?"
chips = 100
bet_amount = ['1', '5', '10', '15', '20', '25', '50', '100']
# define globals for cards
SUITS = ('S', 'H', 'D', 'C')
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
	
# define hand class
class Hand:
    def __init__(self):
        self.cards=[]

    def __str__(self):
        output=""
        for i in self.cards:
        	output+= i.suit + i.rank + " "
        return "hand contains" + " " + output

    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        has_ace=False
        value=0
        for i in self.cards:
            if i.rank=="A":
                has_ace=True
            value+=VALUES[i.rank]
        if has_ace and value<=11:
            value+=10
        return value

# define deck class
class Deck:
    def __init__(self):
        self.cards=range(52)

    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        card=self.cards.pop()
        return Card(SUITS[card//13], RANKS[card%13])
    
    def __str__(self):
        output=""
        for i in self.cards:
            output+=str(i)+", "
        return "Deck contains" + " " +output


def deal():
    global outcome, player_message, in_play, chips, bet, bet_amount, deck, player_hand, dealer_hand
    deck=Deck()
    deck.shuffle()
    player_hand=Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand=Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "chips = " + str(chips)
    
    print "What is your bet? (1, 5, 10, 15, 20, 25, 50, 100)"
    bet = raw_input(' > ')
    if bet in bet_amount:
    	bet = int(bet)
    	if bet <= chips:
    		chips -= bet
    		print "chips left = " + str(chips)
    	else:
    		print "You don't have enough chips for that bet."
    		deal()
    else:
    	print "invalid bet amount!"
    	deal()
    print "player " + str(player_hand) + " points = " + str(player_hand.get_value())
    sstt = str(dealer_hand)
    new_str = string.replace(str(dealer_hand), sstt[14]+sstt[15], 'XX')
    print "dealer " + str(new_str)
    in_play = True
    player_message="[H]it or [S]tand or [Q]uit: "
    
    

def hit():
    global outcome, player_message, in_play, deck, player_hand, dealer_hand
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        
        # if busted, assign an message to outcome
        if player_hand.get_value()>21:
        	outcome = "You busted with " + str(player_hand) + "points = " + str(player_hand.get_value())
        	print outcome
        	print "dealer " + str(dealer_hand) + " points = " + str(dealer_hand.get_value())
        	player_message="[N]ew deal or [Q]uit: "
        else:
        	print "player " + str(player_hand) + " points = " + str(player_hand.get_value())
        	sstt = str(dealer_hand)
        	new_str = string.replace(str(dealer_hand), sstt[14]+sstt[15], 'XX')
        	print "dealer " + str(new_str)

    
       
def stand():
    global outcome, player_message, chips, bet, in_play, deck, player_hand, dealer_hand
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_hand.get_value()<17:
    	dealer_hand.add_card(deck.deal_card())
    
    if dealer_hand.get_value()>21:
    	print "player " + str(player_hand) + " points = " + str(player_hand.get_value())
        outcome="Dealer busted with " + str(dealer_hand) + "points = " + str(dealer_hand.get_value())
        print outcome
        chips += 2 * int(bet)
        print "chips = " + str(chips)
    else:
		if player_hand.get_value() > dealer_hand.get_value():
			print "player " + str(player_hand) + " points = " + str(player_hand.get_value())
			print "dealer " + str(dealer_hand) + " points = " + str(dealer_hand.get_value())
			outcome="You win!"
			print outcome
			chips += 2 * int(bet)
			print "Total chips = " + str(chips)
		elif player_hand.get_value() == dealer_hand.get_value():
			print "player " + str(player_hand) + " points = " + str(player_hand.get_value())
			print "dealer " + str(dealer_hand) + " points = " + str(dealer_hand.get_value())
			outcome="Its tie! dealer wins!"
			print outcome
		else:
			print "player " + str(player_hand) + " points = " + str(player_hand.get_value())
			print "dealer " + str(dealer_hand) + " points = " + str(dealer_hand.get_value())
			outcome="You lose."
			print outcome
    player_message=" [N]ew deal or [Q]uit: "


# deal an initial hand
deal()
	
while in_play == True:
    c = raw_input(player_message).lower()
    if c == 'h':
        hit()
        
    elif c == 's':
        stand()
        
    elif c == 'n':
    	if chips == 0:
    		print "You don't have chips left. bye! \n"
    		in_play = False
        else:
        	deal()
        
    else:
        if c == 'q':
            in_play = False
        else:
            print "Invalid choice."
    if chips < 0:
            print "You're out of cash!"
            in_play = False
