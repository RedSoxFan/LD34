#!/usr/bin/python2
# -*- coding: utf-8 -*-

import math
import pygame
from utils import Constants


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Initialize the image
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color(0, 0, 255))

        # Get the bounding box
        self.rect = self.image.get_rect()

        # Initialize some physical properties
        self.rect.x = Constants.WIDTH // 2 - self.rect.width // 2
        self.rect.y = -50

    def event(self, event):
        pass

    @property
    def force(self):
        return self.mass * Constants.GRAVITY

    @property
    def mass(self):
        return self.rect.width * self.rect.height

    def tick(self, surface, delta):
        # If not in the center, fall to center of the screen
        if self.rect.centery < Constants.HEIGHT // 2:
            self.rect.y += math.ceil(Constants.GRAVITY / Constants.FPS * delta)
            self.rect.y = min(Constants.HEIGHT // 2, self.rect.y)
        # If on screen, paint
        if self.rect.bottom > 0:
            surface.blit(self.image, (self.rect.x, self.rect.y))