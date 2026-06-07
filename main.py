import pygame

from game.menu import Menu

from config import (
    LARGURA,
    ALTURA,
    FPS,
    TELA_REDIMENSIONAVEL,
    FULLSCREEN
)
from game.tabuleiro import Tabuleiro
from utils.carregar import carregar_imagem

pygame.init()

flags = 0

if TELA_REDIMENSIONAVEL:
    flags |= pygame.RESIZABLE

if FULLSCREEN:
    flags |= pygame.FULLSCREEN

tela = pygame.display.set_mode(
    (LARGURA, ALTURA),
    flags
)

pygame.display.set_caption("Jogo da Memória")

clock = pygame.time.Clock()

menu = Menu(tela)

rodando = True

while rodando:

    clock.tick(FPS)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.VIDEORESIZE:

            tela = pygame.display.set_mode(
                (evento.w, evento.h),
                flags
            )

            menu.tela = tela

            if menu.jogo:
                menu.jogo.tela = tela
                menu.jogo.tabuleiro = Tabuleiro(
                    evento.w,
                    evento.h
                )
                menu.jogo.fundo = carregar_imagem(
                    "assets/fundo/fundo.png",
                    (evento.w, evento.h)
                )
        menu.eventos(evento)

    menu.desenhar()


    pygame.display.update()

pygame.quit()