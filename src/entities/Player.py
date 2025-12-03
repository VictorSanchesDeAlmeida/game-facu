import pygame
import json
import os

from config import GRAVITY
from entities.Bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, image, x=400, y=300):
        super().__init__()

        # Inicializar atributos de animação primeiro
        self.facing_left = False  # Player inicia olhando para a esquerda
        self.current_animation = "idle"
        self.current_frame = 0
        self.frame_timer = 0
        
        # Carregar configuração de animação
        self.load_animation_config()
        
        # Configurar sprite inicial
        self.animation_speed = self.animations[self.current_animation]["frameDuration"]
        
        # Imagem e posição usando o sistema de animação
        self.image = self.get_current_frame_image()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

        self.speed_y = 0
        self.on_ground = False
        self.is_moving = False  # Para controlar animação de caminhada

        self.shoot_cooldown = 0
        self.shoot_delay = 10 
    
        self.muzzle_flash_timer = 0
        self.muzzle_flash_duration = 3
        
        # Sistema de dano
        self.health = 5
        self.invincible_timer = 0
        self.invincible_duration = 60  # 1 segundo de invencibilidade

    def load_animation_config(self):
        config_path = os.path.join("src", "sprite", "Player.json")
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Carregar spritesheet
            spritesheet_path = os.path.join("assets", config["spriteSheet"])
            self.spritesheet = pygame.image.load(spritesheet_path)
            
            # Processar animações
            self.animations = {}
            for sprite_config in config["sprites"]:
                name = sprite_config["name"]
                self.animations[name] = {
                    "frames": sprite_config["frames"],
                    "frameDuration": sprite_config["frameDuration"]
                }
                
        except FileNotFoundError:
            # Fallback para uma imagem simples se não encontrar o arquivo
            self.spritesheet = pygame.Surface((37, 57))
            self.spritesheet.fill((0, 100, 200))  # Azul para o player
            self.animations = {
                "idle": {
                    "frames": [{"x": 0, "y": 0, "width": 37, "height": 57}],
                    "frameDuration": 100
                },
                "walk": {
                    "frames": [{"x": 0, "y": 0, "width": 37, "height": 57}],
                    "frameDuration": 80
                }
            }
    
    def get_current_frame_image(self):
        animation = self.animations[self.current_animation]
        frame_data = animation["frames"][self.current_frame]
        
        # Extrair frame do spritesheet
        frame_rect = pygame.Rect(frame_data["x"], frame_data["y"], 
                                frame_data["width"], frame_data["height"])
        frame_surface = pygame.Surface((frame_data["width"], frame_data["height"]), pygame.SRCALPHA)
        frame_surface.blit(self.spritesheet, (0, 0), frame_rect)
        
        # Escalar para 37x57 para manter o tamanho original do player
        scaled_frame = pygame.transform.scale(frame_surface, (37, 57))
        
        # Flipar se necessário (frames originais olham para a esquerda)
        if not self.facing_left:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)
            
        return scaled_frame
    
    def update_animation(self):
        self.frame_timer += 1
        
        # Velocidade da animação
        speed_divisor = 10
        
        if self.frame_timer >= self.animation_speed // speed_divisor:
            self.frame_timer = 0
            animation = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(animation["frames"])
            self.image = self.get_current_frame_image()
    
    def set_animation(self, animation_name):
        if animation_name in self.animations and self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_timer = 0
            self.animation_speed = self.animations[animation_name]["frameDuration"]

    def update(self, keys_pressed):
        # Atualizar animação
        self.update_animation()
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= 1
            
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        # Resetar flag de movimento
        self.is_moving = False
        
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.is_moving = True
            if not self.facing_left:
                self.facing_left = True
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.is_moving = True
            if self.facing_left:
                self.facing_left = False
        if keys_pressed[pygame.K_UP]:
            self.jump()
        
        # Controlar animação baseado no movimento
        if self.is_moving:
            self.set_animation("walk")
        else:
            self.set_animation("idle")
        
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
            flash_offset = -(self.rect.width // 2 + flash_size) if self.facing_left else (self.rect.width // 2 + flash_size)
            flash_x = self.rect.centerx + flash_offset - camera_x
            flash_y = self.rect.centery - camera_y
            
            pygame.draw.circle(screen, (255, 255, 150), (int(flash_x), int(flash_y)), flash_size)
            pygame.draw.circle(screen, (255, 200, 0), (int(flash_x), int(flash_y)), flash_size // 2)

    def bullet_fire(self):
        bullet_image = pygame.Surface((12, 4))
        bullet_image.fill((255, 255, 0))
        
        sprite_half_width = self.rect.width // 2
        offset_x = -(sprite_half_width + 6) if self.facing_left else (sprite_half_width + 6)
        speed = -12 if self.facing_left else 12
        
        bullet_sprite = Bullet(bullet_image, self.rect.centerx + offset_x, self.rect.centery, speed=speed)
        
        if not self.facing_left:
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
        