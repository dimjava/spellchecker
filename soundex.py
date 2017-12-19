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
            result += cfg['consonants'][idx]
        else:
            result += word[i]

    return result.encode('utf-8')

def soundex_en(word):
    if len(word) == 0:
        return "0000"

    cfg = soundconfig['en']
    word = word.lower()
    snd_arr = [word[0], 0, 0, 0]
    
    word = word[1:]    
    word = re.sub('[%s]' % ''.join(cfg["vowels"]), '', word)
    i=1
    for c in word:
        if c in cfg["codes"]:
            char_code = cfg["codes"][c]
            if snd_arr[i-1] != char_code:
                snd_arr[i] = char_code
                i += 1
            if i == 4:
                break
    return ''.join(map(lambda x: str(x), snd_arr))