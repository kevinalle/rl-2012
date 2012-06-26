#!/usr/bin/env python

import sys, re, random, heapq

def int2ls(i, length):
  return [b=="1" for b in (bin(i)[2:]).zfill(length)]

def ls2int(l):
  return int(''.join([e and "1" or "0" for e in l]), 2)

def xy2i(x, y, w):
  return y*w+x

def i2xy(i, w):
  return (i%w, i/w)

def pack_state(state, w):
  return (xy2i(state["x"], state["y"], w), ls2int(state["board"]), ls2int(state["cube"]))

def unpack_state(pstate, w, h):
  i, board, cube = pstate
  return {"x": i%w, "y": i/w, "board": int2ls(board, w*h), "cube": int2ls(cube, 6)}

def decode(gameid):
  """
  Extrae las condiciones iniciales del tablero a partir de un gameID
  
  El gameID es un string tipo "c4x4:62A4,11", donde "c" significa que es un
  cubo, "4x4" es el tamanio del tablero, "62A4" es la representacion hexadecimal
  del color de las celdas del tablero y "11" es la posicion inicial del cubo.
  """
  if not re.match("c\d{1,2}x\d{1,2}:[A-F0-9]+,\d+", gameid):
    print "Bad GameID"
    exit(1)
  w, h = map(int, gameid[1:].split(":")[0].split("x"))
  boardid, pos = gameid.split(":")[1].split(",")
  # construir una lista a partir de la representacin binaria del tablero inicial
  board = [b=="1" for b in (bin(int(boardid, 16))[2:]).zfill(4*len(boardid))][:w*h]
  x, y = i2xy(int(pos), w)
  return ({"x": x, "y": y, "board": board, "cube": [False]*6}, w, h)

def rotar(self, destino, rot):
  origen = rotate_list(destino, rot)
  self.cara[destino[0]], self.cara[destino[1]], self.cara[destino[2]], self.cara[destino[3]] = \
    self.cara[origen[0]], self.cara[origen[1]], self.cara[origen[2]], self.cara[destino[3]]

N,S,W,E,B,T = 0,1,2,3,4,5
movements = ["Up", "Down", "Left", "Right"]

def rot_N(cube):
  return [cube[T], cube[B], cube[W], cube[E], cube[N], cube[S]]

def rot_S(cube):
  return [cube[B], cube[T], cube[W], cube[E], cube[S], cube[N]]

def rot_W(cube):
  return [cube[N], cube[S], cube[T], cube[B], cube[W], cube[E]]

def rot_E(cube):
  return [cube[N], cube[S], cube[B], cube[T], cube[E], cube[W]]

def rot(cube, to):
  return [rot_N, rot_S, rot_W, rot_E][to](cube)

def iswin(cube):
  return all(cube)

def iswinp(pstate):
  return pstate[2] == 63

def draw(state, w, h):
  board = [b and "#" or "_" for b in state["board"]]
  board[state["y"]*w+state["x"]] = "C"
  board_str = '\n'.join([''.join(board[i*w:i*w+w]) for i in range(h)])
  print board_str

def can(state, w, h):
  return [i for (i,c) in enumerate([state["y"]>0, state["y"]<h-1, state["x"]>0, state["x"]<w-1]) if c]

def go(state, to, w):
  board, cube = state["board"][:], rot(state["cube"], to)
  x, y = [lambda x,y: (x,y-1), lambda x,y: (x,y+1), lambda x,y: (x-1,y), lambda x,y: (x+1,y)][to](state["x"], state["y"])
  board[y*w+x], cube[B] = cube[B], board[y*w+x]
  return {"x": x, "y": y, "board": board, "cube": cube}

def vecinos(pstate, w, h):
  state = unpack_state(pstate, w, h)
  return [(to, pack_state(go(state, to, w), w)) for to in can(state, w, h)]

def solve(pstate, w, h):
  def heuristic(pstate):
    return bin(pstate[1]).count("1")
  g = {pstate: 0}
  f = {pstate: heuristic(pstate)}
  openset = [(f[pstate], pstate)]
  closedset = []
  came_from = {}
  def reconstruct(pstate):
    if pstate in came_from:
      parent, action = came_from[pstate]
      path = reconstruct(parent)
      return path + [action]
    else:
      return []
  while openset:
    fval, ps = heapq.heappop(openset)
    if iswinp(ps):
      return reconstruct(ps)
    closedset.append(ps)
    for action, vecino in vecinos(ps, w, h):
      if vecino in closedset: continue
      tentative_g = g[ps] + 1
      if vecino not in openset or tentative_g < g[vecino]:
        came_from[vecino] = (ps, action)
        g[vecino] = tentative_g
        f[vecino] = tentative_g + heuristic(vecino)
        heapq.heappush(openset, (f[vecino], vecino))
  return False

def main(gameid):
  state, w, h = decode(gameid)
  pstate = pack_state(state, w)
  solution = solve(pstate, w, h)

  #~draw(state, w, h)
  #~for a in solution:
    #~print movements[a]
    #~state = go(state, a, w)
    #~draw(state, w, h)
    #~print state["cube"]
    #~print state["board"]
    #~print

  print '\n'.join([movements[a] for a in solution])

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else:
    print "Need GameId."
