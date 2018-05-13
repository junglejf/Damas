from cmath import rect
from textwrap import fill

import pygame


pygame.init()#inica o jogo

largura_tela = 660
altura_tela = 660

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
red2 = (255,100,0)

gameDisplay = pygame.display.set_mode((largura_tela,altura_tela))
pygame.display.set_caption(' Damas ' )
clock = pygame.time.Clock()

#Quadrado
size = 80

#CORES
yellow = (255,215,0)
cinza = (239, 235, 235)
blue = (100,149,237)
coral = (240,128,128)
#Bordas

casas = 8
gameDisplay.fill(cinza)
bordaexterna = 10

def desenha_tabuleiro(tabuleiro):
    for i in range(0,tabuleiro.dimensao):
        for z in range(0,tabuleiro.dimensao):
            pygame.draw.rect(gameDisplay, tab[i][z].cor,[tab[i][z].tamanho * z + bordaexterna, tab[i][z].tamanho * i + bordaexterna, tab[i][z].tamanho, tab[i][z].tamanho])
    pygame.draw.rect(gameDisplay,black,[bordaexterna,bordaexterna,casas*size,casas*size],5)

def desenha_peca():
    for i in range(0,3):
        deslocamento = 0
        for z in range(0,8,2):
            if (i % 2 == 0):
                deslocamento = 80
            pygame.draw.circle(gameDisplay, coral, [50+(80*z)+deslocamento, 50+(80*i)], int(size / 2 - 10))
            pygame.draw.circle(gameDisplay, blue, [610 - 80*z - deslocamento, 610 - 80*i], int(size / 2 - 10))

    
class Componente():
    print(white)
    def __init__(self, posX , posY, tamanho, cor ):
        self.posX = posX
        self.posY = posY
        self.tamanho = tamanho
        self.cor = cor

class Quadrado(Componente):
    def __init__(self, posX, posY, tamanho,cor, ocupado = False, vira_Rainha = False ):
        Componente.__init__(self, posX, posY, tamanho , cor)
        self.ocupado = ocupado
        self.vira_Rainha = vira_Rainha

class Peca(Componente):
    def __init__(self, posX, posY, tamanho, cor, queen, foipulada):
        Componente.__init__(self, posX, posY, tamanho, cor)
        self.queen = queen
        self.foipulada = foipulada







class Tabuleiro:
    def __init__(self, dimensao,pecas):
        self.dimensao = dimensao
        self.pecas = pecas

    def constroitab(self):
        cnt = 0
        matriz=[]
        for i in range(0, self.dimensao):
            linha = []
            for z in range(0, self.dimensao):
                if cnt % 2 == 0:
                    q = Quadrado(0,0,80, white)
                    pygame.draw.rect(gameDisplay, q.cor, [q.tamanho * z + bordaexterna, q.tamanho * i + bordaexterna, q.tamanho, q.tamanho])
                else:
                    q = Quadrado(0, 0, 80, black)
                    pygame.draw.rect(gameDisplay, q.cor, [q.tamanho * z + bordaexterna, q.tamanho * i + bordaexterna, q.tamanho, q.tamanho])
                linha.append(q)
                cnt += 1
            cnt -= 1
            matriz.append(linha)
        pygame.draw.rect(gameDisplay, black, [bordaexterna, bordaexterna, casas * size, casas * size], 5)
        return matriz

crashed = False


#desenha_tabuleiro()
tab = Tabuleiro(8,0)
board = tab.constroitab()
desenha_peca()
l =[]

while not crashed:
	

	for event in pygame.event.get():

		if (event.type == pygame.QUIT):
			crashed = True
		print(event)


	pygame.display.update() #atualizar o frame do jogo
	clock.tick(60) #parâmetro define


	
pygame.quit()
quit()

#modifiquei arquivo
