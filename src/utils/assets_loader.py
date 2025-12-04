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
    # Primeiro tenta o caminho completo via get_resource_path
    full_path = get_resource_path(os.path.join("assets", file_path))
    
    # Se não encontrar, tenta variações do nome do arquivo
    if not os.path.exists(full_path):
        # Tenta com o nome em maiúsculo (Player.png ao invés de player.png)
        capitalized_name = file_path.title()
        alt_path = get_resource_path(os.path.join("assets", capitalized_name))
        if os.path.exists(alt_path):
            full_path = alt_path
        else:
            # Tenta apenas o caminho relativo para desenvolvimento
            dev_path = os.path.join("assets", file_path)
            if os.path.exists(dev_path):
                full_path = dev_path
            else:
                # Tenta o nome capitalizado no desenvolvimento
                dev_cap_path = os.path.join("assets", capitalized_name)
                if os.path.exists(dev_cap_path):
                    full_path = dev_cap_path
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