from game import BaseGame


class Double(BaseGame):
    key = 'D'
    code = 'DOUBLE'
    short_description = 'Vinci se esce lo stesso numero due volte. x5'
    long_description = (
        'Si lanciano due dadi, se in entrambi lanci esce lo stesso numero'
        ' vinci 5 volte quello che hai puntato.')
    min_bet = 10
    multiplier = 5

    def must_draw(self, previous_draws):
        return len(previous_draws) < 2

    def has_won(self, draws):
        return draws[0] == draws[1]
