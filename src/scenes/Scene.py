import pygame

class Scene:
    """Classe base para todas as cenas do jogo"""
    
    def __init__(self, game):
        self.game = game
        self.next_scene = None
        
    def handle_events(self, events):
        """Lidar com eventos da cena"""
        pass
        
    def update(self):
        """Atualizar lógica da cena"""
        pass
        
    def draw(self, screen):
        """Desenhar a cena"""
        pass