# -*- coding: utf-8 -*-

soundconfig = {
    "ru": {
        "vowels": [u'у', u'е', u'ы', u'а', u'о', u'э', u'я', u'и', u'ю', u'ь', u'ъ', u'й'],
        "indexes": u'бвгджз',
        "consonants": u'пфктшс',
    },
    "en": {
        "vowels": ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y'],
        "consonants": {
            1: ['b', 'f', 'p', 'v'],
            2: ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z'],
            3: ['d', 't'],
            4: ['l'],
            5: ['m', 'n'],
            6: ['r']
        }
    },
}


def revert_config():
    k = 'en'
    soundconfig[k]["codes"] = {}
    for (code) in soundconfig[k]["consonants"].keys():
        for c in soundconfig[k]["consonants"][code]:
            c = c.decode("utf-8") if hasattr(c, 'decode') else c
            soundconfig[k]["codes"][c] = code


revert_config()