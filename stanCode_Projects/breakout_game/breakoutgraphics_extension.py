"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

This is a class BreakoutGraphics file for breakout usage

"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
from campy.gui.events.timer import pause

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks      ori:10
BRICK_COLS = 10        # Number of columns of bricks    ori:10
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 100     # Width of the paddle (in pixels)  original:75
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # create BreakoutGraphics attribute, default setting to soft private or strict private
        self._paddle_offset = paddle_offset
        self.__dx = 0
        self.__dy = 0
        self._ball_radius = BALL_RADIUS
        self._brick_rows = brick_rows
        self._brick_cols = brick_cols
        self._paddle_width = paddle_width
        self._paddle_height = paddle_height
        self._brick_width = brick_width
        self._brick_height = brick_height
        self._brick_spacing = brick_spacing
        self._brick_offset = brick_offset

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # game 1 opening word
        game_1_opening = GLabel('This is a breakout game !!' + '\n' + '\n'
                                + 'user have 3 lives, and click mouse can start game' + '\n' + '\n'
                                + 'If ball falling out of window will lost one live' + '\n' + '\n'
                                + 'If user lost 3 lives or remove all bricks,the game will be over')

        game_1_opening.font = 'dialog-12-italic-bolt'

        self.window.add(game_1_opening, x=(self.window.width / 3.5) - (self.window.width / 4), y=self.window.height)

        game1_start_go = False           # game 1 switch: default is false
        while True:                      # game 1 opening word animation loop
            game_1_opening.move(0, -2)
            pause(10)
            if game_1_opening.y <= -50:
                game1_start_go = True
                break

        if game1_start_go:              # entrance game 1
            # Create a paddle
            self.paddle = GRect(paddle_width, paddle_height, x=(self.window.width - paddle_width)/2, y=self.window.height - paddle_height - paddle_offset)
            self.paddle.filled = True
            self.window.add(self.paddle)

            # Center a filled ball in the graphical window
            self.ball = GOval(2*ball_radius, 2*ball_radius, x=(self.window.width - ball_radius)/2, y=(self.window.height - ball_radius)/2)
            self.window.add(self.ball)
            self.ball.filled = True

            # Draw bricks
            for i in range(0, brick_rows):
                for j in range(0, brick_cols):
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.filled = True
                    if i <= 1:
                        self.brick.fill_color = 'red'
                    elif 2 <= i < 4:
                        self.brick.fill_color = 'orange'
                    elif 4 <= i < 6:
                        self.brick.fill_color = 'yellow'
                    elif 6 <= i < 8:
                        self.brick.fill_color = 'green'
                    else:
                        self.brick.fill_color = 'blue'

                    self.window.add(self.brick, x=j*(self.brick.width + brick_spacing), y=i*(self.brick.height + brick_spacing) + brick_offset)

            # Default initial velocity for the ball
            self.__dx = random.randint(1, MAX_X_SPEED)
            while self.__dx == 0:
                self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:           # 50% 機率 x 方向速度會變號
                self.__dx = - self.__dx
            self.__dy = INITIAL_Y_SPEED

            # Initialize our mouse listeners
            onmousemoved(self.paddle_control)

    # method
    def paddle_control(self, mouse):
        self.paddle.x = mouse.x - self.paddle.width/2              # set mouse center to paddle center
        self.paddle.y = self.window.height - self._paddle_offset   # fixed paddle y axis(is a constant)

        if mouse.x - self.paddle.width/2 <= 0:                 # avoid paddle left side beyond the window
            self.paddle.x = 0
        if mouse.x + self.paddle.width >= self.window.width:   # avoid paddle right side beyond the window
            self.paddle.x = self.window.width - self.paddle.width

    # method (return value to user terminal)
    def get_vx(self):       # pass vx value for user terminal use
        return self.__dx

    def get_vy(self):       # pass vy value for user terminal use
        return self.__dy

    def get_ball_radius(self):    # pass ball radius for user terminal use
        return self._ball_radius

    def brick_count(self):        # pass all bricks counts for user terminal use
        return self._brick_rows*self._brick_cols

    def get_paddle_width(self):  # pass paddle width for user terminal use
        return self._paddle_width

    # *******************************************************************************************************
    # game 2 part

    # method for game 2
    def game_2_stage(self):
        pause(1500)
        self.window.clear()
        pause(1300)
        self.game_2_bricks_counts = 0

        # game 2 opening word
        game_2_opening = GLabel('Congratulations passing stage 1 !!' + '\n' + '\n'
                                + 'user can challenge stage 2' + '\n' + '\n'
                                + 'user have 3 lives, and click mouse can start game' + '\n' + '\n'
                                + 'If ball falling out of window will lost one live' + '\n' + '\n'
                                + 'If user lost 3 lives or paddle remaining counts = 0' + '\n' + '\n'
                                + 'or remove all bricks,the game will be over')

        game_2_opening.font = 'dialog-12-italic-bolt'

        self.window.add(game_2_opening, x=(self.window.width / 3.5) - (self.window.width / 4), y=self.window.height)

        game2_start_go = False     # game 2 switch: default is false(avoid coding direct entrance game 2 part)
        while True:               # game 2 opening word animation loop
            game_2_opening.move(0, -2)
            pause(12)
            if game_2_opening.y <= -50:
                game2_start_go = True
                break

        if game2_start_go:    # entrance game 2

            # Create a paddle
            self.paddle = GRect(self._paddle_width, self._paddle_height, x=(self.window.width - self._paddle_width)/2,
                                y=self.window.height - self._paddle_height - self._paddle_offset)
            self.paddle.filled = True
            self.window.add(self.paddle)

            # Center a filled ball in the graphical window
            self.ball = GOval(2 * self._ball_radius, 2 * self._ball_radius, x=(self.window.width - self._ball_radius)/2,
                              y=(self.window.height - self._ball_radius)/2)
            self.window.add(self.ball)
            self.ball.filled = True

            # Draw game 2 bricks
            for i in range(0, self._brick_rows):
                for j in range(0, self._brick_cols):
                    self.brick = GRect(self._brick_width, self._brick_height)
                    self.brick.filled = True
                    if i <= 1:
                        self.brick.fill_color = 'red'
                    elif 2 <= i < 4:
                        self.brick.fill_color = 'blue'
                    elif 4 <= i < 6:
                        self.brick.fill_color = 'gray'
                    elif 6 <= i < 8:
                        self.brick.fill_color = 'green'
                    else:
                        self.brick.fill_color = 'purple'

                    self.window.add(self.brick, x=j * (self.brick.width + self._brick_spacing),
                                    y=i * (self.brick.height + self._brick_spacing) + self._brick_offset)

                    self.game_2_bricks_counts += 1     # calculate game2 brick counts for user terminal used

    # method
    def get_game_2_bricks_counts(self):   # return game 2 brick counts
        return self.game_2_bricks_counts

    # method
    def set_new_paddle_width(self, new_width):  # create extent paddle length method
        paddle_width2 = new_width
        self.paddle = GRect(paddle_width2, self._paddle_height, x=(self.window.width - paddle_width2) / 2,
                            y=self.window.height - self._paddle_height - self._paddle_offset)
        self.paddle.filled = True
        self.window.add(self.paddle)

