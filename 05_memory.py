# implementation of card game - Memory
# See readme for directions on how to execute this code...

# Match cards to win game

import simplegui
import random
cards = (range(8))
cards.extend(range(8))
exposed = []
done = False

# helper function to initialize globals
def new_game():
    # two shuffles to improve randomness...
    global state, turns
    turns = 0
    state = 0
    random.shuffle(cards)
    random.shuffle(cards)
    label.set_text("Turns = " + str(turns))
    for i in range(16):
        exposed.append(False)
        exposed[i] = False # needed for reset button...
        
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global card_pos, state, card1_pos, card2_pos, turns
    x_axis_pos = pos[0]
    card_pos = x_axis_pos // 50 # each card is 50 pixels wide
    
    # exclude exposed cards
    if not exposed[card_pos]:
        # state 0 corrosponds to new game
        if state == 0:
            state = 1
            exposed[card_pos] = True
            card1_pos = card_pos
            turns += 1            
        
        # state 1 corrosponds to one card flipped up in turn
        elif state == 1:
            state = 2
            exposed[card_pos] = True
            card2_pos = card_pos
        
        # state 2 corrosponds to turn complete, two cards to compare
        else:
            if (cards[card1_pos] != cards[card2_pos]):
                exposed[card1_pos] = False
                exposed[card2_pos] = False
            exposed[card_pos] = True
            card1_pos = card_pos
            state = 1
            turns += 1
            
        label.set_text("Turns = " + str(turns))
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    count = 0
    
    for card in range(16):
        canvas.draw_text(str(cards[card]), (count + 10, 65), 50, "white")
        if not exposed[card]: 
            # "turn card over" i.e.: hide card's value 
            canvas.draw_polygon([(count, 0), (count+50, 0), (count+50, 100), (count, 100)], 1, "black", "green")

        count += 50

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
