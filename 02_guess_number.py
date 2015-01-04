# mini-project: "Guess the number" 
# See readme for directions on how to execute this code...

# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

# helper function to start and restart the game
def new_game(start, end):
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(start, end)
    print
    print "New game: guess a number between " + str(start) + " - " + str(end)
    
    global guess_count
    global guesses_allowed
    
    if (end == 100): 
        guess_count = 7
        guesses_allowed = 7
        
    elif (end == 1000): 
        guess_count = 10
        guesses_allowed = 10
        
    else:
        print "Error: number out of range"
        exit()
    print "Number of remaining guesses is " + str(guess_count)
    print
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    new_game(0, 100)
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game
    new_game(0, 1000)
    
def input_guess(guess):
    # main game logic goes here	
    player_number = int(guess)
    print "Guess was: " + guess
    
    # Decrement the number of guesses left in play...
    global guess_count
    guess_count = guess_count - 1
    print "Number of remaining guesses is " + str(guess_count)
    
    if (guess_count > 0) and (secret_number - player_number > 0): 
        print "Higher"
        print
    elif (guess_count > 0) and (secret_number - player_number < 0): 
        print "Lower"
        print
    else:
        if (guess_count > -1) and (secret_number - player_number == 0): 
            print "Correct!"
            if (guesses_allowed == 7):
                new_game(0, 100)
            elif (guesses_allowed == 10):
                new_game(0, 1000)
            else: 
                print "Error: guesses_allowed out of range"
                exit()
        else: 
            print "You ran out of guesses. The secret number was " + str(secret_number)
            if (guesses_allowed == 7):
                new_game(0, 100)
            elif (guesses_allowed == 10):
                new_game(0, 1000)
            else: 
                print "Error: guesses_allowed out of range"
                exit()
        

# create frame
frame = simplegui.create_frame("Home", 300, 200)

# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter guess", input_guess, 194)

# call new_game 
new_game(0, 100)


"""
secret_number = 74	
input_guess("50")
input_guess("75")
input_guess("62")
input_guess("68")
input_guess("71")
input_guess("73")
input_guess("74")
"""
