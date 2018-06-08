import pygame
import time
import random

pygame.init()

LARGURA = 640
ALTURA = 640

BEGE = (238,238,210)
PRETO = (0, 0, 0)
FOSCO = (158, 158, 158)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERDE_ESCURO = (118,150,86)
YELLOW = (0, 255, 0)
VERMELHO_CLARO = (255, 0, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TAB = (0, 31, 0)
YELLOW = (255,215,0)
CINZA = (222, 235, 235)
MARROM = (235,199,158)
CORAL = (240,128,128)
VERDE_CLARO = (0, 255, 0)
TAMANHO_QUADRADO = 80
TAMANHO_DAMA = 34
TAMANHO_RAINHA = 17


tela = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()


def iI(msg):
    print(str(msg))

# Classe principal

class Jogo:
    # Classe para tomar conta do estado do jogo
    def __init__(self):
        self.estado = 'jogando'
        self.turno = 1
        self.jogadores = ('x', 'o')
        self.cedula_selecionada = None
        self.pulando = False
        self.tabuleiro = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
                          ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
                          ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

    def getTabuleiro(self):
        return self.tabuleiro

    def nao_ha_movimento_obrigatorio(self,movs,i):
        return movs[i]==[]

    def jogadas(self, pos):
        if self.estado == "jogando":
            linha= linha_clicada(pos)
            coluna = coluna_clicada(pos)
            if self.cedula_selecionada:
                movimento = self.is_movimento_valido(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna)
                if movimento[0]:
                    self.jogar(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna, movimento[1])
                elif linha == self.cedula_selecionada[0] and coluna == self.cedula_selecionada[1]:
                    movs = self.movimento_obrigatorio(self.cedula_selecionada)
                    if self.nao_ha_movimento_obrigatorio(movs,0) and self.pulando:
                            self.pulando = False
                            self.proximo_turno()
                    self.cedula_selecionada = None
            else:
                if self.eh_a_vez(None,linha,coluna):
                    self.cedula_selecionada = [linha, coluna]


    def ha_movimentos_obrigatorios(self,ob):
        return ob != {}

    def nao_esta_em(self,a,b):
        return a not in b

    def esta_em(self,a,b):
        return a in b

    def is_movimento_valido(self,jogador, localizacao_cedula, linha_destino, coluna_destino):
        linha_originaria = localizacao_cedula[0]
        coluna_originaria = localizacao_cedula[1]
        obrigatorios = self.todos_obrigatorios()
        if self.ha_movimentos_obrigatorios(obrigatorios):
            if self.nao_esta_em((linha_originaria, coluna_originaria),obrigatorios):
                return False, None
            elif self.nao_esta_em([linha_destino, coluna_destino],obrigatorios[(linha_originaria, coluna_originaria)]):
                return False, None
        movimento, pulo = self.movimentos_possiveis(localizacao_cedula)
        if self.esta_em([linha_destino, coluna_destino],movimento):
            if pulo:
                if len(pulo) == 1:
                    return True, pulo[0]
                else:
                    return self.calcula_pulo(pulo,linha_destino,coluna_destino)
            if self.pulando:
                return False, None
            return True, None
        return False, None

    def calcula_pulo(self,pulo,l_dest,c_dest):
        for i in range(len(pulo)):
            if abs(pulo[i][0]- l_dest)==1 and abs(pulo[i][1]-c_dest==1):
                return True, pulo[i]
        return False,None #########################

    def proximo_turno(self):
        self.turno += 1

    def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
        linha_atual = localizacao_cedula[0]
        coluna_atual = localizacao_cedula[1]
        char = self.tabuleiro[linha_atual][coluna_atual]

        self.tabuleiro[linha_destino][coluna_destino] = char
        self.tabuleiro[linha_atual][coluna_atual] = '-'

        if pulo:
            self.tabuleiro[pulo[0]][pulo[1]] = '-'
            self.cedula_selecionada = [linha_destino, coluna_destino]
            self.pulando = True

            if not self.movimento_obrigatorio((linha_destino, coluna_destino))[0]:
                if(linha_destino == 0):
                    self.tabuleiro[linha_destino][coluna_destino] = char.upper()
                self.pulando = False
                self.cedula_selecionada = None
                self.proximo_turno()
        else:
            if(linha_destino == 0):
                self.tabuleiro[linha_destino][coluna_destino] = char.upper()
            self.pulando = False
            self.cedula_selecionada = None
            self.proximo_turno()

        vencedor = self.verifica_vencedor()

        if vencedor != None:
            self.estado = ('game over')

    def proximo_turno(self):
        self.turno += 1

        # RETORNA TODOS OS MOVIMENTOS OBRIGATORIOS DE UM TURNO
    def todos_obrigatorios(self):
        all = {}
        for r in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[r])):
                ob, pulos = self.movimento_obrigatorio((r, c))
                if ob != []:
                    all[(r, c)] = ob
        return all

    def todos_obrigatorios_IA(self):
        all = {}

        for r in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[r])):
                ob, pulos = self.movimento_obrigatorio((r, c))
                if ob != []:
                    all[(r, c)] = ob
                    print (all)
                    break

        return all

    def eh_a_vez(self,indice,linha,coluna):
        if linha==None or coluna==None:
            return self.turno%2 ==indice
        return self.tabuleiro[linha][coluna].lower() == self.jogadores[self.turno % 2]

    def nao_eh_dama(self,linha,coluna,jogador):
        return self.tabuleiro[linha][coluna].islower() and self.tabuleiro[linha][coluna]==jogador

    def eh_dama(self,linha,coluna,jogador):
        return self.tabuleiro[linha][coluna].isupper() and self.tabuleiro[linha][coluna] == jogador.upper()

    def eh_casa_vazia(self,l,c):
        return self.tabuleiro[l][c]=='-'



    def verifica_e_add_obrigatorios(self,cond,obrigs,pulada,lx,i,lc,j):
        if cond:
            k=obrigs
            m=pulada
            k.append([lx + i, lc + j])
            m.append((lx,lc))
            return (k,m)
        return (obrigs, pulada)

    def obrigs_e_pulada(self,obrigatorios,posicao_cedula_pulada,l_x,i,l_c,j):
        #i=-1
        #j=+1
        obrigatorios.append([l_x +i, l_c + j])
        posicao_cedula_pulada.append((l_x, l_c))
        return obrigatorios,posicao_cedula_pulada

    def obrigs_e_pulada_aux(self,obrigatorios,posicao_cedula_pulada,u,i,v,j,cond):
        if cond and self.eh_casa_vazia((u) + i, (v) + j):
            return self.obrigs_e_pulada(obrigatorios,posicao_cedula_pulada,(u),i,(v),j)
        return obrigatorios,posicao_cedula_pulada

    def tabuleiro_not_in_array(self,obrigatorios,posicao_cedula_pulada,u,i,v,j,cond,array):
        if self.tabuleiro[u][v].lower() not in array:
            return self.obrigs_e_pulada_aux(obrigatorios,posicao_cedula_pulada,u,i,v,j,cond)
        return obrigatorios,posicao_cedula_pulada

    def obrigs_e_pulada_segunda_condic(self, cond, l_x, i, l_c, j, obrig, pulada):
        pulada.append((l_x, l_c))
        while True:
            if cond:
                break
            else:
                if self.eh_casa_vazia(l_x + i, l_c + j):
                    obrig.append([l_x + i, l_c + j])
                else:
                    break
            l_x = l_x + i
            l_c = l_c + j
        return l_x, l_c, obrig, pulada

        # RETORNA OS MOVIMENTOS OBRIGATORIOS DE UMA PECA QUE PODE SER JOGADA EM DETERMINADO TURNO
    def movimento_obrigatorio(self, localizacao_cedula):
        obrigatorios = []
        posicao_cedula_pulada = []
        l = localizacao_cedula[0]#posicao da pedra
        c = localizacao_cedula[1]
        jogador = self.jogadores[self.turno % 2]#quem é a vez
        himself = [jogador.lower(), jogador.upper()]
        index = self.jogadores.index(jogador)#cont de quem é o jogador
        array = [jogador.lower(), jogador.upper(), '-']#indica quem e a vez
        #iI(posicao_cedula_pulada)
        if  self.nao_eh_dama(l,c,jogador) and self.eh_a_vez(index,None,None):
            if l > 0:
                if c < 7:
                    obrigatorios,posicao_cedula_pulada=self.tabuleiro_not_in_array(obrigatorios,posicao_cedula_pulada,(l - 1),-1,(c + 1),+1,(l - 1) - 1 >= 0 and (c + 1) + 1 <= 7,array)
                if c > 0:
                    obrigatorios, posicao_cedula_pulada = self.tabuleiro_not_in_array(obrigatorios, posicao_cedula_pulada, (l - 1),
                                                                         -1, (c - 1), -1,
                                                                         (l - 1) - 1 >= 0 and (c - 1) - 1 >= 0,array)
            if l < 7:
                if c < 7:
                    obrigatorios, posicao_cedula_pulada = self.tabuleiro_not_in_array(obrigatorios, posicao_cedula_pulada, (l + 1),
                                                                         +1, (c + 1), +1,
                                                                         (l + 1) + 1 <= 7 and (c + 1) + 1 <= 7,array)
                if c > 0:
                    obrigatorios, posicao_cedula_pulada = self.tabuleiro_not_in_array(obrigatorios, posicao_cedula_pulada, (l + 1),+1, (c - 1), -1,(l + 1) + 1 <= 7 and (c - 1) - 1 >= 0,array)
        elif self.eh_dama(l,c,jogador) and self.eh_a_vez(index,None,None) :
            if not self.pulando and (jogador.lower() == 'x') or (jogador.lower() == 'o'):
                movimento_x = l
                movimento_y = c
                while True:
                    if movimento_x - 1 < 0 or movimento_y - 1 < 0:
                       break
                    else:
                        if self.tabuleiro[movimento_x - 1][movimento_y - 1] in himself:
                            break
                        if self.tabuleiro[movimento_x - 1][movimento_y - 1] not in array:
                            l_x = movimento_x - 1
                            l_c = movimento_y - 1
                            if l_x - 1 >= 0 and l_c - 1 >= 0:
                                if self.eh_casa_vazia(l_x - 1,l_c - 1):#TTTTTTTT
                                    #l_x, l_c, obrigatorios, posicao_cedula_pulada = self.obrigs_e_pulada_segunda_condic(l_x - 1 < 0 or l_c - 1 < 0, l_x,-1, l_c,-1, obrigatorios, posicao_cedula_pulada)
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.eh_casa_vazia(l_x - 1,l_c - 1):
                                                obrigatorios.append([l_x - 1, l_c - 1])
                                            else:
                                                break
                                        l_x -= 1
                                        l_c -= 1
                            break
                    movimento_x -= 1
                    movimento_y -= 1
                movimento_x = l
                movimento_y = c
                while True:
                    if movimento_x - 1 < 0 or movimento_y + 1 > 7:
                        break
                    else:
                        if self.tabuleiro[movimento_x - 1][movimento_y + 1] in himself:
                            break
                        if self.tabuleiro[movimento_x - 1][movimento_y + 1] not in array:
                            l_x = movimento_x - 1
                            l_c = movimento_y + 1
                            if l_x - 1 >= 0 and l_c + 1 <= 7:
                                if self.eh_casa_vazia(l_x - 1,l_c + 1):####TTTTTTTT
                                #    l_x, l_c, obrigatorios, posicao_cedula_pulada = self.obrigs_e_pulada_segunda_condic(l_x - 1 < 0 or l_c + 1 > 7, l_x,-1, l_c,+1, obrigatorios, posicao_cedula_pulada)
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.eh_casa_vazia(l_x - 1,l_c + 1):
                                                obrigatorios.append([l_x - 1, l_c + 1])
                                            else:
                                                break
                                        l_x -= 1
                                        l_c += 1
                            break
                    movimento_x -= 1
                    movimento_y += 1
                movimento_x = l
                movimento_y = c
                while True:
                    if movimento_x + 1 > 7 or movimento_y + 1 > 7:
                        break
                    else:
                        if self.tabuleiro[movimento_x + 1][movimento_y + 1] in himself:
                            break
                        if self.tabuleiro[movimento_x + 1][movimento_y + 1] not in array:
                            l_x = movimento_x + 1
                            l_c = movimento_y + 1
                            if l_x + 1 <= 7 and l_c + 1 <= 7:
                                if self.eh_casa_vazia(l_x + 1,l_c + 1):##########TTTTTTTTTTTTTTTTTT
                                    #l_x, l_c, obrigatorios, posicao_cedula_pulada = self.obrigs_e_pulada_segunda_condic(
                                    #    l_x + 1 > 7 or l_c + 1 > 7, l_x, +1, l_c, +1, obrigatorios,
                                    #    posicao_cedula_pulada)
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.eh_casa_vazia(l_x + 1,l_c + 1):
                                                obrigatorios.append([l_x + 1, l_c + 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c += 1
                            break
                    movimento_x += 1
                    movimento_y += 1

                movimento_x = l
                movimento_y = c
                while True:
                    if movimento_x + 1 > 7 or movimento_y - 1 < 0:
                        break
                    else:
                        if self.tabuleiro[movimento_x + 1][movimento_y - 1] in himself:
                            break
                        if self.tabuleiro[movimento_x + 1][movimento_y - 1] not in array:
                            l_x = movimento_x + 1
                            l_c = movimento_y - 1

                            if l_x + 1 <= 7 and l_c - 1 >= 0:
                                if self.eh_casa_vazia(l_x + 1,l_c - 1):########ttttttttttttttttt
                                    #l_x, l_c, obrigatorios, posicao_cedula_pulada = self.obrigs_e_pulada_segunda_condic(
                                    #    l_x + 1 > 7 or l_c - 1 < 0, l_x, +1, l_c, -1, obrigatorios,
                                    #    posicao_cedula_pulada)
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.eh_casa_vazia(l_x + 1,l_c - 1):
                                                obrigatorios.append([l_x + 1, l_c - 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c -= 1
                            break
                    movimento_x += 1
                    movimento_y -= 1
        return obrigatorios, posicao_cedula_pulada

    def existe_possivel(self):
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                if self.movimentos_possiveis((l, c))[0]:
                    return True
        return False

    # MOSTRA OS MOVIMENTOS POSSIVEIS DE UMA PECA SELECIONADA
    def movimentos_possiveis(self, localizacao_cedula):
        movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula)

        if movimentos == []:
            linha_atual = localizacao_cedula[0]
            coluna_atual = localizacao_cedula[1]

            if self.tabuleiro[linha_atual][coluna_atual].islower():
                if self.tabuleiro[linha_atual][coluna_atual] == 'o':
                    if linha_atual > 0:
                        if coluna_atual < 7:
                            if self.tabuleiro[linha_atual - 1][coluna_atual + 1] == '-':
                                movimentos.append([linha_atual - 1, coluna_atual + 1])
                        if coluna_atual > 0:
                            if self.tabuleiro[linha_atual - 1][coluna_atual - 1] == '-':
                                movimentos.append([linha_atual - 1, coluna_atual - 1])
                elif self.tabuleiro[linha_atual][coluna_atual] == 'x':
                    if linha_atual < 7:
                        if coluna_atual < 7:
                            if self.tabuleiro[linha_atual + 1][coluna_atual + 1] == '-':
                                movimentos.append([linha_atual + 1, coluna_atual + 1])
                        if coluna_atual > 0:
                            if self.tabuleiro[linha_atual + 1][coluna_atual - 1] == '-':
                                movimentos.append([linha_atual + 1, coluna_atual - 1])
            elif self.tabuleiro[linha_atual][coluna_atual].isupper():
                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha - 1 < 0 or conta_coluna - 1 < 0:
                        break
                    else:
                        if self.tabuleiro[conta_linha - 1][conta_coluna - 1] == '-':
                            movimentos.append([conta_linha - 1, conta_coluna - 1])
                        else:
                            break
                    conta_linha -= 1
                    conta_coluna -= 1

                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha - 1 < 0 or conta_coluna + 1 > 7:
                        break
                    else:
                        if self.tabuleiro[conta_linha - 1][conta_coluna + 1] == '-':
                            movimentos.append([conta_linha - 1, conta_coluna + 1])
                        else:
                            break
                    conta_linha -= 1
                    conta_coluna += 1

                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha + 1 > 7 or conta_coluna + 1 > 7:
                        break
                    else:
                        if self.tabuleiro[conta_linha + 1][conta_coluna + 1] == '-':
                            movimentos.append([conta_linha + 1, conta_coluna + 1])
                        else:
                            break
                    conta_linha += 1
                    conta_coluna += 1

                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha + 1 > 7 or conta_coluna - 1 < 0:
                        break
                    else:
                        if self.tabuleiro[conta_linha + 1][conta_coluna - 1] == '-':
                            movimentos.append([conta_linha + 1, conta_coluna - 1])
                        else:
                            break
                    conta_linha += 1
                    conta_coluna -= 1

        return movimentos, pulos

        # VERIFICA O VENCEDOR
    def verifica_vencedor(self):

            resp1, resp2 = getRandomPosIA(self.tabuleiro)
            if resp1 == None:
                return 'o'

            x = sum([contador.count('x') + contador.count('X') for contador in self.tabuleiro])
            o = sum([contador.count('o') + contador.count('O') for contador in self.tabuleiro])

            if x == 0:
                return 'o'

            if o == 0:
                return 'x'

            if x == 1 and o == 1:
                return 'empate'

            if self.cedula_selecionada:
                if not self.movimentos_possiveis(self.cedula_selecionada)[0]:
                    if x == 1 and self.turno % 2 == 0:
                        return 'o'
                    if o == 1 and self.turno % 2 == 1:
                        return 'x'

            if not self.existe_possivel():
                return 'empate'

            return None


    def desenha(self):
        matriz = []

        for i in range(8):
            if i % 2 == 0:
                matriz.append(['#', '-', '#', '-', '#', '-', '#', '-'])
            else:
                matriz.append(['-', '#', '-', '#', '-', '#', '-', '#'])

        y = 0
        for l in range(len(matriz)):
            x = 0
            for c in range(len(matriz[l])):
                if matriz[l][c] == '#':
                    pygame.draw.rect(tela, VERDE_ESCURO, (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
                else:
                    pygame.draw.rect(tela, BEGE, (x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
                x += TAMANHO_QUADRADO
            y += TAMANHO_QUADRADO

        if self.cedula_selecionada:
            obrigatorios = self.todos_obrigatorios()
            movs = self.movimentos_possiveis(self.cedula_selecionada)

            if obrigatorios != {}:
                if (self.cedula_selecionada[0], self.cedula_selecionada[1]) not in obrigatorios:
                    x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
                    y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]
                    pygame.draw.rect(tela, VERMELHO_CLARO, (x_vermelho, y_vermelho, 80, 80))
                else:
                    if movs[0] == []:
                        x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
                        y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

                        pygame.draw.rect(tela, VERMELHO_CLARO, (x_vermelho, y_vermelho, 80, 80))
                    else:
                        for i in range(len(movs[0])):
                            x_possivel = ALTURA / 8 * movs[0][i][1]
                            y_possivel = ALTURA / 8 * movs[0][i][0]

                            pygame.draw.rect(tela, YELLOW, (x_possivel, y_possivel, 80, 80))
            else:
                if self.pulando:
                    x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
                    y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

                    pygame.draw.rect(tela, VERMELHO_CLARO, (x_vermelho, y_vermelho, 80, 80))
                else:
                    if movs[0] == []:
                        x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
                        y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

                        pygame.draw.rect(tela, VERMELHO_CLARO, (x_vermelho, y_vermelho, 80, 80))
                    else:
                        for i in range(len(movs[0])):
                            x_possivel = ALTURA / 8 * movs[0][i][1]
                            y_possivel = ALTURA / 8 * movs[0][i][0]

                            pygame.draw.rect(tela, YELLOW, (x_possivel, y_possivel, 80, 80))

        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                elemento = self.tabuleiro[l][c]
                if elemento != '-':
                    x = int(ALTURA / 8) * c + int(ALTURA / 16)
                    y = int(ALTURA / 8) * l + int(ALTURA / 16)

                    img = pygame.image.load('coroa.png')
                    img = pygame.transform.scale(img, (60,60))

                    if elemento.lower() == 'x':
                        pygame.draw.circle(tela, PRETO, (x, y), TAMANHO_DAMA, 0)
                        if elemento == 'X':
                            tela.blit(img, (x - 36, y - 36))
                    else:
                        pygame.draw.circle(tela, BRANCO, (x, y), TAMANHO_DAMA, 0)
                        if elemento == 'O':
                            tela.blit(img, (x - 36, y - 36))

def fim_de_jogo(winner):
    fim = False
    while not fim:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim = True
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                fim = True

        tela.fill(AZUL)
        fonte = pygame.font.SysFont('comicsansms', 50)

        surface_texto, rect_texto = None, None

        if winner == "empate":
            surface_texto, rect_texto = texto_na_tela("EMPATE!", fonte, BRANCO)
        elif winner == "x":
            surface_texto, rect_texto = texto_na_tela("PRETO WINS", fonte, PRETO)
        elif winner == "o":
            surface_texto, rect_texto = texto_na_tela("BRANCO WINS", fonte, BRANCO)
        rect_texto.center = ((LARGURA / 2), ALTURA / 3)
        tela.blit(surface_texto, rect_texto)

        fonte = pygame.font.Font(None, 30)
        voltar = fonte.render('Pressione qualquer tecla para jogar novamente.', False, CORAL)

        tela.blit(voltar, (25, 550))

        pygame.display.update()
        clock.tick(60)


def coluna_clicada(pos):
    x = pos[0]
    for i in range(1, 8):
        if x < i * ALTURA / 8:
            return i - 1
    return 7

def texto_na_tela(text, font, color):
	txt = font.render(text, True, color)
	return txt, txt.get_rect()

def linha_clicada(pos):
    y = pos[1]
    for i in range(1, 8):
        if y < i * ALTURA / 8:
            return i - 1
    return 7

def getRandomPosIA(tabuleiro):
    linha_v = []
    coluna_v = []
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            if tabuleiro[i][j].lower() == 'x':
                if i<7:
                    if j<7:
                        if tabuleiro[i+1][j+1] == '-':
                            linha, coluna = i, j
                            linha_v.append(linha)
                            coluna_v.append(coluna)
                    if tabuleiro[i+1][j-1] == '-':
                        linha, coluna = i, j
                        linha_v.append(linha)
                        coluna_v.append(coluna)
                else:
                    if tabuleiro[i][j] == 'X':
                        if j < 7:
                            if tabuleiro[i-1][j+1] == '-':
                                linha, coluna = i, j
                                linha_v.append(linha)
                                coluna_v.append(coluna)
                        elif j==7:
                            if tabuleiro[i-1][j-1] == '-':
                                linha, coluna = i, j
                                linha_v.append(linha)
                                coluna_v.append(coluna)

    if len(linha_v) > 0:
        i = random.randrange(0,len(linha_v),1)
        return linha_v[i], coluna_v[i]
    else:
        return None, None

def IAsimples(jogo, vez):
    pulo = []
    if(jogo.cedula_selecionada != None):
        obrigatorios = jogo.movimento_obrigatorio(jogo.cedula_selecionada)
        if obrigatorios != ([],[]):
            linha_origem = jogo.cedula_selecionada[0]
            coluna_origem = jogo.cedula_selecionada[1]
            linha_dest = obrigatorios[0][0][0]
            coluna_dest = obrigatorios[0][0][1]
        else:
            jogo.cedula_selecionada = None
            return jogo
    else:
        obrigatorios = jogo.todos_obrigatorios_IA()
           
    if obrigatorios != {}: 
        for i in range(len(jogo.tabuleiro)):
            for j in range(len(jogo.tabuleiro[1])):
                if(i,j) in obrigatorios:
                    linha_origem = i
                    coluna_origem = j
                    resp = obrigatorios[(i,j)]
                    linha_dest = resp[0][0]
                    coluna_dest = resp[0][1]
                    break

        y_origem = ALTURA / 8 * linha_origem
        x_origem = ALTURA / 8 * coluna_origem

        y_d = ALTURA / 8 * linha_dest
        x_d = ALTURA / 8 * coluna_dest

        y_dest = int(ALTURA / 8) * linha_dest + int(ALTURA / 16)
        x_dest = int(ALTURA / 8) * coluna_dest + int(ALTURA / 16)

        y = int(ALTURA / 8) * linha_origem + int(ALTURA / 16)
        x = int(ALTURA / 8) * coluna_origem + int(ALTURA / 16)


        img = pygame.image.load('coroa.png')
        img = pygame.transform.scale(img, (60,60))

        pygame.draw.rect(tela, YELLOW, (x_origem, y_origem, 80, 80))
        pygame.draw.circle(tela, PRETO, (int(x), int(y)), TAMANHO_DAMA, 0)
        if jogo.tabuleiro[linha_origem][coluna_origem] == 'X':
            tela.blit(img, (x_origem, y_origem))
        pygame.display.update()
        time.sleep(0.5)
        pygame.draw.circle(tela, FOSCO, (int(x_dest), int(y_dest)), TAMANHO_DAMA, 0)
        pygame.display.update()
        time.sleep(0.5)
        pygame.draw.rect(tela, VERDE_ESCURO, (x_d, y_d, 80, 80))
        pygame.draw.rect(tela, VERDE_ESCURO, (x_origem, y_origem, 80, 80))
        pygame.draw.circle(tela, PRETO, (int(x), int(y)), TAMANHO_DAMA, 0)
        pygame.display.update()
        time.sleep(0.5)

        print('lo: ', linha_origem, ' co: ', coluna_origem, 'ld: ', linha_dest, 'cd: ', coluna_dest)
        print(jogo.tabuleiro[linha_origem][coluna_origem])
        if jogo.tabuleiro[linha_origem][coluna_origem] == 'x':
            print('eh sim')
            if linha_dest > linha_origem:
                pulo.append(linha_origem + 1)
            else:
                pulo.append(linha_origem - 1)
            if coluna_dest > coluna_origem:
                pulo.append(coluna_origem + 1)
            else:
                pulo.append(coluna_origem - 1)
        else:
            print('eh nao')
            if linha_dest > linha_origem:
                pulo.append(linha_dest - 1)
            else:
                pulo.append(linha_dest + 1)
            if coluna_dest > coluna_origem:
                pulo.append(coluna_dest - 1)
            else:
                pulo.append(coluna_dest + 1)

        char = jogo.tabuleiro[linha_origem][coluna_origem]
        jogo.tabuleiro[linha_dest][coluna_dest] = char
        jogo.tabuleiro[linha_origem][coluna_origem] = '-'

        if (linha_dest == 7):
            if jogo.movimentos_possiveis((linha_dest, coluna_dest))[0] == None:
                jogo.tabuleiro[linha_dest][coluna_dest] = char.upper()

        print('pulo: ', pulo)
        jogo.tabuleiro[pulo[0]][pulo[1]] = '-'
        pygame.display.update()
        jogo.cedula_selecionada = [linha_dest, coluna_dest]
        jogo = IAsimples(jogo,2)


    elif obrigatorios == {} and jogo.cedula_selecionada == None and vez ==1:
        linha_origem, coluna_origem = getRandomPosIA(jogo.tabuleiro)
        if linha_origem != None and coluna_origem != None:
            envia = [linha_origem, coluna_origem]
            opcionais = jogo.movimentos_possiveis(envia)
            if len(opcionais) == 0:
                jogo.estado = ('game over')
                return jogo
            print('opcionais', opcionais)
            linha_dest = opcionais[0][0][0]
            coluna_dest = opcionais[0][0][1]

            y_origem = ALTURA / 8 * linha_origem
            x_origem = ALTURA / 8 * coluna_origem

            y_d = ALTURA / 8 * linha_dest
            x_d = ALTURA / 8 * coluna_dest

            y_dest = int(ALTURA / 8) * linha_dest + int(ALTURA / 16)
            x_dest = int(ALTURA / 8) * coluna_dest + int(ALTURA / 16)

            y = int(ALTURA / 8) * linha_origem + int(ALTURA / 16)
            x = int(ALTURA / 8) * coluna_origem + int(ALTURA / 16)

            pygame.draw.rect(tela, YELLOW, (x_origem, y_origem, 80, 80))
            pygame.draw.circle(tela, PRETO, (int(x), int(y)), TAMANHO_DAMA, 0)
            pygame.display.update()
            time.sleep(1)
            pygame.draw.rect(tela, VERDE_ESCURO, (x_d, y_d, 80, 80))
            pygame.draw.rect(tela, VERDE_ESCURO, (x_origem, y_origem, 80, 80))
            pygame.draw.circle(tela, PRETO, (int(x), int(y)), TAMANHO_DAMA, 0)
            pygame.display.update()
            time.sleep(1)

            char = jogo.tabuleiro[linha_origem][coluna_origem]
            jogo.tabuleiro[linha_dest][coluna_dest] = char
            jogo.tabuleiro[linha_origem][coluna_origem] = '-'

            if (linha_dest == 7):
                if jogo.movimentos_possiveis((linha_dest, coluna_dest))[0] == None:
                    jogo.tabuleiro[linha_dest][coluna_dest] = char.upper()

            jogo.cedula_selecionada = None

        else:
            jogo.estado = ('game over')
            return jogo
    else:
        jogo.cedula_selecionada = None
    vencedor = jogo.verifica_vencedor()

    if vencedor != None:
        jogo.estado = ('game over')

    if(jogo.cedula_selecionada == None and linha_dest==7):
        jogo.tabuleiro[linha_dest][coluna_dest] = jogo.tabuleiro[linha_dest][coluna_dest].upper()

    return jogo

def printTabuleiro(tabuleiro):
    for t in tabuleiro:
        print (t)

def loop_jogo():
    sair = False

    jogo = Jogo()

    while not sair:
        if jogo.jogadores[jogo.turno % 2] == 'o':
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sair = True
                    pygame.quit()
                    quit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    jogo.jogadas(pygame.mouse.get_pos())
        else:
            #jogo.cedula_selecionada = None
            time.sleep(0.5)
            jogo = IAsimples(jogo, 1)
            jogo.proximo_turno()

        tela.fill(PRETO)
        jogo.desenha()

        vencedor = jogo.verifica_vencedor()

        if vencedor is not None:
            fim_de_jogo(vencedor)
            sair = True


        pygame.display.update()
        clock.tick(60)



loop_jogo()
pygame.quit()
quit()
