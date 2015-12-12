#!/us/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys

from utils import Constants, Resources

class Game(object):
    def __init__(self):
        # Initialize
        pygame.init()
        # Setup
        pygame.display.set_caption(Constants.TITLE)
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.buffer = pygame.surface.Surface((Constants.WIDTH, Constants.HEIGHT))
        # Game Loop
        clock = pygame.time.Clock()
        running = True
        while running:
            delta = clock.tick(Constants.FPS)
            map(self.event, pygame.event.get())
            self.tick(delta)

    def event(self, e):
        if e.type == pygame.QUIT:
            sys.exit(0)
        elif e.type == pygame.KEYDOWN:
            pass
        elif e.type == pygame.KEYUP:
            pass

    def tick(self, delta):
        self.buffer.fill(pygame.Color(0, 0, 0))
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()