import pygame
import math
import random
from scenes.Scene import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        # Timer para animações
        self.animation_timer = 0
        
        # Fontes
        self.title_font = pygame.font.Font(None, 96)
        self.button_font = pygame.font.Font(None, 42)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.instruction_font = pygame.font.Font(None, 28)
        
        # Cores temáticas (tons sombrios e vermelhos)
        self.bg_color = (15, 15, 25)
        self.title_color = (220, 50, 50)
        self.subtitle_color = (180, 180, 200)
        self.button_color = (80, 20, 20)
        self.button_hover_color = (120, 30, 30)
        self.button_border_color = (200, 50, 50)
        self.button_text_color = (255, 255, 255)
        
        # Partículas de fundo (efeito de fogo/embers)
        self.particles = []
        self.create_particles()
        
        # Botões com posições e estados
        self.start_button = {
            'rect': pygame.Rect((SCREEN_WIDTH - 250) // 2, SCREEN_HEIGHT // 2 - 20, 250, 60),
            'text': 'INICIAR JOGO',
            'hovered': False
        }
        
        self.quit_button = {
            'rect': pygame.Rect((SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT // 2 + 60, 200, 50),
            'text': 'SAIR',
            'hovered': False
        }
        
        # Efeitos visuais
        self.title_glow_intensity = 0
        self.ember_timer = 0
        
    def create_particles(self):
        """Criar partículas de ember/fogo para o fundo"""
        for _ in range(30):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed_y': random.uniform(-0.5, -2.0),
                'speed_x': random.uniform(-0.2, 0.2),
                'size': random.randint(2, 5),
                'color': random.choice([
                    (255, 100, 50),   # Laranja ardente
                    (255, 150, 80),   # Laranja claro
                    (200, 80, 40),    # Vermelho escuro
                    (255, 200, 100),  # Amarelo quente
                ]),
                'life': random.randint(100, 300),
                'max_life': 300
            }
            self.particles.append(particle)
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Verificar hover nos botões
        self.start_button['hovered'] = self.start_button['rect'].collidepoint(mouse_pos)
        self.quit_button['hovered'] = self.quit_button['rect'].collidepoint(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button['rect'].collidepoint(event.pos):
                    # Iniciar o jogo
                    from scenes.GameScene import GameScene
                    self.next_scene = GameScene(self.game)
                elif self.quit_button['rect'].collidepoint(event.pos):
                    # Sair do jogo
                    self.game.running = False
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Iniciar com Enter ou Espaço
                    from scenes.GameScene import GameScene
                    self.next_scene = GameScene(self.game)
                elif event.key == pygame.K_ESCAPE:
                    # Sair com ESC
                    self.game.running = False
    
    def update(self):
        self.animation_timer += 1
        self.ember_timer += 1
        
        # Atualizar partículas
        for particle in self.particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['life'] -= 1
            
            # Remover partículas que "morreram" e criar novas
            if particle['life'] <= 0 or particle['y'] < -10:
                self.particles.remove(particle)
        
        # Criar novas partículas ocasionalmente
        if self.ember_timer % 20 == 0:
            new_particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': SCREEN_HEIGHT + 10,
                'speed_y': random.uniform(-0.8, -2.5),
                'speed_x': random.uniform(-0.3, 0.3),
                'size': random.randint(2, 6),
                'color': random.choice([
                    (255, 100, 50),
                    (255, 150, 80),
                    (200, 80, 40),
                    (255, 200, 100),
                ]),
                'life': random.randint(150, 400),
                'max_life': 400
            }
            self.particles.append(new_particle)
        
        # Efeito de brilho no título
        self.title_glow_intensity = 50 + 20 * math.sin(self.animation_timer * 0.05)
    
    def draw(self, screen):
        # Fundo gradiente
        self.draw_gradient_background(screen)
        
        # Desenhar partículas
        self.draw_particles(screen)
        
        # Título principal com efeito de brilho
        self.draw_title(screen)
        
        # Subtítulo
        self.draw_subtitle(screen)
        
        # Botões
        self.draw_button(screen, self.start_button, is_primary=True)
        self.draw_button(screen, self.quit_button)
        
        # Instruções e créditos
        self.draw_instructions(screen)
        
        # Efeitos decorativos
        self.draw_decorative_elements(screen)
    
    def draw_gradient_background(self, screen):
        """Desenhar fundo gradiente atmosférico"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            # Gradiente de azul escuro no topo para vermelho escuro embaixo
            r = int(15 + (40 - 15) * ratio)
            g = int(15 + (15 - 15) * ratio)
            b = int(25 + (15 - 25) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def draw_particles(self, screen):
        """Desenhar partículas de ember/fogo"""
        for particle in self.particles:
            alpha = int((particle['life'] / particle['max_life']) * 255)
            
            # Criar superfície com alpha para transparência
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            
            # Desenhar partícula com brilho
            color_with_alpha = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, particle['color'], (particle['size'], particle['size']), particle['size'])
            
            # Adicionar brilho central
            if particle['size'] > 2:
                bright_color = tuple(min(255, c + 50) for c in particle['color'])
                pygame.draw.circle(particle_surface, bright_color, (particle['size'], particle['size']), particle['size'] // 2)
            
            screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
    
    def draw_title(self, screen):
        """Desenhar título com efeito de brilho"""
        title_text = "DEMON HUNTER"
        
        # Sombra do título
        shadow_surface = self.title_font.render(title_text, True, (20, 10, 10))
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 3, 103))
        screen.blit(shadow_surface, shadow_rect)
        
        # Título principal
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Efeito de brilho
        glow_color = (255, 80, 80, int(self.title_glow_intensity))
        glow_surface = pygame.Surface(title_surface.get_size(), pygame.SRCALPHA)
        glow_text = self.title_font.render(title_text, True, glow_color[:3])
        glow_surface.blit(glow_text, (0, 0))
        screen.blit(glow_surface, title_rect)
    
    def draw_subtitle(self, screen):
        """Desenhar subtítulo atmosférico"""
        subtitle_text = "Sobreviva ao inferno na Terra"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, self.subtitle_color)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Linha decorativa
        line_y = 180
        pygame.draw.line(screen, (100, 50, 50), 
                        (SCREEN_WIDTH // 2 - 100, line_y), 
                        (SCREEN_WIDTH // 2 + 100, line_y), 2)
    
    def draw_button(self, screen, button_data, is_primary=False):
        """Desenhar botão com efeitos visuais"""
        rect = button_data['rect']
        text = button_data['text']
        hovered = button_data['hovered']
        
        # Cor do botão baseada no estado
        if hovered:
            button_color = self.button_hover_color
            border_width = 4
            # Efeito de brilho quando hover
            glow_rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
            pygame.draw.rect(screen, (150, 50, 50), glow_rect)
        else:
            button_color = self.button_color
            border_width = 2
        
        # Fundo do botão
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, self.button_border_color, rect, border_width)
        
        # Texto do botão
        font_size = self.button_font if is_primary else pygame.font.Font(None, 36)
        button_text_surface = font_size.render(text, True, self.button_text_color)
        text_rect = button_text_surface.get_rect(center=rect.center)
        screen.blit(button_text_surface, text_rect)
        
        # Efeito de pulsação no botão principal
        if is_primary:
            pulse = 1.0 + 0.05 * math.sin(self.animation_timer * 0.1)
            if hovered:
                corner_size = int(8 * pulse)
                corners = [
                    (rect.topleft[0] - corner_size, rect.topleft[1] - corner_size),
                    (rect.topright[0] + corner_size, rect.topright[1] - corner_size),
                    (rect.bottomleft[0] - corner_size, rect.bottomleft[1] + corner_size),
                    (rect.bottomright[0] + corner_size, rect.bottomright[1] + corner_size)
                ]
                for corner in corners:
                    pygame.draw.circle(screen, (255, 100, 100), corner, 3)
    
    def draw_instructions(self, screen):
        """Desenhar instruções e controles"""
        # Título dos controles
        controls_title = "CONTROLES:"
        title_surface = pygame.font.Font(None, 32).render(controls_title, True, (200, 150, 150))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 140))
        screen.blit(title_surface, title_rect)
        
        # Desenhar comandos com ícones visuais em vez de caracteres unicode
        y_start = SCREEN_HEIGHT - 90
        
        # Comando 1: Movimento
        self.draw_control_item(screen, "A/D ou SETAS", "Mover", SCREEN_WIDTH // 2 - 200, y_start)
        
        # Comando 2: Pular  
        self.draw_control_item(screen, "W ou SETA CIMA", "Pular", SCREEN_WIDTH // 2, y_start)
        
        # Comando 3: Atirar
        self.draw_control_item(screen, "ESPACO", "Atirar", SCREEN_WIDTH // 2 + 200, y_start)
        
        # Instruções de navegação
        nav_instructions = [
            "ENTER ou Clique para Iniciar",
            "ESC para Sair"
        ]
        
        y_nav = SCREEN_HEIGHT - 50
        for instruction in nav_instructions:
            text_surface = self.instruction_font.render(instruction, True, (180, 180, 180))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_nav))
            screen.blit(text_surface, text_rect)
            y_nav += 25
    
    def draw_control_item(self, screen, key_text, action_text, center_x, y):
        """Desenhar um item de controle individual com visual melhorado"""
        # Fundo do item de controle
        item_width = 160
        item_height = 50
        item_rect = pygame.Rect(center_x - item_width//2, y - item_height//2, item_width, item_height)
        
        # Desenhar fundo semi-transparente
        overlay = pygame.Surface((item_width, item_height), pygame.SRCALPHA)
        overlay.fill((40, 20, 20, 100))
        screen.blit(overlay, item_rect.topleft)
        
        # Borda do item
        pygame.draw.rect(screen, (100, 50, 50), item_rect, 2)
        
        # Texto da tecla (parte superior)
        key_font = pygame.font.Font(None, 24)
        key_surface = key_font.render(key_text, True, (255, 200, 150))
        key_rect = key_surface.get_rect(center=(center_x, y - 12))
        screen.blit(key_surface, key_rect)
        
        # Texto da ação (parte inferior)
        action_font = pygame.font.Font(None, 20)
        action_surface = action_font.render(action_text, True, (200, 200, 200))
        action_rect = action_surface.get_rect(center=(center_x, y + 8))
        screen.blit(action_surface, action_rect)
        
        # Desenhar setas visuais para movimento
        if "SETAS" in key_text or "A/D" in key_text:
            self.draw_arrow_keys(screen, center_x, y - 25)
        elif "CIMA" in key_text or "W" in key_text:
            self.draw_up_arrow(screen, center_x, y - 25)
        elif "ESPACO" in key_text:
            self.draw_space_key(screen, center_x, y - 25)
    
    def draw_arrow_keys(self, screen, center_x, y):
        """Desenhar representação visual das teclas de seta (esquerda/direita)"""
        # Seta esquerda
        left_arrow = [
            (center_x - 20, y),
            (center_x - 15, y - 5),
            (center_x - 15, y + 5)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), left_arrow)
        
        # Seta direita
        right_arrow = [
            (center_x + 20, y),
            (center_x + 15, y - 5),
            (center_x + 15, y + 5)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), right_arrow)
    
    def draw_up_arrow(self, screen, center_x, y):
        """Desenhar seta para cima"""
        up_arrow = [
            (center_x, y - 5),
            (center_x - 5, y + 3),
            (center_x + 5, y + 3)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), up_arrow)
    
    def draw_space_key(self, screen, center_x, y):
        """Desenhar representação da barra de espaço"""
        space_rect = pygame.Rect(center_x - 15, y - 2, 30, 4)
        pygame.draw.rect(screen, (255, 255, 255), space_rect)
    
    def draw_decorative_elements(self, screen):
        """Desenhar elementos decorativos"""
        # Bordas laterais com efeito de fogo
        for y in range(0, SCREEN_HEIGHT, 20):
            intensity = 50 + 30 * math.sin((y + self.animation_timer) * 0.02)
            color = (int(intensity), int(intensity * 0.3), 0)
            pygame.draw.circle(screen, color, (10, y), 5)
            pygame.draw.circle(screen, color, (SCREEN_WIDTH - 10, y), 5)
        
        # Linha de separação animada no centro
        center_y = SCREEN_HEIGHT // 2 + 150
        wave_offset = 5 * math.sin(self.animation_timer * 0.05)
        for x in range(0, SCREEN_WIDTH, 10):
            point_y = center_y + wave_offset * math.sin(x * 0.02)
            pygame.draw.circle(screen, (80, 40, 40), (x, int(point_y)), 2)