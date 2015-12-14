#!/usr/bin/python2
# -*- coding: utf-8 -*-

import math
import pygame
from input import Keyboard
from messages import Message
from utils import Arithmetic, Constants, Graphics
from math import *
from random import *
from particles import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Initialize the image
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.__draw_image()

        # Initialize some physical properties
        self.rect.x = Constants.WIDTH // 2 - self.rect.width // 2
        self.rect.y = -50
        self.health = self.maxhealth
        self.disphealth = self.health
        self.ready = False

        # Player related effects
        self.particles = []

    def __draw_image(self):
        self.image.fill(pygame.color.Color(0, 0, 0, 0))
        irect = self.image.get_rect()
        col = Graphics.hue_shift("#EE5400", 100)
        pygame.draw.rect(self.image, col, (0, 0, irect.width, irect.height), 2)

    def draw_force(self, surface, font, x, y):
        txt = font.render("Force: %d" % self.force, True, pygame.color.Color("#FFFFFF"))
        surface.blit(txt, (x, y))

    def draw_health(self, surface, font, x, y):
        txt = font.render("Health: %d / %d" % (self.disphealth, self.maxhealth), True, pygame.color.Color("#FFFFFF"))
        surface.blit(txt, (x, y))

    def draw_healthbar(self, surface, x, y, width, height):
        pygame.draw.rect(surface, pygame.color.Color(0, 255, 0), (x, y, width, height))
        hw = Arithmetic.lerp(0, width - 2, 1 - self.disphealth / self.maxhealth)
        if hw > 0:
            pygame.draw.rect(surface, pygame.color.Color(255, 0, 0), (x + 1, y + 1, hw, height - 2))

        if self.disphealth > self.health:
            self.sprayHealthParticles(x + hw, y, y + height)

        map(lambda par: par.tick(), self.particles)
        self.particles = [p for p in self.particles if not p.dead()]
        map(lambda par: par.draw(surface), self.particles)

    def draw_mass(self, surface, font, x, y):
        txt = font.render("Mass: %d" % self.mass, True, pygame.color.Color("#FFFFFF"))
        surface.blit(txt, (x, y))

    @property
    def alive(self):
        return self.health > 0

    @property
    def force(self):
        return self.mass * Constants.GRAVITY

    @property
    def mass(self):
        return self.rect.width * self.rect.height

    @property
    def maxhealth(self):
        return 5000.0

    def sprayHealthParticles(self, x, ymin, ymax):
        for i in xrange(randint(10, 20)):
            y = randint(ymin, ymax)
            print("YMN:{}\tYMX:{}\tY:{}".format(ymin, ymax, y))
            # angle = Arithmetic.lerpf(0.5 * pi, 1.5 * pi, float(y) / float(ymax - ymin))
            angle = Arithmetic.lerpf(5.0 / 6.0 * pi, 7.0 / 6.0 * pi, random())
            # print(angle)
            speed = random() * 4.0 + 1.0
            self.particles.append(FadingParticle([x, y], randint(1, 3), [speed * cos(angle), speed * sin(angle)], pygame.Color(0, 255, 0), 5))

    def tick(self, surface, delta, platforms):
        msgs = []
        if self.disphealth > self.health:
            self.disphealth = Arithmetic.clamp(self.health, self.maxhealth, self.disphealth - ceil((self.disphealth - self.health) / 30.0))

        # If alive, tick
        if self.health > 0:
            # Check for a resize
            if Keyboard.down(Constants.GROW_KEY):
                width = min(self.rect.width + Constants.SIZE_INTERVAL, Constants.MAX_PLAYER_WIDTH)
                height = min(self.rect.height + Constants.SIZE_INTERVAL, Constants.MAX_PLAYER_HEIGHT)
                self.image = pygame.transform.scale(self.image, (width, height)).convert_alpha()
                center = self.rect.center
                self.rect.size = self.image.get_rect().size
                self.rect.center = center
                self.__draw_image()
            elif Keyboard.down(Constants.SHRINK_KEY):
                width = max(Constants.MIN_PLAYER_WIDTH, self.rect.width - Constants.SIZE_INTERVAL)
                height = max(Constants.MIN_PLAYER_HEIGHT, self.rect.height - Constants.SIZE_INTERVAL)
                self.image = pygame.transform.scale(self.image, (width, height)).convert_alpha()
                center = self.rect.center
                self.rect.size = self.image.get_rect().size
                self.rect.center = center
                self.__draw_image()
            # If not in the center, fall to center of the screen
            if self.rect.centery < Constants.HEIGHT // 4:
                self.rect.y += math.ceil(Constants.GRAVITY / Constants.FPS * delta)
                self.rect.y = min(Constants.HEIGHT // 4, self.rect.y)
            else:
                self.ready = True
            # Check collision with platforms
            for p in pygame.sprite.spritecollide(self, platforms, False):
                if not p.can_break(self.force):
                    msgs.append(Message("Splat\n-%d" % self.health, self.rect.right + 100, self.rect.centery, "bad"))
                    self.health = 0
                    break
                elif p.can_splinter(self.force):
                    self.health = max(0, self.health - p.damage)
                    p.kill()
                    msgs.append(Message("Splinter\n-%d" % p.damage, self.rect.right + 100, self.rect.centery, "bad"))
                else:
                    p.kill()
        # If on screen, paint
        if self.rect.bottom > 0:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        return msgs
