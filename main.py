from numpy import true_divide
import fanorona as game

engine = game.Board()


def main():
    print(engine.fields[:][:])
    test = engine.FindAllPossibleMovesForPlayer(1)
    print(test)
main()