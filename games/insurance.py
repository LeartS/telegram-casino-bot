from game import BaseGame


class Insurance(BaseGame):
    key = 'I'
    code = 'INSURANCE'
    short_description = 'Perdi se esce 1. x8/7'
    long_description = (
        'Si lancia un unico dado, se esce 1 perdi, in qualsiasi altro caso'
        ' vinci otto settimi (~1.14) di quello che hai puntato.')
    min_bet = 100
    multiplier = 1.142857

    def has_won(self, draws):
        return draws[0] != 1
