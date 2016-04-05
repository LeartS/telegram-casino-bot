def command_handler(function):
    """
    Decorator for command handlers. Replies with the return value of
    the command function
    """
    def wrapper(bot, update, args):
        message = function(bot, update, args)
        if message:
            bot.reply(update, message, parse_mode='html')
    return wrapper


def restrict(function):
    """
    Decorator that restricts the usage of the function to admin users
    """
    def wrapper(bot, update, args):
        if update.message.from_user.id not in bot.admin_users:
            bot.reply(update, 'Non fare il furbo ;)')
            return
        return function(bot, update, args)
    return wrapper


def restrict_to_chat(func):
    """
    Decorator that restrict the usage of the function in a specific channel
    """
    def wrapper(bot, update, args):
        if bot.casino_channel and update.message.chat_id != bot.casino_channel:
            bot.reply(
                update, 'Non puoi usare quel comando in questa chat.')
            return
        return func(bot, update, args)
    return wrapper


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
                bot.reply(update, 'Manca qualche parametro!')
                return

            # Check type
            converted_args = []
            for (a, t) in zip(args, types):
                try:
                    converted_args.append(t(a))
                except ValueError:
                    bot.reply(update, 'Hai sbagliato qualcosa')
                    break
            else:
                # add remaining unchecked/unconverted args
                args[:len(converted_args)] = converted_args
                return f(bot, update, args)
        return checked_args_f
    return check_args
