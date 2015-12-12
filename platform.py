#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys


class Platform(pygame.sprite.Sprite):
    def __init__(self, color, breakforce, damforce, dam, bounds):
        pygame.sprite.Sprite.__init__(self)

        # Initialize the image
        self.image = pygame.Surface(bounds.size)
        self.image.fill(pygame.Color(color))

        # Get the bounding box
        self.rect = self.image.get_rect()

        # Initialize some physical properties
        self.rect.topleft = bounds.topleft
        self.bforce = breakforce
        self.dforce = damforce
        self.damage = dam

    def can_break(self, force):
        return force >= self.bforce

    def can_splinter(self, force):
        return self.can_break(force) and force < self.dforce

    def tick(self, surface, delta):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class UnbreakablePlatform(Platform):
    def __init__(self, color, bounds):
        Platform.__init__(self, color, sys.maxint, sys.maxint, sys.maxint, bounds)
