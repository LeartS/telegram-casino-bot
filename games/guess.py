from game import BaseGame


class Guess(BaseGame):
    key = 'G'
    code = 'GUESS'
    short_description = 'Indovina quanti lanci vuoi e vinci un sacco!'
    long_description = (
        'Prova ad indovinare quanti lanci vuoi e vinci X 5^numero_lanci.\n'
        'Per esempio, GUESS 2512 significa che prevedi escano, in ordine, '
        '2, 5, 1, 2. Se indovini vinci 5^4 = 625 volte quello che hai puntato.'
        '\nGUESS con un unico numero è equivalente a ONESHOT, per esempio'
        'GUESS 2 è la stessa cosa di ONESHOT 2.')
    multiplier = 5
    has_param = True

    @property
    def multiplier(self):
        return 5**len(str(self.param))

    def check_param(self):
        for digit in str(self.param):
            if int(digit) not in [1, 2, 3, 4, 5, 6]:
                return False
        return True

    def must_draw(self, previous_draws):
        return len(previous_draws) < len(str(self.param))

    def has_won(self, draws):
        return draws[:len(str(self.param))] == list(map(int, str(self.param)))
