from game import BaseGame


class Insurance(BaseGame):
    key = 'I'
    code = 'INSURANCE'
    short_description = 'Perdi se esce un numero a tua scelta. x8/7'
    long_description = (
        'Si lancia un unico dado, se esce il numero che hai scelto perdi,'
        ' in qualsiasi altro caso vinci otto settimi (~1.14) di quello che'
        ' hai puntato.')
    min_bet = 100
    multiplier = 1.142857
    has_param = True

    def check_param(self):
        return self.param in [1, 2, 3, 4, 5, 6]

    def has_won(self, draws):
        return draws[0] != self.param
