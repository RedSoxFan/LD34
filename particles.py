import pygame
from utils import Arithmetic, Constants


class Particle(object):
    def __init__(self, pos, size, vel, col):
        self.pos = pos
        self.size = size
        self.vel = vel
        self.col = col

    def draw(self, surface):
        pygame.draw.circle(surface, self.col, [int(round(self.pos[0])), int(round(self.pos[1]))], self.size)

    def tick(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def dead(self):
        return not (0 <= self.pos[0] <= Constants.WIDTH and 0 <= self.pos[1] <= Constants.HEIGHT)


class FadingParticle(Particle):
    def __init__(self, pos, size, vel, col, fade):
        Particle.__init__(self, pos, size, vel, col)
        self.alpha = col.a
        self.fade = fade

    def tick(self):
        Particle.tick(self)
        self.alpha = Arithmetic.clamp(0.0, 255.0, self.alpha - self.fade)
        self.col.a = int(round(self.alpha))

    def dead(self):
        return Particle.dead(self) or self.alpha <= 0
