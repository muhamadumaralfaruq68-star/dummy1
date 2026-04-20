import turtle
import time
import random

# ajsha
# ----------------- PENGATURAN DASAR -----------------
wn = turtle.Screen()
wn.title("Snake 3 Level - Hard Mode")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

MOVE_PLAYER   = 20       # langkah player per tick
BORDER_LIMIT  = 280      # batas arena (hampir tepi window)
FOOD_SPEED    = 8        # kecepatan gerak makanan
FOOD_LIFETIME = 7        # detik sebelum makanan "bosan" dan pindah tempat
CHASE_DISTANCE = 120     # jarak pemicu musuh mulai mengejar
CHASE_TIME     = 3       # durasi musuh mengejar dalam detik

# ----------------- FUNGSI BANTU -----------------
def random_position():
    x = random.randint(-BORDER_LIMIT + 20, BORDER_LIMIT - 20)
    y = random.randint(-BORDER_LIMIT + 20, BORDER_LIMIT - 20)
    return x, y

# ----------------- PLAYER -----------------
player = turtle.Turtle()
player.speed(0)
player.shape("square")
player.color("lime")
player.penup()
player.goto(0, 0)
player.direction = "stop"

def go_up():
    if player.direction != "down":
        player.direction = "up"

def go_down():
    if player.direction != "up":
        player.direction = "down"

def go_left():
    if player.direction != "right":
        player.direction = "left"

def go_right():
    if player.direction != "left":
        player.direction = "right"

def move_player():
    x = player.xcor()
    y = player.ycor()

    if player.direction == "up":
        player.sety(y + MOVE_PLAYER)
    elif player.direction == "down":
        player.sety(y - MOVE_PLAYER)
    elif player.direction == "left":
        player.setx(x - MOVE_PLAYER)
    elif player.direction == "right":
        player.setx(x + MOVE_PLAYER)

# ----------------- FOOD (BERGERAK & MENGHILANG) -----------------
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()

def respawn_food():
    x, y = random_position()
    food.goto(x, y)
    # arah gerak acak: atas/bawah/kiri/kanan
    food.dx = random.choice([-FOOD_SPEED, FOOD_SPEED])
    food.dy = random.choice([-FOOD_SPEED, FOOD_SPEED])
    food.spawn_time = time.time()

respawn_food()

def move_food():
    # gerakkan food
    food.setx(food.xcor() + food.dx)
    food.sety(food.ycor() + food.dy)

    x, y = food.xcor(), food.ycor()

    # pantul di dinding
    if x > BORDER_LIMIT or x < -BORDER_LIMIT:
        food.dx *= -1
    if y > BORDER_LIMIT or y < -BORDER_LIMIT:
        food.dy *= -1

    # jika sudah terlalu lama tidak dimakan, pindah tempat
    if time.time() - food.spawn_time > FOOD_LIFETIME:
        respawn_food()

# ----------------- MUSUH -----------------
enemies = []

def create_enemy(step):
    e = turtle.Turtle()
    e.speed(0)
    e.shape("square")
    e.color("orange")
    e.penup()
    x, y = random_position()
    e.goto(x, y)

    e.step = step
    # kecepatan acak awal
    e.dx = random.choice([-step, step])
    e.dy = random.choice([-step, step])

    e.mode = "random"        # "random" atau "chase"
    e.chase_end_time = 0.0
    return e

def update_enemy(e):
    now = time.time()
    dist_to_player = e.distance(player)

    # aktifkan mode chase jika cukup dekat
    if e.mode == "random" and dist_to_player < CHASE_DISTANCE:
        e.mode = "chase"
        e.chase_end_time = now + CHASE_TIME

    # hentikan chase setelah 3 detik
    if e.mode == "chase" and now > e.chase_end_time:
        e.mode = "random"
        e.dx = random.choice([-e.step, e.step])
        e.dy = random.choice([-e.step, e.step])

    if e.mode == "random":
        # gerak acak + pantul dinding
        e.setx(e.xcor() + e.dx)
        e.sety(e.ycor() + e.dy)

        x, y = e.xcor(), e.ycor()
        if x > BORDER_LIMIT or x < -BORDER_LIMIT:
            e.dx *= -1
        if y > BORDER_LIMIT or y < -BORDER_LIMIT:
            e.dy *= -1

    elif e.mode == "chase":
        # gerak menuju player
        px, py = player.xcor(), player.ycor()
        ex, ey = e.xcor(), e.ycor()
        vx, vy = px - ex, py - ey
        dist = max((vx**2 + vy**2) ** 0.5, 0.01)
        e.setx(ex + e.step * vx / dist)
        e.sety(ey + e.step * vy / dist)

        # jangan keluar arena (dijepit di tepi)
        x, y = e.xcor(), e.ycor()
        if x > BORDER_LIMIT: e.setx(BORDER_LIMIT)
        if x < -BORDER_LIMIT: e.setx(-BORDER_LIMIT)
        if y > BORDER_LIMIT: e.sety(BORDER_LIMIT)
        if y < -BORDER_LIMIT: e.sety(-BORDER_LIMIT)

# ----------------- SKOR & LEVEL -----------------
score = 0
level = 1
delay = 0.14

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}  Level: {level}",
              align="center", font=("Courier", 16, "normal"))

update_scoreboard()

# ----------------- KONTROL KIBOR -----------------
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# ----------------- GAME LOOP -----------------
game_over = False

while not game_over:
    wn.update()

    move_player()
    move_food()

    # cek tabrakan dengan dinding
    if abs(player.xcor()) > BORDER_LIMIT or abs(player.ycor()) > BORDER_LIMIT:
        game_over = True
        break

    # cek makan makanan
    if player.distance(food) < 20:
        respawn_food()
        score += 1

        # naik level di skor 3 dan 6
        if score == 3:
            level = 2
            delay = 0.12           # sedikit lebih cepat
            enemies.append(create_enemy(step=14))  # 1 musuh

        elif score == 6:
            level = 3
            delay = 0.10
            enemies.append(create_enemy(step=18))  # musuh kedua lebih cepat

        update_scoreboard()

    # gerakkan musuh & cek tabrakan
    for e in enemies:
        update_enemy(e)
        if player.distance(e) < 20:
            game_over = True
            break

    # menang jika skor sudah 9 (3 level x 3 makanan)
    if score >= 9:
        game_over = True
        break

    time.sleep(delay)

# ----------------- PESAN AKHIR -----------------
pen.goto(0, 0)
if score >= 9:
    msg = "YOU WIN!"
else:
    msg = "GAME OVER"

pen.write(f"{msg}\nScore: {score}  Level: {level}",
          align="center", font=("Courier", 20, "bold"))

wn.mainloop()