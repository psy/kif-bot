# -*- coding: utf-8 -*-

from willie.module import rate, rule, interval
from random import random, randint, choice

def setup(bot):
    if 'polly' not in bot.memory:
        bot.memory['polly'] = {}
        bot.memory['polly']['last_sentences'] = []
        bot.memory['polly']['talk_next_time'] = False
        bot.memory['polly']['sentences_since_last_answer'] = 0
        bot.memory['polly']['start_threshold'] = 0

@rule('.*')
def on_msg(bot, trigger):
    if not trigger.sender.startswith('#'):
        return

    if trigger.sender is not 'polly':
        bot.memory['polly']['last_sentences'] = bot.memory['polly']['last_sentences'][-9:].append(trigger.group(0))
        bot.memory['polly']['sentences_since_last_answer'] += 1

    if random() > 0.975:
        bot.memory['polly']['talk_next_time'] = True

@interval(23)
def cron(bot):
    answers = ['Hinter dir, ein dreiköpfiger Affe!', 'Und ne Buddel voll Rum.', 'Du kämpfst wie ein dummer Bauer!',
               'Mr Cottons Papagei, die selbe Frage!', 'Polly Cracker?', 'Klar soweit?', 'Arrrrrrrr!',
               'Ich bin ein mächtiger Pirat!', 'Polly will Cracker!']

    rand = random()
    threshold = bot.memory['polly']['start_threshold'] + 0.0625 * bot.memory['polly']['sentences_since_last_answer']

    if (bot.memory['polly']['talk_next_time'] or rand < threshold):
        if bot.memory['polly']['talk_next_time']:
            bot.memory['polly']['talk_next_time'] = False
        else:
            bot.memory['polly']['sentences_since_last_answer'] = 0
            bot.memory['polly']['start_threshold'] = -1 * random()

        if random() > 0.8:
            answer = choice(answers)
        else:
            answer = choice(bot.memory['polly']['last_sentences'])

        bot.msg('#kif', pollyfier(answer))


def pollyfier(msg, nested=False):
    output = ''

    words = msg.split(' ')

    for i, word in enumerate(words):
        for j, char in enumerate(word):
            output += char
            if char.lower() == 'r' and random() > 0.8:
                output += 'r' * randint(1, 5)

        output += ' '

        if not nested and random() > 0.8:
           output += pollyfier(choice([words[i], '*croack*', '*rrack*', 'Arrrrr!']), nested=True)

    return output
