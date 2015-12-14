#!/usr/bin/python2
# -*- coding: utf-8 -*-

from math import *
from random import *
from audio import Sound

from input import Keyboard
from messages import Message
from particles import *
from tile import Tile
from utils import Graphics


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
        self.sploded = False
        self.innerfire = True

    def __draw_image(self):
        self.image.fill(pygame.color.Color(0, 0, 0, 0))
        irect = self.image.get_rect()
        col = Graphics.hue_shift("#EE5400", 100)
        ashift = 255.0 / (irect.width * 0.125)
        a = col.a
        i = 0
        while a > 0:
            pygame.draw.rect(self.image, col, (i, i, irect.width - 2 * i, irect.height - 2 * i), 2)
            i += 1
            a = Arithmetic.clamp(0, 255, a - ashift)
            col.a = int(a)

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
            angle = Arithmetic.lerpf(5.0 / 6.0 * pi, 7.0 / 6.0 * pi, random())
            speed = random() * 4.0 + 1.0
            self.particles.append(FadingParticle([x, y], randint(1, 3), [speed * cos(angle), speed * sin(angle)], pygame.Color(0, 255, 0), 5))

    def destroyPlatform(self, plat, splinter):
        y = plat.rect.centery
        for x in range(plat.rect.left + Tile.SIZE // 2, plat.rect.right, Tile.SIZE):
            for i in range(4):
                speed = random() * 5.0 + 5.0
                angle = Arithmetic.lerpf(1.25 * pi, 1.75 * pi, random())
                rotRate = random() * (0.5 * pi) - (0.25 * pi)
                size = randint(3, 17 if splinter else 7)
                self.particles.append(FlippyLineParticle([x, y], size, [speed * cos(angle), -speed * sin(angle)], plat.col, random() * 2.0 * pi, rotRate, mingfx=1))

    def generateInnerFire(self):
        # Spawn a bunch of inner particles
        for i in xrange(randint(25, 50)):
            side = randint(0, 3)  # pick a side
            # a and b will become x and y of the particle
            a = bmin = bmax = 0
            off = 2
            if side == 0:  # top side
                a, bmin, bmax = self.rect.top + off, self.rect.left + off, self.rect.right - off
            elif side == 1:  # right side
                a, bmin, bmax = self.rect.right - off, self.rect.top + off, self.rect.bottom - off
            elif side == 2:  # bottom side
                a, bmin, bmax = self.rect.bottom - off, self.rect.left + off, self.rect.right - off
            elif side == 3:  # left side
                a, bmin, bmax = self.rect.left + off, self.rect.top + off, self.rect.bottom - off

            # At really small sizes (aka death sequence), these might switch
            if bmin > bmax:
                bmin, bmax = bmax, bmin

            b = randint(bmin, bmax)

            # a and b may need to be swapped depending on the side of the square
            pos = [a, b] if side % 2 != 0 else [b, a]

            # Direct the fire toward the center of the square
            angle = atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx) + pi
            speed = random() * 2.0 + 1.0
            size = randint(1, 3)
            col = pygame.Color(0, 255, 0)
            self.particles.append(FadingParticle(pos, size, [speed * cos(angle), speed * sin(angle)], col, 255 * 10.0 / self.rect.width))

    def tick(self, surface, delta, platforms):
        msgs = []
        if self.disphealth > self.health:
            self.disphealth = Arithmetic.clamp(self.health, self.maxhealth, self.disphealth - ceil((self.disphealth - self.health) / 30.0))

        if Settings.GRAPHICS >= 2 and self.innerfire:
            self.generateInnerFire()

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
                self.rect.y += ceil(Constants.GRAVITY / Constants.FPS * delta)
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
                    Sound.play('hit{}'.format(randint(1, 3)))
                    self.health = max(0, self.health - p.damage)
                    self.destroyPlatform(p, True)
                    p.kill()
                    msgs.append(Message("Splinter\n-%d" % p.damage, self.rect.right + 100, self.rect.centery, "bad"))
                else:
                    Sound.play('hit{}'.format(randint(1, 3)))
                    self.destroyPlatform(p, False)
                    p.kill()
        else:
            # Death sequence
            if self.rect.width > 2:
                # Shrink until tiny
                width = Arithmetic.clamp(2, Constants.MAX_PLAYER_WIDTH, self.rect.width - 3 * Constants.SIZE_INTERVAL)
                height = Arithmetic.clamp(2, Constants.MAX_PLAYER_HEIGHT, self.rect.height - 3 * Constants.SIZE_INTERVAL)
                self.image = pygame.transform.scale(self.image, (width, height)).convert_alpha()
                center = self.rect.center
                self.rect.size = self.image.get_rect().size
                self.rect.center = center
                self.__draw_image()
            elif not self.sploded:
                # splode
                Sound.play('explode')
                self.sploded = True
                self.innerfire = False
                self.image.fill(pygame.Color(0, 0, 0))

                # Line particles
                for i in xrange(randint(20, 40)):
                    angle = random() * 2.0 * pi
                    speed = random() * 5.0 + 2.5
                    rotRate = random() * (0.5 * pi) - (0.25 * pi)
                    size = randint(3, 17)
                    self.particles.append(FlippyLineParticle([self.rect.center[0], self.rect.center[1]], size, [speed * cos(angle), speed * sin(angle)], pygame.Color(0, 255, 0), random() * 2.0 * pi, rotRate, mingfx=1))

                # Fire particles
                for i in xrange(randint(200, 500)):
                    angle = random() * 2.0 * pi
                    speed = random() * 5.0 + 1.0
                    size = randint(1, 3)
                    self.particles.append(FadingParticle([self.rect.center[0], self.rect.center[1]], size, [speed * cos(angle), speed * sin(angle)], pygame.Color(0, 255, 0), 6, mingfx=1))

        # If on screen, paint
        if self.rect.bottom > 0:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        return msgs
