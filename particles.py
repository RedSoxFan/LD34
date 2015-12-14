import pygame
from utils import Arithmetic, Constants, Settings
from math import *


class Particle(object):
    def __init__(self, pos, size, vel, col, mingfx=2):
        self.pos = pos
        self.size = size
        self.vel = vel
        self.col = col
        self.minfx = mingfx

    def draw(self, surface):
        pygame.draw.circle(surface, self.col, [int(round(self.pos[0])), int(round(self.pos[1]))], self.size)

    def tick(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def dead(self):
        return Settings.GRAPHICS < self.minfx or \
            not(0 <= self.pos[0] <= Constants.WIDTH and 0 <= self.pos[1] <= Constants.HEIGHT)


class FadingParticle(Particle):
    def __init__(self, pos, size, vel, col, fade, mingfx=2):
        Particle.__init__(self, pos, size, vel, col, mingfx=mingfx)
        self.alpha = col.a
        self.fade = fade

    def tick(self):
        Particle.tick(self)
        self.alpha = Arithmetic.clamp(0.0, 255.0, self.alpha - self.fade)
        self.col.a = int(round(self.alpha))

    def dead(self):
        return Particle.dead(self) or self.alpha <= 0


class FlippyLineParticle(Particle):
    def __init__(self, pos, size, vel, col, rot, rotRate, mingfx=2):
        Particle.__init__(self, pos, size, vel, col, mingfx=mingfx)
        self.rot = rot
        self.rotRate = rotRate

    def tick(self):
        Particle.tick(self)
        self.rot += self.rotRate

    def draw(self, surface):
        sx, ex = int(round(self.pos[0] - self.size * cos(self.rot))), int(round(self.pos[0] + self.size * cos(self.rot)))
        sy, ey = int(round(self.pos[1] - self.size * sin(self.rot))), int(round(self.pos[1] + self.size * sin(self.rot)))
        pygame.draw.line(surface, self.col, (sx, sy), (ex, ey))
