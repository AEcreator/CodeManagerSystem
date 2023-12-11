# -*- coding: gbk –*-
# !/usr/bin/python


import builtins
import now_info
from Tools import *
import System_init as base
import compiler
import os
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
    println()
    printf('< Problem Menu >')
    printf('view problems (V/1)')
    printf('create a new problem (C/2)')
    printf('manage your problems (M/3)')
    printf('back (B/4)')
    printf('exit (Q)')
    printline()


def check():
    cursor = base.connection.cursor()
    cursor.execute("select Pid, Pname, Pscore from problem;")
    text = cursor.fetchall()
    printline('{:<10}{:<20}{:<10}'.format('Pid', 'name', 'score'))
    for item in text:
        print(f"{item[0]:<10}{mod(item[1],8):<20}{item[2]:<10}")
    cursor.close()
    print_('solve a problem now! (id/others)')
    ch = input()
    check_p(ch)


def check_p(choose):
    try:
        cursor = base.connection.cursor()
        cursor.execute(f"select * from problem where pid = %s;", (choose,))
        text = cursor.fetchall()
        if text is None or len(text) == 0:
            feedback("have not this problem!")
            return
        printline()
        col = ['id', 'name', 'score', 'text', 'tag', 'master', 'contest']
        for c, item in zip(col, text[0]):
            print(c, item)
        printline("do it!")
        return solve_problem(choose)
    except Exception as e:
        feedback(e)
        return 0

def get_code():
    code = get_txt()
    # 保存代码到文件
    with builtins.open('test.cpp', 'w') as file:
        file.write(code)


def solve_problem(choose):
    if now_info.nowUser is None:
        base.un_register()
    score = 0
    while True:
        printline('solve: quit(Q), continue(others)')
        ch = input()
        if ch == 'Q':
            break
        try:
            program()
            result = compiler.run(str(choose))
            print(result)
            if result == 'Accepted':
                score = 100
            insert_solve(now_info.nowUser, choose, result)
        except Exception as e:
            print_(f'确保你的文件可以运行: {e}')
    return score


def make_std(id):
    printline('make your std_in')
    _in = get_txt()
    with builtins.open('JudgeSystemA/input_'+str(id), 'w') as file:
        file.seek(0)
        file.write(_in)
    printline('make your std_out')
    _out = get_txt()
    with builtins.open('JudgeSystemA/output_std_'+id, 'w') as file:
        file.seek(0)
        file.write(_out)
    

def create_new():
    if now_info.nowUser is None:
        base.un_register()
        return
    println()
    print_("题目名称: ")
    name = input()
    print_("题目难度")
    score = input()
    print_("题目标签")
    tag = input()
    print_("题目内容")
    txt = get_txt()
    print_("隶属比赛")
    cont = input()
    cursor = base.connection.cursor()

    try:
        cid = int(cont)
        cursor.execute("insert into problem (pname, pscore, ptag, ptext, uid, cid) values(%s,%s,%s,%s,%s,%s);",
                       (name, score, tag, txt, now_info.nowUser.Uid, cid))
    except ValueError as e:
        cursor.execute("insert into problem (pname, pscore, ptag, ptext, uid) values(%s,%s,%s,%s,%s);",
                       (name, score, tag, txt, now_info.nowUser.Uid))
    base.connection.commit()
    cursor.execute("SELECT COUNT(*) FROM problem")
    id = cursor.fetchone()[0]
    print_(id)
    cursor.close()
    make_std(str(id))


def destroy():
    try:
        print_('input pid')
        id = input()
        cursor = base.connection.cursor()
        if int(now_info.nowUser.Uid) > 1:
            cursor.execute('delete from problem where pid = %s, uid = %s;', (id, now_info.nowUser.Uid))
        else:
            cursor.execute('delete from problem where pid = %s;', (id,))
        base.connection.commit()
        return 'Destroy Successfully!'
    except Exception as e:
        return e


def manage_my():
    if now_info.nowUser is None:
        print_('NULL')
        return
    cursor = base.connection.cursor()
    if int(now_info.nowUser.Uid) > 1:
        cursor.execute("select pid, pname from problem where uid = %s;", (now_info.nowUser.Uid,))
    else:
        cursor.execute("select pid, pname from problem;")
    lis = cursor.fetchall()
    # print(lis)
    if lis is None or len(lis) == 0:
        print_('NULL')
        return
    printline('{:<10}{:<20}'.format('id', 'name'))
    for item in lis:
        print(f"{item[0]:<10}{mod(item[1], 8):<20}")
    cursor.close()
    printline('destroy one (yes/others)')
    od = input()
    if od != 'yes':
        return
    print_(destroy())


def program():
    printline('program or copy your Code under this line, and input "ok":')
    println()
    # 获取剪贴板内容
    get_code()


def insert_solve(user, pid, result):
    try:
        cursor = base.connection.cursor()
        cursor.execute("INSERT INTO solve (uid, pid, Sresult, Stime) VALUES (%s, %s, %s, %s)",
                       (user.Uid, pid, result, datetime.datetime.today()))

        base.connection.commit()
        cursor.close()
    except Exception as e:
        print_("数据保存失败")


if __name__ == "__main__":
    main()
