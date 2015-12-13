#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys

from utils import Resources
from tile import Tile


class Platform(pygame.sprite.Sprite):
    def __init__(self, breakforce, damforce, dam, bounds, imname="diamond-cross.xpm", hueShift=0):
        pygame.sprite.Sprite.__init__(self)

        # Initialize the image
        self.subimage = Resources.load_colorized_image(imname, hueShift, (Tile.SIZE, Tile.SIZE))
        self.image = pygame.Surface(bounds.size, pygame.SRCALPHA)

        for y in xrange(0, self.image.get_rect().height, self.subimage.get_rect().height):
            for x in xrange(0, self.image.get_rect().width, self.subimage.get_rect().width):
                self.image.blit(self.subimage, (x, 0))

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

    def step(self, s):
        self.rect.y -= s

    def tick(self, surface, delta):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class UnbreakablePlatform(Platform):
    def __init__(self, bounds, imname="square-cross3.xpm", hueShift=0):
        Platform.__init__(self, sys.maxint, sys.maxint, sys.maxint, bounds, imname, hueShift)
