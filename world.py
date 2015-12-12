import pygame
from tile import Tile
from platform import *
from utils import Arithmetic, Constants
from random import randint


class World:
    def __init__(self):
        self.fallen = 0
        self.fallStep = 5
        self.hueShift = 0
        self.hueStep = 3
        self.tilesUntilPlatform = 20
        self.lastPlatformWidth = 50
        self.tiles = [Tile(x, y, pygame.Color(0, 255, 0)) for x in [0, Constants.WIDTH - Tile.SIZE] for y in xrange(0, Constants.HEIGHT, Tile.SIZE)]
        self.platforms = pygame.sprite.Group()

    def generatePlatform(self, width, col):
        y = self.tiles[-1].rect.top
        sideWidth = (Constants.WIDTH - 2 * Tile.SIZE - width) // 2

        l = UnbreakablePlatform(pygame.color.Color("#FFFFFF"), pygame.Rect(Tile.SIZE, y, sideWidth, Tile.SIZE))
        r = UnbreakablePlatform(pygame.color.Color("#FFFFFF"), pygame.Rect(Tile.SIZE + sideWidth + width, y, sideWidth, Tile.SIZE))
        self.platforms.add(l)
        self.platforms.add(r)

        dforce = (.75*width)**2 * Constants.GRAVITY
        bforce = (.5*width)**2 * Constants.GRAVITY
        plat = Platform(pygame.Color("#FF0000"), int(bforce), int(dforce), width, pygame.Rect(Tile.SIZE + sideWidth, y, width, Tile.SIZE))
        self.platforms.add(plat)

    def tick(self, surface, delta):
        if delta > 0:
            self.fallen += self.fallStep
            self.fallStep += .005
            map(lambda t: t.tick(delta, self.fallStep), self.tiles)
            map(lambda p: p.step(self.fallStep), self.platforms)
            while self.tiles[-1].rect.bottom <= Constants.HEIGHT + Tile.SIZE:
                bot = self.tiles[-1].rect.bottom
                col = pygame.Color(0)
                col.hsva = (360.0 + self.hueShift) % 360.0, 100, 100, 100
                map(self.tiles.append, [Tile(x, bot, col) for x in [0, Constants.WIDTH - Tile.SIZE]])
                self.hueShift = (self.hueShift + self.hueStep) % 360.0

                self.tilesUntilPlatform -= 1
                if self.tilesUntilPlatform == 0:
                    self.tilesUntilPlatform = randint(50, 70)
                    threshold = Arithmetic.lerp(100, 175, (self.tilesUntilPlatform - 50.0) / 20.0)
                    width = randint(max(20, self.lastPlatformWidth - threshold),
                                    min(self.lastPlatformWidth + threshold, 350))
                    self.generatePlatform(width, col)
                    self.lastPlatformWidth = width

            while self.tiles[0].rect.bottom < 0:
                self.tiles.pop(0)
            for plat in self.platforms:
                if plat.rect.bottom < 0:
                    self.platforms.remove(plat)
        map(lambda t: t.draw(surface), self.tiles)
        map(lambda t: t.tick(surface, delta), self.platforms)
