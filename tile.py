import pygame


class Tile(pygame.sprite.Sprite):
    SIZE = 48

    def __init__(self, x, y, col):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((48, 48))
        self.image.fill(col)
        self.rect = self.image.get_rect()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def tick(self, delta, step):
        self.rect.y -= step

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

