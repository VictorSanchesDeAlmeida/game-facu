import pygame
import json
import os
from config import GRAVITY

class Demon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Inicializar atributos básicos primeiro
        self.facing_right = True
        self.current_animation = "idle"
        self.current_frame = 0
        self.frame_timer = 0
        
        # Carregar configuração de animação
        self.load_animation_config()
        
        # Configurar sprite inicial
        self.animation_speed = self.animations[self.current_animation]["frameDuration"]
        
        # Imagem e posição
        self.image = self.get_current_frame_image()
        self.rect = self.image.get_rect(center=(x, y))
        
        # Física
        self.speed_x = 1
        self.speed_y = 0
        self.on_ground = False
        
        # IA
        self.direction = 1  # 1 para direita, -1 para esquerda
        self.patrol_range = 128  # pixels de patrulha
        self.start_x = x
        self.detection_range = 200  # pixels para detectar player
        self.state = "patrol"  # patrol, chase, prepare_attack, attack
        
        # Combate
        self.health = 3
        self.damage = 1
        self.attack_cooldown = 0
        self.prepare_attack_timer = 0  # Timer para preparar ataque
        
    def load_animation_config(self):
        config_path = os.path.join("src", "sprite", "Demon.json")
        
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
            self.spritesheet = pygame.Surface((128, 32))
            self.spritesheet.fill((150, 0, 0))  # Vermelho escuro
            self.animations = {
                "idle": {
                    "frames": [{"x": 0, "y": 0, "width": 32, "height": 32}],
                    "frameDuration": 100
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
        
        # Escalar para 64x64 para consistência
        scaled_frame = pygame.transform.scale(frame_surface, (64, 64))
        
        # Flipar se necessário
        if not self.facing_right:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)
            
        return scaled_frame
    
    def update_animation(self):
        self.frame_timer += 1
        
        # Ajustar velocidade baseada na animação
        speed_divisor = 4 if self.current_animation == "attack" else 10
        
        if self.frame_timer >= self.animation_speed // speed_divisor:
            self.frame_timer = 0
            animation = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(animation["frames"])
            self.image = self.get_current_frame_image()
    
    def update(self, player_pos=None):
        # Atualizar animação
        self.update_animation()
        
        # Atualizar cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            # Se estava atacando e cooldown acabou, voltar ao estado normal
            if self.attack_cooldown == 0 and self.state == "attack":
                self.state = "idle"  # Estado temporário antes de decidir próxima ação
        
        if self.prepare_attack_timer > 0:
            self.prepare_attack_timer -= 1
        
        # IA baseada no estado
        if player_pos:
            self.update_ai(player_pos)
        else:
            self.set_animation("idle")
            self.patrol()
        
        # Se não está se movendo e não está em estados especiais, usar animação idle
        if self.speed_x == 0 and self.state not in ["attack", "prepare_attack"]:
            self.set_animation("idle")
            
        # Aplicar movimento
        self.rect.x += self.speed_x
        
        # Aplicar gravidade
        self.apply_gravity()
    
    def update_ai(self, player_pos):
        distance_to_player = abs(self.rect.centerx - player_pos[0])
        distance_vertical = abs(self.rect.centery - player_pos[1])
        
        # Verificar se player está muito próximo para atacar
        # Player: 37x57, Demon: 64x64 - distância para toque: ~51 pixels
        if distance_to_player <= 55 and distance_vertical <= 32:
            if self.attack_cooldown <= 0:
                if self.state != "prepare_attack" and self.state != "attack":
                    # Começar preparação para atacar
                    self.state = "prepare_attack"
                    self.set_animation("idle")
                    self.speed_x = 0  # Parar completamente
                    self.prepare_attack_timer = 10  # Meio segundo de preparação
                    # Olhar na direção do player
                    if self.rect.centerx < player_pos[0]:
                        self.facing_right = True
                    else:
                        self.facing_right = False
                elif self.state == "prepare_attack":
                    if self.prepare_attack_timer <= 0:
                        # Executar ataque
                        self.state = "attack"
                        self.set_animation("attack")
                        self.speed_x = 0  # Continuar parado durante ataque
                        self.attack_cooldown = 90  # Cooldown maior (1.5 segundos)
                elif self.state == "attack":
                    # Manter parado durante animação de ataque
                    self.speed_x = 0
                    # A animação de ataque continua até o cooldown acabar
                    # Não mudar de estado durante o ataque
            else:
                # Em cooldown após ataque, ficar parado olhando para o player
                if self.state == "attack":
                    # Manter animação de ataque até o cooldown acabar
                    self.speed_x = 0
                else:
                    # Em cooldown normal, usar idle
                    self.speed_x = 0
                    self.set_animation("idle")
                    # Continuar olhando na direção do player
                    if self.rect.centerx < player_pos[0]:
                        self.facing_right = True
                    else:
                        self.facing_right = False
        elif distance_to_player <= self.detection_range:
            # Player detectado mas não muito próximo - perseguir (só se não estiver atacando)
            if self.state != "attack" and self.attack_cooldown <= 0:
                self.state = "chase"
                self.set_animation("walk")
                if self.rect.centerx < player_pos[0]:
                    self.direction = 1
                    self.facing_right = True
                else:
                    self.direction = -1
                    self.facing_right = False
                
                self.speed_x = self.direction * 2  # Velocidade de perseguição
        else:
            # Player fora de alcance - patrulhar (só se não estiver atacando)
            if self.state != "attack" and self.attack_cooldown <= 0:
                self.state = "patrol"
                self.set_animation("walk")
                self.patrol()
    
    def set_animation(self, animation_name):
        if animation_name in self.animations and self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_timer = 0
            self.animation_speed = self.animations[animation_name]["frameDuration"]
    
    def patrol(self):
        # Verificar se chegou no limite da patrulha
        if abs(self.rect.centerx - self.start_x) >= self.patrol_range:
            self.direction *= -1
            self.facing_right = not self.facing_right
        
        self.speed_x = self.direction * 1  # Velocidade de patrulha
    
    def apply_gravity(self):
        self.speed_y += GRAVITY
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True  # Morreu
        return False  # Ainda vivo
    
    def get_collision_rect(self):
        return pygame.Rect(self.rect.x + 8, self.rect.y + 8, 
                          self.rect.width - 16, self.rect.height - 8)
    
    def push_away(self, direction):
        push_force = 2  # Força de empurrão mais suave
        self.rect.x += direction * push_force
        
        # Se for empurrado durante patrulha, pode mudar direção temporariamente
        if self.state == "patrol" and abs(direction) > 0:
            # Parar movimento por um momento ao colidir
            self.speed_x = 0