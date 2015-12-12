#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from input import Mouse, Keyboard
from utils import Constants


class Screen(object):
    def __init__(self):
        pass

    def tick(self, surface, delta, fontmap):
        return None


class GameOver(Screen):
    def __init__(self, score=0):
        Screen.__init__(self)
        self.value = score

    def tick(self, surface, delta, fontmap):
        scr = None

        # Paint the background
        surface.fill(pygame.color.Color("#222222"))

        # Paint game over
        go = fontmap["title"].render("Game Over!", True, pygame.color.Color("#FFFFFF"))
        (w, h) = fontmap["title"].size("Game Over!")
        surface.blit(go, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 4 + h // 2))

        # Paint the score
        txt = "Distance: %0.1fkm" % self.value
        sc = fontmap["score"].render(txt, True, pygame.color.Color("#CCCCCC"))
        (w, h) = fontmap["score"].size(txt)
        surface.blit(sc, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 2 + h // 2))

        # Paint the return to main menu message
        txt = "Press <enter> to return to the Main Menu"
        msg = fontmap["hud"].render(txt, True, pygame.color.Color("#999999"))
        (w, h) = fontmap["hud"].size(txt)
        surface.blit(msg, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT - h - 10))

        # Check to see if enter is pressed
        if Keyboard.released(pygame.K_RETURN):
            scr = MainMenu

        return scr


class MainMenu(Screen):
    options = []
    screens = []

    def __init__(self):
        Screen.__init__(self)
        self.sel = 0

    @staticmethod
    def register_option(text, screen):
        MainMenu.options.append(text)
        MainMenu.screens.append(screen)

    def tick(self, surface, delta, fontmap):
        scr = None

        # Paint the background
        surface.fill(pygame.color.Color("#222222"))

        # Paint the title
        ttl = fontmap["title"].render(Constants.TITLE, True, pygame.color.Color("#FFFFFF"))
        (w, h) = fontmap["title"].size(Constants.TITLE)
        surface.blit(ttl, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 4 + h // 2))

        # Paint the options
        msel = -1
        for i, option in enumerate(MainMenu.options):
            # Get the bounding box
            (w, h) = fontmap["option"].size(option)
            (x, y) = (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 2 + i * h * 2)
            # Determine if the option is highlighted or if the mouse is hovering over it
            m = Mouse.getX() in xrange(x, x+w) and Mouse.getY() in xrange(y, y+h)
            msel = i if m else msel
            s = self.sel == i or m
            # Paint the option
            txt = fontmap["option"].render(option, True, pygame.color.Color("#00FF00" if s else "#CCCCCC"))
            surface.blit(txt, (x, y))

        # Check for input
        if len(MainMenu.options) > 0:
            if Keyboard.released(pygame.K_DOWN):
                # If not at bottom, move the selection down
                self.sel = min(self.sel + 1, len(MainMenu.options) - 1)
            elif Keyboard.released(pygame.K_UP):
                # If not at top, move the selection up
                self.sel = max(0, self.sel - 1)
            elif Keyboard.released(pygame.K_RETURN):
                # Select the highlighted option
                scr = MainMenu.screens[self.sel]
            elif msel >= 0 and Mouse.leftReleased():
                # Select the option that mouse is hovering over
                scr = MainMenu.screens[msel]

        return scr