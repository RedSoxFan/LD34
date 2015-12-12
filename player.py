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
        self.health = self.maxhealth

    def event(self, event):
        pass

    @property
    def force(self):
        return self.mass * Constants.GRAVITY

    @property
    def mass(self):
        return self.rect.width * self.rect.height

    @property
    def maxhealth(self):
        return 5000

    def tick(self, surface, delta, platforms):
        # If alive, tick
        if self.health > 0:
            # If not in the center, fall to center of the screen
            if self.rect.centery < Constants.HEIGHT // 2:
                self.rect.y += math.ceil(Constants.GRAVITY / Constants.FPS * delta)
                self.rect.y = min(Constants.HEIGHT // 2, self.rect.y)
            # Check collision with platforms
            for p in pygame.sprite.spritecollide(self, platforms, False):
                if not p.can_break(self.force):
                    self.health = 0
                elif p.can_splinter(self.force):
                    self.health = max(0, self.health - p.damage)
                    p.kill()
                    print "DEBUG: Splinter ~ Health is %d / %d" % (self.health, self.maxhealth)
                else:
                    p.kill()
                    print "DEBUG: Splat ~ Game Over ~ Health is %d / %d" % (self.health, self.maxhealth)
        # If on screen, paint
        if self.rect.bottom > 0:
            surface.blit(self.image, (self.rect.x, self.rect.y))