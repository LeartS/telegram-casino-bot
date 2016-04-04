from game import BaseGame


class Seven(BaseGame):
    key = 'S'
    code = 'SEVEN'
    short_description = 'Vinci se la somma di due lanci fa 7. x5'
    long_description = (
        'Si lanciano due dadi, se la somma dei 2 lanci è 7'
        ' vinci 5 volte quello che hai puntato.')
    min_bet = 10
    multiplier = 5

    def must_draw(self, previous_draws):
        return len(previous_draws) < 2

    def has_won(self, draws):
        return draws[0] + draws[1] == 7
