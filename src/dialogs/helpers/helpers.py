#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import logging

logger = logging.getLogger('dialogs')

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
}


def colored_print(text, fg_colour=None, bg_colour=None):
    try:
        if len(text) == 0:
            return ''
        if isinstance(text, (str, unicode)):
            pass
        elif len(text) == 1:
            text = text[0]
        else:
            text = "[" + ", ".join(text) + "]"
    except TypeError:
        pass

    if not fg_colour and not bg_colour:
        return text
    if not fg_colour:
        return format_colour('$BG-' + bg_colour.upper() + text + "$RESET", True)
    if not bg_colour:
        return format_colour('$' + fg_colour.upper() + text + "$RESET", True)

    return format_colour('$BG-' + bg_colour.upper() + '$' + fg_colour.upper() + text + "$RESET", True)


def format_colour(message, use_color=True):
    if not use_color:
        RESET_SEQ = ""
        COLOR_SEQ = ""
        BOLD_SEQ = ""
    else:
        RESET_SEQ = "\033[0m"
        COLOR_SEQ = "\033[1;%dm"
        BOLD_SEQ = "\033[1m"

    message = message.replace("$RESET", RESET_SEQ) \
        .replace("$BOLD", BOLD_SEQ)

    for k, v in COLORS.items():
        message = message.replace("$" + k, COLOR_SEQ % (v + 30) if use_color else "") \
            .replace("$BG" + k, COLOR_SEQ % (v + 40) if use_color else "") \
            .replace("$BG-" + k, COLOR_SEQ % (v + 40) if use_color else "")
    return message + RESET_SEQ


def get_console_handler():
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    log_handler.setFormatter(formatter)

    return log_handler


def get_file_handler(filename):
    log_handler = logging.FileHandler(filename)
    log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    log_handler.setFormatter(formatter)

    return log_handler


def check_results(res, expected, allow_question_mark=False):
    def check_triplets(tr, te):
        sr, pr, orr = tr.split()
        se, pe, oe = te.split()

        if not allow_question_mark and \
                ('?' in se or '?' in sr):
            return False

        return (sr == se or se == '*') and \
               (pr == pe or pe == '*') and \
               (orr == oe or oe == '*')

    while res:
        r = res.pop()
        for e in expected:
            if check_triplets(r, e):
                expected.remove(e)
    if expected:
        logger.info("\t**** /Missing statements in result:   ")
        logger.info("\t" + str(expected) + "\n")

    return expected == res


def wait_for_keypress():
    """No way to reliably wait for a key press or even Enter!!
    Tried: raw_input(), sys.stdin.readline(), sys.stdin.read(1)
    """
    pass


if __name__ == '__main__':
    #should print a blue 'Hello World'
    print(format_colour("$BLUEHello World$RESET"))

    #should print a default 'Hello World'
    print(format_colour("$BLUEHello World$RESET", False))

    #should print a blue bold 'Hello World'
    print(format_colour("$BLUE$BOLDHello World$RESET"))

    #should print a yellow bold 'Hello World'
    print(format_colour("$YELLOW$BOLDHello World$RESET"))

    #should print a 'Hello World' on a yellow background.
    print(format_colour("$BG-YELLOWHello World$RESET"))

    #should print a 'Hello World' in bold
    print(format_colour("$BOLDHello World$RESET"))

    #should print a 'Hello World' with normal colour.
    print(format_colour("Hello World"))


def generate_id(with_question_mark=True):
    sequence = "abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sample = random.sample(sequence, 5)
    return ("?" + "".join(sample)) if with_question_mark else ("".join(sample))


