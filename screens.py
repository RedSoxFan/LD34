#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from audio import Sound
from input import Mouse, Keyboard
from utils import Constants, Settings


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


class Credits(Screen):
    def __init__(self):
        Screen.__init__(self)

    def tick(self, surface, delta, fontmap):
        scr = None

        # Paint the background
        surface.fill(pygame.color.Color("#222222"))

        # Paint title
        go = fontmap["title"].render("Credits", True, pygame.color.Color("#FFFFFF"))
        (w, h) = fontmap["title"].size("Credits")
        surface.blit(go, (Constants.WIDTH // 2 - w // 2, 60))

        # Paint the sections
        yoff = -200
        for section in ("krx\nProgrammer and Special Effects", "RedSoxFan\nProgrammer",
                        "Spetsnaz\nGame Idea", "s.a.x Software\nSaxMono Font", "Game Made In\nPython with pygame",
                        "Music Made In\nBFXR + LabChirp", "EXE Creation\npy2exe with pygame2exe script"):
            for i, text in enumerate(section.split("\n")):
                ttype = "msgtitle" if i == 0 else "msgbody"
                col = pygame.color.Color("#CCCCCC" if ttype == "msgtitle" else "#888888")
                sc = fontmap[ttype].render(text, True, col)
                (w, h) = fontmap[ttype].size(text)
                surface.blit(sc, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 2 - h // 2 + yoff))
                yoff += h + 2
            yoff += 25

        # Paint the return to main menu message
        txt = "Press <enter> to return to the Main Menu"
        msg = fontmap["hud"].render(txt, True, pygame.color.Color("#999999"))
        (w, h) = fontmap["hud"].size(txt)
        surface.blit(msg, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT - h - 10))

        # Check to see if enter is pressed
        if Keyboard.released(pygame.K_RETURN):
            Sound.play('menuselect')
            scr = MainMenu

        return scr


class Info(Screen):
    def __init__(self):
        Screen.__init__(self)

    def tick(self, surface, delta, fontmap):
        scr = None

        # Paint the background
        surface.fill(pygame.color.Color("#222222"))

        # Paint title
        go = fontmap["title"].render("Info", True, pygame.color.Color("#FFFFFF"))
        (w, h) = fontmap["title"].size("Info")
        surface.blit(go, (Constants.WIDTH // 2 - w // 2, 100))

        # Paint the sections
        yoff = 200
        for section in ("Objective\nTo get as far down the abyss as possible",
                        "Controls\nUp Arrow - Grow\nDown Arrow - Shrink",
                        "How To Play\n[Grow or shrink the player to either reduce or increase force. You "
                        "will need to have enough force to break the platform (40% of the width). If you "
                        "don't, you will splat and die. Also, if you have enough force to break the "
                        "platform, but not cleanly (60% of the width), you will cause the platform "
                        "to splinter, which will damage you.]"):
            for i, text in enumerate(section.split("\n")):
                ttype = "msgtitle" if i == 0 else "msgbody"
                col = pygame.color.Color("#CCCCCC" if ttype == "msgtitle" else "#888888")
                if text.startswith("[") and text.endswith("]"):
                    words = text[1:-1].split(" ")
                    text = ""
                    while len(words) > 0:
                        (w, h) = fontmap[ttype].size("%s %s" % (text, words[0]))
                        if w < Constants.WIDTH - 20:
                            text = "%s %s" % (text, words[0])
                            words = words[1:]
                        else:
                            sc = fontmap[ttype].render(text, True, col)
                            (w, h) = fontmap[ttype].size(text)
                            surface.blit(sc, (Constants.WIDTH // 2 - w // 2, yoff))
                            yoff += h + 2
                            text = ""
                    if len(text) > 0:
                        sc = fontmap[ttype].render(text, True, col)
                        (w, h) = fontmap[ttype].size(text)
                        surface.blit(sc, (Constants.WIDTH // 2 - w // 2, yoff))
                        yoff += h + 2
                else:
                    # Line
                    sc = fontmap[ttype].render(text, True, col)
                    (w, h) = fontmap[ttype].size(text)
                    surface.blit(sc, (Constants.WIDTH // 2 - w // 2, yoff))
                    yoff += h + 2
            yoff += 20

        # Paint the return to main menu message
        txt = "Press <enter> to return to the Main Menu"
        msg = fontmap["hud"].render(txt, True, pygame.color.Color("#999999"))
        (w, h) = fontmap["hud"].size(txt)
        surface.blit(msg, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT - h - 10))

        # Check to see if enter is pressed
        if Keyboard.released(pygame.K_RETURN):
            Sound.play('menuselect')
            scr = MainMenu

        return scr


class SettingsScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.sel = (0, 0)
        self.options = {"AUDIO": (("Play", lambda: Settings.AUDIO == 1, lambda: setattr(Settings, "AUDIO", 1)),
                                  ("Mute", lambda: Settings.AUDIO == 0,
                                   lambda: setattr(Settings, "AUDIO", 0) or Sound.stop_all(False))),
                        "GRAPHICS": (("High", lambda: Settings.GRAPHICS == 2, lambda: setattr(Settings, "GRAPHICS", 2)),
                                     ("Medium", lambda: Settings.GRAPHICS == 1, lambda: setattr(Settings, "GRAPHICS", 1)),
                                     ("Low", lambda: Settings.GRAPHICS == 0, lambda: setattr(Settings, "GRAPHICS", 0))),
                        "~": (("Return to Main Menu", lambda: False, lambda: MainMenu), )}

    def tick(self, surface, delta, fontmap):
        scr = None

        # Paint the background
        surface.fill(pygame.color.Color("#222222"))

        # Paint the title
        ttl = fontmap["title"].render("Settings", True, pygame.color.Color("#FFFFFF"))
        (w, h) = fontmap["title"].size("Settings")
        surface.blit(ttl, (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 4 + h // 2))

        # Paint the options
        mcb = None
        yoff = 0
        for i, key in enumerate(sorted(self.options.keys())):
            # Get the bounding box
            (w, h) = fontmap["msgtitle"].size(key.replace("~", ""))
            (x, y) = (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 2 + yoff)
            # Paint the option
            txt = fontmap["msgtitle"].render(key.replace("~", ""), True, pygame.color.Color("#CCCCCC"))
            surface.blit(txt, (x, y))
            yoff += h + 2

            for j, (txt, val, cb) in enumerate(self.options[key]):
                # Get the bounding box
                (w, h) = fontmap["msgbody"].size(txt)
                (x, y) = (Constants.WIDTH // 2 - w // 2, Constants.HEIGHT // 2 + yoff)
                # Determine if the option is highlighted or if the mouse is hovering over it
                m = Mouse.getX() in xrange(x, x + w) and Mouse.getY() in xrange(y, y + h)
                mcb = cb if m else mcb
                s = self.sel == (i, j) or m
                # Paint the option
                col = "#008800" if val() else "#CCCCCC"
                txt = fontmap["msgbody"].render(txt, True, pygame.color.Color("#00FF00" if s else col))
                surface.blit(txt, (x, y))
                yoff += h + 2

            yoff += 20

        # Check for input
        if len(MainMenu.options) > 0:
            if Keyboard.released(pygame.K_DOWN):
                # If not at bottom, move the selection down
                if self.sel[1] < len(self.options[sorted(self.options.keys())[self.sel[0]]]) - 1:
                    self.sel = (self.sel[0], self.sel[1] + 1)
                    Sound.play('menumove')
                elif self.sel[0] < len(self.options.keys()) - 1:
                    self.sel = (self.sel[0] + 1, 0)
                    Sound.play('menumove')
            elif Keyboard.released(pygame.K_UP):
                # If not at top, move the selection up
                if self.sel[1] > 0:
                    self.sel = (self.sel[0], self.sel[1] - 1)
                    Sound.play('menumove')
                elif self.sel[0] > 0:
                    self.sel = (self.sel[0] - 1, len(self.options[sorted(self.options.keys())[self.sel[0] - 1]]) - 1)
                    Sound.play('menumove')
            elif Keyboard.released(pygame.K_RETURN):
                # Select the highlighted option
                scr = self.options[sorted(self.options.keys())[self.sel[0]]][self.sel[1]][2]()
                Sound.play('menuselect')
            elif mcb is not None and Mouse.leftReleased():
                # Select the option that mouse is hovering over
                scr = mcb()
                Sound.play('menuselect')

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
            m = Mouse.getX() in xrange(x, x + w) and Mouse.getY() in xrange(y, y + h)
            msel = i if m else msel
            s = self.sel == i or m
            # Paint the option
            txt = fontmap["option"].render(option, True, pygame.color.Color("#00FF00" if s else "#CCCCCC"))
            surface.blit(txt, (x, y))

        # Check for input
        if len(MainMenu.options) > 0:
            if Keyboard.released(pygame.K_DOWN):
                # If not at bottom, move the selection down
                Sound.play('menumove')
                self.sel = min(self.sel + 1, len(MainMenu.options) - 1)
            elif Keyboard.released(pygame.K_UP):
                # If not at top, move the selection up
                Sound.play('menumove')
                self.sel = max(0, self.sel - 1)
            elif Keyboard.released(pygame.K_RETURN):
                # Select the highlighted option
                Sound.play('menuselect')
                scr = MainMenu.screens[self.sel]
            elif msel >= 0 and Mouse.leftReleased():
                # Select the option that mouse is hovering over
                Sound.play('menuselect')
                scr = MainMenu.screens[msel]

        return scr
