#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING'  : YELLOW,
    'INFO'     : WHITE,
    'DEBUG'    : BLUE,
    'CRITICAL' : YELLOW,
    'ERROR'    : RED,
    'RED'      : RED,
    'GREEN'    : GREEN,
    'YELLOW'   : YELLOW,
    'BLUE'     : BLUE,
    'MAGENTA'  : MAGENTA,
    'CYAN'     : CYAN,
    'WHITE'    : WHITE,
}

def format_colour(message, use_color = True):
    
    if not use_color:
        RESET_SEQ = ""
        COLOR_SEQ = ""
        BOLD_SEQ  = ""
    else:
        RESET_SEQ = "\033[0m"
        COLOR_SEQ = "\033[1;%dm"
        BOLD_SEQ  = "\033[1m"
    
    message   = message.replace("$RESET", RESET_SEQ)\
                       .replace("$BOLD",  BOLD_SEQ)
    
    for k,v in COLORS.items():
        message = message.replace("$" + k,    COLOR_SEQ % (v+30) if use_color else "")\
                         .replace("$BG" + k,  COLOR_SEQ % (v+40) if use_color else "")\
                         .replace("$BG-" + k, COLOR_SEQ % (v+40) if use_color else "")
    return message + RESET_SEQ


if __name__ == '__main__':
    
    #should print a blue 'Hello World'
    print format_colour("$BLUEHello World$RESET")
    
    #should print a default 'Hello World'
    print format_colour("$BLUEHello World$RESET", False)
    
    #should print a blue bold 'Hello World'
    print format_colour("$BLUE$BOLDHello World$RESET")
    
    #should print a yellow bold 'Hello World'
    print format_colour("$YELLOW$BOLDHello World$RESET")
    
    #should print a 'Hello World' on a yellow background.
    print format_colour("$BG-YELLOWHello World$RESET")
    
    #should print a 'Hello World' in bold
    print format_colour("$BOLDHello World$RESET")
    
    #should print a 'Hello World' with normal colour.
    print format_colour("Hello World")
