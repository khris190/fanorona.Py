from numpy import true_divide
import fanorona as game

engine = game.Board()


def main():
    print(engine.fields[:][:])
    engine.CheckPossibleMoves(3,4)

main()