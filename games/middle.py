from game import BaseGame


class Middle(BaseGame):
    key = 'M'
    code = 'MIDDLE'
    short_description = 'Vinci se esce 3 o 4. x2.8'
    long_description = (
        'Si lancia un unico dado, se esce 3 o 4 vinci 2.8 volte quello che hai'
        ' puntato.')
    min_bet = 20
    multiplier = 2.8

    def has_won(self, draws):
        return draws[0] in (3, 4)
