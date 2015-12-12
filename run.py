#!/us/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys
from input import *
from player import *
from utils import Constants, Resources


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

    def tick(self, delta):
        # Clear the buffer
        self.buffer.fill(pygame.Color(0, 0, 0))
        # Tick the objects
        self.player.tick(self.buffer, delta)
        # Paint buffer to screen
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
