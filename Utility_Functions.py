import constants
import random
import math
import pygame as game
import os
from ghost import ghost, blinky, pinky, inky, clyde
from pacman import pacman
from UI_elements import TEXT
import threading

def past_point(s):
    if s.direction == "right":
        if(s.pos[0] > s.target.pos[0]):
            return True
    elif s.direction == "left":
        if(s.pos[0] < s.target.pos[0]):
            return True
    elif s.direction == "down":
        if(s.pos[1] > s.target.pos[1]):
            return True
    elif s.direction == "up":
        if(s.pos[1] < s.target.pos[1]):
            return True
    return False
def neighbor_in_direction(pos, direction, point):
    for x in point.neighbors:
        if direction == "right":
            if x.pos[0] > pos[0]:
                return x
        elif direction == "left":
            if x.pos[0] < pos[0]:
                return x
        elif direction == "up":
            if x.pos[1] < pos[1]:
                return x
        elif direction == "down":
            if x.pos[1] > pos[1]:
                return x
    return None
def new_target(s, pick_random = False):
    #pick a spot
    r = None

    if pick_random:
        chances = []
        for x in s.target.neighbors:
            if s.direction == "right" and x.pos[0] < s.pos[0]:
                chances.append(0.1)
            elif s.direction == "left" and x.pos[0] > s.pos[0]:
                chances.append(0.1)
            elif s.direction == "up" and x.pos[1] > s.pos[1]:
                chances.append(0.1)
            elif s.direction == "down" and x.pos[1] < s.pos[1]:
                chances.append(0.1)
            else:
                chances.append(0.9 / (len(s.target.neighbors) - 1))
        #print(chances)
        r = give_random_with_chances([f for f in s.target.neighbors], chances)
    else:
        if(s.future_moves == ""):
            if(s.direction == "right"):
                for x in s.target.neighbors:
                    if(x.pos[0] > s.target.pos[0] and x.pos[1] == s.target.pos[1]):
                        r = x
                        break
            elif(s.direction == "left"):
                for x in s.target.neighbors:
                    if(x.pos[0] < s.target.pos[0] and x.pos[1] == s.target.pos[1]):
                        r = x
                        break
            elif(s.direction == "down"):
                for x in s.target.neighbors:
                    if(x.pos[0] == s.target.pos[0] and x.pos[1] > s.target.pos[1]):
                        r = x
                        break
            elif(s.direction == "up"):
                for x in s.target.neighbors:
                    if(x.pos[0] == s.target.pos[0] and x.pos[1] < s.target.pos[1]):
                        r = x
                        break
        else:
            if(s.future_moves == "right"):
                #first check if there is a point in the direction the player wants
                r = neighbor_in_direction(s.pos, s.future_moves, s.target)
                #if that is not possible
                if r == None:
                    #check if there is one in the direction the player is moving
                    r = neighbor_in_direction(s.pos, s.direction, s.target)
                    #if that is not possible
                    if r == None:
                        #stand still and wait
                        s.future_moves = ""
                        return s.direction, None
                else:
                    s.future_moves = ""


            elif(s.future_moves == "left"):
                #first check if there is a point in the direction the player wants
                r = neighbor_in_direction(s.pos, s.future_moves, s.target)
                #if that is not possible
                if r == None:
                    #check if there is one in the direction the player is moving
                    r = neighbor_in_direction(s.pos, s.direction, s.target)
                    #if that is not possible
                    if r == None:
                        #stand still and wait
                        s.future_moves = ""
                        return s.direction, None
                else:
                    s.future_moves = ""
            elif(s.future_moves == "down"):
                #first check if there is a point in the direction the player wants
                r = neighbor_in_direction(s.pos, s.future_moves, s.target)
                #if that is not possible
                if r == None:
                    #check if there is one in the direction the player is moving
                    r = neighbor_in_direction(s.pos, s.direction, s.target)
                    #if that is not possible
                    if r == None:
                        #stand still and wait
                        s.future_moves = ""
                        return s.direction, None
                else:
                    s.future_moves = ""
            elif(s.future_moves == "up"):
                #first check if there is a point in the direction the player wants
                r = neighbor_in_direction(s.pos, s.future_moves, s.target)
                #if that is not possible
                if r == None:
                    #check if there is one in the direction the player is moving
                    r = neighbor_in_direction(s.pos, s.direction, s.target)
                    #if that is not possible
                    if r == None:
                        #stand still and wait
                        s.future_moves = ""
                        return s.direction, None
                else:
                    s.future_moves = ""

    #return the new target
    if r == None:
        return s.direction, None
    elif r.pos[0] == s.pos[0] and r.pos[1] > s.pos[1]:
        return "down", r
    elif r.pos[0] == s.pos[0] and r.pos[1] < s.pos[1]:
        return "up", r
    elif r.pos[1] == s.pos[1] and r.pos[0] > s.pos[0]:
        return "right", r
    elif r.pos[1] == s.pos[1] and r.pos[0] < s.pos[0]:
        return "left", r
def give_random_with_chances(data, chances):
    chance = 0
    r = random.random()
    for x in range(len(chances)):
        chance += chances[x]
        if r <= chance:
            return data[x]
    return data[-1]
def detect_collision(ob1, ob2):
    if(ob1.hitbox[2] >= ob2.hitbox[0] and
       ob1.hitbox[3] >= ob2.hitbox[1] and
       ob1.hitbox[0] <= ob2.hitbox[2] and
       ob1.hitbox[1] <= ob2.hitbox[3]):
        return True
    else:
       return False
def detect_collision_weapon(ob_with_weapon, ob2):
    if(ob_with_weapon.weapon_hitbox[2] >= ob2.hitbox[0] and
       ob_with_weapon.weapon_hitbox[3] >= ob2.hitbox[1] and
       ob_with_weapon.weapon_hitbox[0] <= ob2.hitbox[2] and
       ob_with_weapon.weapon_hitbox[1] <= ob2.hitbox[3]):
        return True
    else:
       return False
def AStar(s, target):
    pass

def Start_Players_and_Ghosts():
    for ghost in constants.ghosts:
        ghost.freeze = False
    for pacman in constants.players:
        pacman.freeze = False

    game.mixer.music.load(os.getcwd() + "\\music\\" + "waw_waw_waw.wav")
    game.mixer.music.set_volume(0.3)
    game.mixer.music.play(-1)

    constants.ChannelA.play(constants.effects["waki_2"], loops = -1)

def reset_game():
    constants.scene = "Game"

    #mega_food and ammo
    for mega_food in constants.mega_foods:
        mega_food.used = 0
    for ammo in constants.ammos:
        ammo.used = 0

    #constants
    constants.timer = 0
    constants.mode_index = 0
    constants.mode_countdown = constants.mode_durations[constants.level][0] * constants.FPS
    constants.Frightened_timer = 0

    #player
    constants.players[0].pos = [math.floor((216 / constants.original_map_size[0]) * (constants.screen_size[0] - constants.game_offset[0])) + constants.game_offset[0],
                                math.floor((360 / constants.original_map_size[1]) * (constants.screen_size[1] - constants.game_offset[1])) + constants.game_offset[1]]
    constants.players[0].target = constants.spots[29]
    constants.players[0].previous_target = constants.spots[37]
    constants.players[0].direction = "left"
    constants.players[0].future_moves = ""
    constants.players[0].dead = False
    constants.players[0].freeze = False
    constants.players[0].animation_spot = 0
    constants.players[0].ammo = constants.weapons_ammo[constants.players[0].weapon]


    #ghosts
    for x in range(len(constants.ghosts)):

        constants.ghosts[x].pos = [constants.spots[27].pos[0], constants.spots[27].pos[1]]
        constants.ghosts[x].direction = "left"
        constants.ghosts[x].target = constants.spots[18]
        constants.ghosts[x].previous_target = constants.spots[27]
        constants.ghosts[x].freeze = False
        constants.ghosts[x].reborn = False
def start_game():
    constants.scene = "Game"

    #music
    constants.effects["begin_game"].play()
    t = threading.Timer(constants.effects["begin_game"].get_length(), Start_Players_and_Ghosts)
    t.start()

    #constants
    constants.timer = 0

    #ghosts
    constants.ghosts.append(blinky([constants.spots[27].pos[0], constants.spots[27].pos[1]]))
    constants.ghosts[-1].direction = "left"
    constants.ghosts[-1].target = constants.spots[18]
    constants.ghosts[-1].previous_target = constants.spots[27]
    constants.ghosts[-1].freeze = True

    constants.ghosts.append(pinky([constants.spots[27].pos[0], constants.spots[27].pos[1]]))
    constants.ghosts[-1].direction = "left"
    constants.ghosts[-1].target = constants.spots[18]
    constants.ghosts[-1].previous_target = constants.spots[27]
    constants.ghosts[-1].freeze = True

    constants.ghosts.append(inky([constants.spots[27].pos[0], constants.spots[27].pos[1]]))
    constants.ghosts[-1].direction = "left"
    constants.ghosts[-1].target = constants.spots[18]
    constants.ghosts[-1].previous_target = constants.spots[27]
    constants.ghosts[-1].freeze = True

    constants.ghosts.append(clyde([constants.spots[27].pos[0], constants.spots[27].pos[1]]))
    constants.ghosts[-1].direction = "left"
    constants.ghosts[-1].target = constants.spots[18]
    constants.ghosts[-1].previous_target = constants.spots[27]
    constants.ghosts[-1].freeze = True

    #player
    constants.players.append(pacman([math.floor((216 / constants.original_map_size[0]) * (constants.screen_size[0] - constants.game_offset[0])) + constants.game_offset[0],
                             math.floor((360 / constants.original_map_size[1]) * (constants.screen_size[1] - constants.game_offset[1])) + constants.game_offset[1]]))
    constants.players[0].target = constants.spots[29]
    constants.players[0].previous_target = constants.spots[37]
    constants.players[0].direction = "left"
    constants.players[0].freeze = True

    #UI
    for x in range(len(constants.ui_elements)):
        constants.ui_elements.pop(0)
    constants.ui_elements.append(TEXT(pos = [constants.screen_size[0] / 4, 15]))
    constants.ui_elements.append(TEXT(pos = [constants.screen_size[0] / 5 * 3, 15]))
    constants.ui_elements.append(TEXT(pos = [constants.screen_size[0] / 5 * 4, 15]))


def switch_to_from_settings():
    if constants.InGame:
        constants.InGame = False
    else:
        constants.InGame = True
def Quit():
    constants.run = False
def Distance(a, b):
    return math.sqrt((b.pos[0] - a.pos[0])**2 + (b.pos[1] - a.pos[1])**2)
