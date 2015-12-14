#!/us/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.color import Color
from pygame.rect import Rect
import sys
from input import *
from player import Player
from world import World
from platform import Platform, UnbreakablePlatform
import screens
from utils import Constants, Resources

try:
    import pygame._view
except ImportError:
    pass


class Game(object):
    def __init__(self):
        # Initialize
        pygame.init()
        Keyboard.init()

        # Center window
        info = pygame.display.Info()
        cx = info.current_w // 2 - Constants.WIDTH // 2
        cy = info.current_h // 2 - Constants.HEIGHT // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (cx, cy)

        # Create window and buffer
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.buffer = pygame.surface.Surface((Constants.WIDTH, Constants.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption(Constants.TITLE)

        # Create variables objects. These will be populated in reset
        self.player = None
        self.world = None
        self.messages = []

        # Initialize font map
        self.fontmap = {"hud": pygame.font.Font("saxmono.ttf", 14),
                        "title": pygame.font.Font("saxmono.ttf", 48),
                        "option": pygame.font.Font("saxmono.ttf", 28),
                        "score": pygame.font.Font("saxmono.ttf", 28),
                        "msgtitle": pygame.font.Font("saxmono.ttf", 24),
                        "msgbody": pygame.font.Font("saxmono.ttf", 22)}

        # Initialize main menu
        screens.MainMenu.register_option("Play", Constants.GAME_SCREEN)
        screens.MainMenu.register_option("Exit", Constants.EXIT_SCREEN)

        # Game Loop
        self.gamescreen = screens.MainMenu()
        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            delta = self.clock.tick(Constants.FPS)
            map(self.event, pygame.event.get())
            self.tick(delta)

    def event(self, e):
        if e.type == pygame.QUIT:
            self.running = False

    def reset(self):
        # Create the player
        self.player = Player()

        # Create the world
        self.world = World()

        # Empty messages
        self.messages = []

    def tick(self, delta):
        # Poll input
        Mouse.update()
        Keyboard.update()

        # Clear the buffer
        self.buffer.fill(pygame.Color(0, 0, 0, 255))

        # Tick the correct game screen
        if self.gamescreen == Constants.GAME_SCREEN:
            # Tick the world
            self.world.tick(self.buffer, delta if (self.player.ready and self.player.health > 0) else 0)

            # Tick the objects
            msgs = self.player.tick(self.buffer, delta, self.world.platforms)
            if len(msgs) > 0:
                map(self.messages.append, msgs)

            # Draw messages
            self.messages = [msg for msg in self.messages if msg.alive]
            for msg in self.messages:
                msg.tick(self.buffer, delta, self.fontmap,
                         {"msgtitle": pygame.color.Color("#FFFFFF"),
                          "msggood": pygame.color.Color("#00FF00"),
                          "msgneutral": pygame.color.Color("#FFFF00"),
                          "msgbad": pygame.color.Color("#FF0000")})

            # If the player is fallen in, close the "hatch" and show distance
            if self.player.rect.top >= 50:
                pygame.draw.rect(self.buffer, pygame.color.Color("#111111"), (0, 0, Constants.WIDTH, 50))

                # Draw distance
                txt = "%0.1fkm" % (self.world.fallen / 1000)
                dist = self.fontmap["score"].render(txt, True, pygame.color.Color("#FFFFFF"))
                (w, h) = self.fontmap["score"].size(txt)
                self.buffer.blit(dist, (Constants.WIDTH // 2 - w // 2, 25 - h // 2))
            else:
                pygame.draw.rect(self.buffer, pygame.color.Color("#111111"), (0, 0, Constants.WIDTH // 2 - 75, 50))
                pygame.draw.rect(self.buffer, pygame.color.Color("#111111"),
                                 (Constants.WIDTH // 2 + 75, 0, Constants.WIDTH // 2 - 75, 50))

            # Draw health bar and mass/force
            self.player.draw_health(self.buffer, self.fontmap["hud"], Constants.WIDTH - 200, 5)
            self.player.draw_healthbar(self.buffer, Constants.WIDTH - 200, 25, 180, 10)
            self.player.draw_mass(self.buffer, self.fontmap["hud"], 10, 5)
            self.player.draw_force(self.buffer, self.fontmap["hud"], 10, 25)

            # Draw FPS
            text = "FPS: %d" % self.clock.get_fps()
            surf = self.fontmap["hud"].render(text, True, Color("#FFFFFF"))
            (w, _) = self.fontmap["hud"].size(text)
            pygame.draw.rect(self.buffer, pygame.color.Color(17, 17, 17, 30),
                             (Constants.WIDTH - w - 10, Constants.HEIGHT - 20, w + 10, 20))
            self.buffer.blit(surf, (Constants.WIDTH - w - 5, Constants.HEIGHT - 18))

            # If dead, send to game over screen
            if self.player.disphealth == 0 and len(self.player.particles) == 0:
                self.gamescreen = screens.GameOver((self.world.fallen // 100) / 10.0)

        elif self.gamescreen == Constants.EXIT_SCREEN:
            # On exit screen, set running to False so the game quits after this tick
            self.running = False

        elif isinstance(self.gamescreen, screens.Screen):
            # Tick the game screen
            gs = self.gamescreen.tick(self.buffer, delta, self.fontmap)
            # If the game screen changed, update it
            if gs is not None:
                # Set the new game screen
                self.gamescreen = gs if not isinstance(gs, type(screens.Screen)) else gs()
                # If starting a new game, reset
                if self.gamescreen == Constants.GAME_SCREEN:
                    self.reset()

        # Paint buffer to screen
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
