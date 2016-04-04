from game import BaseGame


class Bulldozer(BaseGame):
    key = 'B'
    code = 'BULLDOZER'
    short_description = 'Si lancia finchè non esce un numero a tua scelta'
    long_description = (
        'Si lancia finchè non esce un numero a vostra scelta (o si raggiungono'
        ' i 12 lanci) e si vince un sesto di quanto puntato per ogni lancio'
        ' effettuato. Si vince sempre qualcosa!')
    has_param = True
    min_bet = 60

    def check_param(self):
        return self.param in [1, 2, 3, 4, 5, 6]

    def must_draw(self, previous_draws):
        return self.param not in previous_draws and len(previous_draws) < 12

    def has_won(self, draws):
        return True

    @property
    def predicted_payout(self):
        return 'Da {} a {}'.format(self.bet // 6, self.bet*2)

    @property
    def max_payout(self):
        return int(self.bet * 2)

    def payout(self, draws):
        try:
            multiplier = draws.index(self.param) + 1
        except ValueError:
            # No selected number in the draws, this must mean the max number
            # of draws has been reached
            multiplier = 12
        return int(self.bet * multiplier / 6)
