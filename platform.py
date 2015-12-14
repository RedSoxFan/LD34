#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys
from utils import Graphics
from tile import Tile


class Platform(pygame.sprite.Sprite):
    def __init__(self, breakforce, damforce, dam, bounds, hueShift=10):
        pygame.sprite.Sprite.__init__(self)

        # Initialize the image
        self.hshift = hueShift
        self.image = pygame.Surface(bounds.size, pygame.SRCALPHA)
        self.col = None
        self._draw_image()

        # Get the bounding box
        self.rect = self.image.get_rect()

        # Initialize some physical properties
        self.rect.topleft = bounds.topleft
        self.bforce = breakforce
        self.dforce = damforce
        self.damage = dam

    def _draw_image(self):
        self.image.fill(pygame.color.Color(0, 0, 0, 0))
        irect = self.image.get_rect()
        self.col = col = Graphics.hue_shift("#EE5400", self.hshift)
        for y in xrange(0, self.image.get_rect().height, Tile.SIZE):
            for x in xrange(0, self.image.get_rect().width, Tile.SIZE):
                points = ((x + Tile.SIZE // 2, y),  # Top
                          (x + Tile.SIZE, y + Tile.SIZE // 2),  # Right
                          (x + Tile.SIZE // 2, y + Tile.SIZE),  # Bottom
                          (x, y + Tile.SIZE // 2))  # Left
                pygame.draw.polygon(self.image, col, points, 1)

    def can_break(self, force):
        return force >= self.bforce

    def can_splinter(self, force):
        return self.can_break(force) and force < self.dforce

    def step(self, s):
        self.rect.y -= s

    def tick(self, surface, delta):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class UnbreakablePlatform(Platform):
    def __init__(self, bounds, hueShift=0):
        Platform.__init__(self, sys.maxint, sys.maxint, sys.maxint, bounds, hueShift=hueShift)

    def _draw_image(self):
        self.image.fill(pygame.color.Color(0, 0, 0, 0))
        irect = self.image.get_rect()
        col = Graphics.hue_shift("#EE5400", self.hshift)
        for y in xrange(0, self.image.get_rect().height, Tile.SIZE):
            for x in xrange(0, self.image.get_rect().width, Tile.SIZE):
                pygame.draw.rect(self.image, col, (x, y, x + Tile.SIZE, y + Tile.SIZE), 1)
                pygame.draw.line(self.image, col, (x, y), (x + Tile.SIZE, y + Tile.SIZE), 1)
                pygame.draw.line(self.image, col, (x, y + Tile.SIZE), (x + Tile.SIZE, y), 1)
