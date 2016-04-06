from game import BaseGame


class Decreasing(BaseGame):
    key = '-'
    code = 'DECREASING'
    short_description = 'Vinci se esce una sequenza decrescente. x8'
    long_description = (
        'Si lanciano 3 dadi, se esce una sequenza strettamente decrescente'
        ' (ovvero A &gt; B &gt; C), vinci 8 volte quello che hai puntato')
    multiplier = 8
    min_bet = 5

    def must_draw(self, previous_draws):
        return len(previous_draws) < 3

    def has_won(self, draws):
        return draws[0] > draws[1] > draws[2]
