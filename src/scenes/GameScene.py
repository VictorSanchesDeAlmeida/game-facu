import pygame
import math
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
        image_player = load_image("Player.png")
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
        self.hud.set_total_enemies(len(self.enemies))  # Definir total para barra de progresso
        
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
        self.game_over_timer = 0  # Timer para animações da tela de game over
        self.game_over_particles = []  # Partículas da tela de game over
        
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
            self.game_over_timer = 0  # Resetar timer
            self.create_game_over_particles()  # Criar partículas
            
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
        
        # Atualizar background do level
        self.level.update()
    
    def draw(self, screen):
        # Desenhar background do level com parallax
        self.level.draw_background(screen, self.camera_x, self.camera_y)
        
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
            self.game_over_timer += 1
            self.draw_game_over(screen)
    
    def draw_game_over(self, screen):
        """Tela de Game Over melhorada com efeitos visuais avançados"""
        import random
        
        # Atualizar partículas
        self.update_game_over_particles()
        
        # Fundo gradiente dramático
        self.draw_dramatic_background(screen)
        
        # Partículas de fogo/sangue
        self.draw_game_over_particles(screen)
        
        # Efeito de rachadura na tela
        self.draw_screen_cracks(screen)
        
        # Título "GAME OVER" com efeitos especiais
        self.draw_game_over_title(screen)
        
        # Painel do demon killer
        if self.killer_demon:
            self.draw_killer_demon_panel(screen)
        
        # Estatísticas de morte
        self.draw_death_stats(screen)
        
        # Botões de ação melhorados
        self.draw_game_over_buttons(screen)
        
        # Efeito de vinheta escura nas bordas
        self.draw_vignette_effect(screen)
    
    def create_game_over_particles(self):
        """Criar partículas para a tela de game over"""
        import random
        self.game_over_particles = []
        for _ in range(40):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed_x': random.uniform(-1, 1),
                'speed_y': random.uniform(-2, 0.5),
                'size': random.randint(2, 8),
                'color': random.choice([
                    (150, 0, 0),      # Vermelho escuro
                    (100, 0, 0),      # Vermelho muito escuro
                    (80, 20, 20),     # Marrom avermelhado
                    (60, 60, 60),     # Cinza escuro
                ]),
                'life': random.randint(200, 500),
                'max_life': 500,
                'type': random.choice(['blood', 'ash', 'ember'])
            }
            self.game_over_particles.append(particle)
    
    def update_game_over_particles(self):
        """Atualizar partículas da tela de game over"""
        import random
        
        for particle in self.game_over_particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['life'] -= 1
            
            # Gravidade leve para algumas partículas
            if particle['type'] == 'blood':
                particle['speed_y'] += 0.02
            
            # Remover partículas mortas
            if particle['life'] <= 0:
                self.game_over_particles.remove(particle)
        
        # Adicionar novas partículas ocasionalmente
        if len(self.game_over_particles) < 30 and random.randint(1, 10) == 1:
            new_particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': -10,
                'speed_x': random.uniform(-0.5, 0.5),
                'speed_y': random.uniform(0.5, 2),
                'size': random.randint(2, 6),
                'color': random.choice([
                    (150, 0, 0),
                    (100, 0, 0),
                    (80, 20, 20),
                ]),
                'life': random.randint(200, 400),
                'max_life': 400,
                'type': 'blood'
            }
            self.game_over_particles.append(new_particle)
    
    def draw_dramatic_background(self, screen):
        """Desenhar fundo gradiente dramático"""
        # Gradiente vermelho escuro para preto
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(40 * (1 - ratio))
            g = int(10 * (1 - ratio))
            b = int(10 * (1 - ratio))
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Overlay pulsante
        pulse = 0.3 + 0.1 * abs(math.sin(self.game_over_timer * 0.03))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, int(50 * pulse)))
        screen.blit(overlay, (0, 0))
    
    def draw_game_over_particles(self, screen):
        """Desenhar partículas da tela de game over"""
        for particle in self.game_over_particles:
            alpha_ratio = particle['life'] / particle['max_life']
            alpha = int(255 * alpha_ratio)
            
            if particle['type'] == 'ember':
                # Partículas brilhantes
                glow_size = particle['size'] + 2
                glow_color = (particle['color'][0] + 50, particle['color'][1] + 20, 0)
                pygame.draw.circle(screen, glow_color, (int(particle['x']), int(particle['y'])), glow_size)
            
            # Partícula principal
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])
    
    def draw_screen_cracks(self, screen):
        """Desenhar efeito de rachadura na tela"""
        # Linhas de rachadura partindo do centro
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        for i in range(6):
            angle = (i * 60 + self.game_over_timer * 0.5) * math.pi / 180
            length = 150 + 50 * math.sin(self.game_over_timer * 0.02 + i)
            
            end_x = center_x + length * math.cos(angle)
            end_y = center_y + length * math.sin(angle)
            
            # Linha principal da rachadura
            pygame.draw.line(screen, (100, 50, 50), (center_x, center_y), (int(end_x), int(end_y)), 3)
            
            # Linhas secundárias
            for j in range(2):
                sub_angle = angle + (-1 + j * 2) * 0.3
                sub_length = length * 0.6
                sub_end_x = center_x + sub_length * math.cos(sub_angle)
                sub_end_y = center_y + sub_length * math.sin(sub_angle)
                pygame.draw.line(screen, (80, 30, 30), (center_x, center_y), (int(sub_end_x), int(sub_end_y)), 2)
    
    def draw_game_over_title(self, screen):
        """Desenhar título GAME OVER com efeitos especiais"""
        # Efeito de tremor no texto
        shake_x = int(3 * math.sin(self.game_over_timer * 0.2))
        shake_y = int(2 * math.sin(self.game_over_timer * 0.3))
        
        # Sombra múltipla para profundidade
        font_title = pygame.font.Font(None, 120)
        title_text = "GAME OVER"
        
        for offset in [(4, 4), (2, 2), (1, 1)]:
            shadow_color = (20 - offset[0] * 5, 0, 0)
            shadow_surface = font_title.render(title_text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset[0] + shake_x, 120 + offset[1] + shake_y))
            screen.blit(shadow_surface, shadow_rect)
        
        # Título principal com brilho
        main_color = (255, 50, 50)
        glow_intensity = 50 + 30 * abs(math.sin(self.game_over_timer * 0.1))
        
        title_surface = font_title.render(title_text, True, main_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 120 + shake_y))
        screen.blit(title_surface, title_rect)
        
        # Efeito de brilho
        glow_surface = pygame.Surface(title_surface.get_size(), pygame.SRCALPHA)
        glow_text = font_title.render(title_text, True, (255, 100, 100, int(glow_intensity)))
        glow_surface.blit(glow_text, (0, 0))
        screen.blit(glow_surface, title_rect)
    
    def draw_killer_demon_panel(self, screen):
        """Desenhar painel do demon assassino"""
        # Forçar animação idle e continuar atualizando
        self.killer_demon.set_animation("idle")
        self.killer_demon.speed_x = 0
        self.killer_demon.update_animation()
        
        # Painel para o demon
        panel_width = 500
        panel_height = 200
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = 200
        
        # Fundo do painel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((20, 10, 10, 200))
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Borda do painel
        pygame.draw.rect(screen, (150, 50, 50), (panel_x, panel_y, panel_width, panel_height), 4)
        
        # Demon assassino (maior e mais intimidante)
        killer_image = self.killer_demon.image.copy()
        killer_scaled = pygame.transform.scale(killer_image, (120, 120))
        demon_rect = killer_scaled.get_rect(center=(panel_x + 100, panel_y + panel_height // 2))
        screen.blit(killer_scaled, demon_rect)
        
        # Aura vermelha ao redor do demon
        aura_intensity = 100 + 50 * abs(math.sin(self.game_over_timer * 0.1))
        aura_surface = pygame.Surface((140, 140), pygame.SRCALPHA)
        aura_surface.fill((255, 0, 0, int(aura_intensity * 0.3)))
        aura_rect = aura_surface.get_rect(center=demon_rect.center)
        screen.blit(aura_surface, aura_rect)
        
        # Balão de fala melhorado
        bubble_width = 280
        bubble_height = 100
        bubble_x = panel_x + 180
        bubble_y = panel_y + 50
        
        # Fundo do balão
        bubble_surface = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)
        bubble_surface.fill((40, 20, 20, 220))
        screen.blit(bubble_surface, (bubble_x, bubble_y))
        
        # Borda do balão
        pygame.draw.rect(screen, (255, 150, 150), (bubble_x, bubble_y, bubble_width, bubble_height), 3)
        
        # Pontinha do balão
        bubble_tip = [
            (bubble_x, bubble_y + 40),
            (bubble_x - 15, bubble_y + 35),
            (bubble_x - 15, bubble_y + 45)
        ]
        pygame.draw.polygon(screen, (40, 20, 20), bubble_tip)
        pygame.draw.polygon(screen, (255, 150, 150), bubble_tip, 3)
        
        # Texto do demon (quebrado em linhas se necessário)
        font_taunt = pygame.font.Font(None, 32)
        words = self.killer_taunt.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font_taunt.size(test_line)[0] < bubble_width - 20:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        # Desenhar linhas do texto
        for i, line in enumerate(lines):
            text_surface = font_taunt.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + 30 + i * 35))
            screen.blit(text_surface, text_rect)
    
    def draw_death_stats(self, screen):
        """Desenhar estatísticas da morte"""
        stats_y = 420
        font_stats = pygame.font.Font(None, 36)
        
        # Título das estatísticas
        stats_title = font_stats.render("ESTATÍSTICAS DA MISSÃO", True, (200, 100, 100))
        title_rect = stats_title.get_rect(center=(SCREEN_WIDTH // 2, stats_y))
        screen.blit(stats_title, title_rect)
        
        # Estatísticas (simuladas por agora)
        enemies_defeated = self.hud.total_enemies - len(self.enemies) if hasattr(self.hud, 'total_enemies') else 0
        stats = [
            f"Demônios derrotados: {enemies_defeated}",
            f"Vida restante: 0/{self.player.health + abs(self.player.health)}",
            "Causa da morte: Ataque demônico"
        ]
        
        font_small = pygame.font.Font(None, 28)
        for i, stat in enumerate(stats):
            stat_surface = font_small.render(stat, True, (180, 180, 180))
            stat_rect = stat_surface.get_rect(center=(SCREEN_WIDTH // 2, stats_y + 40 + i * 30))
            screen.blit(stat_surface, stat_rect)
    
    def draw_game_over_buttons(self, screen):
        """Desenhar botões de ação melhorados"""
        # Posições dos botões
        button_width = 220
        button_height = 50
        button_y = SCREEN_HEIGHT - 120
        
        restart_button = pygame.Rect((SCREEN_WIDTH // 2 - button_width - 20), button_y, button_width, button_height)
        menu_button = pygame.Rect((SCREEN_WIDTH // 2 + 20), button_y, button_width, button_height)
        
        # Botão Reiniciar
        self.draw_action_button(screen, restart_button, "TENTAR NOVAMENTE", (100, 50, 50), (150, 70, 70))
        
        # Botão Menu
        self.draw_action_button(screen, menu_button, "VOLTAR AO MENU", (50, 50, 100), (70, 70, 150))
        
        # Instruções
        font_instructions = pygame.font.Font(None, 24)
        instructions = ["R - Reiniciar    ESC - Menu Principal"]
        
        for instruction in instructions:
            text = font_instructions.render(instruction, True, (150, 150, 150))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(text, text_rect)
    
    def draw_action_button(self, screen, rect, text, base_color, hover_color):
        """Desenhar botão de ação com efeitos"""
        # Efeito de pulsação
        pulse = 0.9 + 0.1 * abs(math.sin(self.game_over_timer * 0.05))
        pulsed_rect = pygame.Rect(
            rect.x + (rect.width - rect.width * pulse) // 2,
            rect.y + (rect.height - rect.height * pulse) // 2,
            int(rect.width * pulse),
            int(rect.height * pulse)
        )
        
        # Fundo do botão
        pygame.draw.rect(screen, base_color, pulsed_rect)
        pygame.draw.rect(screen, hover_color, pulsed_rect, 3)
        
        # Texto do botão
        font_button = pygame.font.Font(None, 32)
        text_surface = font_button.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=pulsed_rect.center)
        screen.blit(text_surface, text_rect)
    
    def draw_vignette_effect(self, screen):
        """Desenhar efeito de vinheta escura nas bordas"""
        vignette_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Criar gradiente radial das bordas para o centro
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(0, SCREEN_HEIGHT, 5):
            for x in range(0, SCREEN_WIDTH, 5):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                alpha = min(150, int(150 * (distance / max_distance) ** 2))
                
                pygame.draw.rect(vignette_surface, (0, 0, 0, alpha), (x, y, 5, 5))
        
        screen.blit(vignette_surface, (0, 0))
    
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