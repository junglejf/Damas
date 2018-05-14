import pygame

pygame.init()

LARGURA = 640
ALTURA = 640

BEGE = (238,238,210)
PRETO = (0, 0, 0)
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

    def jogadas(self, pos):
        if self.estado == "jogando":
            linha, coluna = linha_clicada(pos), coluna_clicada(pos)
            if self.cedula_selecionada:
                movimento = self.is_movimento_valido(self.jogadores[self.turno % 2], self.cedula_selecionada, linha,
                                                     coluna)
                if movimento[0]:
                    self.jogar(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna, movimento[1])
                elif linha == self.cedula_selecionada[0] and coluna == self.cedula_selecionada[1]:
                    movs = self.movimento_obrigatorio(self.cedula_selecionada)
                    if movs[0] == []:
                        if self.pulando:
                            self.pulando = False
                            self.proximo_turno()
                    self.cedula_selecionada = None

            else:
                if self.tabuleiro[linha][coluna].lower() == self.jogadores[self.turno % 2]:
                    self.cedula_selecionada = [linha, coluna]

    def is_movimento_valido(self,jogador, localizacao_cedula, linha_destino, coluna_destino):

        linha_originaria = localizacao_cedula[0]
        coluna_originaria = localizacao_cedula[1]

        obrigatorios = self.todos_obrigatorios()

        if obrigatorios != {}:
            if (linha_originaria, coluna_originaria) not in obrigatorios:
                return False, None
            elif [linha_destino, coluna_destino] not in obrigatorios[(linha_originaria, coluna_originaria)]:
                return False, None

        movimento, pulo = self.movimentos_possiveis(localizacao_cedula)

        if [linha_destino, coluna_destino] in movimento:
            if pulo:
                if len(pulo) == 1:
                    return True, pulo[0]
                else:
                    for i in range(len(pulo)):
                        if abs(pulo[i][0] - linha_destino) == 1 and abs(pulo[i][1] - coluna_destino) == 1:
                            return True, pulo[i]

            if self.pulando:
                return False, None

            return True, None

        return False, None

    def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
        linha_atual = localizacao_cedula[0]
        coluna_atual = localizacao_cedula[1]
        char = self.tabuleiro[linha_atual][coluna_atual]

        self.tabuleiro[linha_destino][coluna_destino] = char
        self.tabuleiro[linha_atual][coluna_atual] = '-'

        if pulo:
            self.pulando = True

        if (jogador == 'x' and linha_destino == 7) or (jogador == 'o' and linha_destino == 0):
            if not self.pulando:
                self.tabuleiro[linha_destino][coluna_destino] = char.upper()
            elif not self.movimentos_possiveis((linha_destino, coluna_destino))[0]:
                self.tabuleiro[linha_destino][coluna_destino] = char.upper()

        if pulo:
            self.tabuleiro[pulo[0]][pulo[1]] = '-'
            self.cedula_selecionada = [linha_destino, coluna_destino]
            self.pulando = True

        else:
            self.cedula_selecionada = None
            self.proximo_turno()
        vencedor = self.verifica_vencedor()

        if vencedor != None:
            self.estado = ('game over')

    def proximo_turno(self):
        self.turno += 1

    def existe_possivel(self):
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                if self.movimentos_possiveis((l, c))[0]:
                    return True
        return False

	#MOSTRA OS MOVIMENTOS POSSIVEIS DE UMA PECA SELECIONADA
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

    # RETORNA TODOS OS MOVIMENTOS OBRIGATORIOS DE UM TURNO
    def todos_obrigatorios(self):
        todos = {}

        for r in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[r])):
                ob, pulos = self.movimento_obrigatorio((r, c))
                if ob != []:
                    todos[(r, c)] = ob

        return todos

    # RETORNA OS MOVIMENTOS OBRIGATORIOS DE UMA PECA QUE PODE SER JOGADA EM DETERMINADO TURNO
    def movimento_obrigatorio(self, localizacao_cedula):
        obrigatorios = []
        posicao_cedula_pulada = []

        l = localizacao_cedula[0]
        c = localizacao_cedula[1]

        jogador = self.jogadores[self.turno % 2]
        index = self.jogadores.index(jogador)

        array = [jogador.lower(), jogador.upper(), '-']

        if self.tabuleiro[l][c].islower() and self.tabuleiro[l][c] == jogador and \
                                self.turno % 2 == index:
            if l > 0:
                if c < 7:
                    if self.tabuleiro[l - 1][c + 1].lower() not in array:
                        l_x = l - 1
                        l_c = c + 1

                        if l_x - 1 >= 0 and l_c + 1 <= 7:
                            if self.tabuleiro[l_x - 1][l_c + 1] == '-':
                                obrigatorios.append([l_x - 1, l_c + 1])
                                posicao_cedula_pulada.append((l_x, l_c))
                if c > 0:
                    if self.tabuleiro[l - 1][c - 1].lower() not in array:
                        l_x = l - 1
                        l_c = c - 1

                        if l_x - 1 >= 0 and l_c - 1 >= 0:
                            if self.tabuleiro[l_x - 1][l_c - 1] == '-':
                                obrigatorios.append([l_x - 1, l_c - 1])
                                posicao_cedula_pulada.append((l_x, l_c))
            if l < 7:
                if c < 7:
                    if self.tabuleiro[l + 1][c + 1].lower() not in array:
                        l_x = l + 1
                        l_c = c + 1

                        if l_x + 1 <= 7 and l_c + 1 <= 7:
                            if self.tabuleiro[l_x + 1][l_c + 1] == '-':
                                obrigatorios.append([l_x + 1, l_c + 1])
                                posicao_cedula_pulada.append((l_x, l_c))
                if c > 0:
                    if self.tabuleiro[l + 1][c - 1].lower() not in array:
                        l_x = l + 1
                        l_c = c - 1

                        if l_x + 1 <= 7 and l_c - 1 >= 0:
                            if self.tabuleiro[l_x + 1][l_c - 1] == '-':
                                obrigatorios.append([l_x + 1, l_c - 1])
                                posicao_cedula_pulada.append((l_x, l_c))

        elif self.tabuleiro[l][c].isupper() and self.tabuleiro[l][c] == jogador.upper() and \
                                self.turno % 2 == index:

            if not self.pulando and (jogador.lower() == 'x' and l != 7) or (jogador.lower() == 'o' and l != 0):
                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha - 1 < 0 or conta_coluna - 1 < 0:
                        break
                    else:
                        if self.tabuleiro[conta_linha - 1][conta_coluna - 1] not in array:
                            l_x = conta_linha - 1
                            l_c = conta_coluna - 1

                            if l_x - 1 >= 0 and l_c - 1 >= 0:
                                if self.tabuleiro[l_x - 1][l_c - 1] == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.tabuleiro[l_x - 1][l_c - 1] == '-':
                                                obrigatorios.append([l_x - 1, l_c - 1])
                                            else:
                                                break
                                        l_x -= 1
                                        l_c -= 1
                            break
                    conta_linha -= 1
                    conta_coluna -= 1

                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha - 1 < 0 or conta_coluna + 1 > 7:
                        break
                    else:
                        if self.tabuleiro[conta_linha - 1][conta_coluna + 1] not in array:
                            l_x = conta_linha - 1
                            l_c = conta_coluna + 1

                            if l_x - 1 >= 0 and l_c + 1 <= 7:
                                if self.tabuleiro[l_x - 1][l_c + 1] == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.tabuleiro[l_x - 1][l_c + 1] == '-':
                                                obrigatorios.append([l_x - 1, l_c + 1])
                                            else:
                                                break
                                        l_x -= 1
                                        l_c += 1
                            break
                    conta_linha -= 1
                    conta_coluna += 1

                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha + 1 > 7 or conta_coluna + 1 > 7:
                        break
                    else:
                        if self.tabuleiro[conta_linha + 1][conta_coluna + 1] not in array:
                            l_x = conta_linha + 1
                            l_c = conta_coluna + 1

                            if l_x + 1 <= 7 and l_c + 1 <= 7:
                                if self.tabuleiro[l_x + 1][l_c + 1] == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.tabuleiro[l_x + 1][l_c + 1] == '-':
                                                obrigatorios.append([l_x + 1, l_c + 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c += 1
                            break
                    conta_linha += 1
                    conta_coluna += 1

                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha + 1 > 7 or conta_coluna - 1 < 0:
                        break
                    else:
                        if self.tabuleiro[conta_linha + 1][conta_coluna - 1] not in array:
                            l_x = conta_linha + 1
                            l_c = conta_coluna - 1

                            if l_x + 1 <= 7 and l_c - 1 >= 0:
                                if self.tabuleiro[l_x + 1][l_c - 1] == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.tabuleiro[l_x + 1][l_c - 1] == '-':
                                                obrigatorios.append([l_x + 1, l_c - 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c -= 1
                            break
                    conta_linha += 1
                    conta_coluna -= 1

        return obrigatorios, posicao_cedula_pulada



	# VERIFICA O VENCEDOR
    def verifica_vencedor(self):

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

                    if elemento.lower() == 'x':
                        pygame.draw.circle(tela, PRETO, (x, y), TAMANHO_DAMA, 0)
                        if elemento == 'X':
                            pygame.draw.circle(tela, PRETO, (x, y), TAMANHO_RAINHA, 0)
                            pygame.draw.circle(tela, AZUL, (x, y), int(TAMANHO_RAINHA/2), 0)
                    else:
                        pygame.draw.circle(tela, BRANCO, (x, y), TAMANHO_DAMA, 0)
                        if elemento == 'O':
                            pygame.draw.circle(tela, PRETO, (x, y),TAMANHO_RAINHA, 0)
                            pygame.draw.circle(tela, AZUL, (x, y), int(TAMANHO_RAINHA/2), 0)




def coluna_clicada(pos):
    x = pos[0]
    for i in range(1, 8):
        if x < i * ALTURA / 8:
            return i - 1
    return 7


def linha_clicada(pos):
    y = pos[1]
    for i in range(1, 8):
        if y < i * ALTURA / 8:
            return i - 1
    return 7



def loop_jogo():
    sair = False

    jogo = Jogo()

    while not sair:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                jogo.jogadas(pygame.mouse.get_pos())

        tela.fill(PRETO)
        jogo.desenha()

        vencedor = jogo.verifica_vencedor()

        if vencedor is not None:
            sair = True

        pygame.display.update()
        clock.tick(60)



loop_jogo()
pygame.quit()
quit()
