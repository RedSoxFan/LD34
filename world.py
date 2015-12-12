import pygame
from tile import Tile
from utils import Constants


class World:
    def __init__(self):
        self.fallen = 0
        self.fallStep = 5
        self.hueShift = 0
        self.hueStep = 3
        self.tiles = [Tile(x, y, pygame.Color(0, 255, 0)) for x in [0, Constants.WIDTH - Tile.SIZE] for y in xrange(0, Constants.HEIGHT, Tile.SIZE)]

    def tick(self, surface, delta):
        self.fallen += self.fallStep
        self.fallStep += .01
        map(lambda t: t.tick(surface, delta, self.fallStep), self.tiles)
        while self.tiles[-1].rect.bottom <= Constants.HEIGHT + Tile.SIZE:
            bot = self.tiles[-1].rect.bottom
            col = pygame.Color(0)
            col.hsva = (360.0 + self.hueShift) % 360.0, 100, 100, 100
            map(self.tiles.append, [Tile(x, bot, col) for x in [0, Constants.WIDTH - Tile.SIZE]])
            self.hueShift = (self.hueShift + self.hueStep) % 360.0
        while self.tiles[0].rect.bottom < 0:
            self.tiles.pop(0)
