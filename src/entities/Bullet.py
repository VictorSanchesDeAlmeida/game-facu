import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed=10):
        super().__init__()
        self.image = pygame.transform.scale(image, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        
        # Remover bala se sair dos limites do level (31 colunas × 64 = 1984 pixels)
        if self.rect.x > 1984 or self.rect.x < -16:  # Largura do level expandido ou fora pela esquerda
            self.kill()
        if self.rect.y > 768 or self.rect.y < -16:   # Altura do level ou fora por cima
            self.kill()
    