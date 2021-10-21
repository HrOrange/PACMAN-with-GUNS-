import pygame as game
import constants
import math
import random
import os

class food:
    def __init__(s, pos):
        s.pos = pos
        #s.image = game.image.load(os.getcwd() + '/images/food.png')
        s.image_rect = [4, 4]
        s.eaten = 0
        s.hitbox = [s.pos[0] + s.image_rect[0] * 0.2, s.pos[1] + s.image_rect[1] * 0.2, s.pos[0] + s.image_rect[0] * 0.8, s.pos[1] + s.image_rect[1] * 0.8]

    def update(s):
        pass
        #if s.eaten > 0:
        #   s.eaten -= 1
    def DrawMe(s):
        pass
    def draw(s):
        if s.eaten == 0:
            game.draw.rect(constants.screen, (250, 185, 176), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        #constants.screen.blit(s.image, (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))

class mega_food:
    def __init__(s, pos):
        s.pos = pos
        [math.floor(constants.spot_size[0] * 0.6), math.floor(constants.spot_size[1] * 0.6)]
        s.rect = [constants.spot_size[0] * 0.5, constants.spot_size[1] * 0.5]
        s.hitbox = [s.pos[0] + s.rect[0] * 0.2, s.pos[1] + s.rect[1] * 0.2, s.pos[0] + s.rect[0] * 0.8, s.pos[1] + s.rect[1] * 0.8]
        size = 0.7
        s.radius = int(math.sqrt((s.rect[0] / 2 * size)**2 + (s.rect[1] / 2 * size)**2))
        s.center = [int(s.pos[0] + constants.spot_size[0] / 2), int(s.pos[1] + constants.spot_size[1] / 2)]

        #animation
        s.speed = constants.FPS / 4
        s.animation_spot = 0
        s.used = 0

    def update(s):
        pass
        #if s.used > 0:
         #  s.used -= 1
    def DrawMe(s):
        pass
    def draw(s):
        if s.animation_spot == 0 and s.used == 0:
            game.draw.circle(constants.screen, (250, 185, 176), s.center, s.radius)
        else:
            pass

        if(constants.timer % s.speed == 0 and s.used == 0):
            s.animation_spot += 1
            if s.animation_spot == 2:
                s.animation_spot = 0

class ammo:
    def __init__(s, pos):
        s.pos = [math.floor(pos[0] + constants.spot_size[0] * 0.2), math.floor(pos[1] + constants.spot_size[1] * 0.2)]
        s.image_rect = [math.floor(constants.spot_size[0] * 0.6), math.floor(constants.spot_size[1] * 0.6)]
        s.speed = constants.FPS / 4
        s.image = game.transform.scale(game.image.load(os.getcwd() + '/images/ammo.png'), s.image_rect)
        s.animation_spot = 0
        s.used = 0
        s.hitbox = [s.pos[0], s.pos[1] + s.image_rect[1], s.pos[0] + s.image_rect[0], s.pos[1] + s.image_rect[1]]

    def update(s):
        pass
        #if s.used > 0:
            #s.used -= 1
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        game.draw.rect(constants.screen, (0, 0, 255), (s.hitbox[0], s.hitbox[1], s.hitbox[2] - s.hitbox[0], s.hitbox[3] - s.hitbox[1]))
    def draw(s):
        if s.animation_spot == 0 and s.used == 0:
            constants.screen.blit(s.image, (s.pos[0], s.pos[1], s.image_rect[0], s.image_rect[1]))
        else:
            pass

        if(constants.timer % s.speed == 0 and s.used == 0):
            s.animation_spot += 1
            if s.animation_spot == 2:
                s.animation_spot = 0
