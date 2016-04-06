from game import BaseGame


class First(BaseGame):
    key = 'F'
    code = 'FIRST'
    short_description = 'Vinci se esce 1 o 2. x2.8'
    long_description = (
        'Si lancia un unico dado, se esce 1 o 2 vinci 2.8 volte quello che hai'
        ' puntato.')
    min_bet = 20
    multiplier = 2.8

    def has_won(self, draws):
        return draws[0] in (1, 2)
