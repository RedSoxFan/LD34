import pygame
from tile import Tile
from platform import *
from utils import Arithmetic, Constants
from random import randint
from Box2D import *


class World:
    def __init__(self):
        self.b2dworld = b2World()

        self.testbox = self.b2dworld.CreateDynamicBody(position=(5, 10))
        self.testbox.CreatePolygonFixture(box=(2, 2), density=1, friction=0.3)

        self.fallen = 0
        self.fallStep = 2
        self.hueShift = 0
        self.hueStep = 3
        self.tilesUntilPlatform = 20
        self.lastPlatformWidth = 50
        # self.tiles = [Tile(x, y, pygame.Color(0, 255, 0)) for x in [0, Constants.WIDTH - Tile.SIZE] for y in xrange(0, Constants.HEIGHT, Tile.SIZE)]
        self.tiles = []
        self.platforms = pygame.sprite.Group()
        self.regenTiles()

    def generatePlatform(self, width, col):
        y = self.tiles[-1].rect.top
        sideWidth = (Constants.WIDTH - 2 * Tile.SIZE - width) // 2

        l = UnbreakablePlatform(pygame.color.Color("#FFFFFF"), pygame.Rect(Tile.SIZE, y, sideWidth, Tile.SIZE))
        r = UnbreakablePlatform(pygame.color.Color("#FFFFFF"), pygame.Rect(Tile.SIZE + sideWidth + width, y, sideWidth, Tile.SIZE))
        self.platforms.add(l)
        self.platforms.add(r)

        l.body = self.b2dworld.CreateStaticBody(position=(Arithmetic.pixToB2d(l.rect.x), Arithmetic.pixToB2d(l.rect.y)))
        l.body.CreatePolygonFixture(box=(Arithmetic.pixToB2d(l.rect.width), Arithmetic.pixToB2d(l.rect.height)), density=1, friction=0.3)

        r.body = self.b2dworld.CreateStaticBody(position=(Arithmetic.pixToB2d(r.rect.x), Arithmetic.pixToB2d(r.rect.y)))
        r.body.CreatePolygonFixture(box=(Arithmetic.pixToB2d(r.rect.width), Arithmetic.pixToB2d(r.rect.height)), density=1, friction=0.3)

        dforce = (.75 * width) ** 2 * Constants.GRAVITY
        bforce = (.5 * width) ** 2 * Constants.GRAVITY
        plat = Platform(pygame.Color("#FF0000"), int(bforce), int(dforce), width, pygame.Rect(Tile.SIZE + sideWidth, y, width, Tile.SIZE))
        self.platforms.add(plat)

    def regenTiles(self):
        while len(self.tiles) == 0 or self.tiles[-1].rect.bottom <= Constants.HEIGHT + Tile.SIZE:
            bot = Tile.SIZE if len(self.tiles) == 0 else self.tiles[-1].rect.bottom
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

    def tick(self, surface, delta):
        self.b2dworld.Step(Constants.TIME_STEP, 10, 10)

        for body in self.b2dworld.bodies:
            for fixture in body.fixtures:
                shape = fixture.shape
                vertices = [(body.transform * v) * Constants.PPM for v in shape.vertices]
                # vertices = [(v[0], Constants.HEIGHT - v[1]) for v in vertices]
                pygame.draw.polygon(surface, pygame.Color("#FF00FF"), vertices)
        if delta > 0:
            self.fallen += self.fallStep
            self.fallStep += .005
            map(lambda t: t.tick(delta, self.fallStep), self.tiles)
            map(lambda p: p.step(self.fallStep), self.platforms)
            self.regenTiles()
            for plat in self.platforms:
                if plat.rect.bottom < 0:
                    self.b2dworld.DestroyBody(plat.body)
                    self.platforms.remove(plat)
        map(lambda t: t.draw(surface), self.tiles)
        map(lambda t: t.tick(surface, delta), self.platforms)
