import pygame
import os
import sys

def get_resource_path(relative_path):
    """Obter caminho correto para recursos em exe ou desenvolvimento"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Se não estiver compilado, usar o caminho normal
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, relative_path)

def load_image(file_path):
    """Carregar imagem com caminho correto para desenvolvimento e exe"""
    full_path = get_resource_path(os.path.join("assets", file_path))
    
    # Verificar se o arquivo existe
    if not os.path.exists(full_path):
        # Tentar caminho alternativo para desenvolvimento
        alt_path = os.path.join("assets", file_path)
        if os.path.exists(alt_path):
            full_path = alt_path
        else:
            # Criar uma imagem placeholder se não encontrar
            print(f"Aviso: Imagem não encontrada: {file_path}")
            placeholder = pygame.Surface((64, 64))
            placeholder.fill((255, 0, 255))  # Magenta para indicar erro
            return placeholder.convert_alpha()
    
    try:
        return pygame.image.load(full_path).convert_alpha()
    except pygame.error as e:
        print(f"Erro ao carregar {file_path}: {e}")
        # Retornar placeholder em caso de erro
        placeholder = pygame.Surface((64, 64))
        placeholder.fill((255, 0, 255))
        return placeholder.convert_alpha()