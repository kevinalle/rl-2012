#!/usr/bin/env python
"""Solve Cube with A*"""

import sys, re, heapq


def ls2int(lista):
    """Codifica una lista de Bools en un entero"""
    return int(''.join([e and "1" or "0" for e in lista]), 2)

def int2ls(i, length):
    """Decodifica un int en una lista de Bools con longitud length
    (su repr binaria)"""
    return [b == "1" for b in (bin(i)[2:]).zfill(length)]

def xy2i(xpos, ypos, width):
    """Pasa de coordenadas de una matriz a un indice de su representacion con
    vector unidimensional"""
    return ypos*width+xpos

def i2xy(i, width):
    """Decodifica un indice en coordenadas"""
    return (i%width, i/width)

def pack_state(state, width):
    """Codifica un estado en una tupla de 3 coordenadas (posicion del cubo,
    colores del tablero, colores del cubo)"""
    return (xy2i(state["x"], state["y"], width),
            ls2int(state["board"]),
            ls2int(state["cube"]))

def unpack_state(pstate, width, height):
    """Decodifica una tupla en un estado (x,y del cubo, lista de Bool de los
    colores del tablero, lista de Bool de los colores del cubo)"""
    i, board, cube = pstate
    return {"x": i % width, "y": i / width,
            "board": int2ls(board, width * height),
            "cube": int2ls(cube, 6)}

def decode(gameid):
    """
    Decodifica un gameID en el estado inicial y tamanio del tablero
    
    El gameID es un string tipo "c4x4:62A4,11", donde "c" significa que es un
    cubo, "4x4" es el tamanio del tablero, 62A4 es la representacion hexadecimal
    del color de las celdas del tablero y "11" es la posicion inicial del cubo.
    """
    if not re.match("c\d{1,2}x\d{1,2}:[A-F0-9]+,\d+", gameid):
        print "Bad GameID"
        exit(1)
    width, height = [int(val) for val in gameid[1:].split(":")[0].split("x")]
    boardid, pos = gameid.split(":")[1].split(",")
    # construir una lista de Bool a partir de la representacin bin del tablero
    # (pasar el hexadecimal a binario, sacarle el "0b" del principio, volver a
    # agregarle los 0s de la izquierda que corresponden, y truncarlo al tamanio
    # del tablero (si no tenia multiplo de 4 celdas))
    boardb = (bin(int(boardid, 16))[2:]).zfill(4*len(boardid))[:width * height]
    board = [b == "1" for b in boardb]
    xpos, ypos = i2xy(int(pos), width)
    return ({"x": xpos, "y": ypos, "board": board,
             "cube": [False] * 6}, width, height)

# CONSTs
N, S, W, E, B, T = 0, 1, 2, 3, 4, 5
MOVS = ["Up", "Down", "Left", "Right"]

# El cubo se representa con una lista de Bool que representa los colores de las
# caras: [N, S, W, E, B, T]
# Las rotaciones devuelven el estado del cubo despues de haber rotado en esa
# direccion
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

def rot(cube, rot_to):
    """Llama a la rotacion correspondiente segun el int to"""
    return [rot_north, rot_south, rot_west, rot_east][rot_to](cube)

def iswinp(pstate):
    """Un estado es WIN si el cubo esta todo pintado, osea si el estado del cubo
    es [True,True,True,True,True,True], osea su representacion en int es 63"""
    return pstate[2] == 63

def draw(state, width, height):
    """Representacion ASCII del estado"""
    board = [b and "#" or "_" for b in state["board"]]
    board[state["y"] * width + state["x"]] = "C"
    board_str = '\n'.join(
        [''.join(board[i * width:(i + 1) * width]) for i in range(height)])
    print board_str

def can(state, width, height):
    """Devuelve las acciones que puede tomar desde el estado actual"""
    bounds = [state["y"] > 0, state["y"] < height - 1,
            state["x"] > 0, state["x"] < width - 1]
    return [i for (i, c) in enumerate(bounds) if c]

def moveto(state, rot_to, width):
    """Devuelve el estado resultante de tomar la accion to desde state"""
    board = state["board"][:]
    # Rotar el cubo
    cube = rot(state["cube"], rot_to)
    # Actualizar x, y
    actions = [lambda x, y: (x, y - 1), lambda x, y: (x, y + 1),
               lambda x, y: (x - 1, y), lambda x, y: (x + 1, y)]
    xpos, ypos = actions[rot_to](state["x"], state["y"])
    # Swap de los colores cubo-tablero
    board[ypos * width + xpos], cube[B] = cube[B], board[ypos * width + xpos]
    return {"x": xpos, "y": ypos, "board": board, "cube": cube}

def vecinos(pstate, width, height):
    """Devuelve los estados vecinos del estado actual (empacados)"""
    state = unpack_state(pstate, width, height)
    return [(to, pack_state(moveto(state, to, width), width))
                for to in can(state, width, height)]

def solve(pstate, width, height):
    """Busca camino minimo en el grafo de estados con A*, copiado casi textual
    del pseudocodigo de http://en.wikipedia.org/wiki/A*_search_algorithm"""

    def heuristic(pstate):
        """Heuristica bastante relajada. Cantidad de caras que faltan levantar
        (claramente necesita al menos esa cantidad de pasos para ganar)"""
        return 6 - bin(pstate[2]).count("1")

    g_score = {pstate: 0}
    f_score = {pstate: heuristic(pstate)}
    # heap de los nodos a explorar
    frontera = [(f_score[pstate], pstate)]
    # conjunto de visitados, para evitar ciclos
    visitados = set()
    came_from = {}

    def reconstruct(pstate):
        """Reconstruccion recursiva del camino despues de llegar al goal"""
        if pstate in came_from:
            parent, action = came_from[pstate]
            path = reconstruct(parent)
            return path + [action]
        else:
            return []

    # sacar de a uno de la frontera, actualizar valor, agregar los vecinos
    while frontera:
        _, state = heapq.heappop(frontera)
        if iswinp(state):
            return reconstruct(state)
        visitados.add(state)
        for action, vecino in vecinos(state, width, height):
            if vecino in visitados:
                continue
            tentative_g = g_score[state] + 1
            if vecino not in frontera or tentative_g < g_score[vecino]:
                came_from[vecino] = (state, action)
                g_score[vecino] = tentative_g
                f_score[vecino] = tentative_g + heuristic(vecino)
                heapq.heappush(frontera, (f_score[vecino], vecino))
    raise Exception, "No tiene solucion :("

def main(gameid):
    """Decode GameID, find solution, print solution"""
    state, width, height = decode(gameid)
    pstate = pack_state(state, width)
    solution = solve(pstate, width, height)
    print '\n'.join([MOVS[a] for a in solution])

    # Para debug, imprimo los pasos y acciones
    #~draw(state, w, h)
    #~for a in solution:
        #~print MOVS[a]
        #~state = mvoeto(state, a, w)
        #~draw(state, w, h)
        #~print state["cube"]
        #~print state["board"]
        #~print

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Need GameId."
