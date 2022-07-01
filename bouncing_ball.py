from vpython import *


# set the size of scene as a square and its title
scene.width = 450
scene.height = 450
scene.title = "Falling Ball Simulator \n"

# create a variabe to control ball's falling or not
falling = True


def fall(b):
    '''
    bind to button controling ball start, pause and continue
    show Start at first
    show Pause when ball is falling
    show Continue when ball is pausing
    para: the button
    '''
    global falling
    falling = not falling
    if falling: 
        b.text = "Continue"
    else:
        b.text = "Pause"
button(text = "Falling", pos = scene.title_anchor, bind = fall)

# add a blank line between this button and next item
scene.caption = "\n"

# make a 4-wall square room to limit balls bouncing
left_wall = box(pos = vector(-20, 0, 0), size = vector(1, 40, 1), color = color.white)
right_wall = box(pos = vector(20, 0, 0), size = vector(1, 40, 1), color = color.white)
bottom_wall = box(pos = vector(0, -20, 0), size = vector(40, 1, 1), color = color.white)
upper_wall = box(pos = vector(0, 20, 0), size = vector(40, 1, 1), color = color.white)

# define the edges of wall
left_edge = left_wall.pos.x + left_wall.size.x / 2
right_edge = right_wall.pos.x - right_wall.size.x / 2
bottom_edge = bottom_wall.pos.y + bottom_wall.size.y / 2
upper_edge = upper_wall.pos.y - upper_wall.size.y / 2

# create a ball 
ball = sphere(visible = True, pos = vector(-16.5, 16.5, 0), radius = 1, color = color.red)

# define ball surfaces/limits
left_sfc = ball.pos.x - ball.radius
right_sfc = ball.pos.x + ball.radius
bottom_sfc = ball.pos.y - ball.radius
upper_sfc = ball.pos.y + ball.radius

# create a graph to track ball speed, in x, y dimension and the compounded speed
x_speed_plot = gcurve(color = color.red, label = "x_speed")
y_speed_plot = gcurve(color = color.blue, label = "y_speed")
speed_plot = gcurve(color = color.magenta, label = "speed")
# create a time variable as the x value of the graph
time = 0

scene.append_to_caption("\n Select ball color: \n")


def ball_color(m):
    '''
    bind to ball color menu, choose ball color from it
    show Choose ball color at first
    para: menu
    '''
    global ball
    ball.visible = False
    if m.selected == "red":
        ball.color = color.red
    elif m.selected == "blue":
        ball.color = color.blue
    elif m.selected == "green":
        ball.color = color.green
    elif m.selected == "orange":
        ball.color = color.orange
    elif m.selected == "yellow":
        ball.color = color.yellow
    elif m.selected == "purple":
        ball.color = color.purple
    else:
        ball.color = color.white
    ball.visible = True
menu(choices = ["Choose a ball color:", "red", "blue", "green", "orange", "yellow", "purple", "white"], bind = ball_color)

scene.append_to_caption("\n Select trial color: \n")

# attach trails to ball to show its moving pattern
attach_trail(ball, color = color.red)


def trail_color(m):
    '''
    bind to trail color menu, choose trail color from it
    show Choose trail color at first
    para: menu
    '''
    global ball
    ball.visible = False
    if m.selected == "red":
        attach_trail(ball, color = color.red)
    elif m.selected == "blue":
        attach_trail(ball, color = color.blue)
    elif m.selected == "green":
        attach_trail(ball, color = color.green)
    elif m.selected == "orange":
        attach_trail(ball, color = color.orange)
    elif m.selected == "yellow":
        attach_trail(ball, color = color.yellow)
    elif m.selected == "purple":
        attach_trail(ball, color = color.purple)
    else:
        attach_trail(ball, color = color.white)
    ball.visible = True
menu(choices = ["Choose a trail color:", "red", "blue", "green", "orange", "yellow", "purple", "white"], bind = trail_color)

scene.append_to_caption("\n Select walls color: \n")

# make a list of 4 walls so that they can be set at once
walls_list = [left_wall, right_wall, upper_wall, bottom_wall]


def walls_color(m):
    '''
    bind to wall color menu, choose wall color from it
    show Choose wall color at first
    para: menu
    '''
    global walls_list
    for wall in walls_list:
        wall.visible = False
        if m.selected == "red":
            wall.color = color.red
        elif m.selected == "blue":
            wall.color = color.blue
        elif m.selected == "green":
            wall.color = color.green
        elif m.selected == "orange":
            wall.color = color.orange
        elif m.selected == "yellow":
            wall.color = color.yellow
        elif m.selected == "purple":
            wall.color = color.purple
        else:
            wall.color = color.white
        wall.visible = True
menu(choices = ["Choose walls color:", "red", "blue", "green", "orange", "yellow", "purple", "white"], bind = walls_color)

scene.append_to_caption("\n Change ball size: \n")


def ball_size(r):
    '''
    bind to ball size slider, control ball size
    default = 0.5, min = 0, max = 2
    para: slider
    '''
    global ball
    ball.radius = r.value
slider(bind = ball_size, min = 0, max = 2, step = 0.01, value = 0.5)

scene.append_to_caption("\n Change gravity: \n")

# set a vertical speed variable to simulate gravity
y_gravity = 0.002


def grav(g):
    '''
    bind to gravity slider
    cannot equals 0 or ball will not fall
    default = 0.002, min = 0.0005, max = 0.004
    para: slider
    '''
    global y_gravity
    y_gravity = g.value
slider(bind = grav, min = 0.0005, max = 0.004, step = 0.00001, value = 0.002)

scene.append_to_caption("\n Change wind speed (default: 0): \n")

# set a horizontal wind speed
x_wind = 0


def wind(w):
    '''
    bind to wind speed slider to change wind speed
    default = 0, which is no wind
    min = -0.002 wind from right to left
    max = 0.002 wind from left to right
    para: slider
    '''
    global x_wind
    x_wind = w.value
slider(bind = wind, min = -0.002, max = 0.002, step = 0.00001, value = 0)

scene.append_to_caption("\n\n")

# Attach boolean to check if balls are in the square
in_sqr = bool(left_sfc >= left_wall.pos.x and right_sfc <= right_wall.pos.x and bottom_sfc >= bottom_wall.pos.y and upper_sfc <= upper_wall.pos.y)

# set starting speed
x_speed = 0.1
y_speed = 0


# while loop make animation keep ball falling, rate() is needed
while in_sqr:
    # set how fast the loop running
    rate(100)
    # bind the start/pause/continue button to ball's falling
    if not falling:
        left_sfc = ball.pos.x - ball.radius
        right_sfc = ball.pos.x + ball.radius
        if (left_sfc <= left_edge) or (right_sfc >= right_edge):
            # if ball reaches right or left edge it change direction
            x_speed = -x_speed
        # wind changes ball speed in x dimension
        x_speed += x_wind
        ball.pos.x += x_speed

        bottom_sfc = ball.pos.y - ball.radius
        upper_sfc = ball.pos.y + ball.radius
        if (bottom_sfc <= bottom_edge) or (upper_sfc >= upper_edge):
            # if ball reaches bottom or upper edge ti change direction
            y_speed = -y_speed
        # gravity changes ball speed in y dimension
        y_speed -= y_gravity
        ball.pos.y += y_speed
        # calculate the compounded speed so graph can track it
        speed = (x_speed ** 2 + y_speed ** 2) ** 0.5
        # lively generating graph 
        x_speed_plot.plot(time, x_speed)
        y_speed_plot.plot(time, y_speed)
        speed_plot.plot(time, speed)
        time += 0.01
        # to confirm if ball still in the confined space
        in_sqr = bool(left_sfc >= left_wall.pos.x and right_sfc <= right_wall.pos.x and bottom_sfc >= bottom_wall.pos.y and upper_sfc <= upper_wall.pos.y)
