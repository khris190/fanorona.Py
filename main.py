from numpy import true_divide
import fanorona as game

engine = game.Board()


def main():
    print(engine.fields[:][:])
    test = engine.GetAllPlayerMovements(2)
    print(test)
main()