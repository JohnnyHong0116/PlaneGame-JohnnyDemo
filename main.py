import pygame
import sys
import traceback
from pygame.locals import *
from random import *

import myplane
import enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Plane Game by Johnny Demo 1')

background = pygame.image.load('images/background.png')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 100, 0)

# music
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.1)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.3)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.3)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.3)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    # crearte my plane
    me = myplane.MyPlane(bg_size)

    enemies = pygame.sprite.Group()

    # create enemy small plane
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # create enemy middle plane
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 7)

    # create enemy large plane
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 5)

    # create normal bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # create super bullets
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
    clock = pygame.time.Clock()

    # hit
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # difficulty level
    level = 1

    # bomb
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/font.ttf', 48)
    bomb_num = 5

    # supply package 20 sec each
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 20 * 1000)

    # super bullet timer
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # super bullet
    is_double_bullet = False

    # stop super time
    INVINCIBLE_TIME = USEREVENT + 2

    # plane lives
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # end platform
    gameover_font = pygame.font.Font('font/font.ttf', 48)
    again_image = pygame.image.load('images/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # repoen files
    recorded = False

    # switch image
    switch_image = True

    # score
    score = 0
    score_font = pygame.font.Font('font/font.ttf', 36)

    # pause the game
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.right, paused_rect.top = width - 10, 10
    paused_image = pause_nor_image

    running = True

    # extention of time
    delay = 100

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 20 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # levels
        if level == 1 and score > 200:
            level = 2
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 2)
            add_mid_enemies(mid_enemies, enemies, 1)
            add_big_enemies(big_enemies, enemies, 1)

            # speed up
            inc_speed(small_enemies, 0.5)
        elif level == 2 and score > 400:
            level = 3
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)

            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 3 and score > 700:
            level = 4
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 4)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 4 and score > 1000:
            level = 5
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 3)

            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 5 and score > 1500:
            level = 6
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 4)
            add_big_enemies(big_enemies, enemies, 3)
            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 6 and score > 2000:
            level = 7
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 5)
            add_big_enemies(big_enemies, enemies, 4)
            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 7 and score > 3000:
            level = 8
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 5)
            add_big_enemies(big_enemies, enemies, 5)
            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 8 and score > 4500:
            level = 9
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 6)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 5)
            # speed up
            inc_speed(small_enemies, 0.5)
            inc_speed(mid_enemies, 0.5)
        elif level == 9 and score > 6000:
            level = 10
            upgrade_sound.play()

            add_small_enemies(small_enemies, enemies, 6)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 6)
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 4
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            # speed up
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        screen.blit(background, (0, 0))

        if life_num and not paused:
            # checking for keyboard manage
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # check whether have bomb or not
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 5:
                        bomb_num += 1
                    bomb_supply.active = False

            # super bullet have or not
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # shooting
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # hit the enemies
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # big plane
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        # dead
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    # blood
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # blood color
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2 and energy_remain < 0.5:
                        energy_color = ORANGE

                    elif energy_remain > 0.5:
                        energy_color = GREEN
                    else:
                        energy_color = RED

                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                    # sound
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    # big plane die
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 40
                            each.reset()

            # create middle plane
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # blood
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # blood color
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2 and energy_remain < 0.5:
                        energy_color = ORANGE

                    elif energy_remain > 0.5:
                        energy_color = GREEN
                    else:
                        energy_color = RED

                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # middle die
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 20
                            each.reset()

            # create small
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # destroy
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 5
                            each.reset()

            # hit or not
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for each in enemies_down:
                    each.active = False

            # create my plane
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # destroy
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # bomb number
            bomb_text = bomb_font.render('× %d' % bomb_num, True, BLACK)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # create lives
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width - 10 - (i + 1) * life_rect.width, \
                                 height - 10 - life_rect.height))
            # score
            score_text = score_font.render('Score : %s' % str(score), True, BLACK)
            screen.blit(score_text, (10, 5))

        # ending
        elif life_num == 0:
            # stop music
            pygame.mixer.music.stop()

            # stop all sound
            pygame.mixer.stop()

            # stop supply
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                # highest score
                recorded = True
                with open('record.txt', 'r')as f:
                    record_score = int(f.read())

                # higher score, save
                if score > record_score:
                    with open('record.txt', 'w')as f:
                        f.write(str(score))

            # ending surface
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # mouse movement
            # left
            if pygame.mouse.get_pressed()[0]:
                # coordinate
                pos = pygame.mouse.get_pos()
                # restart
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # restart
                    main()
                # close           
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # close game
                    pygame.quit()
                    sys.exit()

                    # pause button
        screen.blit(paused_image, paused_rect)

        # switch images
        if not (delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()

        clock.tick(100)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
