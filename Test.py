<<<<<<< HEAD:Test.py
import unittest
from Damas.Damas import *

tabuleiro = [['-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-'],
             ['x', '-', '-', '-', 'x', '-', 'x', '-'],
             ['-', '-', '-', '-', '-', '-', '-', 'o'],
             ['-', '-', '-', '-', 'x', '-', '-', '-'],
             ['-', 'o', '-', '-', '-', '-', '-', 'o'],
             ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
             ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

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

print("BOOM")
class testJogar(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        print("aqui")

    def Inicializa(self):
        self.jogo.assertEqual(self.jogo.tabuleiro,tabuleiro, msg = 'inicializou corretamente')


=======
from unittest import TestCase
from Damas import *#_testes import *

class TestJogo(TestCase):
    def test1_verifica_vencedor(self):
        sair = False
        jogo = Jogo()
        #####################GARANTINDO QUE OCORRA A CONDIÇÃO 1 DO TESTE
        # fazendo com que resp1<-randomIA<-none
        assert (jogo.tabuleiro==[
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', 'x'],
                          ['-', '-', '-', '-', '-', '-', 'o', '-'],
                          ['-', '-', '-', '-', '-', 'o', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-']
        ])

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
                # jogo.cedula_selecionada = None
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

        ### como garantir que a função verifica_vencedor aqui retorne o que se quer ?
        ###
        #self.fail()
        return True


