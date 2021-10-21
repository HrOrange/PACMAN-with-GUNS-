import constants
import pygame as game
import os
import random
import math
from shooting_animation import shotgun_shot
import Utility_Functions as util
from UI_elements import TEXT

class combo:
    def __init__(s, combo):
        s.combo = combo

class pacman:
    def __init__(s, pos, speed = 120):
        #general
        s.lives = 3
        s.pos = [pos[0], pos[1]]
        s.offset = [0, 0]
        s.charged = False
        s.dead = False
        s.can_die = True
        s.can_eat = True
        s.can_eat_mega_food = True
        s.can_reload = True
        s.freeze = False

        #animations
        s.rect = constants.spot_size
        s.animations = {}
        for x in ["up", "down", "right", "left"]:
            s.animations[x] = []
            #for name in os.listdir(os.getcwd() + '/images/pacman/' + x):
            for name in range(1, len(os.listdir(os.getcwd() + '/images/pacman/' + x)) + 1):
                img = game.image.load(os.getcwd() + '/images/pacman/' + x + "/frame" + str(name) + ".png")
                s.animations[x].append(game.transform.scale(img, s.rect))
        for x in ["death"]:
            s.animations[x] = []
            for name in range(1, len(os.listdir(os.getcwd() + '/images/pacman/' + x)) + 1):
                img = game.image.load(os.getcwd() + '/images/pacman/' + x + "/frame" + str(name) + ".png")
                s.animations[x].append(game.transform.scale(img, constants.screen_size))
        s.animation_loop = True
        s.animation_spot = 0
        s.death_animation_speed = math.floor(constants.FPS / 5)
        s.movement_animation_speed = math.floor(constants.FPS / 10)
        s.hitbox = [s.pos[0] + s.rect[0] * 0.2, s.pos[1] + s.rect[1] * 0.2, s.pos[0] + s.rect[0] * 0.8, s.pos[1] + s.rect[1] * 0.8]

        #direction
        s.direction = "down"
        s.directions = {"up" : [0, -1], "down" : [0, 1], "right" : [1, 0], "left" : [-1, 0]}
        s.speed = int(constants.FPS / speed)

        #spots
        s.future_moves = ""
        s.target = constants.spots[1]
        s.previous_target = None

        #cheats
        s.cheats_on = True
        s.cheats = {combo(["up", "up", "down", "down", "left", "right", "left", "right"]) : s.konami}
                    #combo(["left", "up", "right", "down", "left", "up", "right", "down"]) : s.next_weapon}
        """s.cheats = {combo(["v", "b", "v", "b", "v", "b", "v", "b"]) : s.konami,
                    combo(["x", "b", "x", "b", "x", "b", "x", "b"]) : s.next_weapon}"""
        s.key_logger = []
        s.active_keys = {"down" : False, "left" : False, "right" : False, "up" : False}

        #weapons
        s.weapon = "shotgun"
        s.ammo = constants.weapons_ammo[s.weapon]
        #shooting_modes = ["single", "burst", "auto"]
        s.shooting_mode = "single"
        s.trigger = False
        s.weapon_hitbox = [0,0,0,0]

    def update(s):

        #get input and change direction if needed
        keyboard_pressed = game.key.get_pressed()
        mouse_pressed = game.mouse.get_pressed()
        if(keyboard_pressed[game.K_s] or keyboard_pressed[game.K_DOWN]):
            if s.freeze == False:
                if s.target == None and s.direction != "down":
                    for x in s.previous_target.neighbors:
                        if(x.pos[0] == s.pos[0] and x.pos[1] > s.pos[1]):
                            s.target = x
                            s.direction = "down"
                            break
                elif constants.reverse["down"] == s.direction or s.target == None:
                    s.direction = "down"
                    #if(s.pos[0] == s.previous_target[-1].pos[0] and s.pos[1] == s.previous_target[-1].pos[1]):
                    #    s.target = s.previous_target[-2]
                    #else:
                    temp = s.target
                    s.target = s.previous_target
                    s.previous_target = temp
                else:
                    if s.direction != "down":
                        s.future_moves = "down"

                if s.active_keys["down"] == False:
                    s.active_keys["down"] = True
                    s.key_logger.append("down")
                    if len(s.key_logger) > 8:
                        s.key_logger.remove(s.key_logger[0])
                    if len(s.key_logger) == 8:
                        for combo in s.cheats:
                            if combo.combo == s.key_logger:
                                s.cheats[combo]
                                break
        else:
            s.active_keys["down"] = False
        if(keyboard_pressed[game.K_w] or keyboard_pressed[game.K_UP]):
            if s.freeze == False:
                if s.target == None and s.direction != "up":
                    for x in s.previous_target.neighbors:
                        if(x.pos[0] == s.pos[0] and x.pos[1] < s.pos[1]):
                            s.target = x
                            s.direction = "up"
                            break
                elif constants.reverse["up"] == s.direction or s.target == None:
                    s.direction = "up"
                    temp = s.target
                    s.target = s.previous_target
                    s.previous_target = temp
                else:
                    if s.direction != "up":
                        s.future_moves = "up"

                if s.active_keys["up"] == False:
                    s.active_keys["up"] = True
                    s.key_logger.append("up")
                    if len(s.key_logger) > 8:
                        s.key_logger.remove(s.key_logger[0])
                    if len(s.key_logger) == 8:
                        for combo in s.cheats:
                            if combo.combo == s.key_logger:
                                s.cheats[combo]
                                break
        else:
            s.active_keys["up"] = False
        if(keyboard_pressed[game.K_d] or keyboard_pressed[game.K_RIGHT]):
            if s.freeze == False:
                if s.target == None and s.direction != "right":
                    for x in s.previous_target.neighbors:
                        if(x.pos[0] > s.pos[0] and x.pos[1] == s.pos[1]):
                            s.target = x
                            s.direction = "right"
                            break
                elif constants.reverse["right"] == s.direction:
                    s.direction = "right"
                    temp = s.target
                    s.target = s.previous_target
                    s.previous_target = temp
                else:
                    if s.direction != "right":
                        s.future_moves = "right"

                if s.active_keys["right"] == False:
                    s.active_keys["right"] = True
                    if s.cheats_on:
                        s.key_logger.append("right")
                        if len(s.key_logger) > 8:
                            s.key_logger.remove(s.key_logger[0])
                        if len(s.key_logger) == 8:
                            for combo in s.cheats:
                                if combo.combo == s.key_logger:
                                    print(combo.combo)
                                    s.cheats[combo]()
                                    break
        else:
            s.active_keys["right"] = False
        if(keyboard_pressed[game.K_a] or keyboard_pressed[game.K_LEFT]):
            if s.freeze == False:
                if s.target == None and s.direction != "left":
                    for x in s.previous_target.neighbors:
                        if(x.pos[0] < s.pos[0] and x.pos[1] == s.pos[1]):
                            s.target = x
                            s.direction = "left"
                            break
                elif constants.reverse["left"] == s.direction:
                    s.direction = "left"
                    temp = s.target
                    s.target = s.previous_target
                    s.previous_target = temp
                else:
                    if s.direction != "left":
                        s.future_moves = "left"


                if s.active_keys["left"] == False:
                    s.active_keys["left"] = True
                    s.key_logger.append("left")
                    if len(s.key_logger) > 8:
                        s.key_logger.remove(s.key_logger[0])
                    if len(s.key_logger) == 8:
                        for combo in s.cheats:
                            if combo.combo == s.key_logger:
                                s.cheats[combo]
                                break
        else:
            s.active_keys["left"] = False

        if mouse_pressed[0] and s.dead:
            util.reset_game()
            constants.score = 0
            constants.level = 1
            s.animation_loop = True
            s.lives = 3
            for food in constants.foods:
                food.eaten = 0
            game.mixer.music.play(-1)
            constants.ChannelB.stop()

        #shoot with a gun, if you have it
        if(keyboard_pressed[game.K_f] and s.weapon in ["shotgun", "pistol"]):
            if s.ammo >= 1:
                if s.shooting_mode == "single" and s.trigger == False:
                    s.trigger = True
                    if s.weapon == "shotgun":
                        #hitbox = []
                        if s.direction == "up":
                            for y in range(constants.spot_size[1] * 2):
                                s.weapon_hitbox = [int(s.pos[0] + s.rect[0] * 0.2), int(s.pos[1] + s.rect[1] * 0.2 - y), int(s.pos[0] + s.rect[0] * 0.8), int(s.pos[1] + s.rect[1] * 0.8)]
                                pixel = constants.screen.get_at([s.weapon_hitbox[0], s.weapon_hitbox[1]])[0:3]
                                if pixel[0] == 33 and pixel[1] == 33 and pixel[2] == 255:
                                    break
                            constants.bullets.append(shotgun_shot(pos = [s.pos[0], s.pos[1] - y], direction = s.direction))
                        elif s.direction == "down":
                            for y in range(constants.spot_size[1] * 2):
                                s.weapon_hitbox = [int(s.pos[0] + s.rect[0] * 0.2), int(s.pos[1] + s.rect[1] * 0.2), int(s.pos[0] + s.rect[0] * 0.8), int(s.pos[1] + s.rect[1] * 0.8 + y)]
                                pixel = constants.screen.get_at([s.weapon_hitbox[0], s.weapon_hitbox[3]])[0:3]
                                if pixel[0] == 33 and pixel[1] == 33 and pixel[2] == 255:
                                    break
                            constants.bullets.append(shotgun_shot(pos = [s.pos[0], s.pos[1] + s.rect[1] * 1.1], direction = s.direction))
                        elif s.direction == "right":
                            for x in range(constants.spot_size[1] * 2):
                                s.weapon_hitbox = [int(s.pos[0] + s.rect[0] * 0.2), int(s.pos[1] + s.rect[1] * 0.2), int(s.pos[0] + s.rect[0] * 0.8 + x), int(s.pos[1] + s.rect[1] * 0.8)]
                                pixel = constants.screen.get_at([s.weapon_hitbox[2], s.weapon_hitbox[1]])[0:3]
                                if pixel[0] == 33 and pixel[1] == 33 and pixel[2] == 255:
                                    break
                            constants.bullets.append(shotgun_shot(pos = [s.pos[0] + s.rect[0] * 1.1, s.pos[1]], direction = s.direction))
                        elif s.direction == "left":
                            for x in range(constants.spot_size[1] * 2):
                                s.weapon_hitbox = [int(s.pos[0] + s.rect[0] * 0.2 - x), int(s.pos[1] + s.rect[1] * 0.2), int(s.pos[0] + s.rect[0] * 0.8), int(s.pos[1] + s.rect[1] * 0.8)]
                                pixel = constants.screen.get_at([s.weapon_hitbox[0], s.weapon_hitbox[1]])[0:3]
                                if pixel[0] == 33 and pixel[1] == 33 and pixel[2] == 255:
                                    break
                            constants.bullets.append(shotgun_shot(pos = [s.pos[0] - x, s.pos[1]], direction = s.direction))

                        constants.ui_elements.append(TEXT(text = str(s.ammo - 1), fade = True, pos = [s.pos[0] + s.rect[0] / 2, s.pos[1] + s.rect[1] / 2]))

                        for ghost in constants.ghosts:
                            if util.detect_collision_weapon(s, ghost):
                                ghost.kill()
                               #constants.deleteMe.append(ghost)
                    if s.weapon == "pistol":
                        if s.direction == "up":
                            hitbox = [0, s.pos[1] - s.spot_size[1] * 2, s.spot_size, s.spot_size[1] * 2]
                        elif s.direction == "up":
                            hitbox = [0, s.pos[1] - s.spot_size[1] * 2, s.spot_size, s.spot_size[1] * 2]
                        elif s.direction == "up":
                            hitbox = [0, s.pos[1] - s.spot_size[1] * 2, s.spot_size, s.spot_size[1] * 2]
                        elif s.direction == "up":
                            hitbox = [0, s.pos[1] - s.spot_size[1] * 2, s.spot_size, s.spot_size[1] * 2]
                        for ghost in constants.ghosts:
                            pass
                    s.ammo -= 1
                    print("Ammo: " + str(s.ammo))
        else:
            s.trigger = False

        #move the character
        if s.dead == False and s.freeze == False:
            if(constants.timer % s.speed == 0):
                if(s.target != None):
                    if(util.past_point(s) == False):
                        s.pos[0] += s.directions[s.direction][0]
                        s.pos[1] += s.directions[s.direction][1]
                        s.hitbox = [s.pos[0] + s.rect[0] * 0.2, s.pos[1] + s.rect[1] * 0.2, s.pos[0] + s.rect[0] * 0.8, s.pos[1] + s.rect[1] * 0.8]
                        if(util.past_point(s)):
                            s.pos = [s.target.pos[0], s.target.pos[1]]
                            s.previous_target = s.target
                            s.direction, s.target = util.new_target(s)
                            if s.target:
                                constants.ChannelA.play(constants.effects["waki_2"], loops = -1)
                                #constants.effects["waki_2"].play(loops = -1)
                            else:
                                constants.ChannelA.pause()

        #check for collision with ghosts, in which case, DIE!!!                 MUHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA
        if s.can_die:
            if s.dead == False:
                for ghost in constants.ghosts:
                    if util.detect_collision(s, ghost):
                        if(ghost.eaten == True):
                            continue
                        elif(s.charged or constants.ghost_mode == "Frightened" and ghost.reborn == False):
                            ghost.kill()
                            constants.ui_elements.append(TEXT(text = str(20), fade = True, pos = [s.pos[0] + s.rect[0] / 2, s.pos[1] + s.rect[1] / 2]))
                            constants.score += 20
                        else:
                            s.lives -= 1
                            if s.lives == 0:
                                s.dead = True
                                s.animation_spot = 0
                                s.animation_loop = False
                                for g in constants.ghosts:
                                    g.freeze = True

                                constants.ChannelB.play(constants.effects["die"])
                                game.mixer.music.stop()
                                constants.ChannelA.stop()

                                if constants.score > constants.high_score:
                                    constants.high_score = constants.score
                                    #print("New Highscore: " + str(constants.high_score))
                            else:
                                util.reset_game()
                        break

        #check for collision with food, in which case, GET SCORE!!!
        if s.can_eat:
            for food in constants.foods:
                if util.detect_collision(s, food):
                    if food.eaten == 0:
                        food.eaten = 1#constants.FPS * 10
                        constants.score += 1

                        done = True
                        for x in constants.foods:
                            if x.eaten == 0:
                                done = False
                                break
                        if done == True:
                            constants.level += 1
                            util.reset_game()
                            for food in constants.foods:
                                food.eaten = 0
                        break

        #check for collision with mega food, in which case, KILL GHOSTS!!!
        if s.can_eat_mega_food:
            for mega_food in constants.mega_foods:
                if mega_food.used == 0:
                    if util.detect_collision(s, mega_food):
                        mega_food.used = constants.FPS * 20
                        constants.saved_ghost_mode = constants.ghost_mode
                        constants.ghost_mode = "Frightened"
                        constants.Frightened_timer = 8 * constants.FPS
                        for ghost in constants.ghosts:
                            ghost.direction = constants.reverse[ghost.direction]
                            temp = ghost.target
                            ghost.target = ghost.previous_target
                            ghost.previous_target = temp
                            ghost.reborn = False

        #check for collision with ammo boxes, in which case, GET AMMO!!!
        if s.can_reload:
            for ammo in constants.ammos:
                if ammo.used == 0:
                    if util.detect_collision(s, ammo):
                        ammo.used = constants.FPS * 20
                        s.ammo += 2
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.rect[0], s.rect[1]))
        game.draw.rect(constants.screen, (255, 255, 102), (s.weapon_hitbox[0], s.weapon_hitbox[1], s.weapon_hitbox[2] - s.weapon_hitbox[0], s.weapon_hitbox[3] - s.weapon_hitbox[1]))
        game.draw.rect(constants.screen, (0, 0, 255), [s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]])
    def draw(s):
        if s.dead:
            constants.screen.blit(s.animations["death"][s.animation_spot], (0, 0, constants.screen_size[0], constants.screen_size[1]))

            #print(s.animation_spot)

            if(constants.timer % s.death_animation_speed == 0):
                if len(s.animations["death"]) - 1 != s.animation_spot:
                    s.animation_spot += 1
                if len(s.animations["death"]) == s.animation_spot:
                    if s.animation_loop:
                        s.animation_spot = 0
        else:
            constants.screen.blit(s.animations[s.direction][s.animation_spot], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.rect[0], s.rect[1]))
            constants.screen.blit(constants.weapons[s.weapon][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.rect[0], s.rect[1]))

            if(constants.timer % s.movement_animation_speed == 0):
                if s.target != None:
                    if len(s.animations[s.direction]) - 1 != s.animation_spot or s.animation_loop:
                        s.animation_spot += 1
                    if len(s.animations[s.direction]) == s.animation_spot:
                        if s.animation_loop:
                            s.animation_spot = 0

    #cheat functions
    def konami(s):
        s.ammo = 9999
        s.lives += 9999
        print("!!!!!KONAMI!!!!!")
    def next_weapon(s):
        """weapons = list(constants.weapons)
        index = weapons.index(s.weapon)
        index += 1
        if index == len(weapons):
            index = 0
        s.weapon = list(constants.weapons)[index]"""
        print("NEXT WEAPON!!!!!")
