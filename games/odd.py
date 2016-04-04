from game import BaseGame


class Odd(BaseGame):
    key = 'Z'
    code = 'ODD'
    short_description = 'Vinci se esce un numero dispari. x1.8'
    long_description = (
        'Si lancia un unico dado, se esce dispari vinci 1.8 volte quello che hai'
        ' puntato.')
    min_bet = 50
    multiplier = 1.8

    def has_won(self, draws):
        return draws[0] % 2 == 1
