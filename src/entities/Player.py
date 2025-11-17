import pygame

from config import GRAVITY
from entities.Bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, image, x=400, y=300):
        super().__init__()

        self.original_image = pygame.transform.scale(image, (37, 57)) 
        self.image_right = self.original_image
        self.image_left = pygame.transform.flip(self.original_image, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = 5

        self.speed_y = 0
        self.on_ground = False
        self.facing_right = True  

        self.shoot_cooldown = 0
        self.shoot_delay = 10 
    
        self.muzzle_flash_timer = 0
        self.muzzle_flash_duration = 3
        
        # Sistema de dano
        self.health = 5
        self.invincible_timer = 0
        self.invincible_duration = 60  # 1 segundo de invencibilidade

    def update(self, keys_pressed):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= 1
            
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.facing_right:
                self.facing_right = False
                self.image = self.image_left
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if not self.facing_right:
                self.facing_right = True
                self.image = self.image_right
        if keys_pressed[pygame.K_UP]:
            self.jump()
        
        if keys_pressed[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            return self.bullet_fire()
        
        return None

    def jump(self):
        if self.on_ground:
            self.speed_y = -16
            self.on_ground = False

    def apply_gravity(self):
        self.speed_y += GRAVITY

    def draw_muzzle_flash(self, screen, camera_x, camera_y):
        if self.muzzle_flash_timer > 0:
            flash_size = 8
            flash_offset = self.rect.width // 2 + flash_size if self.facing_right else -(self.rect.width // 2 + flash_size)
            flash_x = self.rect.centerx + flash_offset - camera_x
            flash_y = self.rect.centery - camera_y
            
            pygame.draw.circle(screen, (255, 255, 150), (int(flash_x), int(flash_y)), flash_size)
            pygame.draw.circle(screen, (255, 200, 0), (int(flash_x), int(flash_y)), flash_size // 2)

    def bullet_fire(self):
        bullet_image = pygame.Surface((12, 4))
        bullet_image.fill((255, 255, 0))
        
        sprite_half_width = self.rect.width // 2
        offset_x = sprite_half_width + 6 if self.facing_right else -(sprite_half_width + 6)
        speed = 12 if self.facing_right else -12
        
        bullet_sprite = Bullet(bullet_image, self.rect.centerx + offset_x, self.rect.centery, speed=speed)
        
        if not self.facing_right:
            bullet_sprite.image = pygame.transform.flip(bullet_sprite.image, True, False)
        
        self.shoot_cooldown = self.shoot_delay
        self.muzzle_flash_timer = self.muzzle_flash_duration
        
        return bullet_sprite

    def take_damage(self, damage):
        """Recebe dano se não estiver invencível"""
        if self.invincible_timer <= 0:
            self.health -= damage
            self.invincible_timer = self.invincible_duration
            print(f"Player levou {damage} de dano! Vida restante: {self.health}")
            
            if self.health <= 0:
                print("Game Over!")
                # Aqui você pode adicionar lógica de game over
            
            return True  # Dano foi aplicado
        return False  # Player estava invencível
        