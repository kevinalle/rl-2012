#!/usr/bin/env python
"""Correr el cube y mandarle acciones"""

import commands, os, time, random, argparse
from state import State

def move(where):
    """Espera .1s y apreta la tecla "where" (en la ventana activa)"""
    time.sleep(.1)
    os.system("xdotool key %s" % where)


def main(game_id=None, solver=None, size=(4, 4)):
    """Correr cube, correr solver, mandarle las acciones del solver"""
    # correr el cube con --generate, que nos genera un identificador de una
    # instancia del juego (del tipo "c4x4:62A4,11").
    gameid = game_id or commands.getoutput(
                            "cube --generate 1 c%dx%d" % tuple(size))
    print gameid
    # parsear el id del juego y extraer el tablero inicial y posicion del cubo.
    game = State(gameid=gameid)
    game.draw()

    if not game_id:
        # correr el cube con la instancia que generamos antes (abre una ventana
        # con el mismo juego que generamos y decodificamos antes.
        os.system("cube %s &" % gameid)
        # tomar el tiempo
        starttime = time.time()

    if solver:
        output = commands.getoutput("%s %s" % (solver, gameid))
        actions = output.strip().split("\n")
    else:
        moves = ["Up", "Right", "Down", "Left"]
        actions = [random.choice(moves) for _ in xrange(20)]

    # encontrar el Window ID de la ventana que abrio.
    windowid = commands.getoutput(
                   'xwininfo -name "Cube" | grep "Window id" | cut -d\    -f4')
    # activar esa ventana para poder mandarle teclas
    os.system("xdotool windowactivate %s" % windowid)

    if not game_id:
        # (darle 2s para que se abra)
        tardo = time.time() - starttime
        if solver:
            print "solver took %ss" % tardo
        if tardo < 2:
            time.sleep(2 - tardo)

    for action in actions:
        if action in ["Up", "Right", "Down", "Left"]:
            move(action)
        else:
            # raise Exception, "Accion invalida: %s"%action
            print action

def parseargs():
    """Parse command line arguments and run main"""
    parser = argparse.ArgumentParser(description='Solve "Cube".')
    parser.add_argument('--solver', default="./astar.py",
                        help='executable that solves the algorithm')
    parser.add_argument('--game', default=None, help='Game ID')
    parser.add_argument('--size', nargs=2, type=int, default=(4, 4),
                        help='Board size')
    args = parser.parse_args()

    main(game_id=args.game, solver=args.solver, size=args.size)

if __name__ == "__main__":
    parseargs()
