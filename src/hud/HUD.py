import pygame
from hud.HealthBar import HealthBar

class HUD:
    def __init__(self):
        # Inicializar componentes do HUD
        self.health_bar = HealthBar(20, 20, 200, 25, max_health=5)
        
        # Font para textos gerais
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw(self, screen, player):
        # Desenhar barra de vida
        self.health_bar.draw(screen, player.health)
        
        # Desenhar informações adicionais (opcional)
        self.draw_ammo_info(screen, player)
        
    def draw_ammo_info(self, screen, player):
        # Mostrar status do cooldown de tiro
        if player.shoot_cooldown > 0:
            cooldown_text = "Reloading..."
            color = (255, 200, 100)  # Amarelo
        else:
            cooldown_text = "Ready to fire"
            color = (100, 255, 100)  # Verde
            
        text_surface = self.small_font.render(cooldown_text, True, color)
        screen.blit(text_surface, (20, 55))
        
        # Mostrar controles (canto inferior)
        controls = [
            "Left/Right: Move",
            "Up: Jump", 
            "Space: Shoot"
        ]
        
        y_offset = 0
        for control in controls:
            text_surface = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text_surface, (20, screen.get_height() - 80 + y_offset))
            y_offset += 25