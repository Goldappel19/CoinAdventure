import pgzrun
import random

WIDTH = 800
HEIGHT = 600

coins = 0
speed = 5
shop_open = False
frame = 0

# COOLDOWNS

cat_cooldown = 0
dog_cooldown = 0
snake_cooldown = 0

dog_active = False
dog_timer = 0

snake_active = False
snake_timer = 0

# PLAYER

player = Actor("player_idle")
player.pos = (100, 300)

# TREE

tree = Actor("tree")
tree.pos = (650, 300)

# SHOP

shop = Actor("shop")
shop.pos = (60, 50)

shop_background = Actor("shop_background")
shop_background.pos = (400, 300)

close_button = Actor("close")
close_button.pos = (560, 150)

buy_speed = Actor("buy_speed")
buy_speed.pos = (400, 140)

buy_cat = Actor("buy_cat")
buy_cat.pos = (400, 260)

buy_snake = Actor("buy_snake")
buy_snake.pos = (400, 360)

buy_dog = Actor("buy_dog")
buy_dog.pos = (400, 500)

# ABILITY BUTTONS

cat_button = Actor("cat_ability")
cat_button.pos = (620, 40)

dog_button = Actor("dog_ability")
dog_button.pos = (700, 40)

snake_button = Actor("snake_ability")
snake_button.pos = (780, 40)

# PETS

has_cat = False
has_dog = False
has_snake = False

cat = Actor("cat")
cat.pos = (100, 100)

dog = Actor("dog")
dog.pos = (-100, -100)

snake = Actor("snake")
snake.pos = (-100, -100)

cat_active = False
cat_target = None

# COINS

coins_on_map = []

for i in range(3):

    c = Actor("coin")

    c.pos = (
        random.randint(100, 700),
        random.randint(100, 500)
    )

    coins_on_map.append(c)


def respawn_coin(c):

    c.pos = (
        random.randint(100, 700),
        random.randint(100, 500)
    )


def update():

    global frame
    global coins

    global cat_cooldown
    global dog_cooldown
    global snake_cooldown

    global dog_active
    global dog_timer

    global snake_active
    global snake_timer

    global cat_active
    global cat_target

    # COOLDOWNS

    if cat_cooldown > 0:
        cat_cooldown -= 1

    if dog_cooldown > 0:
        dog_cooldown -= 1

    if snake_cooldown > 0:
        snake_cooldown -= 1

    if dog_active:

        dog_timer -= 1

        if dog_timer <= 0:
            dog_active = False

    if snake_active:

        snake_timer -= 1

        if snake_timer <= 0:
            snake_active = False

    if not shop_open:

        old_x = player.x
        old_y = player.y

        moving = False

        if keyboard.right:

            player.x += speed
            moving = True

            frame += 0.15

            if int(frame) % 2 == 0:
                player.image = "player_right1"
            else:
                player.image = "player_right2"

        elif keyboard.left:

            player.x -= speed
            moving = True

            frame += 0.15

            if int(frame) % 2 == 0:
                player.image = "player_left1"
            else:
                player.image = "player_left2"

        if keyboard.up:
            player.y -= speed
            moving = True

        if keyboard.down:
            player.y += speed
            moving = True

        if not moving:
            player.image = "player_idle"

        player.x = max(20, min(WIDTH - 20, player.x))
        player.y = max(20, min(HEIGHT - 20, player.y))

        player_box = Rect(
            (player.x - 20, player.y - 20),
            (40, 40)
        )

        tree_box = Rect(
            (tree.x - 50, tree.y - 50),
            (100, 100)
        )

        if player_box.colliderect(tree_box):
            player.x = old_x
            player.y = old_y

        if has_dog:

            dog.x += (player.x - 40 - dog.x) * 0.08
            dog.y += (player.y + 40 - dog.y) * 0.08

        if has_snake:

            snake.x += (player.x + 40 - snake.x) * 0.08
            snake.y += (player.y + 40 - snake.y) * 0.08


            # CAT ABILITY

        if has_cat:

            if cat_active and cat_target:

                cat.x += (cat_target.x - cat.x) * 0.15
                cat.y += (cat_target.y - cat.y) * 0.15

                if cat.distance_to(cat_target) < 20:

                    coins += 1

                    respawn_coin(cat_target)

                    cat_active = False
                    cat_target = None

            else:

                cat.x += (player.x - cat.x) * 0.08
                cat.y += (player.y - cat.y) * 0.08

        active_coins = 3 if dog_active else 1

        for c in coins_on_map[:active_coins]:

            if snake_active:

                c.x += (player.x - c.x) * 0.01
                c.y += (player.y - c.y) * 0.01

            coin_box = Rect(
                (c.x - 10, c.y - 10),
                (20, 20)
            )

            if player_box.colliderect(coin_box):

                reward = 3 if snake_active else 1

                coins += reward

                respawn_coin(c)


def on_mouse_down(pos):

    global coins
    global speed
    global shop_open

    global has_cat
    global has_dog
    global has_snake

    global cat_active
    global cat_target

    global cat_cooldown
    global dog_cooldown
    global snake_cooldown

    global dog_active
    global dog_timer

    global snake_active
    global snake_timer

    # CAT ABILITY

    if has_cat and cat_button.collidepoint(pos):

        if cat_cooldown <= 0:

            cat_target = random.choice(coins_on_map)

            cat_active = True

            cat_cooldown = 60 * 5

    # DOG ABILITY

    if has_dog and dog_button.collidepoint(pos):

        if dog_cooldown <= 0:

            dog_active = True

            dog_timer = 60 * 5

            dog_cooldown = 60 * 10

    # SNAKE ABILITY

    if has_snake and snake_button.collidepoint(pos):

        if snake_cooldown <= 0:

            snake_active = True

            snake_timer = 60 * 5

            snake_cooldown = 60 * 15

    # SHOP

    if shop.collidepoint(pos):
        shop_open = True
        return

    if not shop_open:
        return

    if close_button.collidepoint(pos):
        shop_open = False
        return

    if buy_speed.collidepoint(pos):

        if coins >= 5:
            coins -= 5
            speed += 2

    if buy_cat.collidepoint(pos):

        if coins >= 10 and not has_cat:
            coins -= 10
            has_cat = True

    if buy_dog.collidepoint(pos):

        if coins >= 25 and not has_dog:
            coins -= 25
            has_dog = True

    if buy_snake.collidepoint(pos):

        if coins >= 50 and not has_snake:
            coins -= 50
            has_snake = True


def draw():

    screen.fill((100, 200, 255))

    tree.draw()

    active_coins = 3 if dog_active else 1

    for c in coins_on_map[:active_coins]:
        c.draw()

    if has_cat:
        cat.draw()

    if has_dog:
        dog.draw()

    if has_snake:
        snake.draw()

    player.draw()

    shop.draw()

    screen.draw.text(
        f"Coins: {coins}",
        (10, 70),
        fontsize=40,
        color="black"
    )

    screen.draw.text(
        f"Speed: {speed}",
        (10, 120),
        fontsize=30,
        color="black"
    )

    if has_cat:
        cat_button.draw()
        screen.draw.text(
            str(cat_cooldown // 60),
            (610, 80),
            color="white"
        )

    if has_dog:
        dog_button.draw()
        screen.draw.text(
            str(dog_cooldown // 60),
            (690, 80),
            color="white"
        )

    if has_snake:
        snake_button.draw()
        screen.draw.text(
            str(snake_cooldown // 60),
            (770, 80),
            color="white"
        )

    if shop_open:

        shop_background.draw()

        buy_speed.draw()
        buy_cat.draw()
        buy_dog.draw()
        buy_snake.draw()

        close_button.draw()


pgzrun.go()
