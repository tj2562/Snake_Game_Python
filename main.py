# reference: Christian Thompson @ Sanke game in Python
import turtle
import time
import random

def press_up():
    if user_head.direction != "down":
        user_head.direction = "up"

def press_down():
    if user_head.direction != "up":
        user_head.direction = "down"

def press_left():
    if user_head.direction != "right":
        user_head.direction = "left"

def press_right():
    if user_head.direction != "left":
        user_head.direction = "right"

def move_user_snake():
    y = user_head.ycor()
    x = user_head.xcor()

    if user_head.direction == "up":
        user_head.sety(y + 20)

    if user_head.direction == "down":
        user_head.sety(y - 20)

    if user_head.direction == "right":
        user_head.setx(x + 20)
    if user_head.direction == "left":
        user_head.setx(x - 20)

    if user_head.xcor() > 240 or user_head.xcor() < -240:
        user_head.goto(-x,y)
    elif user_head.ycor() > 240 or user_head.ycor() < -240:
        user_head.goto(x, -y)

def move_com_snake(turtle, move_dir, move_count):
    for i in range(5):
        y = turtle[i].ycor()
        x = turtle[i].xcor()

        prev_dir = move_dir[i]
        #같은 방향을 최소 3번은 가도록 한다.(진동 방지)
        if move_count[i] <= 2:
           rand_dir = prev_dir
        else:
        #진행방향대로 3번 간 후 반대 방향을 제외하고 나머지 방향으로 회전
            if prev_dir == "up":
               rand_dir = random.choice(["right", "left"])
            elif prev_dir == "down":
                rand_dir = random.choice(["right", "left"])
            elif prev_dir == "left":
                rand_dir = random.choice(["up", "down"])
            elif prev_dir == "right":
                rand_dir = random.choice(["up", "down"])
            move_count[i] = 0

        if rand_dir == "up":
            turtle[i].sety(y + 20)
        elif rand_dir == "down":
            turtle[i].sety(y - 20)
        elif rand_dir == "right":
            turtle[i].setx(x + 20)
        else:
            turtle[i].setx(x - 20)
        y = turtle[i].ycor()
        x = turtle[i].xcor()
        if turtle[i].xcor() > 240 or turtle[i].xcor() < -240:
            turtle[i].goto(-turtle[i].xcor() , 0)
            move_count[i] = 0
        elif turtle[i].ycor() > 240 or turtle[i].ycor() < -240:
            turtle[i].goto(0, -turtle[i].ycor())
            move_count[i] = 0
        move_dir[i] = rand_dir
        move_count[i] += 1

#몸체 이동
def move_body(turtle, head):
    for i in range(len(turtle) - 1, 0, -1):
        x = turtle[i - 1].xcor()
        y = turtle[i - 1].ycor()
        turtle[i].goto(x, y)
    if len(turtle) > 0:
        x = head.xcor()
        y = head.ycor()
        turtle[0].goto(x, y)


#Init Screen
count_com_snake = 5
srn = turtle.Screen()
srn.title("Snake Game")
srn.setup(width=500, height=500)
srn.bgpic('tenor.gif')
srn.tracer(0)

#Input Level
t = turtle.Turtle()
Level = turtle.textinput("Level ", "1: easy 2: hard 3: hell")
Level = float(Level)
#Set count_com_snake, Life, Level
count_com_snake = 5
life = 5
Level = 0.1  * ((-Level + 3) * 0.25 + 1)
delay = Level
#Set Key
srn.listen()
srn.onkeypress(press_up, "w")
srn.onkeypress(press_down, "s")
srn.onkeypress(press_right, "d")
srn.onkeypress(press_left, "a")
#Set count_com_snakeboard
Scrboard = turtle.Turtle()
Scrboard.speed(0)
Scrboard.color("white")
Scrboard.penup()
Scrboard.direction = "stop"
Scrboard.hideturtle()
Scrboard.goto(0, 0)
Scrboard.clear()
Scrboard.write("Remain Snake {}, Life {}".format(count_com_snake, life), align="center", font=("Courier", 24, "normal"))

#Target (turtle)
target_turtle = turtle.Turtle()
target_turtle.speed(0)
target_turtle.shape("turtle")
target_turtle.color("red")
target_turtle.penup()
target_turtle.goto(0, 100)

#User_snake_head
user_head = turtle.Turtle()
user_head.speed(0)
user_head.shape("square")
user_head.color("blue")
user_head.penup()  # so that it doesn't draw anything
user_head.goto(0, 0)
user_head.direction = "stop"
user_body = []

#com_snake_
com_snakes=[]
com_body_list = [[],[],[],[],[]]
com_move_count=[0,0,0,0,0]
com_move_dir = [ "up", "down", "right","left","up"]

#com_snake_head
for i in range(5):
    com_head = turtle.Turtle()
    com_head.speed(0)
    com_head.shape("square")
    com_head.color("gray")
    com_head.penup()  # so that it doesn't draw anything
    com_head.goto(random.randint(-200, 200), random.randint(-200, 200))
    com_head.direction = "up"
    com_snakes.append(com_head)
    # com_snake_body
    for r in range(i+2):
        new_body = turtle.Turtle()
        new_body.speed(0)
        new_body.color("gray")
        new_body.penup()
        new_body.shape("circle")
        com_body_list[i].append(new_body)

#Play Game
while True:
    srn.update()
    # Move computer snake_head
    move_com_snake(com_snakes, com_move_dir, com_move_count)
    # Move computer snake_body
    for i in range(5):
        move_body(com_body_list[i], com_snakes[i])

    #Check eliminate target turtle
    if user_head.distance(target_turtle) < 20:
        x = random.randint(-240, 240)
        y = random.randint(-240, 240)
        target_turtle.goto(x, y)
        new_user_body = turtle.Turtle()
        new_user_body.speed(0)
        new_user_body.color("blue")
        new_user_body.penup()
        new_user_body.shape("square")
        user_body.append(new_user_body)
        # make the game faster
        delay -= 0.001

    #Move user snake_head
    move_body(user_body, user_head)
    move_user_snake()

    # Check the collision between User and Com Snakes
    for user_body_part in user_body:
        for i in range(5):
            for j in range(len(com_body_list[i])-1):
                if user_body_part.distance(com_body_list[i][j]) < 20:
                    #lose
                    if len(user_body) < len(com_body_list[i]):
                        time.sleep(1)
                        user_head.goto(0, 0)
                        user_head.direction = "stop"
                        for user_body_part in user_body:
                            user_body_part.goto(500, 500)
                        user_body.clear()
                        life -= 1
                        Scrboard.clear()
                        Scrboard.write("Remain Snake {}, Life {}".format(count_com_snake,life), align="center", font=("Courier", 24, "normal"))
                        # reset the delay
                        delay = Level
                        break
                    #win
                    else:
                        time.sleep(0.1)
                        com_snakes[i].goto(500, 500)
                        com_snakes[i].direction = "stop"
                        for j in range(len(com_body_list[i])):
                            com_body_list[i][j].goto(1000, 1000)  # hide all the previous user_body
                        com_body_list[i].clear()
                        count_com_snake -= 1
                        Scrboard.clear()
                        Scrboard.write("Remain Snake {}, Life {}".format(count_com_snake, life), align="center", font=("Courier", 24, "normal"))
                        break

    if life == 0:
        Scrboard.clear()
        Scrboard.write("Game Over", align="center", font=("Courier", 24, "normal"))
    if count_com_snake == 0:
        Scrboard.clear()
        Scrboard.write("Game Win", align="center", font=("Courier", 24, "normal"))
        user_head.pensize(30)
        user_head.penup()
        user_head.goto(-70,15)
        user_head.pendown()
        user_head.goto(70,15)
    time.sleep(delay)
srn.mainloop()  # startover