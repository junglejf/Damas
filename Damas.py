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

            else:
                if self.tabuleiro[linha][coluna].lower() == self.jogadores[self.turno % 2]:
                    self.cedula_selecionada = [linha, coluna]

    def is_movimento_valido(self,jogador, localizacao_cedula, linha_destino, coluna_destino):

        matriz = self.getTabuleiro()
        linha_originaria = localizacao_cedula[0]
        coluna_originaria = localizacao_cedula[1]
        if(matriz[linha_destino][coluna_destino] == '-'):
            return True, None

        return False, None

    def movimento_obrigatorio(self, tabuleiro):
        must_action = []
        jumped_square = []

        l = tabuleiro[0]
        c = tabuleiro[1]

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
                                must_action.append([l_x - 1, l_c + 1])
                                jumped_square.append((l_x, l_c))
                if c > 0:
                    if self.tabuleiro[l - 1][c - 1].lower() not in array:
                        l_x = l - 1
                        l_c = c - 1

                        if l_x - 1 >= 0 and l_c - 1 >= 0:
                            if self.tabuleiro[l_x - 1][l_c - 1] == '-':
                                must_action.append([l_x - 1, l_c - 1])
                                jumped_square.append((l_x, l_c))
            if l < 7:
                if c < 7:
                    if self.tabuleiro[l + 1][c + 1].lower() not in array:
                        l_x = l + 1
                        l_c = c + 1

                        if l_x + 1 <= 7 and l_c + 1 <= 7:
                            if self.tabuleiro[l_x + 1][l_c + 1] == '-':
                                must_action.append([l_x + 1, l_c + 1])
                                jumped_square.append((l_x, l_c))
                if c > 0:
                    if self.tabuleiro[l + 1][c - 1].lower() not in array:
                        l_x = l + 1
                        l_c = c - 1

                        if l_x + 1 <= 7 and l_c - 1 >= 0:
                            if self.tabuleiro[l_x + 1][l_c - 1] == '-':
                                must_action.append([l_x + 1, l_c - 1])
                                jumped_square.append((l_x, l_c))

		# movimento Rainha
        elif self.tabuleiro[l][c].isupper() and self.tabuleiro[l][c] == jogador.upper() and \
                                self.turno % 2 == index:

            if not self.pulando and (jogador.lower() == 'x' and l != 7) or (jogador.lower() == 'o' and l != 0):
                movimento_x = l
                movimento_y = c
                while True:
                    if movimento_x - 1 < 0 or movimento_y - 1 < 0:
                        break
                    else:
                        if self.tabuleiro[movimento_x - 1][movimento_y - 1] not in array:
                            l_x = movimento_x - 1
                            l_c = movimento_y - 1

                            if l_x - 1 >= 0 and l_c - 1 >= 0:
                                if self.tabuleiro[l_x - 1][l_c - 1] == '-':
                                    jumped_square.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.tabuleiro[l_x - 1][l_c - 1] == '-':
                                                must_action.append([l_x - 1, l_c - 1])
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
                        if self.tabuleiro[movimento_x - 1][movimento_y + 1] not in array:
                            l_x = movimento_x - 1
                            l_c = movimento_y + 1

                            if l_x - 1 >= 0 and l_c + 1 <= 7:
                                if self.tabuleiro[l_x - 1][l_c + 1] == '-':
                                    jumped_square.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.tabuleiro[l_x - 1][l_c + 1] == '-':
                                                must_action.append([l_x - 1, l_c + 1])
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
                        if self.tabuleiro[movimento_x + 1][movimento_y + 1] not in array:
                            l_x = movimento_x + 1
                            l_c = movimento_y + 1

                            if l_x + 1 <= 7 and l_c + 1 <= 7:
                                if self.tabuleiro[l_x + 1][l_c + 1] == '-':
                                    jumped_square.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.tabuleiro[l_x + 1][l_c + 1] == '-':
                                                must_action.append([l_x + 1, l_c + 1])
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
                        if self.tabuleiro[movimento_x + 1][movimento_y - 1] not in array:
                            l_x = movimento_x + 1
                            l_c = movimento_y - 1

                            if l_x + 1 <= 7 and l_c - 1 >= 0:
                                if self.tabuleiro[l_x + 1][l_c - 1] == '-':
                                    jumped_square.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.tabuleiro[l_x + 1][l_c - 1] == '-':
                                                must_action.append([l_x + 1, l_c - 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c -= 1
                            break
                    movimento_x += 1
                    movimento_y -= 1

        return must_action, jumped_square

    def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
        pass

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

        pygame.display.update()
        clock.tick(60)



loop_jogo()
pygame.quit()
quit()
