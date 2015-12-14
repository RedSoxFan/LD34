import pygame
from utils import Graphics


class Tile(pygame.sprite.Sprite):
    SIZE = 20

    def __init__(self, x, y, hueShift=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((Tile.SIZE, Tile.SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        irect = self.image.get_rect()
        col = Graphics.hue_shift("#EE5400", hueShift)
        pygame.draw.rect(self.image, col, (0, 0, irect.width, irect.height), 1)
        pygame.draw.line(self.image, col, (irect.width // 2, 0), (irect.width // 2, irect.height), 1)
        pygame.draw.line(self.image, col, (0, irect.height // 2), (irect.width, irect.height // 2), 1)

    def tick(self, delta, step):
        self.rect.y -= step

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
