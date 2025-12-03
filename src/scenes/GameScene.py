import pygame
from scenes.Scene import Scene
from entities.Player import Player
from levels.Level_1 import Level_1
from utils.assets_loader import load_image
from hud.HUD import HUD
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # Inicializar componentes do jogo
        image_player = load_image("player.png")
        self.player = Player(image_player, 150, 650)
        self.all_sprites = pygame.sprite.Group()
        
        # Criar o level
        self.level = Level_1(game)
        self.all_sprites.add(self.level.blocks)
        
        # Grupo para as balas
        self.bullets = pygame.sprite.Group()
        
        # Obter inimigos do level
        self.enemies = self.level.get_enemies()
        
        # HUD
        self.hud = HUD()
        
        # Sistema de câmera
        self.camera_x = 0
        self.camera_y = 0
        self.camera_smooth = 0.1
        
        # Dimensões do level (31 colunas x 12 linhas, cada tile 64x64)
        self.level_width = 31 * 64  # 1984 pixels
        self.level_height = 12 * 64  # 768 pixels
        
        # Variáveis para Game Over
        self.game_over = False
        self.killer_demon = None
        self.killer_taunt = ""  # Texto fixo do demon que matou
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    # Reiniciar jogo
                    self.next_scene = GameScene(self.game)
                elif event.key == pygame.K_ESCAPE:
                    # Voltar ao menu
                    from scenes.MenuScene import MenuScene
                    self.next_scene = MenuScene(self.game)
    
    def update(self):
        if self.game_over:
            return
            
        keys_pressed = pygame.key.get_pressed()
        
        # Atualizar player e capturar bala se disparada
        bullet = self.player.update(keys_pressed)
        if bullet:
            self.bullets.add(bullet)
        
        # Aplicar gravidade
        self.player.apply_gravity()
        
        # Atualizar inimigos
        for enemy in self.enemies:
            enemy.update(player_pos=(self.player.rect.centerx, self.player.rect.centery))
        
        # Verificar colisões entre personagens
        self.check_character_collisions()
        
        # Verificar ataques de demons
        self.check_demon_attacks()
        
        # Verificar colisões entre player e blocos
        self.check_collisions()
        
        # Atualizar câmera
        self.update_camera()
        
        # Atualizar balas
        self.bullets.update()
        
        # Verificar colisões entre balas e blocos
        self.check_bullet_collisions()
        
        # Verificar colisões com inimigos
        self.check_enemy_collisions()
        
        # Verificar Game Over
        if self.player.health <= 0 and not self.game_over:
            self.game_over = True
            # Encontrar o demon mais próximo como "killer"
            closest_demon = None
            closest_distance = float('inf')
            for enemy in self.enemies:
                distance = abs(self.player.rect.centerx - enemy.rect.centerx)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_demon = enemy
            
            self.killer_demon = closest_demon
            
            # Escolher um texto provocativo fixo
            if self.killer_demon:
                import random
                taunts = [
                    "Você é muito fraco, humano!",
                    "Suas habilidades são patéticas!",
                    "Que decepção... Esperava mais!",
                    "Treine mais da próxima vez!",
                    "Você não passa de comida para mim!",
                    "Hahaha! Muito fácil!",
                    "Isso foi... decepcionante.",
                    "Nem valeu a pena lutar!",
                    "Você precisa treinar MUITO mais!"
                ]
                self.killer_taunt = random.choice(taunts)
        
        # Verificar Vitória - todos os demônios foram derrotados
        if len(self.enemies) == 0 and not self.game_over:
            from scenes.VictoryScene import VictoryScene
            self.next_scene = VictoryScene(self.game)
        
        self.all_sprites.update()
    
    def draw(self, screen):
        screen.fill((30, 30, 30))
        
        # Desenhar todos os sprites com offset da câmera
        for sprite in self.all_sprites:
            screen_rect = sprite.rect.copy()
            screen_rect.x -= self.camera_x
            screen_rect.y -= self.camera_y
            screen.blit(sprite.image, screen_rect)
        
        # Desenhar o player com offset da câmera
        if not self.game_over:
            player_screen_rect = self.player.rect.copy()
            player_screen_rect.x -= self.camera_x
            player_screen_rect.y -= self.camera_y
            
            # Efeito de invencibilidade (piscar)
            if self.player.invincible_timer > 0 and self.player.invincible_timer % 10 < 5:
                pass  # Não desenhar o player (efeito piscar)
            else:
                screen.blit(self.player.image, player_screen_rect)
            
            # Desenhar efeito muzzle flash
            self.player.draw_muzzle_flash(screen, self.camera_x, self.camera_y)
        
        # Desenhar inimigos com offset da câmera
        for enemy in self.enemies:
            enemy_screen_rect = enemy.rect.copy()
            enemy_screen_rect.x -= self.camera_x
            enemy_screen_rect.y -= self.camera_y
            screen.blit(enemy.image, enemy_screen_rect)
        
        # Desenhar as balas com offset da câmera
        for bullet in self.bullets:
            bullet_screen_rect = bullet.rect.copy()
            bullet_screen_rect.x -= self.camera_x
            bullet_screen_rect.y -= self.camera_y
            screen.blit(bullet.image, bullet_screen_rect)
        
        # Desenhar HUD
        if not self.game_over:
            self.hud.draw(screen, self.player, len(self.enemies))
        
        # Desenhar tela de Game Over
        if self.game_over:
            self.draw_game_over(screen)
    
    def draw_game_over(self, screen):
        # Overlay semi-transparente
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Título Game Over
        font_title = pygame.font.Font(None, 96)
        game_over_text = font_title.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(game_over_text, game_over_rect)
        
        # Desenhar o demon killer (com animação idle)
        if self.killer_demon:
            # Forçar animação idle e continuar atualizando
            self.killer_demon.set_animation("idle")
            self.killer_demon.speed_x = 0  # Parar movimento
            self.killer_demon.update_animation()  # Continuar animação
            
            # Pegar imagem atual da animação e escalar
            killer_image = self.killer_demon.image.copy()
            killer_scaled = pygame.transform.scale(killer_image, (96, 96))
            
            # Posicionar o demon no centro-esquerda
            demon_rect = killer_scaled.get_rect(center=(screen.get_width() // 4, 250))
            screen.blit(killer_scaled, demon_rect)
            
            # Desenhar balão de fala atrás do texto
            bubble_rect = pygame.Rect(screen.get_width() // 2 - 200, 200, 400, 80)
            pygame.draw.rect(screen, (40, 40, 40), bubble_rect)
            pygame.draw.rect(screen, (255, 200, 100), bubble_rect, 3)
            
            # Desenhar "pontinha" do balão de fala
            bubble_tip = [
                (bubble_rect.left, bubble_rect.centery),
                (bubble_rect.left - 15, bubble_rect.centery - 10),
                (bubble_rect.left - 15, bubble_rect.centery + 10)
            ]
            pygame.draw.polygon(screen, (40, 40, 40), bubble_tip)
            pygame.draw.polygon(screen, (255, 200, 100), bubble_tip, 3)
            
            # Mensagem provocativa fixa do demon
            font_taunt = pygame.font.Font(None, 36)
            taunt_text = font_taunt.render(self.killer_taunt, True, (255, 255, 255))
            taunt_rect = taunt_text.get_rect(center=bubble_rect.center)
            screen.blit(taunt_text, taunt_rect)
        
        # Instruções
        font_instructions = pygame.font.Font(None, 32)
        instructions = [
            "Pressione R para tentar novamente",
            "Pressione ESC para voltar ao menu"
        ]
        
        y_offset = 400
        for instruction in instructions:
            text = font_instructions.render(instruction, True, (200, 200, 200))
            text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40
    
    # Métodos de colisão (copiados do game.py original)
    def update_camera(self):
        target_camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        target_camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2
        
        target_camera_x = max(0, min(target_camera_x, self.level_width - SCREEN_WIDTH))
        target_camera_y = max(0, min(target_camera_y, self.level_height - SCREEN_HEIGHT))
        
        self.camera_x += (target_camera_x - self.camera_x) * self.camera_smooth
        self.camera_y += (target_camera_y - self.camera_y) * self.camera_smooth

    def check_collisions(self):
        # Reset on_ground no início de cada frame
        self.player.on_ground = False
        
        # Colisão horizontal
        collisions = pygame.sprite.spritecollide(self.player, self.level.blocks, False)
        for block in collisions:
            if self.player.rect.centerx < block.rect.centerx:
                self.player.rect.right = block.rect.left
            else:
                self.player.rect.left = block.rect.right
        
        # Aplicar movimento vertical
        self.player.rect.y += self.player.speed_y
        
        # Colisão vertical
        collisions = pygame.sprite.spritecollide(self.player, self.level.blocks, False)
        for block in collisions:
            if self.player.speed_y > 0:  # Caindo
                self.player.rect.bottom = block.rect.top
                self.player.speed_y = 0
                self.player.on_ground = True
            elif self.player.speed_y < 0:  # Subindo
                self.player.rect.top = block.rect.bottom
                self.player.speed_y = 0
        
        # Verificar limites da tela (chão de emergência)
        if self.player.rect.bottom > SCREEN_HEIGHT:
            self.player.rect.bottom = SCREEN_HEIGHT
            self.player.speed_y = 0
            self.player.on_ground = True

    def check_bullet_collisions(self):
        for bullet in self.bullets:
            collisions = pygame.sprite.spritecollide(bullet, self.level.blocks, False)
            if collisions:
                bullet.kill()

    def check_enemy_collisions(self):
        # Verificar colisão entre balas e inimigos
        for bullet in self.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in hit_enemies:
                bullet.kill()
                enemy.take_damage(1)
        
        # Verificar colisão entre inimigos e blocos
        for enemy in self.enemies:
            enemy.on_ground = False
            
            # Colisão horizontal
            collisions = pygame.sprite.spritecollide(enemy, self.level.blocks, False)
            for block in collisions:
                if enemy.rect.centerx < block.rect.centerx:
                    enemy.rect.right = block.rect.left
                    enemy.direction *= -1
                    enemy.facing_right = not enemy.facing_right
                else:
                    enemy.rect.left = block.rect.right
                    enemy.direction *= -1
                    enemy.facing_right = not enemy.facing_right
            
            # Aplicar movimento vertical
            enemy.rect.y += enemy.speed_y
            
            # Colisão vertical
            collisions = pygame.sprite.spritecollide(enemy, self.level.blocks, False)
            for block in collisions:
                if enemy.speed_y > 0:  # Caindo
                    enemy.rect.bottom = block.rect.top
                    enemy.speed_y = 0
                    enemy.on_ground = True
                elif enemy.speed_y < 0:  # Subindo
                    enemy.rect.top = block.rect.bottom
                    enemy.speed_y = 0

    def check_character_collisions(self):
        # Colisão entre player e demons
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                player_center_x = self.player.rect.centerx
                enemy_center_x = enemy.rect.centerx
                
                if player_center_x < enemy_center_x:
                    self.player.rect.right = enemy.rect.left - 1
                    enemy.push_away(1)
                else:
                    self.player.rect.left = enemy.rect.right + 1
                    enemy.push_away(-1)
        
        # Colisão entre demons
        enemies_list = list(self.enemies)
        for i, enemy1 in enumerate(enemies_list):
            for enemy2 in enemies_list[i+1:]:
                if enemy1.rect.colliderect(enemy2.rect):
                    enemy1_center_x = enemy1.rect.centerx
                    enemy2_center_x = enemy2.rect.centerx
                    
                    if enemy1_center_x < enemy2_center_x:
                        enemy1.rect.right = enemy2.rect.left - 1
                        enemy1.push_away(-1)
                        enemy2.push_away(1)
                    else:
                        enemy1.rect.left = enemy2.rect.right + 1
                        enemy1.push_away(1)
                        enemy2.push_away(-1)

    def check_demon_attacks(self):
        for enemy in self.enemies:
            if enemy.state == "attack" and enemy.current_animation == "attack":
                distance = abs(self.player.rect.centerx - enemy.rect.centerx)
                distance_vertical = abs(self.player.rect.centery - enemy.rect.centery)
                
                if distance <= 70 and distance_vertical <= 40:
                    damage_applied = self.player.take_damage(enemy.damage)
                    
                    if damage_applied:
                        knockback = 15
                        if self.player.rect.centerx < enemy.rect.centerx:
                            self.player.rect.x -= knockback
                        else:
                            self.player.rect.x += knockback