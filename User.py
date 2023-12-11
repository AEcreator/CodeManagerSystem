# -*- coding: gbk –*-
# !/usr/bin/python
import now_info
import System_init as base
from Tools import *


def main():
    while True:
        board()
        print_('Input your order:')
        order = input()
        if order == '1' or order == 'U':
            update()
        elif order == '2' or order == 'D':
            destroy()
        elif order == '3' or order == 'CU':
            check_user_list()
        elif order == '4' or order == 'C':
            check_contest_history()
        elif order == '5' or order == 'P':
            check_problem_history()
        elif order == '6' or order == 'B':
            break
        elif order == 'Q':
            exit()
        else:
            print_('useless.')


def board():
    show_info()
    println()
    printf('< User Menu >')
    printf('update', '(U/1)')
    printf('destroy', '(D/2)')
    printf('check users', '(CU/3)')
    printf('contests history', '(C/4)')
    printf('problems history', '(P/5)')
    printf('back', '(B/6)')
    printf('exit', '(Q)')
    printf('useless', '(others)')
    printline()


def update():
    if now_info.nowUser is None:
        base.un_register()
    else:
        printline('now update your information, enter to pass:')
        print_('Input your name')
        name = input()
        print_('Input your phone')
        phone = input()
        print_('Input your email')
        email = input()
        print_('Input your address')
        address = input()
        data = []
        col_name = []
        if name != "":
            col_name.append('Uname')
            data.append(name)
        if phone != "":
            col_name.append('Uphone')
            data.append(phone)
        if email != "":
            col_name.append('Uemail')
            data.append(email)
        if address != "":
            col_name.append('Uaddress')
            data.append(address)
        cursor = base.connection.cursor()
        sql = "update user set "
        for i, col in enumerate(col_name):
            sql += f"{col} = '{data[i]}'"
            if i < len(col_name) - 1:
                sql += ", "
        sql += " where uid = " + str(now_info.nowUser.Uid) + ";"
        # print(sql)
        cursor.execute(sql)
        base.connection.commit()
        feedback('Update Account Successfully')
        cursor.close()


def show_disclaimer():
    printline("请阅读免责声明：")
    # 显示免责声明的内容
    disclaimer_text = "这是免责声明的内容，用户需要阅读并确认同意后才能继续。1.用户清楚账号一旦销毁，将不可恢复的风险;2.用户清楚此举为个人行为，与平台无关。"
    print(disclaimer_text)
    agreed = input("您是否同意免责声明？(yes/no): ").lower()
    return agreed


def destroy():
    agreed = show_disclaimer()
    if now_info.nowUser is not None and agreed == "yes":
        print_('Input your password:')
        pwd = input()
        cursor = base.connection.cursor()
        cursor.execute('select upwd from user where uid = %s;', (now_info.nowUser.Uid,))
        confirm = cursor.fetchall()[0][0]
        print_(confirm)
        if pwd == confirm:
            cursor.execute('delete from user where uid = %s', (now_info.nowUser.Uid,))
            base.connection.commit()
            now_info.nowUser = None
            feedback('Destroy Successfully.')
            cursor.close()
    else:
        feedback('Account destroy failed, please keep your account safe.')


def check_user_list():
    cursor = base.connection.cursor()
    cursor.execute("select urating, uname from user order by Urating desc;")
    text = cursor.fetchall()
    # print(text)
    printline('{:<10}{:<10}'.format('rating', 'name'))
    for item in text:
        print(f"{item[0]:<10}{item[1]:<10}")
    cursor.close()
    pause()


def check_contest_history():
    if now_info.nowUser is None:
        print('NULL')
        return
    cursor = base.connection.cursor()
    cursor.execute("select c.cid,c.cname,p.ppscore from participation p join contest c on p.cid = c.cid where p.uid = %s;",
                   (now_info.nowUser.Uid,))
    text = cursor.fetchall()
    printline()
    if text is None or len(text) == 0:
        print('NULL')
        return
    for item in text:
        print(item)
    cursor.close()
    pause()


def check_problem_history():
    if now_info.nowUser is None:
        print('NULL')
        return
    cursor = base.connection.cursor()
    cursor.execute("select p.pid,p.pname,s.sresult from solve s join problem p on s.pid = p.pid where s.uid = %s;",
                   (now_info.nowUser.Uid,))
    text = cursor.fetchall()
    printline()
    if text is None or len(text) == 0:
        print_('NULL')
        return
    for item in text:
        print(item)
    cursor.close()
    pause()


def show_info():
    printf('< User Info >')
    if now_info.nowUser is None:
        printf('uid', 'tourist')
        printf('others', 'null')
        return
    cursor = base.connection.cursor()
    col_name = ['uid', 'uname', 'uphone', 'uemail', 'uaddress', 'urating']
    columns = ', '.join(col_name)
    cursor.execute(f"select {columns} from User where Uid = %s", (now_info.nowUser.Uid,))
    info = cursor.fetchall()[0]
    printline()
    for i1, i2 in zip(col_name, info):
        printf(str(i1), str(i2))
    println()
    cursor.close()
    pause()
