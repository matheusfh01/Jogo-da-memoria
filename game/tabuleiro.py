import random
import math

from game.carta import Carta

from utils.carregar import carregar_cartas

class Tabuleiro:

    def __init__(self, largura_tela, altura_tela):

        self.cartas = []

        self.criar_cartas(
            largura_tela,
            altura_tela
        )

    def criar_cartas(
        self,
        largura_tela,
        altura_tela
    ):

        imagens = carregar_cartas()

        if len(imagens) < 2:
            raise Exception(
                "Coloque imagens em assets/cartas/"
            )

        quantidade_pares = min(
            len(imagens),
            30
        )

        imagens = imagens[:quantidade_pares]

        pares = imagens * 2

        random.shuffle(pares)

        total_cartas = len(pares)

        colunas = math.ceil(
            math.sqrt(total_cartas)
        )

        linhas = math.ceil(
            total_cartas / colunas
        )

        margem = 20
        espaco = 10

        largura_disponivel = (
            largura_tela - margem * 2
        )

        altura_disponivel = (
            altura_tela - 160
        )

        largura_carta = (
            largura_disponivel -
            (colunas - 1) * espaco
        ) // colunas

        altura_carta = int(
            largura_carta * 1.4
        )

        while (
            linhas * altura_carta +
            (linhas - 1) * espaco
        ) > altura_disponivel:

            largura_carta -= 5

            altura_carta = int(
                largura_carta * 1.4
            )

        tamanho = (
            largura_carta,
            altura_carta
        )

        largura_total = (
            colunas * largura_carta +
            (colunas - 1) * espaco
        )

        altura_total = (
            linhas * altura_carta +
            (linhas - 1) * espaco
        )

        x_inicial = (
            largura_tela - largura_total
        ) // 2

        y_inicial = (
            altura_tela - altura_total
        ) // 2 + 30

        indice = 0

        for linha in range(linhas):

            for coluna in range(colunas):

                if indice >= total_cartas:
                    return

                x = x_inicial + coluna * (
                    largura_carta + espaco
                )

                y = y_inicial + linha * (
                    altura_carta + espaco
                )

                imagem = pares[indice]

                raridade, pontos = (
                    self.definir_raridade(imagem)
                )

                self.cartas.append(
                    Carta(
                        imagem,
                        (x, y),
                        tamanho,
                        raridade,
                        pontos
                    )
                )

                indice += 1

        for linha in range(linhas):

            for coluna in range(colunas):

                if indice >= total_cartas:
                    return

                x = x_inicial + coluna * (
                    largura_carta + espaco
                )

                y = y_inicial + linha * (
                    altura_carta + espaco
                )

                imagem = pares[indice]

                raridade, pontos = (
                    self.definir_raridade(imagem)
                )

                self.cartas.append(
                    Carta(
                        imagem,
                        (x, y),
                        tamanho,
                        raridade,
                        pontos
                    )
                )

                indice += 1
        for linha in range(linhas):

            for coluna in range(colunas):

                if indice >= total_cartas:
                    return

                x = x_inicial + coluna * (
                    largura_carta + espaco
                )

                y = y_inicial + linha * (
                    altura_carta + espaco
                )

                imagem = pares[indice]

                raridade, pontos = (
                    self.definir_raridade(imagem)
                )

                carta = Carta(
                    imagem,
                    (x, y),
                    tamanho,
                    raridade,
                    pontos
                )

                self.cartas.append(carta)

                indice += 1
    
    def definir_raridade(self, imagem):

        nome = imagem.lower()

        if "lendaria" in nome:
            return "Lendária", 100

        elif "epica" in nome:
            return "Épica", 75

        elif "rara" in nome:
            return "Rara", 50

        elif "incomum" in nome:
            return "Incomum", 25

        return "Comum", 15

    def desenhar(self, tela):

        for carta in self.cartas:
            carta.desenhar(tela)