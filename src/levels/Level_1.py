import pygame
from entities.Block import Block
from entities.Demon import Demon
from utils.assets_loader import load_image

class Level_1:
    def __init__(self, game):
        self.game = game
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

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

        self.create_level()
        self.spawn_enemies()

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