#!/usr/bin/env python

import sys, re, random, heapq

def ls2int(l):
  """Codifica una lista de Bools en un entero"""
  return int(''.join([e and "1" or "0" for e in l]), 2)

def int2ls(i, length):
  """Decodifica un int en una lista de Bools con longitud length (su repr binaria)"""
  return [b=="1" for b in (bin(i)[2:]).zfill(length)]

def xy2i(x, y, w):
  """Pasa de coordenadas de una matriz a un indice de su representacion con vector unidimensional"""
  return y*w+x

def i2xy(i, w):
  """Decodifica un indice en coordenadas"""
  return (i%w, i/w)

def pack_state(state, w):
  """Codifica un estado en una tupla de 3 coordenadas (posicion del cubo, colores del tablero, colores del cubo)"""
  return (xy2i(state["x"], state["y"], w), ls2int(state["board"]), ls2int(state["cube"]))

def unpack_state(pstate, w, h):
  """Decodifica una tupla en un estado (x,y del cubo, lista de Bool de los colores del tablero, lista de Bool de los colores del cubo)"""
  i, board, cube = pstate
  return {"x": i%w, "y": i/w, "board": int2ls(board, w*h), "cube": int2ls(cube, 6)}

def decode(gameid):
  """
  Decodifica un gameID en el estado inicial y tamanio del tablero
  
  El gameID es un string tipo "c4x4:62A4,11", donde "c" significa que es un
  cubo, "4x4" es el tamanio del tablero, "62A4" es la representacion hexadecimal
  del color de las celdas del tablero y "11" es la posicion inicial del cubo.
  """
  if not re.match("c\d{1,2}x\d{1,2}:[A-F0-9]+,\d+", gameid):
    print "Bad GameID"
    exit(1)
  w, h = map(int, gameid[1:].split(":")[0].split("x"))
  boardid, pos = gameid.split(":")[1].split(",")
  # construir una lista de Bool a partir de la representacin binaria del tablero
  # (pasar el hexadecimal a binario, sacarle el "0b" del principio, volver a
  # agregarle los 0s de la izquierda que corresponden, y truncarlo al tamanio
  # del tablero (si no tenia multiplo de 4 celdas))
  boardbool = (bin(int(boardid, 16))[2:]).zfill(4*len(boardid))[:w*h]
  board = [b=="1" for b in boardbool]
  x, y = i2xy(int(pos), w)
  return ({"x": x, "y": y, "board": board, "cube": [False]*6}, w, h)

# CONSTs
N, S, W, E, B, T = 0,1,2,3,4,5
movements = ["Up", "Down", "Left", "Right"]

# El cubo se representa con una lista de Bool que representa los colores de las
# caras: [N, S, W, E, B, T]
# Las rotaciones devuelven el estado del cubo despues de haber rotado en esa
# direccion
def rot_N(cube):
  return [cube[T], cube[B], cube[W], cube[E], cube[N], cube[S]]

def rot_S(cube):
  return [cube[B], cube[T], cube[W], cube[E], cube[S], cube[N]]

def rot_W(cube):
  return [cube[N], cube[S], cube[T], cube[B], cube[W], cube[E]]

def rot_E(cube):
  return [cube[N], cube[S], cube[B], cube[T], cube[E], cube[W]]

# Llama a la rotacion correspondiente segun el int to
def rot(cube, to):
  return [rot_N, rot_S, rot_W, rot_E][to](cube)

# Un estado es WIN si el cubo esta todo pintado, osea si el estado del cubo es
# [True, True, True, True, True, True], osea si su representacion en int es 63
def iswinp(pstate):
  return pstate[2] == 63

def draw(state, w, h):
  board = [b and "#" or "_" for b in state["board"]]
  board[state["y"]*w+state["x"]] = "C"
  board_str = '\n'.join([''.join(board[i*w:i*w+w]) for i in range(h)])
  print board_str

# Devuelve las acciones que puede tomar desde el estado actual
def can(state, w, h):
  return [i for (i,c) in enumerate([state["y"]>0, state["y"]<h-1, state["x"]>0, state["x"]<w-1]) if c]

# Devuelve el estado resultante de tomar la accion to desde state
def go(state, to, w):
  board, cube = state["board"][:], rot(state["cube"], to)
  x, y = [lambda x,y: (x,y-1), lambda x,y: (x,y+1), lambda x,y: (x-1,y), lambda x,y: (x+1,y)][to](state["x"], state["y"])
  board[y*w+x], cube[B] = cube[B], board[y*w+x]
  return {"x": x, "y": y, "board": board, "cube": cube}

# Devuelve los estados vecinos del estado actual (empacados)
def vecinos(pstate, w, h):
  state = unpack_state(pstate, w, h)
  return [(to, pack_state(go(state, to, w), w)) for to in can(state, w, h)]

def solve(pstate, w, h):
  def heuristic(pstate):
    # Heuristica bastante "suelta". Cantidad de caras que faltan levantar
    return 6 - bin(pstate[2]).count("1")
  g = {pstate: 0}
  f = {pstate: heuristic(pstate)}
  # heap de los nodos a explorar
  frontera = [(f[pstate], pstate)]
  # conjunto de visitados, para evitar ciclos
  visitados = set()
  came_from = {}
  # Reconstruccion recursiva del camino despues de llegar al goal
  def reconstruct(pstate):
    if pstate in came_from:
      parent, action = came_from[pstate]
      path = reconstruct(parent)
      return path + [action]
    else:
      return []
  # sacar de a uno de la frontera, actualizar valor, agregar los vecinos
  while frontera:
    fval, ps = heapq.heappop(frontera)
    if iswinp(ps):
      return reconstruct(ps)
    visitados.add(ps)
    for action, vecino in vecinos(ps, w, h):
      if vecino in visitados: continue
      tentative_g = g[ps] + 1
      if vecino not in frontera or tentative_g < g[vecino]:
        came_from[vecino] = (ps, action)
        g[vecino] = tentative_g
        f[vecino] = tentative_g + heuristic(vecino)
        heapq.heappush(frontera, (f[vecino], vecino))
  raise Exception, "No tiene solucion :("

def main(gameid):
  state, w, h = decode(gameid)
  pstate = pack_state(state, w)
  solution = solve(pstate, w, h)
  print '\n'.join([movements[a] for a in solution])

  # Para debug, imprimo los pasos y acciones
  #~draw(state, w, h)
  #~for a in solution:
    #~print movements[a]
    #~state = go(state, a, w)
    #~draw(state, w, h)
    #~print state["cube"]
    #~print state["board"]
    #~print


if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else:
    print "Need GameId."
