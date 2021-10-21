import constants
import pygame as game
import os
import math
import random
import Utility_Functions as util
from point import point

class ghost:
    def __init__(s, pos, col, speed = 70):
        #general
        s.pos = pos
        s.offset = [0, -2]
        s.dead = False
        s.vulnerable = False
        s.col = col
        s.hitbox = [0, 0, 0, 0]
        s.freeze = False

        #animations
        s.image_rect = constants.spot_size
        s.animations = {}
        for x in ["up", "down", "right", "left"]:
            s.animations[x] = game.transform.scale(game.image.load(os.getcwd() + '/images/ghost/' + col + "/" + x + ".png"), s.image_rect)
        s.death_animation_speed = int(constants.FPS / 5)
        s.movement_animation_speed = int(constants.FPS / 11)
        s.timer = 0

        #direction
        s.direction = "down"
        s.directions = {"up" : [0, -1], "down" : [0, 1], "right" : [1, 0], "left" : [-1, 0]}
        s.speed = int(constants.FPS / speed)

        #spots
        s.future_moves = ""
        s.target = constants.spots[1]
        s.previous_target = s.target

        #weapons
        r = random.randint(0, len(list(constants.weapons)) - 1)
        s.weapon = "knife"
        #s.weapon = list(constants.weapons)[r]
    def update(s):
        if s.freeze == False:
            if(constants.timer % s.speed == 0):
                s.pos[0] += s.directions[s.direction][0]
                s.pos[1] += s.directions[s.direction][1]
                s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]
                if(util.past_point(s)):
                    s.pos = [s.target.pos[0], s.target.pos[1]]
                    s.previous_target = s.target
                    s.direction, s.target  = util.new_target(s, pick_random = True)
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        game.draw.rect(constants.screen, (0, 0, 255), [s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]])
    def draw(s):
        constants.screen.blit(s.animations[s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        constants.screen.blit(constants.weapons[s.weapon][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[0], s.image_rect[0], s.image_rect[1]))

class blinky:
    def __init__(s, pos, speed = 120):
        #general
        s.pos = pos
        s.offset = [0, -2]
        s.eaten = False
        s.vulnerable = False
        s.col = "red"
        s.freeze = False
        s.reborn = False

        #animations
        s.image_rect = constants.spot_size
        s.animations = {}
        for phase in ["Chase", "Eaten", "Frightened", "Scatter"]:
            s.animations[phase] = {}
            for x in ["up", "down", "right", "left"]:
                s.animations[phase][x] = game.transform.scale(game.image.load(os.getcwd() + '/images/ghost/red/' + phase + "_" + x + ".png"), s.image_rect)
        s.death_animation_speed = int(constants.FPS / 5)
        s.movement_animation_speed = int(constants.FPS / 11)
        s.timer = 0
        s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]


        #direction
        s.direction = "down"
        s.speed = int(constants.FPS / speed)

        #spots
        s.future_moves = ""
        s.target = constants.spots[1]
        s.previous_target = s.target
        s.scatter_spot = point([constants.screen_size[0], 0])
        s.route_to_home = []

        s.Level_Dots_Remaining_Needed = {1 : 20, 2 : 30, 3 : 40, 4 : 40, 5 : 40, 6 : 50, 7 : 50, 8 : 50, 9 : 60, 10 : 60, 11 : 60, 12 : 80, 13 : 80, 14 : 80, 15 : 100, 16 : 100, 17 : 100, 18 : 100}
        s.Level_Dots_Remaining_Top = 120

        #weapons
        r = random.randint(0, len(list(constants.weapons)) - 1)
        s.weapon = "knife"
        #s.weapon = list(constants.weapons)[r]
    def update(s):
        if s.freeze == False:
            if(constants.timer % s.speed == 0):
                s.pos[0] += constants.directions[s.direction][0]
                s.pos[1] += constants.directions[s.direction][1]
                s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]
                if(util.past_point(s)):
                    s.pos = [s.target.pos[0], s.target.pos[1]]
                    s.previous_target = s.target

                    if(s.eaten):
                        if(s.target == constants.spots[27]):
                            s.eaten = False
                            if constants.ghost_mode == "Frightened":
                                s.reborn = True
                        else:
                            s.chase(constants.spots[27])
                    if(s.eaten == False):
                        dots_remaining = 0
                        for x in constants.foods:
                            if x.eaten == 0:
                                dots_remaining += 1

                        if constants.level in s.Level_Dots_Remaining_Needed:
                            dots_needed = s.Level_Dots_Remaining_Needed[constants.level]
                        else:
                            dots_needed = s.Level_Dots_Remaining_Top


                        if(dots_remaining <= dots_needed or constants.ghost_mode == "Chase" or s.reborn):
                            s.chase(constants.players[0])
                        elif(constants.ghost_mode == "Scatter"):
                            s.chase(s.scatter_spot)
                        elif(constants.ghost_mode == "Frightened"):
                            s.target = s.target.neighbors[random.randint(0, len(s.target.neighbors) - 1)]
                            if(s.target.pos[1] > s.pos[1]):
                                s.direction = "down"
                            elif(s.target.pos[1] < s.pos[1]):
                                s.direction = "up"
                            elif(s.target.pos[0] > s.pos[0]):
                                s.direction = "right"
                            else:
                                s.direction = "left"
    def chase(s, target):
        lowest_distance = 9999
        lowest_distance_index = -1

        noGO = util.neighbor_in_direction(s.pos, constants.reverse[s.direction], s.target)

        for neighbor in range(len(s.target.neighbors)):
            if noGO == s.target.neighbors[neighbor]:
                continue

            d = util.Distance(s.target.neighbors[neighbor], target)
            if d < lowest_distance:
                lowest_distance = d
                lowest_distance_index = neighbor
            elif d == lowest_distance:
                if s.target.neighbors[neighbor].pos[1] > s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[0] < s.target.neighbors[lowest_distance_index].pos[0]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[1] < s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor

        s.target = s.target.neighbors[lowest_distance_index]
        if(s.target.pos[1] > s.pos[1]):
            s.direction = "down"
        elif(s.target.pos[1] < s.pos[1]):
            s.direction = "up"
        elif(s.target.pos[0] > s.pos[0]):
            s.direction = "right"
        else:
            s.direction = "left"
    def kill(s):
        s.eaten = True
        s.reborn = False
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        game.draw.rect(constants.screen, (0, 0, 255), [s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]])
        if constants.ghost_mode == "Chase":
            target_pos = [int(constants.players[0].pos[0] + constants.players[0].rect[0] / 2),
                          int(constants.players[0].pos[1] + constants.players[0].rect[1] / 2)]
            game.draw.circle(constants.screen, (255, 0, 0), target_pos, 5)
        elif constants.ghost_mode == "Scatter":
            game.draw.circle(constants.screen, (255, 192, 203), [s.scatter_spot.pos[0], s.scatter_spot.pos[1]], 5)
    def draw(s):
        if(s.reborn == True):
            constants.screen.blit(s.animations["Chase"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        elif(s.eaten == True):
            constants.screen.blit(s.animations["Eaten"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        else:
            constants.screen.blit(s.animations[constants.ghost_mode][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        constants.screen.blit(constants.weapons[s.weapon][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[0], s.image_rect[0], s.image_rect[1]))
class pinky:
    def __init__(s, pos, speed = 120):
        #general
        s.pos = pos
        s.offset = [0, -2]
        s.eaten = False
        s.vulnerable = False
        s.col = "red"
        s.freeze = False
        s.reborn = False

        #animations
        s.image_rect = constants.spot_size
        s.animations = {}
        for phase in ["Chase", "Eaten", "Frightened", "Scatter"]:
            s.animations[phase] = {}
            for x in ["up", "down", "right", "left"]:
                s.animations[phase][x] = game.transform.scale(game.image.load(os.getcwd() + '/images/ghost/pink/' + phase + "_" + x + ".png"), s.image_rect)
        s.death_animation_speed = int(constants.FPS / 5)
        s.movement_animation_speed = int(constants.FPS / 11)
        s.timer = 0
        s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]

        #direction
        s.direction = "down"
        s.speed = int(constants.FPS / speed)

        #spots
        s.future_moves = ""
        s.target = constants.spots[1]
        s.previous_target = s.target
        s.scatter_spot = point([0, 0])

        #weapons
        r = random.randint(0, len(list(constants.weapons)) - 1)
        s.weapon = "knife"
        #s.weapon = list(constants.weapons)[r]
    def update(s):
        if s.freeze == False:
            if(constants.timer % s.speed == 0):
                s.pos[0] += constants.directions[s.direction][0]
                s.pos[1] += constants.directions[s.direction][1]
                s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]
                if(util.past_point(s)):
                    s.pos = [s.target.pos[0], s.target.pos[1]]
                    s.previous_target = s.target

                    if(s.eaten):
                        if(s.target == constants.spots[27]):
                            s.eaten = False
                            if constants.ghost_mode == "Frightened":
                                s.reborn = True
                        else:
                            s.chase(constants.spots[27])
                    if(s.eaten == False):
                        if(constants.ghost_mode == "Chase" or s.reborn):
                            s.chase(constants.players[0], offset = True)
                        elif(constants.ghost_mode == "Scatter"):
                            s.chase(s.scatter_spot)
                        elif(constants.ghost_mode == "Frightened"):
                            s.target = s.target.neighbors[random.randint(0, len(s.target.neighbors) - 1)]
                            if(s.target.pos[1] > s.pos[1]):
                                s.direction = "down"
                            elif(s.target.pos[1] < s.pos[1]):
                                s.direction = "up"
                            elif(s.target.pos[0] > s.pos[0]):
                                s.direction = "right"
                            else:
                                s.direction = "left"
    def chase(s, target, offset = False):
        lowest_distance = 9999
        lowest_distance_index = -1

        noGO = util.neighbor_in_direction(s.pos, constants.reverse[s.direction], s.target)

        for neighbor in range(len(s.target.neighbors)):
            if noGO == s.target.neighbors[neighbor]:
                continue

            if offset == False:
                d = util.Distance(s.target.neighbors[neighbor], target)
            else:
                d = math.sqrt((target.pos[0] + constants.directions[target.direction][0] * constants.spot_size[0] * 2 - s.target.neighbors[neighbor].pos[0])**2 +
                              (target.pos[1] + constants.directions[target.direction][1] * constants.spot_size[1] * 2 - s.target.neighbors[neighbor].pos[1])**2)

            if d < lowest_distance:
                lowest_distance = d
                lowest_distance_index = neighbor
            elif d == lowest_distance:
                if s.target.neighbors[neighbor].pos[1] > s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[0] < s.target.neighbors[lowest_distance_index].pos[0]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[1] < s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor

        s.target = s.target.neighbors[lowest_distance_index]
        if(s.target.pos[1] > s.pos[1]):
            s.direction = "down"
        elif(s.target.pos[1] < s.pos[1]):
            s.direction = "up"
        elif(s.target.pos[0] > s.pos[0]):
            s.direction = "right"
        else:
            s.direction = "left"
    def kill(s):
        s.eaten = True
        s.reborn = False
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        game.draw.rect(constants.screen, (0, 0, 255), [s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]])
        if constants.ghost_mode == "Chase":
            target_pos = [int(constants.players[0].pos[0] + constants.players[0].rect[0] / 2 + constants.directions[constants.players[0].direction][0] * constants.spot_size[0] * 2),
                          int(constants.players[0].pos[1] + constants.players[0].rect[1] / 2 + constants.directions[constants.players[0].direction][1] * constants.spot_size[1] * 2)]
            game.draw.circle(constants.screen, (255, 192, 203), target_pos, 5)
        elif constants.ghost_mode == "Scatter":
            game.draw.circle(constants.screen, (255, 192, 203), [s.scatter_spot.pos[0], s.scatter_spot.pos[1]], 5)
    def draw(s):

        if(s.reborn == True):
            constants.screen.blit(s.animations["Chase"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        elif(s.eaten == True):
            constants.screen.blit(s.animations["Eaten"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        else:
            constants.screen.blit(s.animations[constants.ghost_mode][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        constants.screen.blit(constants.weapons[s.weapon][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[0], s.image_rect[0], s.image_rect[1]))
class inky:
    def __init__(s, pos, speed = 120):
        #general
        s.pos = pos
        s.offset = [0, -2]
        s.eaten = False
        s.vulnerable = False
        s.col = "red"
        s.freeze = False
        s.reborn = False

        #animations
        s.image_rect = constants.spot_size
        s.animations = {}
        for phase in ["Chase", "Eaten", "Frightened", "Scatter"]:
            s.animations[phase] = {}
            for x in ["up", "down", "right", "left"]:
                s.animations[phase][x] = game.transform.scale(game.image.load(os.getcwd() + '/images/ghost/cyan/' + phase + "_" + x + ".png"), s.image_rect)
        s.death_animation_speed = int(constants.FPS / 5)
        s.movement_animation_speed = int(constants.FPS / 11)
        s.timer = 0
        s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]

        #direction
        s.direction = "down"
        s.speed = int(constants.FPS / speed)

        #spots
        s.future_moves = ""
        s.target = constants.spots[1]
        s.previous_target = s.target
        s.scatter_spot = point([constants.screen_size[0], constants.screen_size[1]])

        #weapons
        r = random.randint(0, len(list(constants.weapons)) - 1)
        s.weapon = "knife"
    def update(s):
        if s.freeze == False:
            if(constants.timer % s.speed == 0):
                s.pos[0] += constants.directions[s.direction][0]
                s.pos[1] += constants.directions[s.direction][1]
                s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]
                if(util.past_point(s)):
                    s.pos = [s.target.pos[0], s.target.pos[1]]
                    s.previous_target = s.target

                    if(s.eaten):
                        if(s.target == constants.spots[27]):
                            s.eaten = False
                            if constants.ghost_mode == "Frightened":
                                s.reborn = True
                        else:
                            s.chase(constants.spots[27])
                    if(s.eaten == False):
                        if(constants.ghost_mode == "Chase" or s.reborn):
                            s.chase(constants.players[0], player = True)
                        elif(constants.ghost_mode == "Scatter"):
                            s.chase(s.scatter_spot)
                        elif(constants.ghost_mode == "Frightened"):
                            s.target = s.target.neighbors[random.randint(0, len(s.target.neighbors) - 1)]
                            if(s.target.pos[1] > s.pos[1]):
                                s.direction = "down"
                            elif(s.target.pos[1] < s.pos[1]):
                                s.direction = "up"
                            elif(s.target.pos[0] > s.pos[0]):
                                s.direction = "right"
                            else:
                                s.direction = "left"
    def chase(s, target, player = False):
        lowest_distance = 9999
        lowest_distance_index = -1

        noGO = util.neighbor_in_direction(s.pos, constants.reverse[s.direction], s.target)

        for neighbor in range(len(s.target.neighbors)):
            if noGO == s.target.neighbors[neighbor]:
                continue

            if player == False:
                d = util.Distance(s.target.neighbors[neighbor], target)
            else:
                for ghost in constants.ghosts:
                    if type(ghost) == blinky:
                        d = math.sqrt(((ghost.pos[0] - target.pos[0]) * -1 + target.pos[0] - s.target.neighbors[neighbor].pos[0])**2 +
                                      ((ghost.pos[1] - target.pos[1]) * -1 + target.pos[1] - s.target.neighbors[neighbor].pos[1])**2)
                        break

            if d < lowest_distance:
                lowest_distance = d
                lowest_distance_index = neighbor
            elif d == lowest_distance:
                if s.target.neighbors[neighbor].pos[1] > s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[0] < s.target.neighbors[lowest_distance_index].pos[0]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[1] < s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor

        s.target = s.target.neighbors[lowest_distance_index]
        if(s.target.pos[1] > s.pos[1]):
            s.direction = "down"
        elif(s.target.pos[1] < s.pos[1]):
            s.direction = "up"
        elif(s.target.pos[0] > s.pos[0]):
            s.direction = "right"
        else:
            s.direction = "left"
    def kill(s):
        s.eaten = True
        s.reborn = False
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        game.draw.rect(constants.screen, (0, 0, 255), [s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]])
        if constants.ghost_mode == "Chase":
            for ghost in constants.ghosts:
                if type(ghost) == blinky:
                    target_pos = [int((ghost.pos[0] - constants.players[0].pos[0]) * -1 + constants.players[0].pos[0] + constants.players[0].rect[0] / 2),
                                  int((ghost.pos[1] - constants.players[0].pos[1]) * -1 + constants.players[0].pos[1] + constants.players[0].rect[1] / 2)]
                    game.draw.circle(constants.screen, (0, 255, 255), target_pos, 5)
                    break
        elif constants.ghost_mode == "Scatter":
            game.draw.circle(constants.screen, (0, 255, 255), [s.scatter_spot.pos[0], s.scatter_spot.pos[1]], 5)
    def draw(s):
        if(s.reborn == True):
            constants.screen.blit(s.animations["Chase"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        elif(s.eaten == True):
            constants.screen.blit(s.animations["Eaten"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        else:
            constants.screen.blit(s.animations[constants.ghost_mode][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        constants.screen.blit(constants.weapons[s.weapon][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[0], s.image_rect[0], s.image_rect[1]))
class clyde:
    def __init__(s, pos, speed = 120):
        #general
        s.pos = pos
        s.offset = [0, -2]
        s.eaten = False
        s.vulnerable = False
        s.col = "red"
        s.freeze = False
        s.reborn = False

        #animations
        s.image_rect = constants.spot_size
        s.animations = {}
        for phase in ["Chase", "Eaten", "Frightened", "Scatter"]:
            s.animations[phase] = {}
            for x in ["up", "down", "right", "left"]:
                s.animations[phase][x] = game.transform.scale(game.image.load(os.getcwd() + '/images/ghost/orange/' + phase + "_" + x + ".png"), s.image_rect)
        s.death_animation_speed = int(constants.FPS / 5)
        s.movement_animation_speed = int(constants.FPS / 11)
        s.timer = 0
        s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]


        #direction
        s.direction = "down"
        s.speed = int(constants.FPS / speed)
        print("Ghosts: " + str(s.speed))

        #spots
        s.future_moves = ""
        s.target = constants.spots[1]
        s.previous_target = s.target
        s.scatter_spot = point([0, constants.screen_size[1]])

        #weapons
        r = random.randint(0, len(list(constants.weapons)) - 1)
        s.weapon = "knife"
        #s.weapon = list(constants.weapons)[r]
    def update(s):
        if s.freeze == False:
            if(constants.timer % s.speed == 0):
                s.pos[0] += constants.directions[s.direction][0]
                s.pos[1] += constants.directions[s.direction][1]
                s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]
                if(util.past_point(s)):
                    s.pos = [s.target.pos[0], s.target.pos[1]]
                    s.previous_target = s.target

                    if(s.eaten):
                        if(s.target == constants.spots[27]):
                            s.eaten = False
                            if constants.ghost_mode == "Frightened":
                                s.reborn = True
                        else:
                            s.chase(constants.spots[27])
                    if(s.eaten == False):
                        if(constants.ghost_mode == "Chase" or s.reborn):
                            s.chase(constants.players[0], player = True)
                        elif(constants.ghost_mode == "Scatter"):
                            s.chase(s.scatter_spot)
                        elif(constants.ghost_mode == "Frightened"):
                            s.target = s.target.neighbors[random.randint(0, len(s.target.neighbors) - 1)]
                            if(s.target.pos[1] > s.pos[1]):
                                s.direction = "down"
                            elif(s.target.pos[1] < s.pos[1]):
                                s.direction = "up"
                            elif(s.target.pos[0] > s.pos[0]):
                                s.direction = "right"
                            else:
                                s.direction = "left"
    def chase(s, target, player = False):
        lowest_distance = 9999
        lowest_distance_index = -1

        noGO = util.neighbor_in_direction(s.pos, constants.reverse[s.direction], s.target)

        for neighbor in range(len(s.target.neighbors)):
            if noGO == s.target.neighbors[neighbor]:
                continue

            d = util.Distance(s.target.neighbors[neighbor], target)
            if player:
                if d < math.sqrt(constants.spot_size[0]**2 + constants.spot_size[1]**2) * 3:
                    d = util.Distance(s.target.neighbors[neighbor], s.scatter_spot)


            if d < lowest_distance:
                lowest_distance = d
                lowest_distance_index = neighbor
            elif d == lowest_distance:
                if s.target.neighbors[neighbor].pos[1] > s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[0] < s.target.neighbors[lowest_distance_index].pos[0]:
                    lowest_distance = d
                    lowest_distance_index = neighbor
                elif s.target.neighbors[neighbor].pos[1] < s.target.neighbors[lowest_distance_index].pos[1]:
                    lowest_distance = d
                    lowest_distance_index = neighbor

        s.target = s.target.neighbors[lowest_distance_index]
        if(s.target.pos[1] > s.pos[1]):
            s.direction = "down"
        elif(s.target.pos[1] < s.pos[1]):
            s.direction = "up"
        elif(s.target.pos[0] > s.pos[0]):
            s.direction = "right"
        else:
            s.direction = "left"
    def kill(s):
        s.eaten = True
        s.reborn = False
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        game.draw.rect(constants.screen, (0, 0, 255), [s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]])
        if constants.ghost_mode == "Chase":
            d = util.Distance(s, constants.players[0])
            if d > math.sqrt(constants.spot_size[0]**2 + constants.spot_size[1]**2) * 3:
                game.draw.circle(constants.screen, (255, 165, 0), [int(constants.players[0].pos[0] + constants.players[0].rect[0] / 2), int(constants.players[0].pos[1] + constants.players[0].rect[1] / 2)], int(math.sqrt(constants.spot_size[0]**2 + constants.spot_size[1]**2) * 3), 3)
            else:
                game.draw.circle(constants.screen, (255, 165, 0), s.scatter_spot.pos, 5)
        elif constants.ghost_mode == "Scatter":
            game.draw.circle(constants.screen, (255, 165, 0), s.scatter_spot.pos, 5)
    def draw(s):
        if(s.reborn == True):
            constants.screen.blit(s.animations["Chase"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        elif(s.eaten == True):
            constants.screen.blit(s.animations["Eaten"][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        else:
            constants.screen.blit(s.animations[constants.ghost_mode][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[1], s.image_rect[0], s.image_rect[1]))
        constants.screen.blit(constants.weapons[s.weapon][s.direction], (s.pos[0] + s.offset[0], s.pos[1] + s.offset[0], s.image_rect[0], s.image_rect[1]))
