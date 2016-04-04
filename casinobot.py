#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import redis
from telegram.ext import Updater

from game import InvalidGameParams
from round import Round, UnacceptableBetError
from games import games


__package__ = 'casinobot'

TOKEN = '173695676:AAF25jZo_Q13Zyi66upxtYuzefuJ4QT4Q-Y'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

admin_users = [
    8553438,  # LeartS
]
casino_chat_id = -1001044483707

r = redis.StrictRedis(host='localhost', port=6379)
j = None

active_rounds = {}


antiscam_text = """
Ho un sistema antitruffa incorporato; esso garantisce che le
estrazioni sono casuali e determinate prima di qualsiasi puntata, rendendo così
impossibile per me "barare" e creare estrazioni in base alle puntate.


COME FUNZIONA:

Per generare numeri casuali, uso un PRNG (Pseudo Random Number Generator),
un algoritmo che dato un <i>seed</i> iniziale genera una sequenza
deterministica di numeri che possono essere considerati statisticamente
casuali.
Ciò che significa che con lo stesso seed verrà generata sempre la stessa
sequenza, da qualsiasi programma che utilizzi lo stesso algoritmo con gli
stessi parametri! Potete pure provare a copiare il seed
e usarlo per Python `random.seed()` sul vostro computer e otterrete anche lì
la stessa sequenza!

Per ogni giro genero un seed diverso e all'inizio di ogni giro,
<b>prima di qualsiasi puntata</b>, mostro i primi 8 caratteri dell'hash MD5
del seed che verrà utilizzato per le estrazioni.


PERCHÈ MD5

Se mostrassi direttamente il seed, come detto, potreste barare voi usandolo
sul vostro computer per sapere in anticipo quali numeri verranno generati.
Con MD5 invece non potete risalire al seed originale (per cui non potete barare)
ma quando vi do il seed originale (alla fine dell'estrazione) potete facilmente
verificare, anche usando generatori MD5 online come http://www.md5.cz/,
che combaciano e che quindi ho effettivamente utilizzato quel seed (stabilito
prima di qualsiasi puntata) per generare i numeri casuali.
""".replace('\n', ' ').replace('   ', '\n\n').replace('  ', '\n')


def restrict(function):
    def wrapper(bot, update, args):
        if update.message.from_user.id not in admin_users:
            bot.sendMessage(update.message.chat_id, text='Non fare il furbo ;)')
            return
        return function(bot, update, args)
    return wrapper


def restrict_to_chat(chat_id):
    def check_channel(func):
        def wrapper(bot, update, *args):
            if update.message.chat_id != chat_id:
                bot.sendMessage(
                    update.message.chat_id,
                    text='Non puoi usare quel comando in questa chat.')
                return
            return func(bot, update, *args)
        return wrapper
    return check_channel


def name(value):
    """Fake type that raises ValueError if value does not start with @"""
    if not str(value).startswith('@'):
        raise ValueError
    return str(value)


def args(*types):
    """
    Check the passed arguments to see if they match the signature.
    Types is an array that can contains the standard types
    (e.g. int, float, string) plus the specific "types":
    - name: an username starting with '@'
    """

    def check_args(f):
        def checked_args_f(bot, update, args):
            # Check number of arguments
            if len(args) < len(types):
                bot.sendMessage(
                    update.message.chat_id, text='Manca qualche parametro!')
                return

            # Check type
            converted_args = []
            for (a, t) in zip(args, types):
                try:
                    converted_args.append(t(a))
                except ValueError:
                    bot.sendMessage(
                        update.message.chat_id, text='Hai sbagliato qualcosa')
                    break
            else:
                # add remaining unchecked/unconverted args
                args[:len(converted_args)] = converted_args
                return f(bot, update, args)
        return checked_args_f
    return check_args


def get_game(key_or_code):
    try:
        return next(
            filter(lambda g: key_or_code.upper() in (g.key, g.code), games))
    except StopIteration:
        return None


def get_current_round(chat_id):
    return active_rounds.get(chat_id, None)


def set_current_round(chat_id, round_):
    active_rounds[chat_id] = round_


def antiscam(bot, update):
    bot.sendMessage(
        update.message.chat_id, text=antiscam_text, parse_mode='html')


def chips(bot, update):
    chips = r.hget('users:{}'.format(update.message.from_user.name), 'chips')
    if not chips:
        message = '{} non hai chips! Contatta @LeartS per fare buy-in'.format(
            update.message.from_user.name)
    else:
        message = '{} hai {} chips'.format(
            update.message.from_user.name, chips.decode())
    bot.sendMessage(update.message.chat_id, message)


@restrict
@restrict_to_chat(casino_chat_id)
@args(name, int)
def buyin(bot, update, args):
    name, amount = args[:2]
    balance = r.hincrby('users:{}'.format(name), 'chips', amount)
    message = ('{} {} chips sono state aggiunte al tuo conto!\n'
               'Hai ora {} chips.').format(name, amount, balance)
    bot.sendMessage(update.message.chat_id, text=message)
    logger.info('{} buy-in {}'.format(name, amount))


@restrict_to_chat(casino_chat_id)
@args(name, int)
def transfer(bot, update, args):
    """Transfer chips"""
    name, amount = args
    chips = int(
        r.hget('users:{}'.format(update.message.from_user.name), 'chips') or 0)
    if amount > chips:
        message = 'Non puoi trasferire chips che non hai ;)'
        bot.sendMessage(update.message.chat_id, text=message)
        return
    r.hincrby(
        'users:{}'.format(update.message.from_user.name), 'chips', -amount)
    r.hincrby(
        'users:{}'.format(name), 'chips', amount)
    message = '{} hai dato {} delle tue chips a {}. Che gentile!'.format(
        update.message.from_user.name, amount, name)
    bot.sendMessage(update.message.chat_id, text=message)


def info(bot, update, args):
    """
    Returns info about a game
    """
    game = get_game(args[0])
    if game:
        msg = "{} {}\n- Puntata minima: {}".format(
            game.code, game.long_description, game.min_bet)
        bot.sendMessage(update.message.chat_id, text=msg)


def list_games(bot, update, args):
    msg = '\n'.join(
        '<b>[{}] {}</b>: {}'.format(g.key, g.code, g.short_description)
        for g in games
    )
    bot.sendMessage(update.message.chat_id, text=msg, parse_mode='html')


@restrict
@restrict_to_chat(casino_chat_id)
@args(name, int)
def buyout(bot, update, args):
    name, amount = args
    r.hincrby(
        'users:{}'.format(update.message.from_user.name), 'chips', -amount)
    message = '{} {} chips sono state tolte dal tuo conto'.format(
        name, amount)
    bot.sendMessage(update.message.chat_id, text=message)
    logger.info('{} buy-out {}'.format(name, amount))


@restrict
@restrict_to_chat(casino_chat_id)
@args(int)
def limit(bot, update, args):
    amount = args[0]
    r.hset('config', 'payout_limit', amount)
    bot.sendMessage(
        update.message.chat_id,
        text='Impostato limite vincite round a {}'.format(amount))


@restrict_to_chat(casino_chat_id)
@args(int, str)
def bet(bot, update, args):
    current_round = get_current_round(update.message.chat_id)
    if current_round is None:
        bot.sendMessage(update.message.chat_id, text='Nessun giro attivo!')
        return
    amount, game_key_or_code = args[:2]
    game = get_game(game_key_or_code)
    if not game:
        message = 'Nessun gioco trovato per: {}'.format(game_key_or_code)
        bot.sendMessage(update.message.chat_id, text=message)
        return
    chips = int(
        r.hget('users:{}'.format(update.message.from_user.name), 'chips') or 0)
    if amount > chips:
        message = 'Non hai chips sufficienti per fare questa puntata'
        bot.sendMessage(update.message.chat_id, text=message)
        return
    param = int(args[2]) if len(args) > 2 else None
    try:
        bet = game(update.message.from_user, amount, param)
        current_round.add_bet(bet)
    except (InvalidGameParams, UnacceptableBetError) as e:
        bot.sendMessage(update.message.chat_id, text=str(e))
        return
    # all went well
    r.hincrby(
        'users:{}'.format(update.message.from_user.name), 'chips', -amount)
    game_variant = bet.code + ' ' + str(param) if bet.has_param else bet.code
    message = '{} punti {} su {}. Possibile vincita: {}\n\nIn gioco:\n'.format(
        update.message.from_user.name, amount, game_variant,
        bet.predicted_payout)
    message += '\n'.join(str(b) for b in current_round.bets)
    message += '\n\npayout <b>{}/{}</b> - codice antitruffa: <b>{}</b>\n'.format(
        current_round.total_round_payout, current_round.payout_limit,
        current_round.proof)
    bot.sendMessage(update.message.chat_id, text=message, parse_mode='html')
    logger.info('{} bets {} on {}'.format(
        update.message.from_user.name, amount, game_variant))


@restrict_to_chat(casino_chat_id)
def start_round(bot, update):
    """Starts a new round"""
    current_round = get_current_round(update.message.chat_id)
    if current_round is not None:
        bot.sendMessage(
            update.message.chat_id, text='C\'è già un round attivo')
        return
    limit = r.hget('config', 'payout_limit')
    if limit:
        limit = int(limit)
    else:
        limit = None
    new_round = Round(payout_limit=limit)
    set_current_round(update.message.chat_id, new_round)
    message = ('Inizia un nuovo giro!\nMassimo payout: <b>{}</b> - '
               'Codice antitruffa: <b>{}</b>').format(limit, new_round.proof)
    bot.sendMessage(update.message.chat_id, text=message, parse_mode='html')


@restrict_to_chat(casino_chat_id)
def play(bot, update):
    """Plays a round"""
    current_round = get_current_round(update.message.chat_id)
    if not current_round:
        bot.sendMessage(update.message.chat_id, text='Nessun giro attivo.')
        return
    if not current_round.bets:
        bot.sendMessage(
            update.message.chat_id,
            text='Aspetta! Nessuno ha ancora puntato in questo round!')
        return
    draws = current_round.go()
    message = '\n'.join(
        'Lancio #{}: esce <b>{}</b>!'.format(i+1, d)
        for i, d in enumerate(draws))
    bot.sendMessage(update.message.chat_id, text=message, parse_mode='html')
    # Winners
    message = ''
    total_bet = 0
    total_payout = 0
    for bet in current_round.bets:
        total_bet += bet.bet
        payout = bet.payout(draws)
        if payout > 0:
            total_payout += payout
            message += bet.winning_message(draws) + '\n'
            r.hincrby(
                'users:{}'.format(bet.player.name), 'chips', payout)
    if message == '':  # noone won!
        message = 'Nessun vincitore a questo giro!\n'
    message += '\nTotale giocato: <b>{}</b>\nTotale vinto: <b>{}</b>'.format(
        total_bet, total_payout)
    message += '\nIl seed per il random utilizzato era: {}'.format(
        current_round.seed)
    j.put(
        lambda b: b.sendMessage(update.message.chat_id, text=message,
                                parse_mode='html'),
        1, repeat=False
    )
    set_current_round(update.message.chat_id, None)


def error(bot, update, args):
    logger.info('Error')

if __name__ == '__main__':
    updater = Updater(TOKEN)
    j = updater.job_queue
    dispatcher = updater.dispatcher
    dispatcher.addTelegramCommandHandler('deposita', buyin)
    dispatcher.addTelegramCommandHandler('preleva', buyout)
    dispatcher.addTelegramCommandHandler('trasferisci', transfer)
    dispatcher.addTelegramCommandHandler('chips', chips)
    dispatcher.addTelegramCommandHandler('punta', bet)
    dispatcher.addTelegramCommandHandler('limita', limit)
    dispatcher.addTelegramCommandHandler('spiega', info)
    dispatcher.addTelegramCommandHandler('lista', list_games)
    dispatcher.addTelegramCommandHandler('giro', start_round)
    dispatcher.addTelegramCommandHandler('gioca', play)
    dispatcher.addTelegramCommandHandler('antitruffa', antiscam)
    dispatcher.addErrorHandler(error)
    updater.start_polling()
    updater.idle()
