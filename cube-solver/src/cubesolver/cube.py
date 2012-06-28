#!/usr/bin/env python

import commands, os, sys, time, random, re, argparse

def move(where):
  """Espera .1s y apreta la tecla "where" (en la ventana activa)"""
  time.sleep(.1)
  os.system("xdotool key %s"%where)

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
  # (pasar el hexadecimal a binario, sacarle el "0b" del principio, volver a
  # agregarle los 0s de la izquierda que corresponden, y truncarlo al tamanio
  # del tablero (si no tenia multiplo de 4 celdas))
  boardbool = (bin(int(boardid, 16))[2:]).zfill(4*len(boardid))[:w*h]
  # representacion en ASCII del tablero: _ celda blanca, # celda azul, C cubo
  board = [{"0":"_", "1": "#"}[b] for b in boardbool]
  board[int(pos)] = "C"
  # agregar "\n" cada w celdas
  board_str = '\n'.join([''.join(board[i*w:i*w+w]) for i in range(h)])
  return {"w": w, "h": h, "board": board_str, "pos": pos}

def main(game_id=None, solver=None, size=(4,4)):
  # correr el cube con --generate, que nos genera un identificador de una
  # instancia del juego (del tipo "c4x4:62A4,11").
  gameid = game_id or commands.getoutput("cube --generate 1 c%dx%d"%tuple(size))
  print gameid
  # parsear el id del juego y extraer el tablero inicial y posicion del cubo.
  game = decode(gameid)
  print game["board"]

  if not game_id:
    # correr el cube con la instancia que generamos antes (abre una ventana con el
    # mismo juego que generamos y decodificamos antes.
    os.system("cube %s &"%gameid)
    # (darle 2s para que se abra)
    wait2sFromNow = time.time()

  if solver:
    output = commands.getoutput("%s %s"%(solver,gameid))
    actions = output.strip().split("\n")
  else:
    moves = ["Up", "Right", "Down", "Left"]
    actions = [random.choice(moves) for _ in xrange(20)]

  # encontrar el Window ID de la ventana que abrio.
  windowid = commands.getoutput('xwininfo -name "Cube" | grep "Window id" | cut -d\  -f4')
  # activar esa ventana para poder mandarle teclas
  os.system("xdotool windowactivate %s"%windowid)
  
  if not game_id:
    # (darle 2s para que se abra)
    tardo = time.time()-wait2sFromNow
    if solver: print "solver took %ss"%tardo
    if tardo < 2: time.sleep(2-tardo)

  for a in actions:
    if a in ["Up", "Right", "Down", "Left"]:
      move(a)
    else:
      raise Exception, "Accion invalida"

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Solve "Cube".')
  parser.add_argument('--solver', default="./astar.py", help='executable that solves the algorithm')
  parser.add_argument('--game', default=None, help='Game ID')
  parser.add_argument('--size', nargs=2, type=int, default=(4,4), help='Board size')
  args = parser.parse_args()

  main(game_id=args.game, solver=args.solver, size=args.size)
