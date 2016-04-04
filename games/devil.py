from game import BaseGame


class Devil(BaseGame):
    key = 'V'
    code = 'DEVIL'
    short_description = 'Vinci se esce 666. x100'
    long_description = (
        'Si lanciano 3 dadi, se escono tre 6, vinci 100 volte quello che hai'
        ' puntato')
    multiplier = 100
    min_bet = 1

    def must_draw(self, previous_draws):
        return len(previous_draws) < 3

    def has_won(self, draws):
        return draws[0] == draws[1] == draws[2] == 6
