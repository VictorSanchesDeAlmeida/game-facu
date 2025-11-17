import pygame
import os

def load_image(file_path):
    path = os.path.join("assets", file_path)
    return pygame.image.load(path).convert_alpha()