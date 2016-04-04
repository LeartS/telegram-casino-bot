from game import BaseGame


class Triple(BaseGame):
    key = 'T'
    code = 'TRIPLE'
    short_description = 'Vinci se esce 3 volte lo stesso numero. x20'
    long_description = (
        'Si lanciano 3 dadi, se esce lo stesso numero in tutti e 3 i lanci'
        ' vinci 20 volte quello che hai puntato')
    multiplier = 20

    def must_draw(self, previous_draws):
        return len(previous_draws) < 3

    def has_won(self, draws):
        return draws[0] == draws[1] == draws[2]
