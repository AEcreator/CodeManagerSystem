# -*- coding: gbk –*-
# !/usr/bin/python
import User
import Contest
import Problem
import now_info
from Tools import *


def order_board():
    println()
    printf('< Main Menu >')
    printf('About User', '(U/1)')
    printf('About Problem', '(P/2)')
    printf('About Contest', '(C/3)')
    printf('Back', '(B/4)')
    printf('Exit', '(Q)')
    printf('Useless', '(others)')
    printline()


def body():
    while True:
        order_board()
        if now_info.nowUser is not None:
            print_(now_info.nowUser.Uname+', Input your order:')
        else:
            print_('Input your order:')
        order = input()
        if order == 'U' or order == '1':
            User.main()
        elif order == 'P' or order == '2':
            Problem.main()
        elif order == 'C' or order == '3':
            Contest.main()
        elif order == 'B' or order == '4':
            back()
            break
        elif order == 'Q':
            exit()
        else:
            pass


def back():
    if now_info.nowUser is None:
        return
    feedback('Bye, '+now_info.nowUser.Uname)
    now_info.nowUser = None
