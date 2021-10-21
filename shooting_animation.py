import constants
import pygame as game
import os
import math
import random
import Utility_Functions as util
from point import point

class shotgun_shot:
    def __init__(s, pos = [0, 0], speed = 50, direction = "right"):
        s.pos = [int(pos[0]), int(pos[1])]
        s.speed = int(constants.FPS / speed)
        s.clock = 1
        s.direction = direction

        s.animation_clips = [game.image.load(os.getcwd() + '\\images\\Shooting_anim\\shotgun\\' + s.direction + "\\img_" + str(x) + ".png") for x in range(len(os.listdir(os.getcwd() + '\\images\\Shooting_anim\\shotgun\\' + s.direction)))]
        s.animation_index = 0
        s.animation_index_max = len(s.animation_clips) - 1

        s.rect = s.animation_clips[0].get_rect()
        s.middle = [s.pos[0] + s.rect[2] / 2, s.pos[1] + s.rect[3] / 2]
        if s.direction == "down":
            for x in range(1, s.rect[3] + 1):
                s.weapon_hitbox = [int(s.pos[0]), int(s.pos[1]), int(s.pos[0] + s.rect[2]), int(s.pos[1] + s.rect[3] + x)]
                pixel = constants.screen.get_at([s.weapon_hitbox[2], s.weapon_hitbox[1]])[0:3]
                if pixel[0] == 33 and pixel[1] == 33 and pixel[2] == 255:
                    break
            if x != s.rect[3]:
                print(s.animation_index_max - 1)
                print(math.floor(x / 2))
        elif s.direction == "right":
            for x in range(s.rect[2] + 1):
                s.weapon_hitbox = [int(s.middle[0] + x), int(s.middle[1])]
                pixel = constants.screen.get_at([s.weapon_hitbox[0], s.weapon_hitbox[1]])#[0:3]
                if pixel[2] == 255:
                    break
            if x != s.rect[3]:
                s.animation_index_max = math.floor(x / s.rect[2] * s.animation_index_max)
        elif s.direction == "left":
            for x in range(s.rect[2] + 1):
                s.weapon_hitbox = [int(s.middle[0] - x), int(s.middle[1])]
                pixel = constants.screen.get_at([s.weapon_hitbox[0], s.weapon_hitbox[1]])#[0:3]
                if pixel[2] == 255:
                    break
            if x != s.rect[3]:
                s.animation_index_max = math.floor(x / s.rect[2] * s.animation_index_max)
        elif s.direction == "up":
            for x in range(s.rect[3] + 1):
                s.weapon_hitbox = [int(s.middle[0]), int(s.middle[1] - x)]
                pixel = constants.screen.get_at([s.weapon_hitbox[0], s.weapon_hitbox[1]])#[0:3]
                if pixel[2] == 255:
                    break
            if x != s.rect[3]:
                s.animation_index_max = math.floor(x / s.rect[2] * s.animation_index_max)
    def update(s):
        if(s.clock % s.speed == 0):
            if(s.animation_index != s.animation_index_max):
                s.animation_index += 1
            else:
                constants.deleteMe.append(s)
        s.clock += 1
    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 102), (s.pos[0], s.pos[1], s.rect[0], s.rect[1]))
    def draw(s):
        constants.screen.blit(s.animation_clips[s.animation_index], (s.pos[0], s.pos[1], s.rect[0], s.rect[1]))
