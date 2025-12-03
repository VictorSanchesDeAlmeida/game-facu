import pygame
import math
import random
from entities.Block import Block
from entities.Demon import Demon
from utils.assets_loader import load_image
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Level_1:
    def __init__(self, game):
        self.game = game
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Background elements
        self.background_elements = []
        self.parallax_layers = []
        self.atmospheric_particles = []
        self.animation_timer = 0

        self.map_data = [
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            "@.............................@",
            "@.............................@",
            "@.............................@",
            "@.........##..................@",
            "@.............................@",
            "@.............................@",
            "@....##.......#...............@",
            "@....@@.......@...............@",
            "@.....................#.......@",
            "@.......##.##.........@.......@",
            "@#######@@#@@#########@#######@"
        ]

        # Definir posições dos inimigos
        self.enemy_spawns = [
            (400, 600),   # Posição 1
            (800, 600),   # Posição 2  
            (1000, 400),  # Posição 3
            (1500, 650)   # Posição 4 - ajustada para o chão
        ]

        self.create_background()
        self.create_level()
        self.spawn_enemies()
        self.create_atmospheric_effects()

    def create_background(self):
        """Criar elementos de background em camadas"""
        level_width = 31 * 64  # Largura total do level
        level_height = 12 * 64  # Altura total do level
        
        # Camada 1: Céu gradiente
        self.sky_gradient = self.create_sky_gradient()
        
        # Camada 2: Montanhas distantes (parallax lento)
        self.create_mountain_layer(level_width, level_height)
        
        # Camada 3: Árvores mortas (parallax médio)
        self.create_dead_trees(level_width, level_height)
        
        # Camada 4: Neblina/fog (parallax rápido)
        self.create_fog_layers(level_width, level_height)
        
        # Camada 5: Elementos decorativos no chão
        self.create_ground_decorations(level_width, level_height)

    def create_sky_gradient(self):
        """Criar gradiente do céu"""
        sky_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Gradiente do céu (vermelho sombrio para preto)
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(60 * (1 - ratio) + 20 * ratio)
            g = int(20 * (1 - ratio) + 10 * ratio)
            b = int(30 * (1 - ratio) + 25 * ratio)
            pygame.draw.line(sky_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        return sky_surface

    def create_mountain_layer(self, level_width, level_height):
        """Criar camada de montanhas distantes"""
        mountains = []
        num_mountains = 8
        
        for i in range(num_mountains):
            x = (level_width / num_mountains) * i + random.randint(-100, 100)
            height = random.randint(150, 250)
            width = random.randint(200, 400)
            
            mountain = {
                'x': x,
                'y': level_height - height - 200,
                'width': width,
                'height': height,
                'color': (40, 20, 30),
                'parallax_speed': 0.2
            }
            mountains.append(mountain)
        
        self.parallax_layers.append({
            'elements': mountains,
            'type': 'mountain',
            'parallax_speed': 0.2
        })

    def create_dead_trees(self, level_width, level_height):
        """Criar árvores mortas"""
        trees = []
        num_trees = 15
        
        for i in range(num_trees):
            x = random.randint(0, level_width)
            tree_height = random.randint(80, 150)
            
            tree = {
                'x': x,
                'y': level_height - tree_height - 64,  # Acima do chão
                'height': tree_height,
                'width': random.randint(8, 15),
                'branches': random.randint(2, 4),
                'color': (60, 40, 30),
                'parallax_speed': 0.5
            }
            trees.append(tree)
        
        self.parallax_layers.append({
            'elements': trees,
            'type': 'tree',
            'parallax_speed': 0.5
        })

    def create_fog_layers(self, level_width, level_height):
        """Criar camadas de neblina"""
        fog_patches = []
        num_patches = 12
        
        for i in range(num_patches):
            patch = {
                'x': random.randint(0, level_width + 200),
                'y': random.randint(level_height // 2, level_height - 100),
                'width': random.randint(150, 300),
                'height': random.randint(50, 100),
                'alpha': random.randint(30, 80),
                'drift_speed': random.uniform(0.1, 0.3),
                'parallax_speed': 0.8
            }
            fog_patches.append(patch)
        
        self.parallax_layers.append({
            'elements': fog_patches,
            'type': 'fog',
            'parallax_speed': 0.8
        })

    def create_ground_decorations(self, level_width, level_height):
        """Criar decorações no chão"""
        decorations = []
        
        # Pedras
        for _ in range(25):
            decoration = {
                'x': random.randint(0, level_width),
                'y': level_height - random.randint(10, 30),
                'size': random.randint(8, 20),
                'type': 'rock',
                'color': (70, 60, 50),
                'parallax_speed': 1.0
            }
            decorations.append(decoration)
        
        # Ossadas
        for _ in range(8):
            decoration = {
                'x': random.randint(0, level_width),
                'y': level_height - random.randint(5, 15),
                'width': random.randint(20, 40),
                'height': random.randint(8, 15),
                'type': 'bone',
                'color': (200, 190, 180),
                'parallax_speed': 1.0
            }
            decorations.append(decoration)
        
        # Crateras pequenas
        for _ in range(10):
            decoration = {
                'x': random.randint(0, level_width),
                'y': level_height - 5,
                'radius': random.randint(15, 35),
                'depth': random.randint(3, 8),
                'type': 'crater',
                'color': (30, 20, 20),
                'parallax_speed': 1.0
            }
            decorations.append(decoration)
        
        self.parallax_layers.append({
            'elements': decorations,
            'type': 'decoration',
            'parallax_speed': 1.0
        })

    def create_atmospheric_effects(self):
        """Criar partículas atmosféricas"""
        for _ in range(20):
            particle = {
                'x': random.randint(0, 31 * 64),
                'y': random.randint(0, 12 * 64),
                'speed_x': random.uniform(-0.2, 0.2),
                'speed_y': random.uniform(-0.5, 0.1),
                'size': random.randint(1, 3),
                'color': random.choice([
                    (100, 80, 70),   # Cinza acastanhado
                    (80, 70, 60),    # Marrom claro
                    (60, 50, 40),    # Marrom escuro
                ]),
                'life': random.randint(300, 800),
                'max_life': 800,
                'type': 'ash'
            }
            self.atmospheric_particles.append(particle)

    def create_level(self):
        grass = load_image("grass_block.png")
        rocky = load_image("rocky_block.png")

        for row_index, row in enumerate(self.map_data):
            for col_index, tile in enumerate(row):
                if tile == "#":
                    block = Block(grass, col_index * 64, row_index * 64)
                    self.blocks.add(block)
                if tile == "@":
                    block = Block(rocky, col_index * 64, row_index * 64)
                    self.blocks.add(block)
    
    def spawn_enemies(self):
        """Cria os inimigos do level"""
        for x, y in self.enemy_spawns:
            demon = Demon(x, y)
            self.enemies.add(demon)
    
    def get_enemies(self):
        """Retorna o grupo de inimigos do level"""
        return self.enemies
    
    def update(self):
        """Atualizar elementos animados do background"""
        self.animation_timer += 1
        
        # Atualizar partículas atmosféricas
        self.update_atmospheric_particles()
        
        # Atualizar neblina (movimento lento)
        for layer in self.parallax_layers:
            if layer['type'] == 'fog':
                for fog in layer['elements']:
                    fog['x'] += fog['drift_speed']
                    # Reposicionar quando sair da tela
                    if fog['x'] > 31 * 64 + 300:
                        fog['x'] = -300

    def update_atmospheric_particles(self):
        """Atualizar partículas atmosféricas"""
        for particle in self.atmospheric_particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['life'] -= 1
            
            # Remover partículas mortas
            if particle['life'] <= 0:
                self.atmospheric_particles.remove(particle)
        
        # Adicionar novas partículas ocasionalmente
        if len(self.atmospheric_particles) < 15 and random.randint(1, 30) == 1:
            new_particle = {
                'x': random.randint(-50, 31 * 64 + 50),
                'y': random.randint(-20, 12 * 64),
                'speed_x': random.uniform(-0.3, 0.3),
                'speed_y': random.uniform(-0.8, 0.2),
                'size': random.randint(1, 4),
                'color': random.choice([
                    (100, 80, 70),
                    (80, 70, 60),
                    (60, 50, 40),
                ]),
                'life': random.randint(400, 1000),
                'max_life': 1000,
                'type': 'ash'
            }
            self.atmospheric_particles.append(new_particle)

    def draw_background(self, screen, camera_x, camera_y):
        """Desenhar todas as camadas do background com parallax"""
        # Céu gradiente (fixo)
        screen.blit(self.sky_gradient, (0, 0))
        
        # Desenhar camadas com parallax
        for layer in self.parallax_layers:
            self.draw_parallax_layer(screen, layer, camera_x, camera_y)
        
        # Desenhar partículas atmosféricas
        self.draw_atmospheric_particles(screen, camera_x, camera_y)
        
        # Efeitos de iluminação
        self.draw_lighting_effects(screen, camera_x, camera_y)

    def draw_parallax_layer(self, screen, layer, camera_x, camera_y):
        """Desenhar uma camada específica com efeito parallax"""
        parallax_x = camera_x * layer['parallax_speed']
        parallax_y = camera_y * layer['parallax_speed']
        
        for element in layer['elements']:
            screen_x = element['x'] - parallax_x
            screen_y = element['y'] - parallax_y
            
            # Só desenhar se estiver visível na tela
            if -200 <= screen_x <= SCREEN_WIDTH + 200 and -200 <= screen_y <= SCREEN_HEIGHT + 200:
                
                if layer['type'] == 'mountain':
                    self.draw_mountain(screen, element, screen_x, screen_y)
                elif layer['type'] == 'tree':
                    self.draw_dead_tree(screen, element, screen_x, screen_y)
                elif layer['type'] == 'fog':
                    self.draw_fog_patch(screen, element, screen_x, screen_y)
                elif layer['type'] == 'decoration':
                    self.draw_ground_decoration(screen, element, screen_x, screen_y)

    def draw_mountain(self, screen, mountain, x, y):
        """Desenhar silhueta de montanha"""
        # Montanha principal (triângulo)
        points = [
            (x, y + mountain['height']),
            (x + mountain['width'] // 2, y),
            (x + mountain['width'], y + mountain['height'])
        ]
        pygame.draw.polygon(screen, mountain['color'], points)
        
        # Picos menores para mais realismo
        for i in range(2):
            peak_x = x + (mountain['width'] // 3) * (i + 1)
            peak_height = mountain['height'] // (2 + i)
            peak_points = [
                (peak_x - 30, y + peak_height),
                (peak_x, y),
                (peak_x + 30, y + peak_height)
            ]
            pygame.draw.polygon(screen, (mountain['color'][0] - 10, mountain['color'][1] - 5, mountain['color'][2] - 5), peak_points)

    def draw_dead_tree(self, screen, tree, x, y):
        """Desenhar árvore morta"""
        # Tronco
        trunk_rect = pygame.Rect(x, y, tree['width'], tree['height'])
        pygame.draw.rect(screen, tree['color'], trunk_rect)
        
        # Galhos
        branch_y = y + tree['height'] // 3
        for i in range(tree['branches']):
            branch_length = random.randint(20, 40)
            branch_angle = (-1 + i * 0.5) if i % 2 == 0 else (1 - i * 0.3)
            
            end_x = x + tree['width'] // 2 + branch_length * branch_angle
            end_y = branch_y + random.randint(-15, 15)
            
            pygame.draw.line(screen, tree['color'], 
                           (x + tree['width'] // 2, branch_y), 
                           (int(end_x), int(end_y)), 3)
            
            branch_y += tree['height'] // (tree['branches'] + 1)

    def draw_fog_patch(self, screen, fog, x, y):
        """Desenhar patch de neblina"""
        # Criar superfície com alpha
        fog_surface = pygame.Surface((fog['width'], fog['height']), pygame.SRCALPHA)
        
        # Gradiente circular para neblina
        center_x = fog['width'] // 2
        center_y = fog['height'] // 2
        max_radius = min(center_x, center_y)
        
        for radius in range(max_radius, 0, -5):
            alpha = int(fog['alpha'] * (radius / max_radius))
            color = (150, 150, 150, alpha)
            pygame.draw.circle(fog_surface, color, (center_x, center_y), radius)
        
        screen.blit(fog_surface, (int(x), int(y)))

    def draw_ground_decoration(self, screen, decoration, x, y):
        """Desenhar decorações do chão"""
        if decoration['type'] == 'rock':
            # Pedra (círculo irregular)
            pygame.draw.circle(screen, decoration['color'], (int(x), int(y)), decoration['size'])
            # Sombra
            pygame.draw.circle(screen, (decoration['color'][0] - 20, decoration['color'][1] - 20, decoration['color'][2] - 20), 
                             (int(x + 2), int(y + 2)), decoration['size'] - 2)
            
        elif decoration['type'] == 'bone':
            # Osso (retângulo alongado)
            bone_rect = pygame.Rect(x, y, decoration['width'], decoration['height'])
            pygame.draw.ellipse(screen, decoration['color'], bone_rect)
            # Extremidades do osso
            pygame.draw.circle(screen, decoration['color'], (int(x), int(y + decoration['height'] // 2)), decoration['height'] // 2)
            pygame.draw.circle(screen, decoration['color'], (int(x + decoration['width']), int(y + decoration['height'] // 2)), decoration['height'] // 2)
            
        elif decoration['type'] == 'crater':
            # Cratera (círculo escuro com borda)
            pygame.draw.circle(screen, decoration['color'], (int(x), int(y)), decoration['radius'])
            pygame.draw.circle(screen, (decoration['color'][0] + 20, decoration['color'][1] + 10, decoration['color'][2] + 10), 
                             (int(x), int(y)), decoration['radius'], 2)

    def draw_atmospheric_particles(self, screen, camera_x, camera_y):
        """Desenhar partículas atmosféricas"""
        for particle in self.atmospheric_particles:
            screen_x = particle['x'] - camera_x
            screen_y = particle['y'] - camera_y
            
            # Só desenhar se visível
            if -10 <= screen_x <= SCREEN_WIDTH + 10 and -10 <= screen_y <= SCREEN_HEIGHT + 10:
                # Alpha baseado na vida da partícula
                alpha_ratio = particle['life'] / particle['max_life']
                alpha = int(255 * alpha_ratio * 0.6)  # Máximo 60% de alpha
                
                # Criar superfície com alpha
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                color_with_alpha = (*particle['color'], alpha)
                pygame.draw.circle(particle_surface, particle['color'], (particle['size'], particle['size']), particle['size'])
                
                screen.blit(particle_surface, (int(screen_x - particle['size']), int(screen_y - particle['size'])))

    def draw_lighting_effects(self, screen, camera_x, camera_y):
        """Desenhar efeitos de iluminação atmosférica"""
        # Luz vermelha sinistra (simulando lua vermelha)
        light_intensity = 30 + 10 * abs(math.sin(self.animation_timer * 0.02))
        light_color = (int(light_intensity), int(light_intensity * 0.3), int(light_intensity * 0.2))
        
        # Overlay de luz
        light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        light_surface.fill((*light_color, 20))
        screen.blit(light_surface, (0, 0))