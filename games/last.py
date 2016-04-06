from game import BaseGame


class Last(BaseGame):
    key = 'L'
    code = 'LAST'
    short_description = 'Vinci se esce 5 o 6. x2.8'
    long_description = (
        'Si lancia un unico dado, se esce 5 o 6 vinci 2.8 volte quello che hai'
        ' puntato.')
    min_bet = 20
    multiplier = 2.8

    def has_won(self, draws):
        return draws[0] in (5, 6)
