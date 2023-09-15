"""
File: bouncing_ball.py
Name: chun yen chen (Alex)
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

# constant
VX = 3       # horizontal speed
DELAY = 10
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40
switch = False
count = 3

# Global variables
ball = GOval(SIZE, SIZE, x=START_X, y=START_Y)    # main function and ball_switch function will be used


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    global ball
    global count
    global switch

    window = GWindow(800, 500, title='bouncing_ball.py')
    ball.filled = True
    window.add(ball)

    onmouseclicked(ball_switch)
    while count > 0:   # limit falling ball counts (can falling 3 times)

        vy = 0

        while switch:  # switch is true(open) will entrance bouncing_ball function loop
            ball.move(VX, vy)
            vy += GRAVITY     # ball vertical speed, which will increase as gravity constant

            if ball.y + ball.height >= window.height:      # reverse ball direction when ball.y > 500
                time = 0
                if time == 0:
                    vy = -1 * REDUCE * vy

            if ball.x + ball.width >= window.width+100:    # stop function when ball.x > 800+100
                switch = False
                window.add(ball, x=START_X, y=START_Y)
                count -= 1
                break                # break 47 row while loop
            pause(DELAY)
        pause(DELAY)


def ball_switch(event):     # define ball switch function
    global switch
    switch = True      # click mouse can turn on switch


if __name__ == "__main__":
    main()
