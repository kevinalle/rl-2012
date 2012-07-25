#!/usr/bin/env python
"""(Try to?) solve Cube with Q Learning"""

import numpy as np
import random
from state import State, MOVS
import sys

class superdict(dict):
    def __init__(self, rowsize):
        super(superdict, self).__init__()
        self.rowsize = rowsize

    def __getitem__(self, item):
        if not self.has_key(item):
            self[item] = np.zeros(self.rowsize)
        return super(superdict, self).__getitem__(item)

def choose_action(Q, state):
    epsilon = 0.1
    posibles = state.can()
    if random.random() < epsilon:
        # Random
        return random.choice(posibles)
    else:
        # Romper empates
        s = state.pack()
        actions = np.where(Q[s]==Q[s].max())[0]
        return random.choice([a for a in actions if a in posibles])
    
def simular_ambiente(state, a):
    # Asumo determinismo
    return state.moveto(a)

def qlearning(inicial):
    Q = superdict(len(MOVS))

    num_episodios = 10000
    alpha = 0.1
    gamma = 0.1
    max_steps = 50

    for e in range(num_episodios):
        s = inicial
        state = State(packed=s)
        steps = 0
        r = False
        while not r and steps < max_steps: 
            # Elegir una accion
            a = choose_action(Q, state)
            # Tomar la accion y observar el resultado (s' y r)
            s_next = simular_ambiente(state, a)
            state = State(packed=s_next)
            r = state.iswin()
            # Actualizar Q
            Q[s][a] += alpha * (r + (gamma * max(Q[s_next])) - Q[s][a])
            # Actualizar el estado actual s
            s = s_next
            steps += 1
            # Si tengo reward, es win y se termina el episodio
        if r:
            print >> sys.stderr, "llego en %d pasos"%steps
    return Q

def solve(Q, inicial):
    s = State(packed=inicial)
    solution = []
    steps = 0
    while not s.iswin() and steps < 100:
        sp = s.pack()
        posibles = s.can()
        actions = np.where(Q[sp]==Q[sp].max())[0]
        a = random.choice([a for a in actions if a in posibles])
        s = State(packed=s.moveto(a))
        steps += 1
        solution.append(a)
    if s.iswin():
        return solution
    else:
        return None

def main(gameid):
    """Decode GameID, find solution, print solution"""
    state = State(gameid=gameid)
    Q = qlearning(state.pack())
    solution = solve(Q, state.pack())
    if solution:
        print '\n'.join([MOVS[a] for a in solution])
    else:
        raise Exception, "No la encontre :("

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Need GameId."
