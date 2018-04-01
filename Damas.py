from cmath import rect
from textwrap import fill

import pygame

pygame.init()  # inica o jogo

largura_tela = 660
altura_tela = 660

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
azure = (252,230,251)

gameDisplay = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption(' Damas ')
clock = pygame.time.Clock()

# Quadrado
size = 80

# CORES
yellow = (255, 215, 0)
cinza = (239, 235, 235)
blue = (100, 149, 237)
coral = (240, 128, 128)
brown = (139,69,19)
bege = (255,211,155)
# Bordas

casas = 8
gameDisplay.fill(cinza)
bordaexterna = 10


def desenha_tabuleiro():
    cnt = 0
    for i in range(0, casas):
        for z in range(0, casas):
            if cnt % 2 == 0:
                pygame.draw.rect(gameDisplay, bege, [size * z + bordaexterna, size * i + bordaexterna, size, size])
            else:
                pygame.draw.rect(gameDisplay, brown, [size * z + bordaexterna, size * i + bordaexterna, size, size])
            cnt += 1
        cnt -= 1
    pygame.draw.rect(gameDisplay, brown, [bordaexterna, bordaexterna, casas * size, casas * size], 5)


def desenha_peca():
    for i in range(0, 3):
        deslocamento = 0
        for z in range(0, 8, 2):
            if (i % 2 == 0):
                deslocamento = 80
            pygame.draw.circle(gameDisplay, azure, [50 + (80 * z) + deslocamento, 50 + (80 * i)], int(size / 2 - 10))
            pygame.draw.circle(gameDisplay, black, [610 - 80 * z - deslocamento, 610 - 80 * i], int(size / 2 - 10))


class Peca:
    def __init__(self, cor, queen=False):
        self.cor = cor
        self.queen = queen


crashed = False

desenha_tabuleiro()
desenha_peca()
while not crashed:

    # check para eventos de erro
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()  # atualizar o frame do jogo
    clock.tick(60)  # parâmetro define fps

pygame.quit()
quit()