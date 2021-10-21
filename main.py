import pygame as game
import constants
import Utility_Functions as util
import time
import os
import math
import random
from ghost import ghost
from pacman import pacman
from point import point
from UI_elements import Button, TEXT


background = game.image.load(os.getcwd() + '\\images\\maze_empty.png')
background = game.transform.scale(background, (constants.screen_size[0], constants.screen_size[0]))


#-----SPAWN Main menu-----
constants.ui_elements.append(Button(pos = [constants.screen_size[0] / 30, constants.screen_size[1] * 0.32 + constants.game_offset[1]], size = [50, 25], centered = False, text = "Start", func = util.start_game, visible_background = False))
#constants.ui_elements.append(Button(pos = [constants.screen_size[0] / 50, constants.screen_size[1] * 0.51 + constants.game_offset[1]], size = [70, 25], centered = False, text = "Settings", func = util.switch_to_from_settings, visible_background = False))
constants.ui_elements.append(Button(pos = [constants.screen_size[0] * 0.85, constants.screen_size[1] * 0.32 + constants.game_offset[1]], size = [45, 25], centered = False, text = "Quit", func = util.Quit, visible_background = False))

#-----SPAWN settings-----
constants.settings.append(Button(pos = [constants.screen_size[0] / 2, constants.screen_size[1] / 2], centered = True, text = "Resume", func = util.switch_to_from_settings, visible_background = False))

show_spots = False

while constants.run:
    for event in game.event.get():
        if event.type == game.QUIT:
            constants.run = False

    game.draw.rect(constants.screen, (0, 0, 0), (0, 0, constants.screen_size[0], constants.screen_size[1]))
    if(constants.scene == "Game"):
        constants.screen.blit(background, (constants.game_offset[0], constants.game_offset[1], constants.screen_size[0], constants.screen_size[1]))

        #mode_text = constants.medium_font.render(constants.ghost_mode, True, (0, 0, 255))
        #constants.screen.blit(mode_text, (50, 4, 100, 100))

        #score
        constants.ui_elements[0].update_text(str(constants.score))
        #high score
        constants.ui_elements[1].update_text(str(constants.high_score))
        #level
        constants.ui_elements[2].update_text(str(constants.level))

        if(constants.Frightened_timer > 0):
            constants.Frightened_timer -= 1
            if(constants.Frightened_timer == 0):
                constants.ghost_mode = constants.saved_ghost_mode
                for ghost in constants.ghosts:
                    ghost.reborn = False
        else:
            constants.mode_countdown -= 1
            if(constants.mode_countdown == 0):
                if(len(constants.mode_durations[constants.level]) - 1 != constants.mode_index):
                    constants.mode_index += 1
                    constants.mode_countdown = constants.mode_durations[constants.level][constants.mode_index] * constants.FPS
                    if(constants.ghost_mode == "Chase"):
                        constants.ghost_mode = "Scatter"
                    else:
                        constants.ghost_mode = "Chase"

                    for ghost in constants.ghosts:
                        ghost.direction = constants.reverse[ghost.direction]
                        temp = ghost.target
                        ghost.target = ghost.previous_target
                        ghost.previous_target = temp

        constants.timer += 1

        #draw and update every object in the scene
        for lists in constants.object_lists:
            for i in lists:
                i.update()
                #i.DrawMe()
                i.draw()
    elif(constants.scene == "Main Menu"):
        constants.screen.blit(background, (constants.game_offset[0], constants.game_offset[1], constants.screen_size[0], constants.screen_size[1]))

        #constants.timer += 1

        #draw and update every object in scene
        for i in constants.ui_elements:
            i.update()
            #i.DrawMe()
            i.draw()
    elif(constants.scene == "Paused"):
        game.draw.rect(constants.screen, (0, 0, 0), (0, 0, constants.screen_size[0], constants.screen_size[1]))
        for i in constants.settings:
            i.update()
            #i.DrawMe()
            i.draw()

    if(len(constants.deleteMe) > 0):
        for x in constants.deleteMe:
            for y in range(len(constants.object_lists)):
                if(x in constants.object_lists[y]):
                    constants.deleteMe.remove(x)
                    constants.object_lists[y].remove(x)

    if show_spots:
        for x in range(len(constants.spots)):
            game.draw.rect(constants.screen, (255, 102, 0), (constants.spots[x].pos[0] + 10, constants.spots[x].pos[1] + 10, 15, 15))

    game.display.update()
    constants.clock.tick(constants.FPS)

game.quit()
