import pygame as game
import time
import random
import math
import constants

class Button:
    def __init__(s, pos = [0, 0], size = [0, 0], text = "", func = None, font = constants.small_font, centered = True, visible_background = True, hover_img = "", idle_img = "", pressed_img = ""):
        if centered:
            s.pos = [pos[0] - size[0] / 2, pos[1] - size[1] / 2]
        else:
            s.pos = pos
        s.text_pos = [pos[0] + 5, pos[1] + 5]
        if size[0] == 0 and size[1] == 0:
            s.size = [len(text) * 10 + 10, 25]
        else:
            s.size = size
        s.func = func

        s.centered = centered
        s.visible_background = visible_background

        s.trigger = False
        s.text = font.render(text, True, (255, 255, 255))

        s.state = 0
        s.hover_img = hover_img
        s.pressed_img = pressed_img
        if idle_img == "":
            s.idle_color = (0, 0, 0)
            s.idle_img = 0
        else:
            s.idle_img = game.image.load(os.getcwd() + "\\" + idle_img)
        if hover_img == "":
            s.hover_color = (50, 50, 50)
            s.hover_img = 0
        else:
            s.idle_img = game.image.load(os.getcwd() + "\\" + hover_img)
        if pressed_img == "":
            s.pressed_color = (150, 150, 150)
            s.pressed_img = 0
        else:
            s.idle_img = game.image.load(os.getcwd() + "\\" + pressed_img)
    def update(s):
        if(game.mouse.get_pos()[0] >= s.pos[0] and
           game.mouse.get_pos()[0] <= s.pos[0] + s.size[0] and
           game.mouse.get_pos()[1] >= s.pos[1] and
           game.mouse.get_pos()[1] <= s.pos[1] + s.size[1]):
            if game.mouse.get_pressed()[0]:
                s.state = 2
                if s.trigger == False:
                    s.trigger = True
                    if s.func != None:
                        s.func()
            else:
                s.state = 1
                s.trigger = False
        else:
            s.state = 0

    def DrawMe(s):
        game.draw.rect(constants.screen, (255, 0, 0), (s.pos[0], s.pos[1], s.size[0], s.size[1]))

    def draw(s):
        if s.visible_background:
            if s.idle_img == 0:
                if s.state == 0:
                    game.draw.rect(constants.screen, s.idle_color, (s.pos[0], s.pos[1], s.size[0], s.size[1]))
                elif s.state == 1:
                    game.draw.rect(constants.screen, s.hover_color, (s.pos[0], s.pos[1], s.size[0], s.size[1]))
                elif s.state == 2:
                    game.draw.rect(constants.screen, s.pressed_color, (s.pos[0], s.pos[1], s.size[0], s.size[1]))
            else:
                if s.state == 0:
                    constants.screen.blit(s.idle_img, (s.text_pos[0], s.text_pos[1], s.size[0], s.size[1]))
                elif s.state == 1:
                    constants.screen.blit(s.hover_img, (s.text_pos[0], s.text_pos[1], s.size[0], s.size[1]))
                elif s.state == 2:
                    constants.screen.blit(s.pressed_img, (s.text_pos[0], s.text_pos[1], s.size[0], s.size[1]))
        constants.screen.blit(s.text, (s.text_pos[0], s.text_pos[1], s.size[0], s.size[1]))

class TEXT:
    def __init__(s, pos = [0, 0], text = "", col = [255, 255, 255], font = constants.small_font, fade = False, fade_duration = 2):
        s.pos = [int(pos[0]), int(pos[1])]
        s.col = col
        #s.font = game.font.Font('freesansbold.ttf', font.get_height())
        s.font = game.font.Font('freesansbold.ttf', 20)
        s.text_str = text
        s.text = s.font.render(text, True, s.col)
        s.rect = s.text.get_rect(center = s.pos)
        s.fade = fade
        s.fade_interval = [s.col[0] / (fade_duration * constants.FPS), s.col[1] / (fade_duration * constants.FPS), s.col[2] / (fade_duration * constants.FPS)]
    def update(s):
        if s.fade == True:
            s.update_text()
            s.col = [int(s.col[0] - s.fade_interval[0]),
                     int(s.col[1] - s.fade_interval[1]),
                     int(s.col[2] - s.fade_interval[2])]
            if(s.col[0] <= 0):
                constants.deleteMe.append(s)
        #if(s.update_text):
            #s.text = s.font.render(str(s.variable), True, s.col)
            #s.rect = s.text.get_rect(center = s.pos)
    def update_text(s, new_text = None):
        if(new_text == None):
            s.text = s.font.render(s.text_str, True, s.col)
        else:
            s.text = s.font.render(str(new_text), True, s.col)
        s.rect = s.text.get_rect(center = s.pos)
    def DrawMe(s):
        pass
    def draw(s):
        #s.text = s.font.render(s.text_str, True, s.col)
        constants.screen.blit(s.text, s.rect)
