from game import BaseGame


class Extremes(BaseGame):
    key = 'X'
    code = 'EXTREMES'
    short_description = 'Vinci se escono solo 1 e/o 6 in due lanci. x7'
    long_description = (
        'Si lanciano 2 dadi, se escono solo gli "estremi" (1 e/o 6) vinci'
        ' 7 volte quello che hai puntato')
    multiplier = 7
    min_bet = 5

    def must_draw(self, previous_draws):
        return len(previous_draws) < 2

    def has_won(self, draws):
        return draws[0] in (1,6) and draws[1] in (1,6)
