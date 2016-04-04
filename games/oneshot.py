from game import BaseGame


class Oneshot(BaseGame):
    key = 'O'
    code = 'ONESHOT'
    short_description = 'Unico tiro risultato esatto: x5'
    long_description = ('Unico tiro, scegli un numero. Se esce quel numero'
                        ' vinci 5 volte quello che hai puntato.')
    multiplier = 5
    has_param = True

    def check_param(self):
        return self.param in [1, 2, 3, 4, 5, 6]

    def has_won(self, draws):
        return draws[0] == self.param
