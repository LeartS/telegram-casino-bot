from game import BaseGame


class Devil(BaseGame):
    key = 'V'
    code = 'DEVIL'
    short_description = 'Vinci se esce 666. x135'
    long_description = (
        'Si lanciano 3 dadi, se escono tre 6, vinci 135 volte quello che hai'
        ' puntato')
    multiplier = 135
    min_bet = 5

    def must_draw(self, previous_draws):
        return len(previous_draws) < 3

    def has_won(self, draws):
        return draws[0] == draws[1] == draws[2] == 6
