import pygame
from scenes.SceneManager import SceneManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        self.tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Demon Hunter")

        self.clock = pygame.time.Clock()
        self.running = True
        
        # Gerenciador de cenas
        self.scene_manager = SceneManager(self)
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            # Capturar eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Atualizar cena atual
            self.scene_manager.handle_events(events)
            self.scene_manager.update()
            
            # Desenhar cena atual
            self.scene_manager.draw(self.tela)
            pygame.display.flip()


    