import pygame
import math
from scenes.Scene import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class VictoryScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.animation_timer = 0
        self.sparkle_particles = []
        self.victory_message_timer = 0
        
        # Criar algumas partículas de comemoração
        self.create_sparkles()
        
    def create_sparkles(self):
        """Criar partículas de comemoração"""
        import random
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            speed_x = random.uniform(-2, 2)
            speed_y = random.uniform(-3, -1)
            color = random.choice([
                (255, 215, 0),   # Dourado
                (255, 255, 255), # Branco
                (255, 192, 203), # Rosa
                (173, 216, 230), # Azul claro
            ])
            self.sparkle_particles.append({
                'x': x, 'y': y, 
                'speed_x': speed_x, 'speed_y': speed_y,
                'color': color, 'life': 255
            })
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reiniciar jogo
                    from scenes.GameScene import GameScene
                    self.next_scene = GameScene(self.game)
                elif event.key == pygame.K_ESCAPE:
                    # Voltar ao menu
                    from scenes.MenuScene import MenuScene
                    self.next_scene = MenuScene(self.game)
    
    def update(self):
        self.animation_timer += 1
        self.victory_message_timer += 1
        
        # Atualizar partículas
        for particle in self.sparkle_particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['life'] -= 2
            
            # Remover partículas que "morreram"
            if particle['life'] <= 0:
                self.sparkle_particles.remove(particle)
        
        # Criar novas partículas ocasionalmente
        if self.animation_timer % 30 == 0:
            self.create_sparkles()
    
    def draw(self, screen):
        # Fundo gradiente celebrativo
        for y in range(SCREEN_HEIGHT):
            # Gradiente do topo (azul escuro) para baixo (dourado)
            ratio = y / SCREEN_HEIGHT
            r = int(25 + (255 - 25) * ratio * 0.3)
            g = int(25 + (215 - 25) * ratio * 0.7)
            b = int(112 - 112 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Desenhar partículas de comemoração
        for particle in self.sparkle_particles:
            alpha = max(0, particle['life'])
            color = (*particle['color'][:3], alpha)
            
            # Desenhar uma pequena estrela
            star_size = 3
            star_x = int(particle['x'])
            star_y = int(particle['y'])
            
            pygame.draw.circle(screen, particle['color'], (star_x, star_y), star_size)
            # Adicionar brilho
            if alpha > 128:
                pygame.draw.circle(screen, (255, 255, 255), (star_x, star_y), 1)
        
        # Título principal "VITÓRIA!"
        font_title = pygame.font.Font(None, 128)
        
        # Efeito de pulsação no título
        pulse = 1.0 + 0.1 * abs(math.cos(self.animation_timer * 0.1))
        
        victory_text = font_title.render("VITÓRIA!", True, (255, 215, 0))
        victory_scaled = pygame.transform.scale(
            victory_text, 
            (int(victory_text.get_width() * pulse), int(victory_text.get_height() * pulse))
        )
        victory_rect = victory_scaled.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Sombra do título
        shadow_text = font_title.render("VITÓRIA!", True, (139, 69, 19))
        shadow_scaled = pygame.transform.scale(
            shadow_text, 
            (int(shadow_text.get_width() * pulse), int(shadow_text.get_height() * pulse))
        )
        shadow_rect = shadow_scaled.get_rect(center=(SCREEN_WIDTH // 2 + 3, 153))
        screen.blit(shadow_scaled, shadow_rect)
        screen.blit(victory_scaled, victory_rect)
        
        # Mensagem de parabéns
        font_message = pygame.font.Font(None, 48)
        messages = [
            "Parabéns, guerreiro!",
            "Você derrotou todos os demônios!",
            "A terra está segura novamente!"
        ]
        
        y_offset = 280
        for i, message in enumerate(messages):
            # Fazer as mensagens aparecerem gradualmente
            if self.victory_message_timer > i * 60:
                alpha = min(255, (self.victory_message_timer - i * 60) * 5)
                
                # Criar superfície para aplicar alpha
                message_surface = font_message.render(message, True, (255, 255, 255))
                alpha_surface = pygame.Surface(message_surface.get_size(), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, alpha))
                alpha_surface.blit(message_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                message_rect = alpha_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(alpha_surface, message_rect)
            
            y_offset += 60
        
        # Estatísticas (opcional - pode ser expandido futuramente)
        if self.victory_message_timer > 240:  # Após 4 segundos
            font_stats = pygame.font.Font(None, 32)
            stats_text = font_stats.render("Missão Completa!", True, (173, 216, 230))
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, 480))
            screen.blit(stats_text, stats_rect)
        
        # Instruções
        if self.victory_message_timer > 300:  # Após 5 segundos
            font_instructions = pygame.font.Font(None, 28)
            instructions = [
                "Pressione R para jogar novamente",
                "Pressione ESC para voltar ao menu principal"
            ]
            
            y_offset = 550
            for instruction in instructions:
                text = font_instructions.render(instruction, True, (200, 200, 200))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, text_rect)
                y_offset += 35
        
        # Efeito de borda dourada
        border_color = (255, 215, 0)
        pygame.draw.rect(screen, border_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)