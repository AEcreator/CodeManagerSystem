# -*- coding: gbk –*-
# !/usr/bin/python

import Problem
import now_info
from Tools import *
import System_init as base
import datetime


def main():

    while True:
        board()
        print_('Input your order:')
        order = input()
        if order == '1' or order == 'V':
            check()
        elif order == '2' or order == 'C':
            create_new()
        elif order == '3' or order == 'M':
            manage_my()
        elif order == '4' or order == 'B':
            break
        elif order == 'Q':
            exit()
        else:
            print_('useless.')


def board():
    printline()
    printf('< Contest Menu >')
    printf('view contests', '(V/1)')
    printf('create a new contest', '(C/2)')
    printf('manage your contests', '(M/3)')
    printf('back', '(B/4)')
    printf('exit', '(Q)')
    printf('useless', '(others)')
    printline()


def check():
    cursor = base.connection.cursor()
    cursor.execute("select * from contest;")
    text = cursor.fetchall()
    printline('{:<10}{:<20}{:<10}'.format('Cid', 'name', 'level'))
    for item in text:
        print(f"{item[0]:<10}{mod(item[1],8):<20}{item[2]:<10}")
    cursor.close()
    print_('join a contest now! (id/others)')
    ch = input()
    check_c(ch)


def insert_participation(uid, cid, result):
    cursor = base.connection.cursor()
    cursor.execute('insert into participation (uid,cid,PPscore) values(%s,%s,%s);', (uid, cid, result))
    base.connection.commit()
    cursor.close()


def participate_contest(cid, lev):
    if now_info.nowUser is None:
        base.un_register()
        return
    rating = 0
    try:
        cursor = base.connection.cursor()
        cursor.execute('select * from problem where cid=%s;', (cid,))
        lis = cursor.fetchall()
        for prob in lis:
            rating += Problem.check_p(prob[0])
            print_('part: Quit(Q) Continue(others)')
            od = input()
            if od == 'Q':
                break
        cursor.close()
    except Exception as e:
        print_(e)
        SomethingWrong()
    feedback('your get score:'+str(rating))
    insert_participation(now_info.nowUser.Uid, cid, rating+lev)


def check_c(choose):
    try:
        cursor = base.connection.cursor()
        cursor.execute(f"select * from contest where cid = %s;", (choose,))
        text = cursor.fetchall()
        if text is None or len(text) == 0:
            feedback("have not this contest!")
            return
        printline()
        col = ['id', 'name', 'level', 'start', 'end']
        lev = 1
        for c, item in zip(col, text[0]):
            printf(c, item)
            if c == 'level':
                lev = int(item)
        feedback("do it!")
        participate_contest(choose, lev)
    except Exception as e:
        feedback(e)


def create_new():
    if now_info.nowUser is None or int(now_info.nowUser.Uid) != 1:
        feedback('Only Manager can create new contest.')
        return
    printline()
    printf('Input contest name')
    name = input()
    print_('Input contest level')
    lev = input()

    # 用户输入时间字符串
    user_input = input("请输入开始时间（格式：YYYY-MM-DD HH:MM:SS）: ")
    parsed_time = datetime.datetime.today()
    try:
        # 尝试将用户输入的时间字符串解析为 datetime 类型
        parsed_time = datetime.datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
        print_("输入时间成功:", parsed_time)
    except ValueError:
        print_("输入的时间格式不正确，请按照 YYYY-MM-DD HH:MM:SS 格式输入。")
    start = parsed_time
    user_input = input("请输入结束时间（格式：YYYY-MM-DD HH:MM:SS）: ")
    try:
        # 尝试将用户输入的时间字符串解析为 datetime 类型
        parsed_time = datetime.datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
        print_("输入时间成功:", parsed_time)
    except ValueError:
        print_("输入的时间格式不正确，请按照 YYYY-MM-DD HH:MM:SS 格式输入。")
    end = parsed_time
    try:
        cursor = base.connection.cursor()
        cursor.execute('insert into contest (cname,clevel,cstart,cend) values(%s,%s,%s,%s);', (name, lev, start, end))
        base.connection.commit()
        cursor.close()
        feedback('create successfully')
    except Exception as e:
        print_('create failed')


def destroy():
    try:
        print_('input cid')
        id = input()
        cursor = base.connection.cursor()
        cursor.execute('delete from contest where cid = %s;', (id,))
        base.connection.commit()
        return 'Destroy Successfully!'
    except Exception as e:
        return e


def manage_my():
    if now_info.nowUser is None or int(now_info.nowUser.Uid) > 1:
        feedback('Only Manager can manage contest')
        return
    cursor = base.connection.cursor()
    cursor.execute("select cid, cname from contest;")
    lis = cursor.fetchall()
    # print(lis)
    if lis is None or len(lis) == 0:
        print_('NULL')
        return
    printline('{:<10}{:<20}'.format('cid', 'name'))
    for item in lis:
        print_(f"{item[0]:<10}{mod(item[1], 8):<20}")
    cursor.close()
    printline('destroy one (yes/others)')
    od = input()
    if od != 'yes':
        return
    print_(destroy())
