#!/usr/bin/env python
"""Solve Cube with A*"""

import sys, heapq
from state import State, MOVS

def solve(state):
    """Busca camino minimo en el grafo de estados con A*, copiado casi textual
    del pseudocodigo de http://en.wikipedia.org/wiki/A*_search_algorithm"""

    def heuristic(pstate):
        """Heuristica bastante relajada. Cantidad de caras que faltan levantar
        (claramente necesita al menos esa cantidad de pasos para ganar)"""
        return 6 - bin(pstate[2]).count("1")

    pstate = state.pack()
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
        _, packed = heapq.heappop(frontera)
        state = State(packed=packed)
        if state.iswin():
            return reconstruct(packed)
        visitados.add(packed)
        for action, vecino in state.vecinos():
            if vecino in visitados:
                continue
            tentative_g = g_score[packed] + 1
            if vecino not in frontera or tentative_g < g_score[vecino]:
                came_from[vecino] = (packed, action)
                g_score[vecino] = tentative_g
                f_score[vecino] = tentative_g + heuristic(vecino)
                heapq.heappush(frontera, (f_score[vecino], vecino))
    raise Exception, "No tiene solucion :("

def main(gameid):
    """Decode GameID, find solution, print solution"""
    state = State(gameid=gameid)
    solution = solve(state)
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
