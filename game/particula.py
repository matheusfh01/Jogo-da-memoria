import pygame
import random

class Particula:

    def __init__(self, x, y, cor):

        self.x = x
        self.y = y

        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)

        self.vida = 30

        self.cor = cor

        self.tamanho = random.randint(3, 7)

    def atualizar(self):

        self.x += self.vel_x
        self.y += self.vel_y

        self.vida -= 1

    def desenhar(self, tela):

        if self.vida > 0:

            pygame.draw.circle(
                tela,
                self.cor,
                (int(self.x), int(self.y)),
                self.tamanho
            )