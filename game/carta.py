from cmath import rect

import pygame
import math

from utils.carregar import carregar_imagem

class Carta:

    def __init__(
        self,
        imagem,
        posicao,
        tamanho,
        raridade,
        pontos
    ):
        self.tempo_preview = 0
        self.tempo_brilho = 0
        self.tamanho = tamanho
        self.tempo_zoom = 0
        self.frente_original = carregar_imagem(imagem)

        self.verso_original = carregar_imagem(
            "assets/verso/verso.png"
        )

        self.frente = pygame.transform.smoothscale(
            self.frente_original,
            tamanho
        )

        self.verso = pygame.transform.smoothscale(
            self.verso_original,
            tamanho
        )

        self.rect = self.frente.get_rect(
            topleft=posicao
        )

        self.revelada = False
        self.encontrada = False

        self.raridade = raridade
        self.pontos = pontos

        self.id = imagem

        self.flip = 0

    def atualizar(self):

        alvo = 180 if self.revelada else 0

        self.flip += (alvo - self.flip) * 0.2

    def cor_raridade(self):

        cores = {
            "Comum": (180, 180, 180),
            "Incomum": (80, 255, 120),
            "Rara": (80, 160, 255),
            "Épica": (180, 80, 255),
            "Lendária": (255, 180, 60)
        }

        return cores.get(
            self.raridade,
            (255, 255, 255)
        )

    def desenhar(self, tela):

        self.atualizar()

        escala_x = abs(
            math.cos(
                math.radians(self.flip)
            )
        )

        largura = max(
            1,
            int(self.tamanho[0] * escala_x)
        )

        altura = self.tamanho[1]

        imagem = self.verso

        if self.flip > 90:
            imagem = self.frente

        imagem = pygame.transform.smoothscale(
            imagem,
            (largura, altura)
        )

        rect = imagem.get_rect(
            center=self.rect.center
        )
        tempo = pygame.time.get_ticks()

        if (
            self.revelada and
            tempo - self.tempo_zoom < 400
        ):

            progresso = (
                tempo - self.tempo_zoom
            ) / 400

            zoom = 1.5 - (0.5 * progresso)

            largura_zoom = int(
                largura * zoom
            )

            altura_zoom = int(
                altura * zoom
            )

            imagem = pygame.transform.smoothscale(
                imagem,
                (
                    largura_zoom,
                    altura_zoom
                )
            )

            rect = imagem.get_rect(
                center=self.rect.center
            )
        if self.revelada:
            self.desenhar_brilho(tela)

        tela.blit(imagem, rect)
        if (
            self.revelada and
            tempo - self.tempo_zoom < 400
        ):

            fonte = pygame.font.SysFont(
                "arial",
                32,
                bold=True
            )

            texto = fonte.render(
                f"{self.simbolo_raridade()} {self.raridade}",
                True,
                self.cor_raridade()
            )

            sombra = fonte.render(
                f"{self.simbolo_raridade()} {self.raridade}",
                True,
                (0, 0, 0)
            )

            texto_rect = texto.get_rect(
                center=(
                    self.rect.centerx,
                    self.rect.y - 30
                )
            )

            tela.blit(
                sombra,
                (
                    texto_rect.x + 2,
                    texto_rect.y + 2
                )
            )

            tela.blit(
                texto,
                texto_rect
            )

    def clicar(self, pos):
        
        return self.rect.collidepoint(pos)
    
    def desenhar_brilho(self, tela):

        if self.tempo_brilho == 0:
            return

        tempo = pygame.time.get_ticks()

        if tempo - self.tempo_brilho > 600:
            return

        if self.raridade == "Lendária":
            cor = (255, 215, 0)

        elif self.raridade == "Épica":
            cor = (180, 0, 255)

        elif self.raridade == "Rara":
            cor = (0, 120, 255)

        elif self.raridade == "Incomum":
            cor = (0, 220, 100)

        else:
            cor = (220, 220, 220)

        alpha = int(
            180 * (
                1 -
                (tempo - self.tempo_brilho)
                / 600
            )
        )

        brilho = pygame.Surface(
            (
                self.rect.width + 20,
                self.rect.height + 20
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            brilho,
            (*cor, alpha),
            brilho.get_rect(),
            border_radius=20
        )

        tela.blit(
            brilho,
            (
                self.rect.x - 10,
                self.rect.y - 10
            )
        )
    def simbolo_raridade(self):

        simbolos = {
            "Comum": "●",
            "Incomum": "◆",
            "Rara": "★",
            "Épica": "★★",
            "Lendária": "★★★"
        }

        return simbolos.get(
            self.raridade,
            "●"
        )
    def desenhar_preview(self, tela):

        tempo = pygame.time.get_ticks()

        if (
            not hasattr(self, "tempo_zoom")
            or self.tempo_zoom == 0
            or tempo - self.tempo_zoom > 1000
        ):
            return

        largura = int(tela.get_width() * 0.45)
        altura = int(tela.get_height() * 0.65)

        imagem = pygame.transform.smoothscale(
            self.frente,
            (largura, altura)
        )

        rect = imagem.get_rect(
            center=(
                tela.get_width() // 2,
                tela.get_height() // 2
            )
        )

        sombra = pygame.Surface(
            tela.get_size(),
            pygame.SRCALPHA
        )

        sombra.fill((0, 0, 0, 180))

        tela.blit(sombra, (0, 0))
        tela.blit(imagem, rect)

        simbolos = {
            "Comum": "●",
            "Incomum": "◆",
            "Rara": "★",
            "Épica": "★★",
            "Lendária": "★★★"
        }

        cores = {
            "Comum": (200, 200, 200),
            "Incomum": (0, 255, 100),
            "Rara": (0, 150, 255),
            "Épica": (180, 0, 255),
            "Lendária": (255, 215, 0)
        }

        fonte = pygame.font.SysFont(
            "arial",
            70,
            bold=True
        )

        texto = fonte.render(
            simbolos[self.raridade],
            True,
            cores[self.raridade]
        )

        texto_rect = texto.get_rect(
            center=(
                rect.centerx,
                rect.top - 50
            )
        )

        tela.blit(texto, texto_rect)