import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size=64):
        super().__init__()
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))