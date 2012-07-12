'''
Created on Jul 11, 2012

@author: mariano
'''
import re

# CONSTs
N, S, W, E, B, T = 0, 1, 2, 3, 4, 5
MOVS = ["Up", "Down", "Left", "Right"]

class State:
    """Representacion de un estado del juego, con metodos de vecinos, etc"""

    width = None
    height = None

    def __init__(self, gameid=None, packed=None, state=None):
        if gameid:
            self.decode(gameid)
        else:
            if not State.width or not State.height:
                raise Exception, "No width or height"
            if packed:
                self.unpack(packed)
            elif state:
                self.xpos = state["x"]
                self.ypos = state["y"]
                self.board = state["board"]
                self.cube = state["cube"]
            else:
                raise Exception, "Uninitialized state!"

    def pack(self):
        """Devuelve el estado empacado en una tupla"""
        return State.pack_state(self.xpos, self.ypos, self.board, self.cube)

    @staticmethod
    def pack_state(xpos, ypos, board, cube):
        """Codifica un estado en una tupla de 3 coordenadas (posicion del cubo,
        colores del tablero, colores del cubo)"""
        return (State._xy2i(xpos, ypos),
                State._ls2int(board),
                State._ls2int(cube))

    def unpack(self, packed):
        """Decodifica una tupla en un estado (x,y del cubo, lista de Bool de los
        colores del tablero, lista de Bool de los colores del cubo)"""
        i, board, cube = packed
        self.xpos = i % State.width
        self.ypos = i / State.width
        self.board = State._int2ls(board, State.width * State.height)
        self.cube = State._int2ls(cube, 6)

    def decode(self, gameid):
        """
        Decodifica un gameID en el estado inicial y tamanio del tablero
        
        El gameID es un string tipo "c4x4:62A4,11", donde "c" significa que es
        un cubo, "4x4" es el tamanio del tablero, 62A4 es la representacion hexa
        del color de las celdas del tablero y 11 es la posicion inicial del cubo
        """
        if not re.match("c\d{1,2}x\d{1,2}:[A-F0-9]+,\d+", gameid):
            raise Exception, "Bad GameID"
        State.width, State.height = \
                [int(val) for val in gameid[1:].split(":")[0].split("x")]
        boardid, pos = gameid.split(":")[1].split(",")
        # construir una lista de Bool a partir de la representacin binaria del
        # tablero (pasar el hexadecimal a binario, sacarle el 0b del principio,
        # volver a agregarle los 0 de la izquierda que corresponden, y truncarlo
        # al tamanio del tablero (si no tenia multiplo de 4 celdas)).
        boardbool = bin(int(boardid, 16))[2:]
        boardb = boardbool.zfill(4 * len(boardid))[:State.width * State.height]
        board = [b == "1" for b in boardb]
        xpos, ypos = State._i2xy(int(pos))
        self.xpos = xpos
        self.ypos = ypos
        self.board = board
        self.cube = [False] * 6

    # El cubo se representa con una lista de Bool que representa los colores de
    # las caras: [N, S, W, E, B, T]
    # Las rotaciones devuelven el estado del cubo despues de haber rotado en esa
    # direccion
    @staticmethod
    def rot(cube, rot_to):
        """Llama a la rotacion correspondiente segun el int to"""
        def rot_north(cube):
            """Return ratated cube list"""
            return [cube[T], cube[B], cube[W], cube[E], cube[N], cube[S]]

        def rot_south(cube):
            """Return ratated cube list"""
            return [cube[B], cube[T], cube[W], cube[E], cube[S], cube[N]]

        def rot_west(cube):
            """Return ratated cube list"""
            return [cube[N], cube[S], cube[T], cube[B], cube[W], cube[E]]

        def rot_east(cube):
            """Return ratated cube list"""
            return [cube[N], cube[S], cube[B], cube[T], cube[E], cube[W]]
        return [rot_north, rot_south, rot_west, rot_east][rot_to](cube)

    def iswin(self):
        """Un estado es WIN si el cubo esta todo pintado"""
        return all(self.cube)

    def draw(self):
        """Representacion ASCII del estado"""
        board = [b and "#" or "_" for b in self.board]
        board[self.ypos * State.width + self.xpos] = "C"
        board_str = '\n'.join(
            [''.join(board[i * State.width:(i + 1) * State.width])
                    for i in range(State.height)])
        return board_str

    def can(self):
        """Devuelve las acciones que puede tomar desde el estado actual"""
        bounds = [self.ypos > 0, self.ypos < State.height - 1,
                  self.xpos > 0, self.xpos < State.width - 1]
        return [i for (i, c) in enumerate(bounds) if c]

    def moveto(self, rot_to):
        """Devuelve el estado resultante de tomar la accion to desde state"""
        board = self.board[:]
        # Rotar el cubo
        cube = State.rot(self.cube, rot_to)
        # Actualizar x, y
        actions = [lambda x, y: (x, y - 1), lambda x, y: (x, y + 1),
                   lambda x, y: (x - 1, y), lambda x, y: (x + 1, y)]
        xpos, ypos = actions[rot_to](self.xpos, self.ypos)
        # Swap de los colores cubo-tablero
        board[ypos * State.width + xpos], cube[B] = \
                cube[B], board[ypos * State.width + xpos]
        return State.pack_state(xpos, ypos, board, cube)

    def vecinos(self):
        """Devuelve los estados vecinos del estado actual (empacados)"""
        return [(to, self.moveto(to)) for to in self.can()]

    @staticmethod
    def _ls2int(lista):
        """Codifica una lista de Bools en un entero"""
        return int(''.join([e and "1" or "0" for e in lista]), 2)

    @staticmethod
    def _int2ls(i, length):
        """Decodifica un int en una lista de Bools con longitud length
        (su repr binaria)"""
        return [b == "1" for b in (bin(i)[2:]).zfill(length)]

    @staticmethod
    def _xy2i(xpos, ypos):
        """Pasa de coordenadas de una matriz a un indice de su representacion
        con vector unidimensional"""
        return ypos * State.width + xpos

    @staticmethod
    def _i2xy(i):
        """Decodifica un indice en coordenadas"""
        return (i % State.width, i / State.width)

