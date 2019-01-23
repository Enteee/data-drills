# vim: set fenc=utf8 ts=4 sw=4 et :
import itertools

from master.drill import Drill
from enum import Enum

class CharClass(Enum):
    """
    Calssifies and counts characters.

    Returns
    ---
    """

    CONTROL = 1
    WHITESPACE = 2
    SPECIAL = 3
    DIGIT = 4
    LETTER_LOW = 5
    LETTER_UP = 6
    UNDEFINED = 7

    @staticmethod
    def getClass(c):
        try:
            return {
                "\x00": CharClass.CONTROL,
                "\x01": CharClass.CONTROL,
                "\x02": CharClass.CONTROL,
                "\x03": CharClass.CONTROL,
                "\x04": CharClass.CONTROL,
                "\x05": CharClass.CONTROL,
                "\x06": CharClass.CONTROL,
                "\x07": CharClass.CONTROL,
                "\x08": CharClass.CONTROL,
                "\x09": CharClass.WHITESPACE,
                "\x0a": CharClass.WHITESPACE,
                "\x0b": CharClass.WHITESPACE,
                "\x0c": CharClass.CONTROL,
                "\x0d": CharClass.WHITESPACE,
                "\x0e": CharClass.CONTROL,
                "\x0f": CharClass.CONTROL,
                "\x10": CharClass.CONTROL,
                "\x11": CharClass.CONTROL,
                "\x12": CharClass.CONTROL,
                "\x13": CharClass.CONTROL,
                "\x14": CharClass.CONTROL,
                "\x15": CharClass.CONTROL,
                "\x16": CharClass.CONTROL,
                "\x17": CharClass.CONTROL,
                "\x18": CharClass.CONTROL,
                "\x19": CharClass.CONTROL,
                "\x1a": CharClass.CONTROL,
                "\x1b": CharClass.CONTROL,
                "\x1c": CharClass.CONTROL,
                "\x1d": CharClass.CONTROL,
                "\x1e": CharClass.CONTROL,
                "\x1f": CharClass.CONTROL,
                "\x20": CharClass.WHITESPACE,
                "\x21": CharClass.SPECIAL,
                "\x22": CharClass.SPECIAL,
                "\x23": CharClass.SPECIAL,
                "\x24": CharClass.SPECIAL,
                "\x25": CharClass.SPECIAL,
                "\x26": CharClass.SPECIAL,
                "\x27": CharClass.SPECIAL,
                "\x28": CharClass.SPECIAL,
                "\x29": CharClass.SPECIAL,
                "\x2a": CharClass.SPECIAL,
                "\x2b": CharClass.SPECIAL,
                "\x2c": CharClass.SPECIAL,
                "\x2d": CharClass.SPECIAL,
                "\x2e": CharClass.SPECIAL,
                "\x2f": CharClass.SPECIAL,
                "\x30": CharClass.DIGIT,
                "\x31": CharClass.DIGIT,
                "\x32": CharClass.DIGIT,
                "\x33": CharClass.DIGIT,
                "\x34": CharClass.DIGIT,
                "\x35": CharClass.DIGIT,
                "\x36": CharClass.DIGIT,
                "\x37": CharClass.DIGIT,
                "\x38": CharClass.DIGIT,
                "\x39": CharClass.DIGIT,
                "\x3a": CharClass.SPECIAL,
                "\x3b": CharClass.SPECIAL,
                "\x3c": CharClass.SPECIAL,
                "\x3d": CharClass.SPECIAL,
                "\x3e": CharClass.SPECIAL,
                "\x3f": CharClass.SPECIAL,
                "\x40": CharClass.SPECIAL,
                "\x41": CharClass.LETTER_UP,
                "\x42": CharClass.LETTER_UP,
                "\x43": CharClass.LETTER_UP,
                "\x44": CharClass.LETTER_UP,
                "\x45": CharClass.LETTER_UP,
                "\x46": CharClass.LETTER_UP,
                "\x47": CharClass.LETTER_UP,
                "\x48": CharClass.LETTER_UP,
                "\x49": CharClass.LETTER_UP,
                "\x4a": CharClass.LETTER_UP,
                "\x4b": CharClass.LETTER_UP,
                "\x4c": CharClass.LETTER_UP,
                "\x4d": CharClass.LETTER_UP,
                "\x4e": CharClass.LETTER_UP,
                "\x4f": CharClass.LETTER_UP,
                "\x50": CharClass.LETTER_UP,
                "\x51": CharClass.LETTER_UP,
                "\x52": CharClass.LETTER_UP,
                "\x53": CharClass.LETTER_UP,
                "\x54": CharClass.LETTER_UP,
                "\x55": CharClass.LETTER_UP,
                "\x56": CharClass.LETTER_UP,
                "\x57": CharClass.LETTER_UP,
                "\x58": CharClass.LETTER_UP,
                "\x59": CharClass.LETTER_UP,
                "\x5a": CharClass.LETTER_UP,
                "\x5b": CharClass.SPECIAL,
                "\x5c": CharClass.SPECIAL,
                "\x5d": CharClass.SPECIAL,
                "\x5e": CharClass.SPECIAL,
                "\x5f": CharClass.SPECIAL,
                "\x60": CharClass.SPECIAL,
                "\x61": CharClass.LETTER_LOW,
                "\x62": CharClass.LETTER_LOW,
                "\x63": CharClass.LETTER_LOW,
                "\x64": CharClass.LETTER_LOW,
                "\x65": CharClass.LETTER_LOW,
                "\x66": CharClass.LETTER_LOW,
                "\x67": CharClass.LETTER_LOW,
                "\x68": CharClass.LETTER_LOW,
                "\x69": CharClass.LETTER_LOW,
                "\x6a": CharClass.LETTER_LOW,
                "\x6b": CharClass.LETTER_LOW,
                "\x6c": CharClass.LETTER_LOW,
                "\x6d": CharClass.LETTER_LOW,
                "\x6e": CharClass.LETTER_LOW,
                "\x6f": CharClass.LETTER_LOW,
                "\x70": CharClass.LETTER_LOW,
                "\x71": CharClass.LETTER_LOW,
                "\x72": CharClass.LETTER_LOW,
                "\x73": CharClass.LETTER_LOW,
                "\x74": CharClass.LETTER_LOW,
                "\x75": CharClass.LETTER_LOW,
                "\x76": CharClass.LETTER_LOW,
                "\x77": CharClass.LETTER_LOW,
                "\x78": CharClass.LETTER_LOW,
                "\x79": CharClass.LETTER_LOW,
                "\x7a": CharClass.LETTER_LOW,
                "\x7b": CharClass.SPECIAL,
                "\x7c": CharClass.SPECIAL,
                "\x7d": CharClass.SPECIAL,
                "\x7e": CharClass.SPECIAL,
                "\x7f": CharClass.CONTROL
            }[c];
        except KeyError:
            return CharClass.UNDEFINED

class CharClassDrill(Drill):

    def get_headers(self):
        return (
            ["{}".format(h.name) for h in CharClass]
            + ["{}/{}".format(c[0].name, c[1].name) for c in itertools.combinations(CharClass, 2)]
        )

    def drill(self, raw):
        data = []
        counters = {c: 0 for c in CharClass}
        for c in raw:
            counters[CharClass.getClass(c)] += 1

        for c in CharClass:
            data += [counters[c]/len(raw)] if counters[c] != 0 else [0]

        for (c1, c2) in itertools.combinations(CharClass, 2):

            if counters[c1] != 0 and counters[c2] != 0:
                data += [counters[c1] / counters[c2]] 
            elif counters[c1] == 0 and counters[c2] == 0:
                data += [-1]
            elif counters[c2] == 0:
                data += [0]
            else:
                data += [-1]
        return data
