# mini-project: "Stopwatch: The Game" 
# See readme for directions on how to execute this code...

import simplegui

# define global variables
t = 0
x = 0
y = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    C = t % 100 // 10
    B = t % 600 // 100
    A = t // 600
    
    return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()

def stop_handler():
    global x, y
    if timer.is_running():
        timer.stop()
        y = y + 1
        if t % 10 == 0:
            x = x + 1
      
def reset_handler():
    global t, x, y
    timer.stop()
    t = 0
    x = 0
    y = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t
    t = t + 1

    # define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(t), [75, 150], 50, "red")
    canvas.draw_text(str(x) + "/" + str(y), [0, 15], 20, "red")
    
    
# create frame
frame = simplegui.create_frame("Stop Watch", 300, 300)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)

frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_handler)
frame.add_button("Stop", stop_handler)
frame.add_button("Reset", reset_handler)

# start frame
frame.start()
# Please remember to review the grading rubric
