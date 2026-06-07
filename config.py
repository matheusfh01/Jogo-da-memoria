import pygame

pygame.init()

info = pygame.display.Info()

LARGURA = int(info.current_w * 0.85)
ALTURA = int(info.current_h * 0.85)

FPS = 60

TELA_REDIMENSIONAVEL = True
FULLSCREEN = False

BASE_LARGURA = 1280
BASE_ALTURA = 720

CORES = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "verde": (0, 255, 0),
    "vermelho": (255, 0, 0),
    "cinza": (40, 40, 40)
}