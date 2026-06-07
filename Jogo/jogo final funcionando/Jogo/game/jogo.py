import pygame
import json
import os
from game import carta
from Ranking import (
    carregar,
    salvar_pontuacao
)
from game.tabuleiro import Tabuleiro
from game.jogador import Jogador
from game.particula import Particula
from utils.carregar import carregar_imagem
from config import (
    CORES,
    LARGURA,
    ALTURA
)



class Jogo:

    def __init__(self, tela):

        self.tela = tela
        self.fim_de_jogo = False

        self.ranking = carregar()
        self.particulas = []

        self.fundo = carregar_imagem(
            "assets/fundo/fundo.jpg",
            (
                self.tela.get_width(),
                self.tela.get_height()
            )
        )

        largura = self.tela.get_width()
        altura = self.tela.get_height()

        self.tabuleiro = Tabuleiro(
            largura,
            altura
        )

        self.jogador = Jogador()

        self.cartas_selecionadas = []

        self.tempo_espera = 0

        tamanho_fonte = int(
            self.tela.get_width() * 0.018
        )

        self.fonte = pygame.font.SysFont(
            "arial",
            tamanho_fonte
        )

    def atualizar(self):

        if self.tempo_espera > 0:

            tempo = pygame.time.get_ticks()

            if tempo - self.tempo_espera > 900:

                self.verificar_cartas()

                self.tempo_espera = 0

        for particula in self.particulas:

            particula.atualizar()

        self.particulas = [

            p for p in self.particulas

            if p.vida > 0

        ]

    def clicar(self, pos):

        if len(self.cartas_selecionadas) >= 2:
            return

        for carta in self.tabuleiro.cartas:

            if carta.clicar(pos):

                if not carta.revelada and not carta.encontrada:
                    agora = pygame.time.get_ticks()
                    carta.revelada = True
                    carta.tempo_brilho = agora
                    carta.tempo_preview = agora
                    
                    self.cartas_selecionadas.append(carta)

                    if len(self.cartas_selecionadas) == 2:

                        self.tempo_espera = (
                            pygame.time.get_ticks()
                        )

    def criar_particulas(self, x, y, cor):

        for _ in range(20):

            self.particulas.append(

                Particula(
                    x,
                    y,
                    cor
                )

            )

    def verificar_cartas(self):
        if self.jogador.tentativas_restantes <= 0:
            self.finalizar_partida()
            return
        if len(self.cartas_selecionadas) < 2:
            return
        c1, c2 = self.cartas_selecionadas
        self.jogador.turnos += 1
        self.jogador.tentativas_restantes -= 1
        if c1.id == c2.id:

            c1.encontrada = True
            c2.encontrada = True

            ganho = int(
                c1.pontos *
                self.jogador.multiplicador
            )

            self.jogador.pontos += ganho
            self.criar_particulas(
                c1.rect.centerx,
                c1.rect.centery,
                (255, 220, 80)
            )

        else:

            c1.revelada = False
            c2.revelada = False

            self.jogador.pontos -= 1

            self.criar_particulas(
                c1.rect.centerx,
                c1.rect.centery,
                (255, 80, 80)
            )

        if self.venceu():
            self.finalizar_partida()
        self.cartas_selecionadas.clear()

    def desenhar_hud(self):

        hud = pygame.Rect(
            20,
            15,
            340,
            250
        )

        pygame.draw.rect(
            self.tela,
            (20, 20, 30),
            hud,
            border_radius=20
        )

        pygame.draw.rect(
            self.tela,
            (255, 255, 255),
            hud,
            2,
            border_radius=20
        )

        texto = self.fonte.render(
            f"Pontos: {self.jogador.pontos}",
            True,
            CORES["branco"]
        )

        turnos = self.fonte.render(
            f"Turnos: {self.jogador.turnos}",
            True,
            (210, 210, 210)
        )

        tentativas = self.fonte.render(
            f"Tentativas: {self.jogador.tentativas_restantes}",
            True,
            CORES["branco"]
        )

        combo = self.fonte.render(
            f"Combo: x{self.jogador.multiplicador:.1f}",
            True,
            (255, 220, 80)
        )
        raridade1 = "---"
        raridade2 = "---"

        if len(self.cartas_selecionadas) >= 1:
            raridade1 = self.cartas_selecionadas[0].raridade

        if len(self.cartas_selecionadas) >= 2:
            raridade2 = self.cartas_selecionadas[1].raridade

        carta1 = self.fonte.render(
            f"Carta 1: {raridade1}",
            True,
            (255, 255, 255)
        )

        carta2 = self.fonte.render(
            f"Carta 2: {raridade2}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(carta1, (40, 178))
        self.tela.blit(carta2, (40, 208))
        self.tela.blit(texto, (40, 28))
        self.tela.blit(turnos, (40, 58))
        self.tela.blit(tentativas, (40, 118))
        self.tela.blit(combo, (40, 148))

    def desenhar(self):

        self.tela.blit(self.fundo, (0, 0))

        self.tabuleiro.desenhar(self.tela)
        for carta in self.tabuleiro.cartas:

            if (
                carta.tempo_preview > 0 and
                pygame.time.get_ticks() -
                carta.tempo_preview < 1000
            ):
                carta.desenhar_preview(
                    self.tela
                )

        self.desenhar_hud()

        if self.fim_de_jogo:
            self.tela.blit(
                self.fundo,
                (0, 0)
            )
            self.desenhar_ranking()

            return

        for particula in self.particulas:

            particula.desenhar(self.tela)
            
    def venceu(self):

        return all(
            carta.encontrada
            for carta in self.tabuleiro.cartas
        )
    def salvar_recorde(self):

        arquivo = "rank.json"

        if os.path.exists(arquivo):

            with open(
                arquivo,
                "r",
                encoding="utf8"
            ) as f:

                ranking = json.load(f)

        else:

            ranking = []

        ranking.append({

            "pontos": self.jogador.pontos,
            "turnos": self.jogador.turnos

        })

        ranking.sort(
            key=lambda x: x["pontos"],
            reverse=True
        )

        ranking = ranking[:10]

        with open(
            arquivo,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                ranking,
                f,
                indent=4,
                ensure_ascii=False
            )
    def finalizar_partida(self):
        self.ranking = salvar_pontuacao(

            self.jogador.pontos,

            self.jogador.turnos

        )

        self.fim_de_jogo = True

    def desenhar_ranking(self):

        titulo = self.fonte.render(

            "TOP 10",

            True,

            (255, 255, 0)

        )

        self.tela.blit(

            titulo,

            (500, 80)

        )

        y = 150

        for posicao, item in enumerate(
            self.ranking,
            start=1
        ):

            texto = self.fonte.render(

                f"{posicao}º  {item['pontos']} pts",

                True,

                (255, 255, 255)

            )

            self.tela.blit(

                texto,

                (500, y)

            )
            y += 40
        
