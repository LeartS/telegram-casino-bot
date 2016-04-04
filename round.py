import hashlib
import os
import random

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


class UnacceptableBetError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def generate_seed():
    return ''.join(random.choice(CHARS) for i in range(15))


class Round(object):

    def __init__(self, payout_limit=None):
        self.seed = generate_seed()
        self.proof = hashlib.md5(self.seed.encode('utf-8')).hexdigest()[0:8]
        random.seed(self.seed)
        self.random_state = random.getstate()
        self.bets = []
        self.draws = []
        self.payout_limit = payout_limit

    @property
    def total_round_payout(self):
        """Returns the max possible payout at the end of this round"""
        return sum(b.max_payout for b in self.bets)

    def add_bet(self, bet):
        if self.total_round_payout + bet.max_payout > self.payout_limit:
            raise UnacceptableBetError(
                'Questa puntata mi porterebbe oltre il limite')
        self.bets.append(bet)

    def cancel_last_bet(self, player):
        bets = list(b for b in self.bets if b.player.name == player.name)
        if len(bets) == 0:
            return None
        else:
            self.bets.remove(bets[-1])
            return bets[-1]

    def go(self):
        """Make alle the necessary draws"""
        i = 0  # failsafe to avoid infinite loop
        while any(b.must_draw(self.draws) for b in self.bets) and i < 100:
            random.setstate(self.random_state)
            self.draws.append(random.randint(1, 6))
            self.random_state = random.getstate()
            i += 1
        return self.draws
