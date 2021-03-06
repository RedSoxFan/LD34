import pygame
from tile import Tile
from platform import *
from utils import Arithmetic, Constants, Settings
from random import randint


class World:
    def __init__(self):
        self.fallen = 0
        self.fallStep = 5
        self.hueShift = 0
        self.hueStep = 3
        self.tilesUntilPlatform = 20
        self.lastPlatformWidth = 50
        self.tiles = []
        self.platforms = pygame.sprite.Group()

        self.regenTiles()

    def generatePlatform(self, width, col):
        y = self.tiles[-1].rect.top
        sideWidth = (Constants.WIDTH - 2 * Tile.SIZE - width) // 2

        l = UnbreakablePlatform(pygame.Rect(Tile.SIZE, y, sideWidth, Tile.SIZE), hueShift=self.hueShift)
        l.image = pygame.transform.flip(l.image, True, False)  # Horizontal flip to keep bad side against wall

        r = UnbreakablePlatform(pygame.Rect(Tile.SIZE + sideWidth + width, y, sideWidth, Tile.SIZE), hueShift=self.hueShift)
        self.platforms.add(l)
        self.platforms.add(r)

        dforce = (.6 * width) ** 2 * Constants.GRAVITY
        bforce = (.4 * width) ** 2 * Constants.GRAVITY
        plat = Platform(int(bforce), int(dforce), width, pygame.Rect(Tile.SIZE + sideWidth, y, width, Tile.SIZE))
        self.platforms.add(plat)

    def regenTiles(self):
        while len(self.tiles) == 0 or self.tiles[-1].rect.bottom <= Constants.HEIGHT + Tile.SIZE:
            bot = Tile.SIZE if len(self.tiles) == 0 else self.tiles[-1].rect.bottom
            col = pygame.Color(0)
            col.hsva = (360.0 + self.hueShift) % 360.0, 100, 100, 100
            map(self.tiles.append, [Tile(x, bot, hueShift=self.hueShift) for x in [0, Constants.WIDTH - Tile.SIZE]])
            self.hueShift = (self.hueShift + self.hueStep) % 360.0

            self.tilesUntilPlatform -= 1
            if self.tilesUntilPlatform == 0:
                self.tilesUntilPlatform = randint(40, 60)
                threshold = Arithmetic.lerp(70, 140, (self.tilesUntilPlatform - 50.0) / 20.0)
                width = randint(max(20, self.lastPlatformWidth - threshold),
                                min(self.lastPlatformWidth + threshold, 350))
                self.generatePlatform(width, col)
                self.lastPlatformWidth = width

        while self.tiles[0].rect.bottom < 0:
            self.tiles.pop(0)

    def tick(self, surface, delta):
        if delta > 0:
            self.fallen += self.fallStep
            self.fallStep += .001
            map(lambda t: t.tick(delta, self.fallStep), self.tiles)
            map(lambda p: p.step(self.fallStep), self.platforms)
            self.regenTiles()
            for plat in self.platforms:
                if plat.rect.bottom < 0:
                    self.platforms.remove(plat)
        if Settings.GRAPHICS >= 1:
            off = int(self.fallen % Constants.WIDTH)
            for y in xrange(50 - off, Constants.HEIGHT + 150, 25):
                if 0 < y < (Constants.HEIGHT + 150):
                    pygame.draw.line(surface, pygame.color.Color("#111111"), (0, y), (Constants.WIDTH, y - 150))
        map(lambda t: t.draw(surface), self.tiles)
        map(lambda t: t.tick(surface, delta), self.platforms)
