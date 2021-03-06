# -*- coding: utf-8 -*-
from itertools import chain
from atores import ATIVO


VITORIA = 'VITORIA'
DERROTA = 'DERROTA'
EM_ANDAMENTO = 'EM_ANDAMENTO'


class Ponto():
    def __init__(self, x, y, caracter):
        self.caracter = caracter
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.caracter == other.caracter

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s,%s,'%s')" % (self.x, self.y, self.caracter)


class Fase():
    def __init__(self, intervalo_de_colisao=1):
        """
        Método que inicializa uma fase.

        :param intervalo_de_colisao:
        """
        self.intervalo_de_colisao = intervalo_de_colisao
        self._passaros = []
        self._porcos = []
        self._obstaculos = []


    def adicionar_obstaculo(self, *obstaculos):
        """
        Adiciona obstáculos em uma fase

        :param obstaculos:
        """
        self._obstaculos.extend(obstaculos)

    def adicionar_porco(self, *porcos):
        """
        Adiciona porcos em uma fase

        :param porcos:
        """
        self._porcos.extend(porcos)

    def adicionar_passaro(self, *passaros):
        """
        Adiciona pássaros em uma fase

        :param passaros:
        """
        self._passaros.extend(passaros)

    def status(self):
        """
        Método que indica com mensagem o status do jogo

        Se o jogo está em andamento (ainda tem porco ativo e pássaro ativo), retorna essa mensagem.

        Se o jogo acabou com derrota (ainda existe porco ativo), retorna essa mensagem

        Se o jogo acabou com vitória (não existe porco ativo), retorna essa mensagem

        :return:
        """
        porcos = False
        passaros = False
        for p in self._porcos:
            if p.status == ATIVO:
                porcos = True

        for p in self._passaros:
            if p.status == ATIVO:
                passaros = True

        if not porcos:
            return VITORIA

        elif not passaros:
            return DERROTA

        return EM_ANDAMENTO

    def lancar(self, angulo, tempo):
        """
        Método que executa lógica de lançamento.

        Deve escolher o primeiro pássaro não lançado da lista e chamar seu método lançar

        Se não houver esse tipo de pássaro, não deve fazer nada

        :param angulo: ângulo de lançamento
        :param tempo: Tempo de lançamento
        """

        for passaro in self._passaros:
            if passaro.status == ATIVO and not passaro.foi_lancado():
                passaro.lancar(angulo, tempo)
                break

    def calcular_pontos(self, tempo):
        """
        Lógica que retorna os pontos a serem exibidos na tela.

        Cada ator deve ser transformado em um Ponto.

        :param tempo: tempo para o qual devem ser calculados os pontos
        :return: objeto do tipo Ponto
        """
        pontos=[]
        primeiro = True

        for passaro in self._passaros:
            passaro.calcular_posicao(tempo)

            for ator in self._porcos + self._obstaculos:
                if(passaro.status == ATIVO):
                    passaro.colidir(ator, self.intervalo_de_colisao)
                    passaro.colidir_com_chao()
                else:
                    break

            #Apenas o pássaro que será lançado irá aparecer no estilingue, os demais no chão
            if passaro.status == ATIVO and not passaro.foi_lancado():
                if primeiro:
                    passaro.x = passaro._x_inicial
                    passaro.y = passaro._y_inicial
                    primeiro = False
                else:
                    passaro.x = 1
                    passaro.y = 1


            pontos.append(self._transformar_em_ponto(passaro))

        for ator in self._porcos + self._obstaculos:
            pontos.append(self._transformar_em_ponto(ator))

        return pontos

    def _transformar_em_ponto(self, ator):
        return Ponto(ator.x, ator.y, ator.caracter())

