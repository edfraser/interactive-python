# Mini-project RPSLS
import random
"""
 Play an advanced version of rock-paper-scissors,
 called rock-paper-scissors-lizard-spock. 
 The key idea of this program is to equate the strings
 'rock', 'paper', 'scissors', 'lizard', 'Spock' to numbers
 as follows:

 0 - rock
 1 - Spock
 2 - paper
 3 - lizard
 4 - scissors
"""
# Helper function **************
def name_to_number(name):
    if name == "rock": return 0
    elif name == "Spock": return 1
    elif name == "paper": return 2
    elif name == "lizard": return 3
    elif name == "scissors": return 4
    else: 
        print "Note: player can choose only 'rock', 'paper', 'scissors', 'lizard' or 'Spock'"
        exit()

# Helper function **************
def number_to_name(number):
    if number == 0: return "rock"
    elif number == 1: return "Spock"
    elif number == 2: return "paper"
    elif number == 3: return "lizard"
    elif number == 4: return "scissors"
    else: 
        print "Number out of range"
        exit()
        
# Main function *****************
def rpsls(player_choice):
    print
    print "Player chooses " + player_choice
    player_number = name_to_number(player_choice)
    
    comp_number = random.randrange(0, 5)
    print "Computer chooses " + number_to_name(comp_number)

    winner = (comp_number - player_number) % 5
    if winner == 1 or winner == 2: print "Computer wins!"
    elif winner == 3 or winner == 4: print "Player wins!"
    else: print "Player and Computer tie!"
  
        
# test *****************
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# error test of player's incorrect input **************
"""
Uncomment rpsls function to see proper functioning of error.
Without the exit() function above, an error is thrown. 
"""
rpsls("crayon")
