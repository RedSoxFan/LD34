#!/us/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.color import Color
from pygame.rect import Rect
import sys

from player import Player
from platform import Platform, UnbreakablePlatform
from utils import Arithmetic, Constants, Resources


class Game(object):
    def __init__(self):
        # Initialize
        pygame.init()
        # Center window
        info = pygame.display.Info()
        cx = info.current_w // 2 - Constants.WIDTH // 2
        cy = info.current_h // 2 - Constants.HEIGHT // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (cx, cy)
        # Create window and buffer
        pygame.display.set_caption(Constants.TITLE)
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.buffer = pygame.surface.Surface((Constants.WIDTH, Constants.HEIGHT))
        # Create objects
        self.player = Player()
        self.platforms = pygame.sprite.Group()
        left = UnbreakablePlatform("#111111", Rect(0, 0, 50, Constants.HEIGHT))
        right = UnbreakablePlatform("#111111", Rect(Constants.WIDTH - 50, 0, 50, Constants.HEIGHT))
        tl = UnbreakablePlatform("#111111", Rect(50, 0, Constants.WIDTH // 2 - 100, 50))
        tr = UnbreakablePlatform("#111111", Rect(Constants.WIDTH // 2 + 50, 0, Constants.WIDTH // 2 - 100, 50))
        bottom = UnbreakablePlatform("#111111", Rect(50, Constants.HEIGHT - 50, Constants.WIDTH - 100, 50))
        break1 = Platform("#FFFF00", 20000, 24000, 20, Rect(Constants.WIDTH // 2 - 50, 0, 100, 50))
        break2 = Platform("#FF6600", 24000, 26000, 100, Rect(Constants.WIDTH // 2 - 100, 100, 200, 50))
        break3 = Platform("#FF0000", 30000, 50000, 500, Rect(Constants.WIDTH // 2 - 100, 200, 200, 50))
        self.platforms.add(left, right, tl, tr, bottom, break1, break2, break3)
        # Game Loop
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            delta = clock.tick(Constants.FPS)
            map(self.event, pygame.event.get())
            self.tick(delta)

    def event(self, e):
        if e.type == pygame.QUIT:
            self.running = False
        elif e.type == pygame.KEYDOWN:
            pass
        elif e.type == pygame.KEYUP:
            pass

    def tick(self, delta):
        # Clear the buffer
        self.buffer.fill(pygame.Color(0, 0, 0))
        # Tick the objects
        self.player.tick(self.buffer, delta, self.platforms)
        map(lambda p: p.tick(self.buffer, delta), self.platforms)
        # Paint buffer to screen
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()