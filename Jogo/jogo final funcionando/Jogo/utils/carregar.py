import pygame
import os

def carregar_imagem(caminho, tamanho=None):

    imagem = pygame.image.load(caminho).convert_alpha()

    if tamanho:
        imagem = pygame.transform.scale(imagem, tamanho)

    return imagem

def carregar_cartas():

    pasta = os.path.join(BASE_DIR, "assets", "cartas")

    return [
        os.path.join(pasta, arquivo)
        for arquivo in os.listdir(pasta)
    ]

import os
import pygame

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

def carregar_imagem(caminho, tamanho=None):

    caminho_completo = os.path.join(
        BASE_DIR,
        caminho
    )

    imagem = pygame.image.load(
        caminho_completo
    ).convert_alpha()

    if tamanho:
        imagem = pygame.transform.smoothscale(
            imagem,
            tamanho
        )

    return imagem