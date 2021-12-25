import pygame
import random
import os

pygame.init()

WIDTH = 1000
HEIGHT = 750


fps = 100
clock = pygame.time.Clock()


display = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption("Лягуха прыгуха :)")
pygame.mixer.music.load('data/fonpesn.mp3')
pygame.mixer.music.set_volume(0.3)


# jumpzv = pygame.mixer.Sound('data/prig.wav')
# prizemzv = pygame.mixer.Sound('data/priz.wav')
# poterserd = pygame.mixer.Sound('data/serdmin.wav')
# proigral = pygame.mixer.Sound('data/proigral.wav')
# plusserd = pygame.mixer.Sound('data/plusserd.wav')
# click = pygame.mixer.Sound('data/click.wav')


ikonka = pygame.image.load("data/lyag0.png")
pygame.display.set_icon(ikonka)


cac_im = [pygame.image.load("data/Cactus0.png"), pygame.image.load("data/Cactus1.png"),
          pygame.image.load("data/Cactus2.png")]
cac_opt = [69, 573, 37, 534, 40, 544]



pers_im = [pygame.image.load("data/lyag2.png"), pygame.image.load("data/lyag1.png"),
           pygame.image.load("data/lyag0.png")]
im_counter = 0

stone_im = [pygame.image.load("data/Stone0.png"), pygame.image.load("data/Stone1.png")]

cloud_im = [pygame.image.load("data/Cloud0.png"), pygame.image.load("data/Cloud1.png")]

scores = 0
max_score = 0


max_cact = 0
nad_cactus = False


health = 2
health_im = pygame.image.load('data/serd.png')
health_im = pygame.transform.scale(health_im, (30, 30))


def s_men():
    men_im = pygame.image.load("data/fon.jpg")
    show = True

    start_b = Button(260, 70)

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(men_im, (0, 0))
        start_b.draw(350, 400, "ПЕРЕЙТИ В ИГРУ!", s_game, 50)

        pygame.display.update()
        clock.tick(60)


def s_game():
    global scores, m_jump, c_jump, user_y, health
    while game_1():
        scores = 0
        m_jump = False
        c_jump = 30
        user_y = HEIGHT - user_HEIGHT - 126
        health = 2


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:

            return False

    def ret_self(self, rad, y, width, image):
        self.x = rad
        self.y = y
        self.width = width
        self.image = image

        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.active_clr = (0, 200, 0)
        self.noactive_clr = (0, 100, 0)

    def draw(self, x, y, message, action=None, fon_size=30):
        mouse = pygame.mouse.get_pos()
        clicknul = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_clr, (x, y, self.width, self.height))
            if clicknul[0] == 1:
                # pygame.mixer.Sound.play(click)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.noactive_clr, (x, y, self.width, self.height))

        p_text(message, x + 10, x + 60)


user_WIDTH = 70
user_HEIGHT = 60

user_x = WIDTH // 4
user_y = HEIGHT - user_HEIGHT - 126

m_jump = False
c_jump = 30

cac_WIDTH = 25
cac_HEIGHT = 80

cac_x = WIDTH - 40
cac_y = HEIGHT - cac_HEIGHT - 80


def game_1():
    global m_jump
    pygame.mixer.music.play(-1)

    game = True
    cac_array = []
    create_cac_arr(cac_array)
    land = pygame.image.load("data/Land.png")

    stone, cloud = open_r()
    heart = Object(WIDTH, 460, 30, health_im, 4)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            m_jump = True

        if keys[pygame.K_ESCAPE] or keys[pygame.K_PAUSE]:
            pause()

        if m_jump:
            jump()

        if check_colid(cac_array):
            game = False

        count_sc(cac_array)

        display.blit(land, (0, 0))
        p_text("Score: " + str(scores), 800, 10)

        heart.move()
        plus_h(heart)
        show_health()

        draw_array(cac_array)
        move_ob(stone, cloud)

        d_lyag()

        pygame.display.update()
        clock.tick(fps)
    return u_game_over()


def jump():
    global user_y, m_jump, c_jump
    if c_jump >= -30:
        if c_jump == 30:
            pass
        # pygame.mixer.Sound.play(jumpzv)
        if c_jump == -30:
            pass
        # pygame.mixer.Sound.play(prizemzv)
        user_y -= c_jump / 2.5
        c_jump -= 1
    else:
        c_jump = 30
        m_jump = False


def create_cac_arr(array):
    choice = random.randrange(0, 3)
    image = cac_im[choice]
    width = cac_opt[choice * 2]
    height = cac_opt[choice * 2 + 1]
    array.append(Object(WIDTH + 50, height, width, image, 4))

    choice = random.randrange(0, 3)
    image = cac_im[choice]
    width = cac_opt[choice * 2]
    height = cac_opt[choice * 2 + 1]
    array.append(Object(WIDTH + 300, height, width, image, 4))

    choice = random.randrange(0, 3)
    image = cac_im[choice]
    width = cac_opt[choice * 2]
    height = cac_opt[choice * 2 + 1]
    array.append(Object(WIDTH + 600, height, width, image, 4))


def find_rad(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < WIDTH:
        rad = WIDTH
        if rad - maximum < 50:
            rad += 250
    else:
        rad = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        rad += random.randrange(10, 15)
    else:
        rad += random.randrange(200, 350)

    return rad


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            rad = find_rad(array)
            choice = random.randrange(0, 3)
            image = cac_im[choice]
            width = cac_opt[choice * 2]
            height = cac_opt[choice * 2 + 1]

            cactus.ret_self(rad, height, width, image)


def obj_return(objects, obj):
    rad = find_rad(objects)
    choice = random.randrange(0, 3)
    image = cac_im[choice]
    width = cac_opt[choice * 2]
    height = cac_opt[choice * 2 + 1]

    obj.ret_self(rad, height, width, image)


def open_r():
    choice = random.randrange(0, 2)
    im_s = stone_im[choice]

    choice = random.randrange(0, 2)
    im_c = cloud_im[choice]

    stone = Object(WIDTH, HEIGHT - 80, 10, im_s, 5)
    cloud = Object(WIDTH, 80, 80, im_c, 3)

    return cloud, stone


def move_ob(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        im_s = stone_im[choice]
        stone.ret_self(WIDTH, 700 + random.randrange(10, 60), stone.width, im_s)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        im_c = cloud_im[choice]
        cloud.ret_self(WIDTH, random.randrange(10, 200), cloud.width, im_c)


def d_lyag():
    global im_counter
    if im_counter == 18:
        im_counter = 0

    display.blit(pers_im[im_counter // 6], (user_x, user_y))
    im_counter += 1


def p_text(soobsh, x, y, sh_color=(0, 250, 0), sh_type="data/shrift.ttf", sh_size=35):
    sh_type = pygame.font.Font(sh_type, sh_size)
    text = sh_type.render(soobsh, True, sh_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        p_text("ИГРА ОСТАНОВЛЕНА, ЧТОБЫ ПРОДОЛЖИТЬ НАЖМИ НА ENTER", 50, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(20)
    pygame.mixer.music.unpause()


def check_colid(bariers):
    for barier in bariers:
        if barier.y == 449:
            if not m_jump:
                if barier.x <= user_x + user_WIDTH - 35 <= barier.x + barier.width:
                    if check_h():
                        obj_return(bariers, barier)
                        return False
                    else:
                        return True
            elif c_jump >= 0:
                if user_y + user_HEIGHT - 5 >= barier.y:
                    if barier.x <= user_x + user_WIDTH - 40 <= barier.x + barier.width:
                        if check_h():
                            obj_return(bariers, barier)
                            return False
                        else:
                            return True
            else:
                if user_y + user_HEIGHT - 10 >= barier.y:
                    if check_h():
                        obj_return(bariers, barier)
                        return False
                    else:
                        return True
        else:
            if not m_jump:
                if barier.x <= user_x + user_WIDTH - 5 <= barier.x + barier.width:
                    if check_h():
                        obj_return(bariers, barier)
                        return False
                    else:
                        return True
            elif c_jump == 10:
                if user_y + user_HEIGHT - 5 >= barier.y:
                    if barier.x <= user_x + user_WIDTH - 5 <= barier.x + barier.width:
                        if check_h():
                            obj_return(bariers, barier)
                            return False
                        else:
                            return True
            elif c_jump >= 1:
                if user_y + user_HEIGHT - 5 >= barier.y:
                    if barier.x <= user_x + user_WIDTH - 35 <= barier.x + barier.width:
                        if check_h():
                            obj_return(bariers, barier)
                            return False
                        else:
                            return True
                else:
                    if user_y + user_HEIGHT - 10 >= barier.y:
                        if barier.x <= user_x + 5 <= barier.x + barier.width:
                            if check_h():
                                obj_return(bariers, barier)
                                return False
                            else:
                                return True


def count_sc(bar):
    global scores, max_cact, max_score
    nad_cactus = 0

    if -20 <= c_jump < 25:
        for barr in bar:
            if user_y + user_HEIGHT - 5 <= barr.y:
                if barr.x <= user_x <= barr.x + barr.width:
                    nad_cactus += 1
                elif barr.x <= user_x + user_WIDTH <= barr.x + barr.width:
                    nad_cactus += 1

        max_cact = max(max_cact, nad_cactus)
    else:
        if c_jump == -30:
            scores += max_cact
            max_cact = 0


def u_game_over():
    global scores, max_score
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if scores > max_score:
            max_score = scores
            p_text("Новый рекорд! Score: " + str(max_score), 300, 200)
            p_text("ТЫ ПРОИГРАЛ, НИКЧЁМНЫЙ ЛЮДИШКА, Я НЕ УДИВЛЁН", 150, 300)
        p_text("ТЫ ПРОИГРАЛ, НИКЧЁМНЫЙ ЛЮДИШКА, Я НЕ УДИВЛЁН", 150, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            return True

        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(60)


def show_health():
    global health
    health1 = 0
    x = 20
    while health1 != health:
        display.blit(health_im, (x, 20))
        x += 40
        health1 += 1


def check_h():
    global health
    health -= 1
    if health == 0:
        # pygame.mixer.Sound.play(proigral)
        return False
    else:
        # pygame.mixer.Sound.play(poterserd)
        return True


def plus_h(heart):
    global health, user_y, user_x, user_WIDTH, user_HEIGHT
    if user_x <= heart.x <= user_x + user_HEIGHT:
        if user_y <= heart.y <= user_y + user_HEIGHT:
            pass
            # pygame.mixer.Sound.play(plusserd)
            if health < 4:
                health += 1

        radius = WIDTH + random.randrange(500, 1700)
        heart.ret_self(radius, heart.y, heart.width, heart.image)


s_men()


while game_1():
    scores = 0
    m_jump = False
    c_jump = 30
    user_y = HEIGHT - user_HEIGHT - 126
    health = 2


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()