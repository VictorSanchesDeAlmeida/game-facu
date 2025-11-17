import pygame

class HealthBar:
    def __init__(self, x, y, width=200, height=20, max_health=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        
        # Cores
        self.bg_color = (50, 50, 50)        # Fundo cinza escuro
        self.border_color = (255, 255, 255)  # Borda branca
        self.health_color = (220, 50, 50)    # Vermelho para vida
        self.low_health_color = (255, 100, 100)  # Vermelho claro quando vida baixa
        
    def draw(self, screen, current_health):
        """Desenha a barra de vida na tela"""
        # Calcular porcentagem da vida
        health_percentage = max(0, current_health) / self.max_health
        
        # Desenhar fundo da barra
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
        
        # Desenhar vida atual
        health_width = int(self.width * health_percentage)
        if health_width > 0:
            # Mudar cor se vida está baixa (menos de 30%)
            color = self.low_health_color if health_percentage < 0.3 else self.health_color
            pygame.draw.rect(screen, color, (self.x, self.y, health_width, self.height))
        
        # Desenhar borda
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)
        
        # Desenhar texto da vida
        font = pygame.font.Font(None, 24)
        health_text = f"HP: {max(0, current_health)}/{self.max_health}"
        text_surface = font.render(health_text, True, (255, 255, 255))
        
        # Centralizar texto na barra
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))