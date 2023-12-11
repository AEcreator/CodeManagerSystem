from os import *


def print_(*s):
    print('-', end='\t')
    for item in s:
        print(item, end='\t')
    print()


def printline(s=None):
    print('####################################################################')
    if s is not None:
        print(s)


def println():
    printline()


def feedback(s=None):
    printline()
    print('System:', s)
    pause()


def SomethingWrong():
    print_("Something Wrong")


def pause():
    try:
        system('pause')
    except KeyboardInterrupt as e:
        SomethingWrong()


def mod(s, max_len):
    return (s[:max_len] + '...') if len(s) > max_len else s


def get_txt():
    code = ''
    while True:
        line = input()
        if line.strip() == 'ok':
            break
        code += line + '\n'
    return code


def printf(*a):
    print('#', end='\t')
    for item in a:
        print(str(item).ljust(10), end='\t')
    print()
