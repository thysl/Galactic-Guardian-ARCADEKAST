import time
import random
import pygame
import math

# Force field maken voor lasers zodat de lasers van enemy sneller weggehaald worden zodat het makkelijker is om de lasers van enemy te raken, en dus te overleven
# Get_distance functie is er al, alleen nog inplementeren in de shop en in control_laser

# Difficulty settings
minimum_spawn_interval = 0.5
maximum_enemy_speed = 10
maximum_shooting_chance = 70

maximum_spawn_interval = 5
minimum_enemy_speed = 1
minimum_shooting_chance = 120

spawn_interval = int
shooting_chance = int

# Shop
firing_rate_price = 5
ammo_price = 10
speed_price = 10
fire_power_price = 10
strong_laser_price = 10
magnet_laser_price = 10

lmb_down = False

global game_over
global paused
global shopping
game_over = False
paused = False
shopping = False

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.display.init()
pygame.key.set_repeat(1000)

interval = 1000
stopwatch_s = 0
stopwatch = 0
executed = False
score = 0

# Display
width = 700
height = 700
display = pygame.display.set_mode((700, 700))
pygame.display.set_caption('Galactic Guardian')
background_colour = (18, 25, 38)
display.fill(background_colour)

# Spaceship
ammo = 5
fire_interval = 5
curr_speed_x = 0
curr_speed_y = 0
accel = 1
deccel = 1
speed = 10
spaceship_width = 50
spaceship_height = 50
spaceship_img = pygame.image.load('assets/spaceship.png')
spaceship_img = pygame.transform.scale(spaceship_img, (spaceship_width, spaceship_height))
display.blit(spaceship_img, (width, height))
global spaceship_x
global spaceship_y
spaceship_x = width / 2 - spaceship_width / 2
spaceship_y = 400

# Enemy
enemy_speed = 2
enemy_width = 50
enemy_height = 50
enemy_img = pygame.image.load('assets/enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
enemy_img = pygame.transform.rotate(enemy_img, 180)
enemies = []

# Laser
strong_laser = False
magnet_laser = 0
laser_width = 5
laser_height = 15
laser_speed = 10
laser_img = pygame.image.load('assets/laser.png')
laser_img = pygame.transform.scale(laser_img, (laser_width, laser_height))
lasers = []
global timeout
timeout = 60

# Enemy laser
enemy_laser_width = 5
enemy_laser_height = 15
enemy_laser_speed = 5
enemy_laser_img = pygame.image.load('assets/enemy_laser.png')
enemy_laser_img = pygame.transform.scale(enemy_laser_img, (enemy_laser_width, enemy_laser_height))
enemy_lasers = []

# Sounds
explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
laser_sound = pygame.mixer.Sound('assets/sounds/laser.wav')
powerup_sound = pygame.mixer.Sound('assets/sounds/powerup.wav')
click_sound = pygame.mixer.Sound('assets/sounds/click.wav')
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')
enemy_laser_sound = pygame.mixer.Sound('assets/sounds/enemy_laser.wav')

main_theme_music = pygame.mixer.music.load('assets/sounds/music/main_theme.wav')

# GUI
game_over_img = pygame.image.load('assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (500, 125))

play_again_img = pygame.image.load('assets/play_again.png')
play_again_img = pygame.transform.scale(play_again_img, (300, 75))

shop_icon_img = pygame.image.load('assets/shop_icon.png')
shop_icon_img = pygame.transform.scale(shop_icon_img, (50, 50))

pause_button_img = pygame.image.load('assets/pause_icon.png')
pause_button_img = pygame.transform.scale(pause_button_img, (50, 50))

play_button_img = pygame.image.load('assets/play.png')
play_button_img = pygame.transform.scale(play_button_img, (225, 75))

buy_button_img = pygame.image.load('assets/buy.png')
buy_button_img = pygame.transform.scale(buy_button_img, (75, 37.5))

cant_buy_button_img = pygame.image.load('assets/cant_buy.png')
cant_buy_button_img = pygame.transform.scale(cant_buy_button_img, (75, 37.5))

continue_button_img = pygame.image.load('assets/continue.png')
continue_button_img = pygame.transform.scale(continue_button_img, (300, 75))




# Animations
def create_gif_list(name, amount_frames, name_folder, dimensions):
    globals()[name] = []
    for i in range(amount_frames):
        i += 1
        image = pygame.image.load(f'assets/gifs/{name_folder}/{i}.png')
        image = pygame.transform.scale(image, (dimensions))
        globals()[name].append(image)

def add_explosion(pos):
    explosions.append(((pos), 0, 1))

def animate_explosion():
    for explosion in explosions:
        index = explosions.index(explosion)
        pos = explosion[0]
        frame_counter = explosion[1]
        image_counter = explosion[2]

        frame_counter += 1
        if frame_counter >= 3:
            image_counter += 1
            frame_counter = 0
        if image_counter >= 11:
            del explosions[index]
            return None
        image = explosion_gif[image_counter]
        display.blit(image, pos)

        explosions[index] = ((pos), frame_counter, image_counter)

explosions = []
create_gif_list('explosion_gif', 11, 'explosion', (50, 50))
explosion_gif.reverse()



# Event checks
def check_collision(obj, obj1, obj_width, obj_height, obj1_width, obj1_height):
    collision = False
    x_range = range(int(obj[0]), int(obj[0]) + obj_width)
    y_range = range(int(obj[1]), int(obj[1]) + obj_height)
    x_range1 = range(int(obj1[0]), int(obj1[0]) + obj1_width)
    y_range1 = range(int(obj1[1]), int(obj1[1]) + obj1_height)

    for i in x_range:
        for n in y_range:
            if i in x_range1 and n in y_range1:
                collision = True
                return collision
    return collision

def check_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
            lmb_down = True
        else:
            lmb_down = False

def check_keys():
    global timeout
    global score
    keys = pygame.key.get_pressed()
    global spaceship_x
    global spaceship_y
    global accel
    global deccel
    global curr_speed_x
    global curr_speed_y
    global strong_laser_price
    global strong_laser
    if keys[pygame.K_c] and keys[pygame.K_EQUALS]:
        score += 10
        time.sleep(0.1)
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and curr_speed_x >= -speed: #and spaceship_x >= speed and curr_speed_x >= -speed:
        curr_speed_x -= accel
    elif curr_speed_x < 0:
        curr_speed_x += deccel
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and curr_speed_x <= speed: #and spaceship_x <= width - spaceship_width - speed and curr_speed_x <= speed:
        curr_speed_x += accel
    elif curr_speed_x > 0:
        curr_speed_x -= deccel
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and curr_speed_y >= -speed: #and spaceship_y >= speed and curr_speed_y >= -speed:
        curr_speed_y -= accel
    elif curr_speed_y < 0:
        curr_speed_y += deccel
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and curr_speed_y <= speed: #and spaceship_y <= height - spaceship_height - speed and curr_speed_y <= speed:
        curr_speed_y += accel
    elif curr_speed_y > 0:
        curr_speed_y -= deccel

    if (keys[pygame.K_q] or keys[pygame.K_e] or keys[pygame.K_r] or keys[pygame.K_z] or keys[pygame.K_x] or keys[pygame.K_c]) and timeout >= fire_interval and len(lasers) < ammo:
        timeout = 0
        create_laser()
    timeout += 1

    if (curr_speed_x > 0 and spaceship_x <= width - spaceship_width - curr_speed_x) or (curr_speed_x < 0 and spaceship_x >= abs(curr_speed_x)):
        spaceship_x += round(curr_speed_x, 0)
    elif spaceship_x < width / 2 and curr_speed_x != 0:
        spaceship_x = 0
    elif spaceship_x > width / 2 and curr_speed_x != 0:
        spaceship_x = width - spaceship_width
        
    if (curr_speed_y > 0 and spaceship_y <= height - spaceship_height - curr_speed_y) or (curr_speed_y < 0 and spaceship_y >= abs(curr_speed_y)):
        spaceship_y += round(curr_speed_y, 0)
    elif spaceship_y < height / 2 and curr_speed_y != 0:
        spaceship_y = 0
    elif spaceship_y > height / 2 and curr_speed_y != 0:
        spaceship_y = height - spaceship_height 

def get_distance(pos1, pos2, obj1, obj2):
    width1 = pygame.Surface.get_width(obj1)
    height1 = pygame.Surface.get_height(obj1)
    width2 = pygame.Surface.get_width(obj2)
    height2 = pygame.Surface.get_height(obj2)

    pos1 = pos1[0] + width1 / 2, pos1[1]
    pos1 = pos1[0], pos1[1] + height1 / 2

    pos2 = pos2[0] + width2 / 2, pos2[1]
    pos2 = pos2[0], pos2[1] + height2 / 2

    delta_x = abs(pos1[0] - pos2[0])
    delta_y = abs(pos1[1] - pos2[1])
    dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
    return dist

def surface_clicked(image, place, centered):
    global mouse_buttons_pressed
    try:
        width = pygame.Surface.get_width(image)
        height = pygame.Surface.get_height(image)
    except:
        width = image[0]
        height = image[1]
    if centered:
        x = int(place[0] - width / 2)
        y = int(place[1] - height / 2)
    else:
        x = int(place[0])
        y = int(place[1])
    pos = pygame.mouse.get_pos()
    mouse_buttons_pressed = pygame.mouse.get_pressed()
    in_range = pos[0] in range(x, x + width) and pos[1] in range(y, y + height)
    lmb_down = mouse_buttons_pressed[0]
    if in_range and mouse_buttons_pressed[0]:
        return True
    else:
        return False

def update_mouse():
    mouse_buttons_pressed = pygame.mouse.get_pressed()



# Create
def create_enemy():
    enemy_speed = score
    x_coord = random.randint(0, width - enemy_width)
    enemies.append((x_coord, -50))

def create_laser():
    global lasers
    pygame.mixer.Sound.play(laser_sound)
    lasers.append((spaceship_x + spaceship_width / 2 - laser_width / 2, spaceship_y - laser_height))

def create_enemy_laser(enemy):
    global enemy_lasers
    enemy_x = enemy[0]
    enemy_y = enemy[1]
    pygame.mixer.Sound.play(enemy_laser_sound)
    enemy_lasers.append((enemy_x + enemy_width / 2 - enemy_laser_width / 2, enemy_y + enemy_height + enemy_laser_speed))


# Control
def control_enemy():
    global score
    global game_over
    for enemy in enemies:
        index = enemies.index(enemy)
        display.blit(enemy_img, enemy)
        if random.randint(0, round(int(shooting_chance), 0)) == 0:
            create_enemy_laser(enemy)
        enemies[index] = (enemy[0], enemy[1] + enemy_speed)
        if (enemy[1] > 700):
            del enemies[index]
            score -= 1
        
        if check_collision(enemy, (spaceship_x, spaceship_y), enemy_width, enemy_height, spaceship_width, spaceship_height):
            game_over = True

def control_laser():
    broke = False
    global score
    global magnet_laser
    for laser in lasers:
        broke = False
        index = lasers.index(laser)
        if (laser[1] < 0 - laser_height):
            del lasers[index]
            broke = True
        else:
            if len(enemies) > 0 and not broke:
                for enemy in enemies:
                    if check_collision(laser, enemy, laser_width, laser_height, enemy_width, enemy_height):
                        enemies.remove(enemy)
                        score += 1
                        add_explosion(center_image(explosion_gif[0], (enemy[0] + enemy_width / 2, enemy[1] + enemy_height / 2)))
                        pygame.mixer.stop()
                        pygame.mixer.Sound.play(explosion_sound)
                        del lasers[index]
                        broke = True
                for enemy_laser in enemy_lasers:
                    if check_collision(laser, enemy_laser, laser_width, laser_height, enemy_laser_width, enemy_laser_height):
                        enemy_lasers.remove(enemy_laser)
                        if not strong_laser:
                            del lasers[index]
                            broke = True
                    elif (magnet_laser > 0 and get_distance(laser, enemy_laser, laser_img, enemy_laser_img) <= magnet_laser) and not broke:
                        enemy_lasers.remove(enemy_laser)
                        if not strong_laser:
                            del lasers[index]
                            broke = True
        if not broke:
            lasers[index] = (laser[0], laser[1] - laser_speed)
            display.blit(laser_img, laser)

def control_enemy_laser():
    for enemy_laser in enemy_lasers:
        broke = False
        index = enemy_lasers.index(enemy_laser)
        if (enemy_laser[1] > 700):
            del enemy_lasers[index]
            broke = True
        elif not broke:
            if check_collision(enemy_laser, (spaceship_x, spaceship_y), enemy_laser_width, enemy_laser_height, spaceship_width, spaceship_height):
                enemy_lasers.remove(enemy_laser)
                pygame.mixer.stop()
                pygame.mixer.Sound.play(explosion_sound)
                pygame.mixer.Sound.play(game_over_sound)
                global game_over
                game_over = True
                return None
            elif len(enemies) > 0 and not broke:
                for enemy in enemies:
                    if check_collision(enemy_laser, enemy, enemy_laser_width, enemy_laser_height, enemy_width, enemy_height):
                        enemies.remove(enemy)
                        add_explosion(center_image(explosion_gif[0], (enemy[0] + enemy_width / 2, enemy[1] + enemy_height / 2)))
                        pygame.mixer.stop()
                        pygame.mixer.Sound.play(explosion_sound)
                        del enemy_lasers[index]
                        broke = True
        if not broke:
            enemy_lasers[index] = (enemy_laser[0], enemy_laser[1] + enemy_laser_speed)
            display.blit(enemy_laser_img, enemy_laser)

def control_difficulty():
    global spawn_interval
    global enemy_speed
    global enemy_laser_speed
    global shooting_chance
    global difficulty_percentage
    global ammo
    old_shooting_chance = shooting_chance

    spawn_interval = round(-0.03 * score + 3, 1)
    if spawn_interval <= minimum_spawn_interval:
        spawn_interval = minimum_spawn_interval
    elif spawn_interval >= maximum_spawn_interval:
        spawn_interval = maximum_spawn_interval

    enemy_speed = round(0.05 * score + 2, 1)
    if enemy_speed >= maximum_enemy_speed:
        enemy_speed = maximum_enemy_speed
    elif enemy_speed <= minimum_enemy_speed:
        enemy_speed = minimum_enemy_speed
    enemy_laser_speed = enemy_speed + 3

    shooting_chance = round(-0.3 * score + 100, 1)
    if shooting_chance <= maximum_shooting_chance:
        shooting_chance = maximum_shooting_chance
    elif shooting_chance >= minimum_shooting_chance:
        shooting_chance = minimum_shooting_chance
    
    ammo = round(5 + (-1 * spawn_interval + 3))

    spawn_interval_percentage = minimum_spawn_interval / spawn_interval * 100
    enemy_speed_percentage = enemy_speed / maximum_enemy_speed * 100
    shooting_chance_percentage = maximum_shooting_chance / shooting_chance * 100

    difficulty_percentage = round((spawn_interval_percentage + enemy_speed_percentage + shooting_chance_percentage) / 3, 1)
    
    if old_shooting_chance != shooting_chance:
        print('Spawn interval: ', spawn_interval, ' Enemy speed: ', enemy_speed, ' Shooting chance: 1:' + str(shooting_chance))


# Graphics

# Display text            
def display_text(text, place, size, centered):
    font = pygame.font.SysFont('pixel emulator', size)
    text = font.render(text, True, (255, 255, 255))
    if centered:
        text_width = pygame.Surface.get_width(text)
        text_height = pygame.Surface.get_height(text)
        place = (place[0] - text_width / 2, place[1] - text_height / 2)
    display.blit(text, (place))


# Draw screen
def draw_screen():
    display.fill((18, 25, 36))
    display_text('Difficulty: ' + str(difficulty_percentage) + '%', (10, 5), 20, False)
    display_text('Score: ' + str(score), (10, 25), 20, False)
    display_text('Ammo: ' + str(ammo - len(lasers)), (10, 665), 20, False)
    # display.blit(pause_button_img, center_image(pause_button_img, (663.5, 37.5)))
    # display.blit(shop_icon_img, center_image(shop_icon_img, (663.5, 100)))

    control_enemy()
    control_laser()
    control_enemy_laser()
    display.blit(spaceship_img, (spaceship_x, spaceship_y))

# Center image
def center_image(image, place):
    width = pygame.Surface.get_width(image)
    height = pygame.Surface.get_height(image)
    place = (place[0] - width / 2, place[1] - height / 2)
    return ((place))

# Draw shop
def create_shop():
    global score
    global fire_interval
    global firing_rate_price
    global shopping
    global speed
    global accel
    global deccel
    global laser_speed
    global laser_width
    global strong_laser
    global laser_img
    global magnet_laser
    pygame.mixer.music.pause()
    def draw():
        display.fill(background_colour)
        display_text('Points: ' + str(score), (10, 10), 20, False)
        display_text('SHOP', (350, 40), 60, True)
        display.blit(continue_button_img, center_image(continue_button_img, (350, 600)))

        display_text('Firing Rate __ ' + str(firing_rate_price) + ' pts', (50, 100), 30, False)
        display_text('Fire Power ___ ' + str(fire_power_price) + ' pts', (50, 150), 30, False)
        display_text('Magnet Laser _ ' + str(magnet_laser_price) + ' pts', (50, 200), 30, False)
        
        display_text('Speed ________ ' + str(speed_price) + ' pts', (50, 300), 30, False)

        if type(firing_rate_price) == int and score >= firing_rate_price:
            display.blit(buy_button_img, (575, 100))
        elif type(firing_rate_price) == int and score < firing_rate_price:
            display.blit(cant_buy_button_img, (575, 100))

        if type(fire_power_price) == int and score >= fire_power_price:
            display.blit(buy_button_img, (575, 150))
        elif type(fire_power_price) == int and score < fire_power_price:
            display.blit(cant_buy_button_img, (575, 150))

        if type(magnet_laser_price) == int and score >= magnet_laser_price:
            display.blit(buy_button_img, (575, 200))
        elif type(magnet_laser_price) == int and score < magnet_laser_price:
            display.blit(cant_buy_button_img, (575, 200))


        if type(speed_price) == int and score >= speed_price:
            display.blit(buy_button_img, (575, 300))
        elif type(speed_price) == int and score < speed_price:
            display.blit(cant_buy_button_img, (575, 300))

        pygame.display.flip()
        
    def set_prices():
        global firing_rate_price
        global ammo_price
        global speed_price
        global fire_power_price
        global strong_laser
        global magnet_laser_price

        if fire_interval == 3:
            firing_rate_price = 'n/a'
        elif fire_interval == 4:
            firing_rate_price = 20
        elif fire_interval == 5:
            firing_rate_price = 10
        
        if laser_speed == 15:
            fire_power_price = 'n/a'
        elif laser_speed == 10:
            fire_power_price = 20
        
        if magnet_laser == 50:
            magnet_laser_price = 'n/a'
        elif magnet_laser == 25:
            magnet_laser_price = 20
        elif magnet_laser == 0:
            magnet_laser_price = 10


        if speed == 15:
            speed_price = 'n/a'
        elif speed == 10:
            speed_price = 10

    while shopping:
        clock.tick(60)
        check_events()

        # Continue button
        if surface_clicked(continue_button_img, (350, 600), True):
            pygame.mixer.stop()
            pygame.mixer.Sound.play(click_sound)
            pygame.mixer.music.unpause()
            shopping = False

        set_prices()        
        draw()

        # Check buy buttons
        if type(firing_rate_price) == int:
            if surface_clicked(buy_button_img, (550, 100), False) and score >= firing_rate_price and fire_interval > 2:
                score -= firing_rate_price
                fire_interval -= 1
                pygame.mixer.Sound.play(powerup_sound)
                set_prices()
                draw()
                time.sleep(0.5)
                update_mouse()
        
        if type(fire_power_price) == int:
            if surface_clicked(buy_button_img, (550, 150), False) and score >= fire_power_price and laser_speed < 15:
                score -= fire_power_price
                laser_speed += 5
                strong_laser = True
                laser_width = 10
                laser_img = pygame.image.load('assets/laser.png')
                laser_img = pygame.transform.scale(laser_img, (laser_width, laser_height))
                pygame.mixer.Sound.play(powerup_sound)
                set_prices()
                draw()
                time.sleep(0.5)
                update_mouse()

        if type(magnet_laser_price) == int:
            if surface_clicked(buy_button_img, (550, 200), False) and score >= magnet_laser_price and magnet_laser < 50:
                score -= magnet_laser_price
                magnet_laser += 25
                pygame.mixer.Sound.play(powerup_sound)
                set_prices()
                draw()
                time.sleep(0.5)
                update_mouse()


        if type(speed_price) == int:
            if surface_clicked(buy_button_img, (550, 300), False) and score >= speed_price and speed < 15:
                score -= speed_price
                speed += 5
                accel += 1
                deccel += 1
                pygame.mixer.Sound.play(powerup_sound)
                set_prices()
                draw()
                time.sleep(0.5)
                update_mouse()

# Stopwatch functions
def stopwatch_func():
    global stopwatch_s
    global stopwatch
    stopwatch += 1000 / 60 / 1000
    stopwatch_s = round(stopwatch, 3)

def every_x_seconds(seconds, action):
    global stopwatch_s
    global executed
    if round(stopwatch_s % seconds, 1) == 0 and not executed:
        exec(action)
        executed = True
    elif round(stopwatch % seconds, 1) != 0:
        executed = False

def check_mouse_buttons():
    if pygame.mouse.get_pressed()[0]:
        lmb_down = True
    else:
        lmb_down = False

def main_game_loop():
    global paused
    global shopping
    global game_over
    control_difficulty()
    check_events()
    draw_screen()
    animate_explosion()
    check_keys()

    every_x_seconds(spawn_interval, 'create_enemy()')

    stopwatch_func()
    pygame.display.flip()
    if surface_clicked(pause_button_img, (663.5, 37.5), True):
        pygame.mixer.stop()
        pygame.mixer.Sound.play(click_sound)
        paused = True
        return None
    if surface_clicked(shop_icon_img, (663.5, 100), True):
        pygame.mixer.stop()
        pygame.mixer.Sound.play(click_sound)
        shopping = True
        return None

    clock.tick(60)

#while True:
#    create_shop()
#    check_events()
#    clock.tick(60)
#quit()

# global game_over
# global paused
# global shopping
# global enemies
# global enemy_lasers
# global lasers
# global laser_img
# global spaceship_x
# global spaceship_y
# global score
# global curr_speed_x
# global curr_speed_y
# global fire_interval
# global ammo
# global explosions
# global speed
# global accel
# global deccel
# global laser_speed
# global strong_laser
# global laser_width
# global magnet_laser

pygame.mixer.music.play(-1)
while True:
    while not game_over and not paused and not shopping:
        main_game_loop()
        check_mouse_buttons()

    curr_speed_x = 0
    curr_speed_y = 0

    if paused:
        pygame.mixer.music.pause()
        display_text('PAUSED', (350, 250), 75, True)
        display.blit(continue_button_img, center_image(continue_button_img, (350, 375)))
        pygame.display.flip()
    
    while paused:
        check_events()
        clock.tick(60)
        if surface_clicked(continue_button_img, (350, 375), True):
            pygame.mixer.stop()
            pygame.mixer.Sound.play(click_sound)
            pygame.mixer.music.unpause()
            paused = False

    while shopping:
        create_shop()


    if game_over:
        pygame.mixer.music.stop()
        display.fill(background_colour)
        display_text('GAME OVER', (350, 250), 75, True)
        display.blit(play_again_img, center_image(play_again_img, (350, 375)))
        pygame.display.flip()

    while game_over:
        check_events()
        clock.tick(60)
        if (surface_clicked(play_again_img, (350, 375), True)):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(click_sound)
            game_over = False

            spaceship_x = width / 2 - spaceship_width / 2
            spaceship_y = 400
            score = 0
            lasers = []
            enemies = []
            enemy_lasers = []
            curr_speed_x = 0
            curr_speed_y = 0
            fire_interval = 5
            ammo = 5
            explosions = []
            pygame.mixer.music.play(-1)
            speed = 10
            accel = 1
            deccel = 1
            laser_speed = 10
            strong_laser = False
            laser_width = 5
            laser_img = pygame.image.load('assets/laser.png')
            laser_img = pygame.transform.scale(laser_img, (laser_width, laser_height))
            magnet_laser = 0