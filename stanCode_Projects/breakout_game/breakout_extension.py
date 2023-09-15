"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This is a breakout game !!
user have 3 lives, and click mouse can start game
if ball falling out of window will lost one live
If user lost 3 lives or remove all bricks, the game will be over

"""

from campy.gui.events.timer import pause
from breakoutgraphics_extension import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked
from campy.graphics.gobjects import GLabel, GOval


FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts

# global variable
switch = False
switch2 = False


def main():
    global switch
    global switch2

    graphics = BreakoutGraphics()          # calling BreakoutGraphics class, and assign to graphics (裝到 graphics 箱子)

    brick_count = graphics.brick_count()   # game 1 total bricks counts
    speed_increase_switch = True           # ball speed 1 increase switch for user meet some game condition used
    speed_increase_switch2 = True          # ball speed 2 increase switch for user meet some game condition used
    paddle_extent = True                   # paddle extension switch for user meet some game condition used

    # score label define
    scores = 0
    score_label = GLabel('Scores:' + str(scores))
    score_label.font = 'Dialog-20-italic'
    score_label.color = 'blue'
    graphics.window.add(score_label, x=0, y=graphics.window.height)

    # lives label define
    lives = NUM_LIVES
    lives_label = GLabel("Lives:" + str(lives))
    lives_label.font = 'Dialog-20-italic'
    lives_label.color = 'blue'
    graphics.window.add(lives_label, x=graphics.window.width-lives_label.width-5, y=graphics.window.height)

    # speed label define
    speed = GLabel(' Speed:normal ')
    speed.font = 'Dialog-20-italic'
    speed.color = 'blue'
    graphics.window.add(speed, x=graphics.window.width/3.2, y=graphics.window.height)

    # get attribute value from coder terminal
    dx = graphics.get_vx()    # get ball x axis velocity
    dy = graphics.get_vy()    # get ball y axis velocity
    ball_radius = graphics.get_ball_radius()      # get ball radius
    paddle_width = graphics.get_paddle_width()    # get paddle width

    # Add the animation loop here!
    onmouseclicked(game_start_control)     # click mouse can start game(ball start to fall)

    while lives > 0:        # double while loop for game 1 progress
        pause(FRAME_RATE)

        while switch:       # control ball whether falling switch
            pause(FRAME_RATE)

        # update
            graphics.ball.move(dx, dy)   # ball x,y move velocity

        # check
            # check ball rebound when ball touch window left,right,and top side
            if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                dx = -dx
            if graphics.ball.y <= 0:
                if dy < 0:
                    dy = -dy

            # when ball falling out of window bottom side, and user will lost one lives
            if graphics.ball.y + graphics.ball.height >= graphics.window.height+30:
                switch = False
                lives -= 1
                graphics.window.add(graphics.ball, x=(graphics.window.width - ball_radius)/2, y=(graphics.window.height - ball_radius)/2)
                lives_label.text = 'Lives:' + str(lives)
                break

            # trigger 1st increase speed condition
            if scores/brick_count >= 0.1 and speed_increase_switch:
                dx = 1.3 * dx
                dy = 1.3 * dy
                speed.text = '   Speed up!!'
                speed.color = 'red'
                speed_increase_switch = False

            # trigger 2nd increase speed condition
            if scores / brick_count >= 0.25 and speed_increase_switch2:
                dx = 1.3 * dx
                dy = 1.3 * dy
                speed.text = '  Speed up up!!'
                speed.color = 'red'
                speed_increase_switch2 = False

            # trigger extent paddle width condition
            if scores / brick_count >= 0.35 and paddle_extent:
                old_paddle = graphics.window.get_object_at(graphics.paddle.x, graphics.paddle.y)
                graphics.window.remove(old_paddle)
                graphics.set_new_paddle_width(paddle_width * 1.4)
                paddle_extent = False

            # define ball top left vertex(tl), top right vertex(tr), bottom left vertex(bl),and bottom right vertex(br)
            maybe_object_tl = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)
            maybe_object_tr = graphics.window.get_object_at(graphics.ball.x + graphics._ball_radius*2, graphics.ball.y)
            maybe_object_bl = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics._ball_radius*2)
            maybe_object_br = graphics.window.get_object_at(graphics.ball.x + graphics._ball_radius*2, graphics.ball.y + graphics._ball_radius*2)

            # define remove condition
            maybe_object_tl_remove_condition = maybe_object_tl is not score_label and maybe_object_tl is not lives_label and maybe_object_tl is not graphics.paddle and maybe_object_tl is not speed
            maybe_object_tr_remove_condition = maybe_object_tr is not score_label and maybe_object_tr is not lives_label and maybe_object_tr is not graphics.paddle and maybe_object_tr is not speed
            maybe_object_bl_remove_condition = maybe_object_bl is not score_label and maybe_object_bl is not lives_label and maybe_object_bl is not graphics.paddle and maybe_object_bl is not speed
            maybe_object_br_remove_condition = maybe_object_br is not score_label and maybe_object_br is not lives_label and maybe_object_br is not graphics.paddle and maybe_object_br is not speed

            # ball rebound when touch paddle
            if maybe_object_bl is graphics.paddle or maybe_object_br is graphics.paddle:
                if dy > 0:          # avoid ball re-rebound within paddle (fixed bug)
                    dy = -dy

            else:    # remove brick and add score condition (remove brick when ball (4 corner) hitting the brick)
                if maybe_object_tl is not None and maybe_object_tl_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_tl)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

                elif maybe_object_tr is not None and maybe_object_tr_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_tr)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

                elif maybe_object_bl is not None and maybe_object_bl_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_bl)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

                elif maybe_object_br is not None and maybe_object_br_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_br)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

            if scores == brick_count:         # game win condition
                win_label = GLabel("You Win !!")
                win_label.font = 'Dialog-30-italic-bolt'
                win_label.color = 'pink'
                graphics.window.add(win_label, x=(graphics.window.width - win_label.width)/2, y=(graphics.window.height)/2)
                game_2_start_switch = True
                break
        if scores == brick_count:
            break

    if lives == 0:                            # game lose condition
        loss_label = GLabel("You Lose !!")
        loss_label.font = 'Dialog-30-italic-bolt'
        loss_label.color = 'red'
        graphics.window.add(loss_label, x=(graphics.window.width-loss_label.width)/2, y=graphics.window.height/2)
    switch = False       # turn off game 1 switch

    # *******************************************************************************************************
    # if pass game 1 can entrance game 2 part

    game_2_start_switch = False
    if scores == brick_count:
        graphics.game_2_stage()

    # re-assign game 1 needed variable
    dx = graphics.get_vx()
    dy = graphics.get_vy()
    ball_radius = graphics.get_ball_radius()
    speed_increase_switch = True
    speed_increase_switch2 = True
    paddle_extent = True  # paddle extent switch for user meet some game condition used

    scores = 0
    score_label = GLabel('Scores:' + str(scores))
    score_label.font = 'Dialog-20-italic'
    score_label.color = 'blue'
    graphics.window.add(score_label, x=0, y=graphics.window.height)

    lives = NUM_LIVES
    lives_label = GLabel("Lives:" + str(lives))
    lives_label.font = 'Dialog-20-italic'
    lives_label.color = 'blue'
    graphics.window.add(lives_label, x=graphics.window.width - lives_label.width - 5, y=graphics.window.height)

    # game 2 extra add
    stage_2_brick_count = graphics.game_2_bricks_counts       # game 2 total brick counts
    paddle_remaining_counts = int(stage_2_brick_count * 0.7)  # define paddle remaining counts, can adjust 0.7 value

    paddle_count_label = GLabel('Paddle remaining:' + str(paddle_remaining_counts))
    paddle_count_label.font = 'Dialog-16-italic'
    paddle_count_label.color = 'red'
    graphics.window.add(paddle_count_label, x=graphics.window.width / 3.25, y=graphics.window.height)

    # Add the animation loop here!

    onmouseclicked(game2_start_control)    # click mouse can start game2 (ball start to fall)

    while lives > 0:        # double while loop for game 2 progress
        pause(FRAME_RATE)

        while switch2:
            pause(FRAME_RATE)

        # update

            graphics.ball.move(dx, dy)   # define ball vx, vy

        # check
            # check ball rebound when ball touch window left,right,and top side
            if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                dx = -dx
            if graphics.ball.y <= 0:
                if dy < 0:
                    dy = -dy

            # when ball falling out of window bottom side, and user will lost one lives
            if graphics.ball.y + graphics.ball.height >= graphics.window.height+30:
                switch2 = False
                lives -= 1

                # normal ball
                if lives >= 2:
                    graphics.window.add(graphics.ball, x=(graphics.window.width - ball_radius)/2,
                                        y=(graphics.window.height - ball_radius) / 2)

                # last ball, which ball radius *2, and color is gold
                else:
                    graphics.ball = GOval(graphics._ball_radius*2, graphics._ball_radius*2)
                    graphics.ball.filled = 'True'
                    graphics.ball.fill_color = 'gold'
                    graphics.ball.color = 'gold'
                    graphics.window.add(graphics.ball, x=(graphics.window.width - ball_radius)/2,
                                        y=(graphics.window.height - ball_radius) / 2)

                lives_label.text = 'Lives:' + str(lives)
                break

            # trigger 1st increase speed condition
            if scores/brick_count >= 0.1 and speed_increase_switch:
                dx = 1.3 * dx
                dy = 1.3 * dy
                # speed.text = '   Speed up!!'
                # speed.color = 'red'
                speed_increase_switch = False

            # trigger 2nd increase speed condition
            if scores / brick_count >= 0.2 and speed_increase_switch2:
                dx = 1.3 * dx
                dy = 1.3 * dy
                # speed.text = '  Speed up up!!'
                # speed.color = 'red'
                speed_increase_switch2 = False

            # trigger extent paddle width condition
            if scores / brick_count >= 0.5 and paddle_extent:
                old_paddle = graphics.window.get_object_at(graphics.paddle.x, graphics.paddle.y)
                graphics.window.remove(old_paddle)
                graphics.set_new_paddle_width(paddle_width * 1.4)
                paddle_extent = False

            # define ball top left vertex(tl), top right vertex(tr), bottom left vertex(bl),and bottom right vertex(br)
            maybe_object_tl = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)
            maybe_object_tr = graphics.window.get_object_at(graphics.ball.x + graphics._ball_radius*2, graphics.ball.y)
            maybe_object_bl = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics._ball_radius*2)
            maybe_object_br = graphics.window.get_object_at(graphics.ball.x + graphics._ball_radius*2, graphics.ball.y + graphics._ball_radius*2)

            # define remove condition
            maybe_object_tl_remove_condition = maybe_object_tl is not score_label and maybe_object_tl is not lives_label and maybe_object_tl is not graphics.paddle and maybe_object_tl is not speed and maybe_object_tl is not paddle_count_label
            maybe_object_tr_remove_condition = maybe_object_tr is not score_label and maybe_object_tr is not lives_label and maybe_object_tr is not graphics.paddle and maybe_object_tr is not speed and maybe_object_tr is not paddle_count_label
            maybe_object_bl_remove_condition = maybe_object_bl is not score_label and maybe_object_bl is not lives_label and maybe_object_bl is not graphics.paddle and maybe_object_bl is not speed and maybe_object_bl is not paddle_count_label
            maybe_object_br_remove_condition = maybe_object_br is not score_label and maybe_object_br is not lives_label and maybe_object_br is not graphics.paddle and maybe_object_br is not speed and maybe_object_br is not paddle_count_label

            # ball rebound when touch paddle and subtract paddle remaining count
            if maybe_object_bl is graphics.paddle or maybe_object_br is graphics.paddle:
                if dy > 0:
                    dy = -dy
                paddle_remaining_counts -= 1
                paddle_count_label.text = 'Paddle remaining:' + str(paddle_remaining_counts)

            else:  # remove brick and add score condition (remove brick when ball (4 corner) hitting the brick)
                if maybe_object_tl is not None and maybe_object_tl_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_tl)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

                elif maybe_object_tr is not None and maybe_object_tr_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_tr)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

                elif maybe_object_bl is not None and maybe_object_bl_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_bl)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

                elif maybe_object_br is not None and maybe_object_br_remove_condition:
                    dy = -dy
                    graphics.window.remove(maybe_object_br)
                    scores += 1
                    score_label.text = 'Scores:' + str(scores)

            if scores == stage_2_brick_count:                     # game win condition
                win_label = GLabel("You Win !!")
                win_label.font = 'Dialog-30-italic-bolt'
                win_label.color = 'pink'
                graphics.window.add(win_label, x=(graphics.window.width - win_label.width), y=(graphics.window.height)/2)
                break

            if paddle_remaining_counts == 0:                      # game lose condition
                loss_label = GLabel("You Lose !!")
                loss_label.font = 'Dialog-30-italic-bolt'
                loss_label.color = 'red'
                graphics.window.add(loss_label, x=(graphics.window.width - loss_label.width) / 2,
                                    y=graphics.window.height / 2)
                break

        if scores == stage_2_brick_count or paddle_remaining_counts == 0:
            break

    if lives == 0:                                                 # game lose condition
        loss_label = GLabel("You Lose test!!")
        loss_label.font = 'Dialog-30-italic-bolt'
        loss_label.color = 'red'
        graphics.window.add(loss_label, x=(graphics.window.width-loss_label.width)/2, y=graphics.window.height/2)


def game_start_control(event):
    global switch
    switch = True


def game2_start_control(event):
    global switch2
    switch2 = True


if __name__ == '__main__':
    main()


