import pygame

from game.jogo import Jogo

class Menu:

    def __init__(self, tela):

        self.tela = tela

        self.estado = "menu"

        self.jogo = None

        self.fonte_titulo = pygame.font.SysFont(
            "arialblack",
            60
        )

        self.fonte = pygame.font.SysFont(
            "arial",
            32
        )

        self.criar_botoes()

    def criar_botoes(self):

        largura = self.tela.get_width()

        largura_botao = 350
        altura_botao = 70

        x = largura // 2 - largura_botao // 2

        self.botoes = {

            "solo": pygame.Rect(
                x,
                220,
                largura_botao,
                altura_botao
            ),

            "bots": pygame.Rect(
                x,
                320,
                largura_botao,
                altura_botao
            ),

            "multi": pygame.Rect(
                x,
                420,
                largura_botao,
                altura_botao
            ),

            "ajuda": pygame.Rect(
                x,
                520,
                largura_botao,
                altura_botao
            )
        }

    def eventos(self, evento):

        if evento.type == pygame.VIDEORESIZE:
            self.criar_botoes()

        if self.estado == "menu":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if self.botoes["solo"].collidepoint(evento.pos):

                    self.jogo = Jogo(self.tela)

                    self.estado = "jogo"

                elif self.botoes["bots"].collidepoint(evento.pos):

                    self.estado = "bots"

                elif self.botoes["multi"].collidepoint(evento.pos):

                    self.estado = "multi"

                elif self.botoes["ajuda"].collidepoint(evento.pos):

                    self.estado = "ajuda"

        elif self.estado == "jogo":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                self.jogo.clicar(evento.pos)

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    self.estado = "menu"

        else:

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    self.estado = "menu"

    def desenhar_botao(self, nome, texto):

        rect = self.botoes[nome]

        mouse = pygame.mouse.get_pos()

        cor = (60, 60, 60)

        if rect.collidepoint(mouse):

            cor = (100, 100, 100)

        pygame.draw.rect(
            self.tela,
            cor,
            rect,
            border_radius=18
        )

        pygame.draw.rect(
            self.tela,
            (255, 255, 255),
            rect,
            3,
            border_radius=18
        )

        render = self.fonte.render(
            texto,
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            render,
            (
                rect.centerx - render.get_width() // 2,
                rect.centery - render.get_height() // 2
            )
        )

    def desenhar(self):

        self.tela.fill((15, 15, 25))

        if self.estado == "menu":

            titulo = self.fonte_titulo.render(
                "JOGO DA MEMÓRIA",
                True,
                (255, 255, 255)
            )

            self.tela.blit(
                titulo,
                (
                    self.tela.get_width() // 2
                    - titulo.get_width() // 2,
                    90
                )
            )

            self.desenhar_botao(
                "solo",
                "Jogar Sozinho"
            )

            self.desenhar_botao(
                "bots",
                "Contra Bots"
            )

            self.desenhar_botao(
                "multi",
                "Multijogador"
            )

            self.desenhar_botao(
                "ajuda",
                "Ajuda"
            )

        elif self.estado == "jogo":

            self.jogo.atualizar()

            self.jogo.desenhar()

        elif self.estado == "ajuda":

            textos = [

                "AJUDA",
                """- Encontre os pares de cartas idênticas para ganhar pontos.""",
                
                """- Cada carta tem uma raridade que determina quantos pontos ela vale.""",
                
                """- Você começa com 60 pontos e perde 1 ponto a cada tentativa.""",
                
                """- O multiplicador aumenta a cada par encontrado, aumentando os pontos ganhos.""",
                
                """- Encontre todas as cartas antes de ficar sem tentativas!""",
                    """Raridades:
                    - Comum: 15 pontos
                    - Incomum: 25 pontos
                    - Rara: 50 pontos
                    - Épica: 75 pontos
                    - Lendária: 100 pontos"""

            ]

            for i, linha in enumerate(textos):

                render = self.fonte.render(
                    linha,
                    True,
                    (255, 255, 255)
                )

                self.tela.blit(
                    render,
                    (120, 120 + i * 50)
                )

        elif self.estado == "bots":

            render = self.fonte.render(
                "Modo Bots em desenvolvimento",
                True,
                (255, 255, 255)
            )

            self.tela.blit(render, (100, 200))

        elif self.estado == "multi":

            render = self.fonte.render(
                "Modo Multiplayer em desenvolvimento",
                True,
                (255, 255, 255)
            )

            self.tela.blit(render, (100, 200))