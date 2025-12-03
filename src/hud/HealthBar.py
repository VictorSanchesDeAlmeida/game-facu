import pygame
import math

class HealthBar:
    def __init__(self, x, y, width=250, height=35, max_health=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        
        # Cores melhoradas
        self.bg_color = (40, 20, 20)           # Fundo escuro avermelhado
        self.border_color = (150, 150, 150)     # Borda cinza
        self.health_color = (200, 50, 50)       # Vermelho para vida
        self.low_health_color = (255, 100, 50)  # Laranja quando vida baixa
        self.critical_health_color = (255, 0, 0) # Vermelho crítico
        self.health_bg_color = (80, 30, 30)     # Fundo da área de vida
        
        # Timer para animações
        self.animation_timer = 0
        self.last_health = max_health
        self.damage_flash_timer = 0
        
    def draw(self, screen, current_health):
        """Desenha a barra de vida melhorada na tela"""
        self.animation_timer += 1
        
        # Detectar dano para efeito de flash
        if current_health < self.last_health:
            self.damage_flash_timer = 20
        self.last_health = current_health
        
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1
        
        # Calcular porcentagem da vida
        health_percentage = max(0, current_health) / self.max_health
        
        # Desenhar sombra da barra
        shadow_rect = (self.x + 2, self.y + 2, self.width, self.height)
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect)
        
        # Desenhar fundo da barra
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
        
        # Fundo interno (área onde a vida aparece)
        inner_rect = (self.x + 3, self.y + 3, self.width - 6, self.height - 6)
        pygame.draw.rect(screen, self.health_bg_color, inner_rect)
        
        # Desenhar segmentos de vida (corações/unidades)
        segment_width = (self.width - 10) / self.max_health
        for i in range(self.max_health):
            segment_x = self.x + 5 + i * segment_width
            segment_rect = (segment_x, self.y + 5, segment_width - 2, self.height - 10)
            
            if i < current_health:
                # Determinar cor baseada na vida restante
                if health_percentage <= 0.2:  # 20% ou menos
                    color = self.critical_health_color
                    # Efeito pulsante quando crítico
                    pulse = 0.7 + 0.3 * abs(math.sin(self.animation_timer * 0.2))
                    color = tuple(int(c * pulse) for c in color)
                elif health_percentage <= 0.4:  # 40% ou menos
                    color = self.low_health_color
                else:
                    color = self.health_color
                
                # Efeito de flash quando toma dano
                if self.damage_flash_timer > 0:
                    flash_intensity = self.damage_flash_timer / 20
                    color = tuple(min(255, int(c + 100 * flash_intensity)) for c in color)
                
                pygame.draw.rect(screen, color, segment_rect)
                
                # Brilho interno nos segmentos
                highlight_rect = (segment_x + 2, self.y + 7, segment_width - 6, 4)
                highlight_color = tuple(min(255, c + 30) for c in color)
                pygame.draw.rect(screen, highlight_color, highlight_rect)
            else:
                # Segmento vazio (mais escuro)
                empty_color = (60, 20, 20)
                pygame.draw.rect(screen, empty_color, segment_rect)
            
            # Separadores entre segmentos
            if i < self.max_health - 1:
                sep_x = segment_x + segment_width - 1
                pygame.draw.line(screen, self.border_color, 
                               (sep_x, self.y + 5), (sep_x, self.y + self.height - 5))
        
        # Desenhar borda principal
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)
        
        # Desenhar cantos decorativos
        corner_size = 6
        corners = [
            (self.x, self.y),  # Superior esquerdo
            (self.x + self.width - corner_size, self.y),  # Superior direito
            (self.x, self.y + self.height - corner_size),  # Inferior esquerdo
            (self.x + self.width - corner_size, self.y + self.height - corner_size)  # Inferior direito
        ]
        
        for corner in corners:
            pygame.draw.rect(screen, (200, 100, 100), (corner[0], corner[1], corner_size, corner_size))
        
        # Desenhar texto da vida com sombra
        font = pygame.font.Font(None, 24)
        health_text = f"VIDA: {max(0, current_health)}/{self.max_health}"
        
        # Sombra do texto
        shadow_surface = font.render(health_text, True, (20, 20, 20))
        shadow_x = self.x + (self.width - shadow_surface.get_width()) // 2 + 1
        shadow_y = self.y + (self.height - shadow_surface.get_height()) // 2 + 1
        screen.blit(shadow_surface, (shadow_x, shadow_y))
        
        # Texto principal
        text_color = (255, 255, 255)
        if health_percentage <= 0.2:  # Texto vermelho quando crítico
            text_color = (255, 200, 200)
        
        text_surface = font.render(health_text, True, text_color)
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
        
        # Efeito de partículas quando vida crítica
        if health_percentage <= 0.2 and current_health > 0:
            self.draw_critical_particles(screen)
    
    def draw_critical_particles(self, screen):
        """Desenhar partículas de alerta quando vida está crítica"""
        import random
        
        # Criar algumas partículas vermelhas ao redor da barra
        for _ in range(3):
            particle_x = self.x + random.randint(-10, self.width + 10)
            particle_y = self.y + random.randint(-5, self.height + 5)
            
            # Tamanho e cor da partícula baseados na animação
            size = 2 + int(2 * abs(math.sin(self.animation_timer * 0.1 + random.random() * 3)))
            intensity = 150 + int(105 * abs(math.sin(self.animation_timer * 0.15)))
            
            particle_color = (255, intensity, 0)
            pygame.draw.circle(screen, particle_color, (particle_x, particle_y), size)