#!/usr/bin/env python

import commands, os, sys, time, random, re

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
  board = [["_", "#"][b=="1"] for b in (bin(int(boardid, w*h))[2:]).zfill(w*h)]
  board[int(pos)] = "C"
  board_str = '\n'.join([''.join(board[i*w:i*w+w]) for i in range(h)])
  return {"w": w, "h": h, "board": board_str, "pos": pos}

def main(game_id=None):
  # correr el cube con --generate, que nos genera un identificador de una
  # instancia del juego (del tipo "c4x4:62A4,11").
  gameid = game_id or commands.getoutput("cube --generate 1 c4x4")
  print gameid
  # parsear el id del juego y extraer el tablero inicial y posicion del cubo.
  game = decode(gameid)
  print game["board"]

  if not game_id:
    # correr el cube con la instancia que generamos antes (abre una ventana con el
    # mismo juego que generamos y decodificamos antes.
    os.system("cube %s &"%gameid)
    # (darle 2s para que se abra)
    time.sleep(2)
  # encontrar el Window ID de la ventana que abrio.
  windowid = commands.getoutput('xwininfo -name "Cube" | grep "Window id" | cut -d\  -f4')
  # activar esa ventana para poder mandarle teclas
  os.system("xdotool windowactivate %s"%windowid)
  
  # mover randomly :P
  moves = ["Up", "Right", "Down", "Left"]
  for i in xrange(50):
    move(random.choice(moves))

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else:
    main()

