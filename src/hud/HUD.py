import pygame
import math
from hud.HealthBar import HealthBar

class HUD:
    def __init__(self):
        # Inicializar componentes do HUD
        self.health_bar = HealthBar(30, 30, 250, 35, max_health=5)
        
        # Fonts para textos gerais
        self.title_font = pygame.font.Font(None, 28)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.mini_font = pygame.font.Font(None, 20)
        
        # Timer para animações
        self.animation_timer = 0
        
        # Cores temáticas
        self.panel_color = (20, 20, 30, 180)
        self.border_color = (100, 50, 50)
        self.text_color = (255, 255, 255)
        self.accent_color = (220, 50, 50)
        
    def draw(self, screen, player, enemies_count=0):
        self.animation_timer += 1
        
        # Painel principal do HUD (canto superior esquerdo)
        self.draw_main_panel(screen, player)
        
        # Contador de inimigos (canto superior direito)
        self.draw_enemy_panel(screen, enemies_count)
        
        # Status do jogador (canto inferior esquerdo)
        self.draw_status_panel(screen, player)
        
        # Mini-mapa ou radar (canto superior direito, abaixo do contador)
        self.draw_radar_panel(screen, enemies_count)
        
    def draw_main_panel(self, screen, player):
        """Painel principal com vida e informações do jogador"""
        panel_width = 320
        panel_height = 90
        panel_x = 20
        panel_y = 20
        
        # Fundo do painel com transparência
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.panel_color)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Borda do painel
        pygame.draw.rect(screen, self.border_color, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Título do painel
        title_text = self.title_font.render("GUERREIRO", True, self.accent_color)
        screen.blit(title_text, (panel_x + 10, panel_y + 5))
        
        # Barra de vida melhorada (posicionada dentro do painel)
        self.health_bar.x = panel_x + 15
        self.health_bar.y = panel_y + 35
        self.health_bar.draw(screen, player.health)
        
        # Status de invencibilidade
        if player.invincible_timer > 0:
            inv_text = "PROTEGIDO"
            inv_color = (100, 255, 100) if player.invincible_timer % 20 < 10 else (50, 200, 50)
            inv_surface = self.small_font.render(inv_text, True, inv_color)
            screen.blit(inv_surface, (panel_x + 15, panel_y + 75))
        
    def draw_enemy_panel(self, screen, enemies_count):
        """Painel contador de inimigos"""
        panel_width = 280
        panel_height = 60
        panel_x = screen.get_width() - panel_width - 20
        panel_y = 20
        
        # Fundo do painel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.panel_color)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Borda do painel (vermelha se ainda há inimigos, verde se zerou)
        border_color = self.border_color if enemies_count > 0 else (50, 150, 50)
        pygame.draw.rect(screen, border_color, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Ícone de demônio (representação visual)
        demon_icon_x = panel_x + 15
        demon_icon_y = panel_y + panel_height // 2
        self.draw_demon_icon(screen, demon_icon_x, demon_icon_y, enemies_count > 0)
        
        # Texto do contador
        if enemies_count > 0:
            counter_text = f"DEMÔNIOS: {enemies_count}"
            color = (255, 120, 120)
        else:
            counter_text = "ÁREA LIMPA!"
            color = (120, 255, 120)
            
        text_surface = self.font.render(counter_text, True, color)
        screen.blit(text_surface, (panel_x + 60, panel_y + 15))
        
        # Barra de progresso (quantos foram derrotados)
        if hasattr(self, 'total_enemies'):
            progress_width = 180
            progress_x = panel_x + 60
            progress_y = panel_y + 40
            defeated = self.total_enemies - enemies_count
            progress = defeated / self.total_enemies if self.total_enemies > 0 else 1
            
            # Fundo da barra
            pygame.draw.rect(screen, (40, 40, 40), (progress_x, progress_y, progress_width, 8))
            # Progresso
            pygame.draw.rect(screen, (100, 255, 100), (progress_x, progress_y, int(progress_width * progress), 8))
            # Borda
            pygame.draw.rect(screen, (150, 150, 150), (progress_x, progress_y, progress_width, 8), 1)
        
    def draw_status_panel(self, screen, player):
        """Painel de status no canto inferior esquerdo"""
        panel_width = 200
        panel_height = 100
        panel_x = 20
        panel_y = screen.get_height() - panel_height - 20
        
        # Fundo do painel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.panel_color)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Borda
        pygame.draw.rect(screen, self.border_color, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Status da arma
        weapon_y = panel_y + 10
        if player.shoot_cooldown > 0:
            weapon_text = "RECARREGANDO"
            weapon_color = (255, 200, 100)
            
            # Barra de recarga
            reload_progress = 1 - (player.shoot_cooldown / player.shoot_delay)
            reload_width = 150
            reload_x = panel_x + 15
            reload_y = weapon_y + 20
            
            pygame.draw.rect(screen, (60, 60, 60), (reload_x, reload_y, reload_width, 6))
            pygame.draw.rect(screen, (255, 200, 100), (reload_x, reload_y, int(reload_width * reload_progress), 6))
            pygame.draw.rect(screen, (200, 200, 200), (reload_x, reload_y, reload_width, 6), 1)
        else:
            weapon_text = "PRONTO"
            weapon_color = (100, 255, 100)
            
            # Indicador de pronto (pulsante)
            pulse = 0.7 + 0.3 * abs(math.sin(self.animation_timer * 0.1))
            ready_color = tuple(int(c * pulse) for c in weapon_color)
            pygame.draw.circle(screen, ready_color, (panel_x + 25, weapon_y + 25), 8)
            
        weapon_surface = self.small_font.render(weapon_text, True, weapon_color)
        screen.blit(weapon_surface, (panel_x + 15, weapon_y))
        
        # Controles rápidos
        controls_y = panel_y + 55
        controls_title = self.mini_font.render("CONTROLES:", True, (180, 180, 180))
        screen.blit(controls_title, (panel_x + 10, controls_y))
        
        controls = ["WASD/Setas: Mover", "Espaço: Atirar"]
        for i, control in enumerate(controls):
            control_surface = self.mini_font.render(control, True, (150, 150, 150))
            screen.blit(control_surface, (panel_x + 10, controls_y + 15 + i * 15))
    
    def draw_radar_panel(self, screen, enemies_count):
        """Mini radar/mapa no canto superior direito"""
        if enemies_count == 0:
            return
            
        panel_size = 100
        panel_x = screen.get_width() - panel_size - 20
        panel_y = 100
        
        # Fundo do radar
        radar_surface = pygame.Surface((panel_size, panel_size), pygame.SRCALPHA)
        radar_surface.fill((20, 40, 20, 150))
        screen.blit(radar_surface, (panel_x, panel_y))
        
        # Borda do radar
        pygame.draw.rect(screen, (100, 200, 100), (panel_x, panel_y, panel_size, panel_size), 2)
        
        # Centro do radar (jogador)
        center_x = panel_x + panel_size // 2
        center_y = panel_y + panel_size // 2
        pygame.draw.circle(screen, (100, 100, 255), (center_x, center_y), 4)
        
        # Indicadores de inimigos (posições aleatórias para demonstração)
        for i in range(min(enemies_count, 4)):
            angle = (self.animation_timer + i * 90) * 0.02
            radius = 30
            enemy_x = center_x + int(radius * math.cos(angle))
            enemy_y = center_y + int(radius * math.sin(angle))
            
            # Pulso nos pontos inimigos
            pulse_size = 3 + int(2 * abs(math.sin(self.animation_timer * 0.05 + i)))
            pygame.draw.circle(screen, (255, 100, 100), (enemy_x, enemy_y), pulse_size)
        
        # Título do radar
        radar_title = self.mini_font.render("RADAR", True, (200, 255, 200))
        title_rect = radar_title.get_rect(center=(center_x, panel_y - 10))
        screen.blit(radar_title, title_rect)
    
    def draw_demon_icon(self, screen, x, y, active=True):
        """Desenhar ícone representativo de demônio"""
        color = (255, 100, 100) if active else (100, 100, 100)
        
        # Corpo do demônio (círculo)
        pygame.draw.circle(screen, color, (x + 10, y), 8)
        
        # Chifres
        horn1 = [(x + 5, y - 8), (x + 7, y - 12), (x + 9, y - 8)]
        horn2 = [(x + 11, y - 8), (x + 13, y - 12), (x + 15, y - 8)]
        pygame.draw.polygon(screen, color, horn1)
        pygame.draw.polygon(screen, color, horn2)
        
        # Olhos
        if active:
            pygame.draw.circle(screen, (255, 255, 0), (x + 7, y - 2), 2)
            pygame.draw.circle(screen, (255, 255, 0), (x + 13, y - 2), 2)
    
    def set_total_enemies(self, total):
        """Definir total de inimigos para cálculo de progresso"""
        self.total_enemies = total