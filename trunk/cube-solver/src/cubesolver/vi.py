#!/usr/bin/env python
"""Solve Cube with Value Iteration"""

import numpy as np

def vi(T, R, num_states, num_actions):
    epsilon = 0.001
    gamma = 0.9

    # Inicializar V y Q a valores arbitrarios

    Q = np.zeros((num_states, num_actions))
    V = np.zeros((num_states, 1))

    # Ciclar hasta que entre una iteracion y otra haya poco (<epsilon) cambio
    # en los valores
    stop = False
    while not stop:
        delta = 0
        # Para cada estado, para cada accion...
        for s in range(num_states):
            for a in range(num_actions):
                # Guardar Q actual para luego compararlo con el actualizado y
                # medir cuanto cambio (para saber cuando parar el ciclo
                # principal)
                q = Q[s, a]

                # Actualizar Q (se puede optimizar para el cubo)
                TsaxV = # T[s, :, a] * V
                Q[s, a] = R[s, a] + gamma * TsaxV 

                # Medir el cambio maximo en Q
                delta = max(delta, abs(q - Q[s, a]))

                # Calcular V como el Q maximo para cada estado
                V = max(Q.T).T

        # Si delta<epsilon, parar
        stop = delta < epsilon

    # Extraer el policy de Q
    return Q.max(1)

if __name__ == "__main__":
    Q = np.zeros((num_states, num_actions))
    vi()
