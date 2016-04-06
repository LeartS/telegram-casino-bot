import telegram


class InvalidGameParams(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class BaseGame(object):

    key = None
    code = None
    short_description = None
    long_description = None
    multiplier = 1
    min_bet = 10
    max_bet = 1e12
    has_param = False

    def __init__(self, player, bet_amount, param=None):
        self.player = player
        self.bet = bet_amount
        self.param = param
        # check that bet amount and param restrictions
        self.check_valid()

    def __str__(self):
        return '{} punta {} su {}. Possibile vincita: {}'.format(
            self.player.name, self.bet, self.complete_game_name,
            self.predicted_payout)

    @property
    def complete_game_name(self):
        name = self.code
        if self.has_param:
            name += ' {}'.format(self.param)
        return name

    def check_valid(self):
        if self.has_param and self.param is None:
            raise InvalidGameParams(
                'Devi specificare il parametro per giocare a {}'.format(
                    self.code))
        elif self.has_param and not self.check_param():
            raise InvalidGameParams(
                'Il parametro {} non è valido per {}'.format(
                    self.param, self.code))
        elif self.bet < self.min_bet:
            raise InvalidGameParams('La puntata minima per {} è {}'.format(
                self.code, self.min_bet))
        elif self.bet > self.max_bet:
            raise InvalidGameParams('La puntata massima per {} è {}'.format(
                self.code, self.max_bet))

    def check_param(self):
        """
        If the game needs a param, check if a valid one has been provided.
        """
        pass

    def must_draw(self, previous_draws):
        """
        Determine if we should do another draw for this game.
        Most games always need a single draw so the condition will simply
        be len(previous_draws) == 0
        """
        return len(previous_draws) == 0

    def has_won(self, draws):
        """
        Determine if this has won based on the draws.
        Implement in child classes.
        """
        pass

    @property
    def predicted_payout(self):
        """
        Returns the possible payout. By default it's bet * multiplier but could
        be any custom logic. Doesn't necessarily return an integer.
        """
        return int(self.bet * self.multiplier)

    @property
    def max_payout(self):
        """
        Returns the maximum possible payout.
        For most games, this is the same as the payout, as you either win or
        lose. Other though could have variable payouts and this method
        should return the maximum possible one."""
        return int(self.bet * self.multiplier)

    def payout(self, draws):
        """
        Returns the payout based on the draws.
        By default returns bet * multiplier if `has_won() is True`, but can
        be customized in child classes.
        """
        if self.has_won(draws):
            return int(self.bet * self.multiplier)
        return 0

    def winning_message(self, draws):
        """
        Returns the "winning" message. By default this returns the game code,
        who won and how much; but it can be customized in child classes and
        can also depend on the draws.
        """
        return '{} {}! {} vince {} chips!'.format(
            telegram.Emoji.PARTY_POPPER,
            self.complete_game_name, self.player.name, self.payout(draws))



"""
**CHIUSO, STIAMO ASSUMENDO UN BOT!** Scegli una quota e /dai @LeartS la tua puntata

QUOTE DADO:
A: ONE SHOT Unico tiro risultato esatto: Paghi 1 vinci 5!
B: EVEN/ODD Unico tiro pari o dispari. Paghi 5 vinci 9!
C: INSURANCE Unico tiro perdi solo se esce 1. Paghi 7 vinci 8!
D: DOUBLE Stesso numero in due lanci. Paghi 1 vinci 5!
E: SEVEN Due lanci somma 7. Paghi 1 vinci 5!
F: EXTREMES Due lanci solo 1 e/o 6. Paghi 1 vinci 7!
G: TRIPLE Tre lanci stesso numero. Paghi 1 vinci 25!
H: (DE)INCREASING Tre lanci con valori (de)crescenti. Paghi 1 vinci 8
I: DIAVOLO Triplo 6: Paghi 1 vinci 50!
J: JACKPOT! Quattro lanci tutti 1: paghi 1 vinci 150!
K: SUICIDE! Si lancia finchè non esce un numero a vostra scelta e si vincono tante monete quanti i lanci effettuati (massimo 12)! Si paga 5 e si vince sempre, da 1 a 12 monete!
L: DUELLO! 1 VS 1. Ognuno tira il sudo dado, chi fa il numero più alto vince tutto. Se si pareggia vince il banco. Si punta quanto si vuole (ma tutti la stessa cifra)
M: AZZUFFATA! Minimo 3 giocatori. Il banco lancia il dado, dopodichè ognuno lancia il suo dado. Chi fa numero uguale a quello del banco vince tutto. Se nessuno lo fa, il banco si prende 3 monete e si rifa con quello che rimane. Si punta quanto si vuole (ma tutti la stessa cifra)

QUOTE MOLLA:
Z: VEGGENTE Minimo 3 giocatori. Si paga due per giocare e chi si avvicina più al numero vince tutto la posta in gioco meno due monete!

Oppure quote personalizzate su richiesta!
"""
