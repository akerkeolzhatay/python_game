import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("My first game")
icon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load("images/bgg.jpg").convert_alpha()

walk_left = [
    pygame.image.load("images/left/left1.png").convert_alpha(),
    pygame.image.load("images/left/left2.png").convert_alpha(),
    pygame.image.load("images/left/left3.png").convert_alpha(),
    pygame.image.load("images/left/left4.png").convert_alpha()
]
walk_right = [
    pygame.image.load("images/right/right1.png").convert_alpha(),
    pygame.image.load("images/right/right2.png").convert_alpha(),
    pygame.image.load("images/right/right3.png").convert_alpha(),
    pygame.image.load("images/right/right4.png").convert_alpha(),
]
for i in range(0, 4):
    walk_left[i] = walk_left[i].convert_alpha()
    walk_left[i] = pygame.transform.scale(walk_left[i], (80, 80))
    walk_right[i] = walk_right[i].convert_alpha()
    walk_right[i] = pygame.transform.scale(walk_right[i], (80, 80))

ghost = pygame.image.load("images/ghost.png").convert_alpha()
ghost = pygame.transform.scale(ghost, (60, 60))
ghost_x = 1284
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 6
player_x = 550
player_y = 412

is_jump = True
jump_count = 0
score = 0
bg_sound = pygame.mixer.Sound("sounds/bg.mp3")
bg_sound.play(-1)

shot_sound = pygame.mixer.Sound("sounds/shot.mp3")

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 3000)

label = pygame.font.Font("fonts/font.ttf", 70)

win = label.render("You win",False,(255,255,255))
lose_label = label.render("You've lost!", False, (255, 0, 0))
restart_label = label.render("Play again", False, (0, 255, 0))
restart_label_rect = restart_label.get_rect(topleft=(455, 450))

bullets_left = 15
bullet = pygame.image.load("images/shot.png").convert_alpha()
bullet = pygame.transform.scale(bullet, (32, 32))
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1280, 0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10
                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1280:
            bg_x = 0

        if bullets:
            for el in bullets:
                screen.blit(bullet, (el.x, el.y))
                el.x += 10
                if el.x > 1292:
                    bullets.pop()

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(bullets.index(el))
                            score += 100
                            if score == 1500:
                                screen.fill((0, 0, 0))
                                screen.blit(win, (450, 350))
                                pygame.display.update()
                                pygame.time.delay(3000)
                                running = False

    else:
        screen.fill((0, 0, 0))
        screen.blit(lose_label, (450, 350))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 550
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 15

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1284, 565)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 80, player_y + 30)))
            bullets_left -= 1
            shot_sound.play()

    clock.tick(20)