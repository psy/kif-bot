# -*- coding: utf-8 -*-

from willie.module import rate, rule, interval
from random import randint
from datetime import datetime, timedelta


def setup(bot):
    if 'cc' not in bot.memory:
        print('initialising memory')
        bot.memory['cc'] = {}
    return


def shutdown(bot):
    return


@rule('^h?ola(\s.*)?')
@rule('.*cann?abis.*')
@rule('.*weed.*')
def no_cannabis(bot, trigger):
    if trigger.sender.startswith('#'):
        if trigger.nick not in bot.memory['cc']:
            bot.memory['cc'][trigger.nick] = {'dt': datetime.now(),
                                              'count': 1}
            bot.reply('No cannabis!')
        elif datetime.now() - bot.memory['cc'][trigger.nick]['dt'] > timedelta(minutes=10):
            bot.memory['cc'][trigger.nick]['count'] += 1
            bot.memory['cc'][trigger.nick]['dt'] = datetime.now()
            bot.reply('NO CANNABIS!')
        else:
            bot.memory['cc'][trigger.nick]['count'] += 0.5

        if bot.memory['cc'][trigger.nick]['count'] > 2:
            if randint(2, 5) <= bot.memory['cc'][trigger.nick]['count']:
                bot.write(['KICK', trigger.sender, trigger.nick], 'ETOOMUCHCANNABIS')


@rule('.*Por\s?que.*\?')
@rule('.*why.*\?')
@rule('.*(wieso|warum|weshalb).*\?')
@rate(10 * 60)
def why(bot, trigger):
    if trigger.nick in bot.memory['cc'] and datetime.now() - bot.memory['cc'][trigger.nick]['dt'] < timedelta(
            minutes=5):
        bot.reply('This channel is related to a conference of computer science students, not cannabis! That\'s why!')


@interval(3600)
def lower_score(bot):
    for nick in list(bot.memory['cc']):
        bot.memory['cc'][nick]['count'] -= 1

        if bot.memory['cc'][nick]['count'] <= 0:
            bot.memory['cc'].pop(nick)
