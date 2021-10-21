import pygame as game
import math
import os
import random
import time
from point import *
from food import *

game.font.init()
small_font = game.font.Font('freesansbold.ttf', 15)
medium_font = game.font.Font('freesansbold.ttf', 30)
big_font = game.font.Font('freesansbold.ttf', 40)

#global variables
run = True
screen_size = [450, 480]
original_map_size = [448, 496]
spot_size = [30, 30]
game_offset = [0, 30]
fullscreen = False
FPS = 120
timer = 0
level = 1
scene = "Main Menu"
score = 0
high_score = 0
mode_durations = {1 : [7, 10, 7, 10, 5, 20, 5], 2 : [7, 10, 7, 10, 5, 17, 1]}
mode_countdown = mode_durations[1][0] * FPS
mode_index = 0
#"Chase", "Scatter", "Frightened"
ghost_mode = "Chase"
Frightened_timer = 0
saved_ghost_mode = None

#sounds and music
game.mixer.init()
effects = {}
for file in os.listdir(os.getcwd() + "\\sounds"):#range(len(sound_files)):
    effects[file[:len(file) - 4]] = game.mixer.Sound(os.getcwd() + "\\sounds\\" + file)
effects["begin_game"].set_volume(0.6)

ChannelA = game.mixer.Channel(1)
ChannelB = game.mixer.Channel(2)
ChannelC = game.mixer.Channel(3)


#effects["waki_2"].play()
#game.mixer.music.set_volume(0.3)

#ghost help
ghost_colors = ["red", "pink", "blue", "orange"]
directions = {"up" : [0, -1], "down" : [0, 1], "right" : [1, 0], "left" : [-1, 0]}
reverse = {"up" : "down", "down" : "up", "right" : "left", "left" : "right"}


# Setup pygame
game.init()
if fullscreen == True:
    screen = game.display.set_mode((screen_size[0], screen_size[1]), pygame.FULLSCREEN)
else:
    screen = game.display.set_mode((screen_size[0], screen_size[1]))
game.display.set_caption('!!!!PACMAN WITH GUNS!!!!')
game.display.set_icon(game.image.load(os.getcwd() + "\\icon\\icon.png"))
game.mouse.set_cursor(*game.cursors.broken_x)
clock = game.time.Clock()

#map
spots_pos = [

[8, 8],
[8, 72],
[8, 120],
[8, 312],
[8, 360],
[8, 408],
[8, 456],

[40, 360],
[40, 408],

[88, 8],
[88, 72],
[88, 120],
[88, 216],
[88, 312],
[88, 360],
[88, 408],

[136, 72],
[136, 120],
[136, 168],
[136, 216],
[136, 264],
[136, 312],
[136, 360],
[136, 408],

[184, 8],
[184, 72],
[184, 120],
[184, 168],
[184, 312],
[184, 360],
[184, 408],
[184, 456],

[232, 8],
[232, 72],
[232, 120],
[232, 168],
[232, 312],
[232, 360],
[232, 408],
[232, 456],

[280, 72],
[280, 120],
[280, 168],
[280, 216],
[280, 264],
[280, 312],
[280, 360],
[280, 408],

[328, 8],
[328, 72],
[328, 120],
[328, 216],
[328, 312],
[328, 360],
[328, 408],

[376, 360],
[376, 408],

[408, 8],
[408, 72],
[408, 120],
[408, 312],
[408, 360],
[408, 408],
[408, 456]
]
spots_neighbors = [

[1, 9],
[0, 2, 10],
[1, 11],
[4, 13],
[3, 7],
[6, 8],
[5, 31],
[4, 8],
[5, 7, 15],
[0, 10, 24],
[1, 9, 16, 11],
[2, 10, 12],
[11, 13, 19],
[3, 12, 21, 14],
[13, 15, 22],
[8, 14],
[10, 17, 25],
[16, 26],
[27, 19],
[12, 18, 20],
[19, 21, 44],
[13, 20, 28],
[14, 23, 29],
[22, 30],
[9, 25],
[16, 24, 33],
[17, 27],
[18, 26, 35],
[21, 29],
[22, 28, 37],
[23, 31],
[6, 30, 39],
[33, 48],
[25, 32, 40],
[35, 41],
[27, 34, 42],
[37, 45],
[29, 36, 46],
[39, 47],
[31, 38, 63],
[33, 41, 49],
[34, 40],
[35, 43],
[42, 44, 51],
[20, 43, 45],
[36, 44, 52],
[37, 47, 53],
[38, 46],
[32, 49, 57],
[40, 48, 50, 58],
[49, 51, 59],
[43, 50, 52],
[45, 51, 53, 60],
[46, 52, 54],
[53, 56],
[56, 61],
[54, 55, 62],
[48, 58],
[49, 57, 59],
[50, 58],
[52, 61],
[55, 60],
[56, 63],
[39, 62]
]
spots = []
for x in range(len(spots_pos)):
    spots_pos[x][0] = math.floor((spots_pos[x][0] / original_map_size[0]) * (screen_size[0] - game_offset[0])) + game_offset[0]
    spots_pos[x][1] = math.floor((spots_pos[x][1] / original_map_size[1]) * (screen_size[1] - game_offset[1])) + game_offset[1]
    spots.append(point(spots_pos[x]))
for x in range(len(spots)):
    for y in spots_neighbors[x]:
        spots[x].neighbors.append(spots[y])

#food and ammo
food_size = [4, 4]
food_color = (250, 185, 176)
food_pos = [
[22, 22],
[22, 38],
[22, 70],
[22, 86],
[22, 102],
[22, 118],
[22, 134],
[22, 326],
[22, 342],
[22, 358],
[22, 422],
[22, 438],
[22, 454],
[22, 470],
[38, 22],
[38, 86],
[38, 134],
[38, 326],
[38, 374],
[38, 422],
[38, 470],
[54, 22],
[54, 86],
[54, 134],
[54, 326],
[54, 374],
[54, 390],
[54, 406],
[54, 422],
[54, 470],
[70, 22],
[70, 86],
[70, 134],
[70, 326],
[70, 422],
[70, 470],
[86, 22],
[86, 86],
[86, 134],
[86, 326],
[86, 422],
[86, 470],
[102, 22],
[102, 38],
[102, 54],
[102, 70],
[102, 86],
[102, 102],
[102, 118],
[102, 134],
[102, 150],
[102, 166],
[102, 182],
[102, 198],
[102, 214],
[102, 230],
[102, 246],
[102, 262],
[102, 278],
[102, 294],
[102, 310],
[102, 326],
[102, 342],
[102, 358],
[102, 374],
[102, 390],
[102, 406],
[102, 422],
[102, 470],
[118, 22],
[118, 86],
[118, 326],
[118, 374],
[118, 470],
[134, 22],
[134, 86],
[134, 326],
[134, 374],
[134, 470],
[150, 22],
[150, 86],
[150, 102],
[150, 118],
[150, 134],
[150, 326],
[150, 374],
[150, 390],
[150, 406],
[150, 422],
[150, 470],
[166, 22],
[166, 86],
[166, 134],
[166, 326],
[166, 374],
[166, 422],
[166, 470],
[182, 22],
[182, 86],
[182, 134],
[182, 326],
[182, 374],
[182, 422],
[182, 470],
[198, 22],
[198, 38],
[198, 54],
[198, 70],
[198, 86],
[198, 134],
[198, 326],
[198, 342],
[198, 358],
[198, 374],
[198, 422],
[198, 438],
[198, 454],
[198, 470],
[214, 86],
[214, 470],
[230, 86],
[230, 470],
[246, 22],
[246, 38],
[246, 54],
[246, 70],
[246, 86],
[246, 134],
[246, 326],
[246, 342],
[246, 358],
[246, 374],
[246, 422],
[246, 438],
[246, 454],
[246, 470],
[262, 22],
[262, 86],
[262, 134],
[262, 326],
[262, 374],
[262, 422],
[262, 470],
[278, 22],
[278, 86],
[278, 134],
[278, 326],
[278, 374],
[278, 422],
[278, 470],
[294, 22],
[294, 86],
[294, 102],
[294, 118],
[294, 134],
[294, 326],
[294, 374],
[294, 390],
[294, 406],
[294, 422],
[294, 470],
[310, 22],
[310, 86],
[310, 326],
[310, 374],
[310, 470],
[326, 22],
[326, 86],
[326, 326],
[326, 374],
[326, 470],
[342, 22],
[342, 38],
[342, 54],
[342, 70],
[342, 86],
[342, 102],
[342, 118],
[342, 134],
[342, 150],
[342, 166],
[342, 182],
[342, 198],
[342, 214],
[342, 230],
[342, 246],
[342, 262],
[342, 278],
[342, 294],
[342, 310],
[342, 326],
[342, 342],
[342, 358],
[342, 374],
[342, 390],
[342, 406],
[342, 422],
[342, 470],
[358, 22],
[358, 86],
[358, 134],
[358, 326],
[358, 422],
[358, 470],
[374, 22],
[374, 86],
[374, 134],
[374, 326],
[374, 422],
[374, 470],
[390, 22],
[390, 86],
[390, 134],
[390, 326],
[390, 374],
[390, 390],
[390, 406],
[390, 422],
[390, 470],
[406, 22],
[406, 86],
[406, 134],
[406, 326],
[406, 374],
[406, 422],
[406, 470],
[422, 22],
[422, 38],
[422, 70],
[422, 86],
[422, 102],
[422, 118],
[422, 134],
[422, 326],
[422, 342],
[422, 358],
[422, 422],
[422, 438],
[422, 454],
[422, 470]
]
ammo_pos = [

#[8, 40],
[8, 360],
[408, 40]]
#[408, 360]]
mega_food_pos = [

[8, 40],
#[8, 360],
#[408, 40]]
[408, 360]]

for x in range(len(food_pos)):
    food_pos[x][0] = math.floor((food_pos[x][0] / original_map_size[0]) * (screen_size[0] - game_offset[0])) + game_offset[0]
    food_pos[x][1] = math.floor((food_pos[x][1] / original_map_size[1]) * (screen_size[1] - game_offset[1])) + game_offset[1]
foods = [food(f) for f in food_pos]
for x in range(len(ammo_pos)):
    ammo_pos[x][0] = math.floor((ammo_pos[x][0] / original_map_size[0]) * (screen_size[0] - game_offset[0])) + game_offset[0]
    ammo_pos[x][1] = math.floor((ammo_pos[x][1] / original_map_size[1]) * (screen_size[1] - game_offset[1])) + game_offset[1]
ammos = [ammo(f) for f in ammo_pos]
for x in range(len(mega_food_pos)):
    mega_food_pos[x][0] = math.floor((mega_food_pos[x][0] / original_map_size[0]) * (screen_size[0] - game_offset[0])) + game_offset[0]
    mega_food_pos[x][1] = math.floor((mega_food_pos[x][1] / original_map_size[1]) * (screen_size[1] - game_offset[1])) + game_offset[1]
mega_foods = [mega_food(f) for f in mega_food_pos]

#weapons
weapons = {
"shotgun" : {"up" : game.transform.scale(game.image.load(os.getcwd() + '/images/Shotgun/shotgun_up.png'), spot_size), "down" : game.transform.scale(game.image.load(os.getcwd() + '/images/Shotgun/shotgun_down.png'), spot_size), "right" : game.transform.scale(game.image.load(os.getcwd() + '/images/Shotgun/shotgun_right.png'), spot_size), "left" : game.transform.scale(game.image.load(os.getcwd() + '/images/Shotgun/shotgun_left.png'), spot_size)},
"knife" : {"up" : game.transform.scale(game.image.load(os.getcwd() + '/images/Knife/up.png'), spot_size), "down" : game.transform.scale(game.image.load(os.getcwd() + '/images/Knife/down.png'), spot_size), "right" : game.transform.scale(game.image.load(os.getcwd() + '/images/Knife/right.png'), spot_size), "left" : game.transform.scale(game.image.load(os.getcwd() + '/images/Knife/left.png'), spot_size)}
}
weapons_ammo = {"shotgun" : 3, "pistol" : 20}
#s.weapons["shotgun"] = game.transform.scale(s.weapons["shotgun"], (s.image_rect[0], s.image_rect[0]))

deleteMe = []

settings = []
players = []
ghosts = []
ui_elements = []
bullets = []
object_lists = [foods, ammos, mega_foods, players, ghosts, bullets, ui_elements]
