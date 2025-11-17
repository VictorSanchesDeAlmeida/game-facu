import pygame
from scenes.MenuScene import MenuScene

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = MenuScene(game)  # Começar no menu
        
    def handle_events(self, events):
        self.current_scene.handle_events(events)
        
        # Verificar se há uma mudança de cena
        if self.current_scene.next_scene:
            self.current_scene = self.current_scene.next_scene
            
    def update(self):
        self.current_scene.update()
        
    def draw(self, screen):
        self.current_scene.draw(screen)