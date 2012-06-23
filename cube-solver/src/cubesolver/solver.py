'''
Created on Jun 19, 2012

@author: mariano
'''
from cubesolver.vector2d import Vector2d
N = 0
S = 1
W = 2
E = 3
B = 4
T = 5

def rotate_list(l, n=1):
    return l[-n:] + l[:-n]

class Cubo():

    def __init__(self):
        self.cara = [False] * 6

    def rotar_norte(self):
        self.rotar([B, N, T, S], -1)

    def rotar_sur(self):
        self.rotar([B, N, T, S], 1)

    def rotar_este(self):
        self.rotar([B, E, T, W], -1)

    def rotar_oeste(self):
        self.rotar([B, E, T, W], 1)

    def rotar(self, destino, rot):
        origen = rotate_list(destino, rot)
        self.cara[destino[0]], self.cara[destino[1]], self.cara[destino[2]], self.cara[destino[3]] = \
            self.cara[origen[0]], self.cara[origen[1]], self.cara[origen[2]], self.cara[destino[3]]



class Juego(object):




    def __init__(self, size, position=(0, 0)):
        self.size = Vector2d(size, size)
        self.tablero = self.construir_tablero()
        self.position = Vector2d(position)
        self.caras_cubo = Cubo()

    def construir_tablero(self):
        return [[False] * self.size.x for _ in range(self.size.y)]



    def mover_este(self):
        if self.position.x < self.size.x:
            self.position.x += 1
            self.caras_cubo.rotar_este()
            self.caras_cubo.cara[B], self.tablero[self.position.x][self.position.y] = \
                self.tablero[self.position.x][self.position.y], self.caras_cubo.cara[B]

    def __repr__(self):
        return self.tablero, self.caras_cubo.cara


    def pintado(self):
        return all(self.caras_cubo.cara)

def main():

    juego = Juego(3)
    juego.mover_este()



if __name__ == '__main__':
    main()
