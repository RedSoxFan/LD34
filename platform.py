#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys
from utils import Arithmetic
from Box2D import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, color, breakforce, damforce, dam, bounds):
        pygame.sprite.Sprite.__init__(self)

        # Initialize the image
        self.image = pygame.Surface(bounds.size)
        self.image.fill(color)

        # Get the bounding box
        self.rect = self.image.get_rect()

        # Initialize some physical properties
        self.rect.topleft = bounds.topleft
        self.bforce = breakforce
        self.dforce = damforce
        self.damage = dam

        self.body = None

    def can_break(self, force):
        return force >= self.bforce

    def can_splinter(self, force):
        return self.can_break(force) and force < self.dforce

    def step(self, s):
        self.rect.y -= s
        # self.body.position -= (0, Arithmetic.pixToB2d(s))
        if self.body:
            self.body.position = map(Arithmetic.pixToB2d, (self.rect.x, self.rect.y))

    def tick(self, surface, delta):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class UnbreakablePlatform(Platform):
    def __init__(self, color, bounds):
        Platform.__init__(self, color, sys.maxint, sys.maxint, sys.maxint, bounds)
