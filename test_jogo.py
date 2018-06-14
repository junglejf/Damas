from unittest import TestCase
from Damas.Damas import Jogo

tab = [['-', '-', '-', '-', '-', '-', '-', '-'],
       ['-', '-', '-', '-', '-', '-', '-', '-'],
       ['-', '-', '-', '-', 'x', '-', 'x', '-'],
       ['-', 'x', '-', '-', '-', '-', '-', 'o'],
       ['-', '-', '-', '-', 'x', '-', '-', '-'],
       ['-', 'o', '-', '-', '-', '-', '-', 'o'],
       ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
       ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]
tabuleiro2 = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
              ['-', 'x', '-', '-', '-', '-', '-', 'x'],
              ['x', '-', 'x', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', '-', '-', '-', '-', '-', '-', '-'],
              ['-', 'o', '-', '-', '-', 'o', '-', 'o'],
              ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
              ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

tabDAMAS = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
            ['-', 'x', '-', '-', '-', '-', '-', 'x'],
            ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'x', '-', '-', '-'],
            ['-', 'o', '-', '-', '-', '-', '-', 'o'],
            ['o', '-', 'O', '-', 'o', '-', 'o', '-'],
            ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]
tabWINPC = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
            ['-', 'x', '-', '-', '-', '-', '-', 'x'],
            ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
            ['-', '-', '-', '-', '-', '-', '-', 'o'],
            ['-', '-', '-', '-', 'x', '-', '-', '-'],
            ['-', 'o', '-', 'o', '-', '-', '-', 'o'],
            ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
            ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]
tabWINPLAYER = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                ['-', 'x', '-', '-', '-', '-', '-', 'x'],
                ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                ['-', '-', '-', '-', '-', '-', '-', 'o'],
                ['-', '-', '-', '-', 'x', '-', '-', '-'],
                ['-', 'o', '-', 'o', '-', '-', '-', 'o'],
                ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
                ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]


class TestJogo(TestCase):
    """
    def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
        1# linha_atual = localizacao_cedula[0]
        1# coluna_atual = localizacao_cedula[1]
        1# char = self.tabuleiro[linha_atual][coluna_atual]

        1# self.tabuleiro[linha_destino][coluna_destino] = char
        1# self.tabuleiro[linha_atual][coluna_atual] = '-'

        if pulo: #2
            self.tabuleiro[pulo[0]][pulo[1]] = '-'  #3
            self.cedula_selecionada = [linha_destino, coluna_destino] #3
            self.pulando = True #3

            if not self.movimento_obrigatorio((linha_destino, coluna_destino))[0]: #4 
                if(linha_destino == 0): #5
                    self.tabuleiro[linha_destino][coluna_destino] = char.upper() #6
                self.pulando = False #7 
                self.cedula_selecionada = None #7
                self.proximo_turno() #7
                
        else: #8 
            if(linha_destino == 0): #9
                self.tabuleiro[linha_destino][coluna_destino] = char.upper() #10
            self.pulando = False #11
            self.cedula_selecionada = None #11
            self.proximo_turno() #11

        vencedor = self.verifica_vencedor() #12

        if vencedor != None: #13
            self.estado = ('game over') #14
        #15
    """""

    # def setUp(self):
    #   self.jogo = Jogo()
    def test_jogar(self):
        print(self.jogo.turno)
        if (self.jogo.turno >= 3):
            self.jogo.assertEquals(self.getTabuleiro(), tab)


class TestJogo(TestCase,Jogo):
    def test_jogar(self,Jogo):
        if(Jogo.turno == 3):
            Jogo.assertEquals(self.getTabuleiro(), tab)