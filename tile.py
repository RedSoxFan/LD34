import pygame
from utils import Resources


class Tile(pygame.sprite.Sprite):
    SIZE = 20

    def __init__(self, x, y, imname="square-cross3.xpm", hueShift=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = Resources.load_colorized_image(imname, hueShift, (Tile.SIZE, Tile.SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def tick(self, delta, step):
        self.rect.y -= step

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

