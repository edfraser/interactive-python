# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
#ball_pos = [WIDTH / 2, HEIGHT / 2]
#ball_vel = [-40.0 / 60.0,  5.0 / 60.0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    if direction == "RIGHT":
        ball_vel = [random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]
        
    else: # direction == LEFT
        ball_vel = [-random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = 100
    paddle2_pos = 150
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball("LEFT")

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
   
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Red")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Blue")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Top bounds, reflects ball    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # Bottom bounds, reflects ball
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1] 
    
    # Left paddle reflects ball
    elif ball_pos[0] <= 1 + BALL_RADIUS + PAD_WIDTH: 
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            # Multiplier accelerates ball speed to increase difficulty
            ball_vel[0] = -ball_vel[0] * 1.1  
        else: #Score!
            if ball_pos[0] < PAD_WIDTH: # wait until ball is obviously through goal line...
                score2 = score2 + 1
                spawn_ball("RIGHT")
            
    # Right paddle reflects ball
    elif (ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH):
        if (paddle2_pos <= ball_pos[1]) and (paddle2_pos + PAD_HEIGHT >= ball_pos[1]):
            ball_vel[0] = -ball_vel[0] * 1.1 
        else: #Score!
            if ball_pos[0] > WIDTH - PAD_WIDTH: # wait until ball is obviously through goal line...
                score1 = score1 + 1
                spawn_ball("LEFT")
           
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle1's vertical position, keep paddle on the screen
    if (paddle1_pos <= HEIGHT - PAD_HEIGHT) and (paddle1_vel > 0):
        paddle1_pos += paddle1_vel
        
    elif (paddle1_pos >= 0) and (paddle1_vel < 0):
        paddle1_pos += paddle1_vel
    
    else: pass # paddle1 stationary...
    
    # update paddle2's vertical position, keep paddle on the screen    
    if (paddle2_pos <= HEIGHT - PAD_HEIGHT) and (paddle2_vel > 0):
        paddle2_pos += paddle2_vel
        
    elif (paddle2_pos >= 0) and (paddle2_vel < 0):
        paddle2_pos += paddle2_vel
    
    else: pass # paddle2 stationary...
    
    # draw paddles, drawn from upper left corner pixal of paddles, left is paddle1, right is paddle2
    canvas.draw_polygon([(0, paddle1_pos), (PAD_WIDTH, paddle1_pos), (PAD_WIDTH, paddle1_pos+PAD_HEIGHT), (0, paddle1_pos+PAD_HEIGHT)], 1, "Blue", "Blue")
    canvas.draw_polygon([(WIDTH-PAD_WIDTH, paddle2_pos), (WIDTH, paddle2_pos), (WIDTH, paddle2_pos+PAD_HEIGHT), (WIDTH-PAD_WIDTH, paddle2_pos+PAD_HEIGHT)], 1, "Red", "Red")
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 2 - 100, 100), 50, "Blue", "sans-serif")
    canvas.draw_text(str(score2), (WIDTH / 2 + 70, 100), 50, "Red", "sans-serif")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    #print simplegui.KEY_MAP("w")
    if key == 87: paddle1_vel = -10
    elif key == 83: paddle1_vel = 10
    elif key == 34 or key == 38: paddle2_vel = -10 #arrow up 38
    elif key == 35 or key == 40: paddle2_vel = 10 #arrow down 40
    else: pass

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()
