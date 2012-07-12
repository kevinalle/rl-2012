#!/usr/bin/env python
"""Solve Cube with A*"""

import numpy as np

def vi(state, num_states, num_actions):
    epsilon = 0.001

    # Inicializar V y Q a valores arbitrarios

    Q = np.zeros((num_states, num_actions))
    V = np.zeros((num_states, 1))
    stop = False
    gamma = 0.9

    # Ciclar hasta que entre una iteracion y otra haya poco (<epsilon) cambio
    # en los valores
    while not stop:
        delta = 0
        # Para cada estado, para cada accion...
        for s in range(num_states):
            for a in range(num_actions):
                # Guardar Q actual para luego compararlo con el actualizado y
                # medir cuanto cambio (para saber cuando parar el ciclo
                # principal)
                q = Q(s, a)

                # Actualizar Q (se puede optimizar para el cubo)
                Q[s, a] = state.R[s, a] + gamma * state.T[s, :, a] * V

                # Medir el cambio maximo en Q
                delta = max(delta, abs(q - Q(s, a)))

                # Calcular V como el Q maximo para cada estado
                V = max(Q.T).T

        # Si delta<epsilon, parar
        stop = delta < epsilon

    # Extraer el policy de Q
    return Q.max(1)
