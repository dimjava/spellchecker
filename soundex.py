# -*- coding: utf-8 -*-

import re

# from future import builtins
# from builtins import str

from lang_soundconfig import soundconfig

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def soundex(word):
    if is_ascii(word):
        return soundex_en(word)
    else:
        return soundex_ru(word.decode('utf-8'))

def soundex_ru(word):
    if len(word) == 0:
        return u''

    word = word.lower()

    no_repeats = word[0]
    for i in range(1, len(word)):
        if word[i] == word[i - 1]:
            continue
        no_repeats += word[i]
    word = no_repeats

    cfg = soundconfig['ru']
    word = re.sub('[%s]' % (''.join(cfg["vowels"])), '', word)

    result = u''

    for i in range(len(word)):
        idx = cfg['indexes'].find(word[i])

        if idx != -1:
            ch = cfg['consonants'][idx]
            if i > 0 and result[-1] == ch:
                continue
            result += ch
        else:
            result += word[i]

    return result.encode('utf-8')

def soundex_en(word):
    if len(word) == 0:
        return '0000'

    cfg = soundconfig['en']
    word = word.lower()
    snd_arr = [word[0]]
    
    word = word[1:] 
    word = re.sub('[%s]' % ''.join(cfg["vowels"]), '0', word)

    for c in word:
        if c in cfg['codes']:
            char_code = cfg['codes'][c]
            if snd_arr[-1] == char_code:
                continue
            else:
                snd_arr.append(char_code)
        else:
            snd_arr.append(c)

    snd_arr = filter(lambda x: x != '0', snd_arr)

    while len(snd_arr) < 4:
        snd_arr.append('0')

    return ''.join(map(lambda x: str(x), snd_arr))