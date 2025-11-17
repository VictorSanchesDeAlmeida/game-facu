import pygame
from scenes.Scene import Scene

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # Fontes
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 32)
        
        # Cores
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 255, 255)
        self.button_color = (100, 150, 255)
        self.button_hover_color = (150, 200, 255)
        self.button_text_color = (255, 255, 255)
        
        # Botão "Iniciar Jogo"
        self.button_rect = pygame.Rect(
            (game.tela.get_width() - 200) // 2, 
            game.tela.get_height() // 2, 
            200, 60
        )
        self.button_hovered = False
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.button_hovered = self.button_rect.collidepoint(event.pos)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    # Iniciar o jogo
                    from scenes.GameScene import GameScene
                    self.next_scene = GameScene(self.game)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Iniciar com Enter ou Espaço
                    from scenes.GameScene import GameScene
                    self.next_scene = GameScene(self.game)
    
    def update(self):
        pass
    
    def draw(self, screen):
        # Fundo
        screen.fill(self.bg_color)
        
        # Título
        title_text = self.title_font.render("DEMON HUNTER", True, self.title_color)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.subtitle_font.render("Sobreviva aos demônios!", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Botão
        button_color = self.button_hover_color if self.button_hovered else self.button_color
        pygame.draw.rect(screen, button_color, self.button_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, 3)
        
        # Texto do botão
        button_text = self.button_font.render("INICIAR", True, self.button_text_color)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        screen.blit(button_text, button_text_rect)
        
        # Instruções
        instructions = [
            "Use as setas para mover",
            "ESPAÇO para atirar",
            "Pressione ENTER ou clique para começar"
        ]
        
        y_offset = 400
        for instruction in instructions:
            text = pygame.font.Font(None, 24).render(instruction, True, (150, 150, 150))
            text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset + 100))
            screen.blit(text, text_rect)
            y_offset += 30