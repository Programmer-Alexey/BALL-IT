import random
import pygame
from settings import *
from objects import Stick, Player, Ball, Atomizer, Message, Button

pygame.init()
info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.SHOWN)
else:
    win = pygame.display.set_mode(SCREEN, pygame.SHOWN | pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('BALL IT!')

clock = pygame.time.Clock()

# Подключение шрифтов
score_font = "Fonts/DroneflyRegular-K78LA.ttf"
msg_font = "Fonts/Biondi Sans.ttf"

game_msg = Message(90, HEIGHT // 2 + 20, 30, "GaMe", msg_font, RED, win)
over_msg = Message(WIDTH // 2 + 60, HEIGHT // 2 + 20, 30, "OvER :(", msg_font, BLACK, win)

cscore_msg = Message(WIDTH // 2, 50, 20, "Sc0rE", msg_font, GRAY3, win)
cscore_msg2 = Message(WIDTH // 2, 75, 24, "0", msg_font, BLACK, win)
best_msg = Message(WIDTH // 2, 140, 20, "BeST", msg_font, GRAY3, win)
bestscore_msg = Message(WIDTH // 2, 170, 24, "0", msg_font, BLACK, win)

hex_msg = Message(WIDTH // 2, HEIGHT // 2 - 30, 40, "BALL", msg_font, RED, win)
dash_msg = Message(WIDTH // 2, HEIGHT // 2 + 20, 40, "IT!", msg_font, BLACK, win)

score_msg = Message(WIDTH // 2, HEIGHT // 2, 60, "0", score_font, GRAY2, win)

# Кнопки
replay_img = pygame.image.load('Icons/replay.png')
replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT // 2 + 115)

# Создаем объекты
line_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
running = True
left = 100
top = 150
right = WIDTH - left
bottom = HEIGHT - top
mid = HEIGHT // 2

topr = Stick((left, top), (WIDTH - left, top))
l1 = Stick((left - 15, top + 10), (30, mid - 10))
l2 = Stick((30, mid + 10), (left - 15, bottom - 10))
r1 = Stick((right + 15, top + 10), (WIDTH - 30, mid - 10))
r2 = Stick((WIDTH - 30, mid + 10), (right + 15, bottom - 10))
bottom = Stick((left, HEIGHT - top), (WIDTH - left, HEIGHT - top))

line_group.add(topr)
line_group.add(r1)
line_group.add(r2)
line_group.add(bottom)
line_group.add(l2)
line_group.add(l1)

player = Player(WIDTH // 2, HEIGHT // 2)

# Очки
bar_index = random.randint(0, 5)
linea = line_group.sprites()[bar_index]
bar = Stick((linea.x1, linea.y1), (linea.x2, linea.y2))

color = COLORS[random.randint(0, 4)]

while running:
    if counter % 100 == 0:
        ball = Ball(win)
        ball_group.add(ball)
        counter = 0
    counter += 1

    win.fill(GRAY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not clicked and game_page:
                clicked = True
                player.di *= -1
                player.update_index()
                rect = line_group.sprites()[player.index]

            if home_page:
                home_page = False
                game_page = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    if home_page:
        line_group.update(win, color)
        hex_msg.update()
        dash_msg.update()

    if score_page:
        cscore_msg.update(shadow=False)
        cscore_msg2.update(score, shadow=False)
        best_msg.update(shadow=False)
        bestscore_msg.update(high, shadow=False)
        game_msg.update(shadow=False)
        over_msg.update(shadow=False)

        if replay_btn.draw(win):
            ball_group.empty()
            gameover = False
            score = 0

            player = Player(WIDTH // 2, HEIGHT // 2)
            score_msg = Message(WIDTH // 2, HEIGHT // 2, 60, "0", score_font, GRAY2, win)

            game_page = True
            score_page = False
            home_page = False

    # Отрисовываем все объекты
    if game_page:
        score_msg.update(score, shadow=True)
        line_group.update(win)
        particle_group.update()
        bar.update(win, ccolor)
        line = line_group.sprites()[player.index]
        player.update(line, ccolor, win)
        ball_group.update(win)

        # Проверка на проигрыш
        if player.rect.collidepoint(bar.get_center()):
            bar_index = random.randint(0, 5)
            linea = line_group.sprites()[bar_index]
            bar = Stick((linea.x1, linea.y1), (linea.x2, linea.y2))

            score += 1
            if score & score > high:
                high = score
            if score % 3 == 0:
                cindex = (cindex + 1) % 5
                ccolor = COLORS[cindex]

        for ball in ball_group:
            if player.alive and ball.rect.colliderect(player.rect):
                x, y = player.rect.centerx, player.rect.centery
                for i in range(20):
                    particle = Atomizer(x, y, ccolor, win)
                    particle_group.add(particle)
                player.alive = False
                ball.kill()
                if not gameover:
                    gameover = True

        if gameover and len(particle_group) == 0:
            game_page = False
            score_page = True

    pygame.draw.rect(win, BLUE, (0, 0, WIDTH - 2, HEIGHT - 2), 2)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
