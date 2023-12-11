# -*- coding: gbk –*-
# !/usr/bin/python
import datetime

import pymysql
import System_body as body
import now_info
from Tools import *


# 建立数据库连接
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="yueguangwan520",
    database="CodeforcesSystem",
    charset='utf8'
)
# 创建游标
cursor = connection.cursor()


def init_database():
    # 创建User表
    sql = """
        drop table if exists user,solve,participation,problem,contest;
    """
    cursor.execute(sql)

    create_user_table = """
    CREATE TABLE if not exists User (
        Uid INT AUTO_INCREMENT PRIMARY KEY,
        Uname VARCHAR(20) NOT NULL,
        Uphone VARCHAR(11),
        Uemail VARCHAR(50),
        Upwd VARCHAR(20) NOT NULL,
        Uaddress VARCHAR(20),
        Urating INT DEFAULT 0
    )
    """
    cursor.execute(create_user_table)
    cursor.execute('INSERT INTO User (Uid, Uname, Upwd, Urating) VALUES (%s,%s,%s,%s)',
                   ('001', 'God', '000', '9999'))
    cursor.execute('INSERT INTO User (Uid, Uname, Upwd) VALUES (%s,%s,%s)',
                   ('002', 'rpk', '123'))

    # 创建Contest表
    sql = """
            drop table if exists contest;
        """
    cursor.execute(sql)
    create_contest_table = """
        CREATE TABLE Contest (
            Cid INT AUTO_INCREMENT PRIMARY KEY,
            Cname VARCHAR(20) NOT NULL,
            Clevel INT,
            Cstart DATETIME,
            Cend DATETIME
        )
        """
    cursor.execute(create_contest_table)

    insert_query = """
            INSERT INTO Contest (Cname, Clevel, Cstart, Cend)
                VALUES (%s, %s, %s, %s);
            """
    now = datetime.datetime.today()
    data = ('CodeTon1', 1000, now, now + datetime.timedelta(hours=2))
    cursor.execute(insert_query, data)

    # 创建Problem表
    sql = """
        drop table if exists problem;
    """
    cursor.execute(sql)

    create_problem_table = """
    CREATE TABLE Problem (
        Pid INT AUTO_INCREMENT PRIMARY KEY,
        Pname VARCHAR(50) NOT NULL,
        Pscore INT,
        Ptext TEXT,
        Ptag VARCHAR(50),
        Uid INT,
        Cid INT,
        FOREIGN KEY (Uid) REFERENCES User(Uid) ON UPDATE CASCADE ON DELETE SET NULL,
        FOREIGN KEY (Cid) REFERENCES Contest(Cid) ON UPDATE CASCADE ON DELETE SET NULL
    )
    """
    cursor.execute(create_problem_table)

    insert_query = """
    INSERT INTO Problem (Pid, Pname, Pscore, Ptext, Ptag, Uid, Cid)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    data = (1, 'A+B', 100, '给定两个整数A、B，请你给出答案A+B', 'math', 1, 1)
    cursor.execute(insert_query, data)



    # 创建Solve表
    sql = """
        drop table if exists solve;
    """
    cursor.execute(sql)
    create_solve_table = """
    CREATE TABLE Solve (
        Sid INT AUTO_INCREMENT PRIMARY KEY,
        Sresult varchar(20),
        Stime DATETIME,
        Uid INT,
        Pid INT,
        FOREIGN KEY (Uid) REFERENCES User(Uid) ON UPDATE CASCADE ON DELETE SET NULL,
        FOREIGN KEY (Pid) REFERENCES Problem(Pid) ON UPDATE CASCADE ON DELETE SET NULL
    )
    """
    cursor.execute(create_solve_table)

    cursor.execute('INSERT INTO Solve (Uid, Pid, Sresult, Stime) VALUES (%s,%s,%s,%s)',
                   ('001', '001', 'Accepted', datetime.datetime.today()))


    # 创建Participation表
    sql = """
        drop table if exists participation;
    """
    cursor.execute(sql)
    create_participation_table = """
    CREATE TABLE Participation (
        PPid INT AUTO_INCREMENT PRIMARY KEY,
        PPscore INT DEFAULT 0,
        Uid INT,
        Cid INT,
        FOREIGN KEY (Uid) REFERENCES User(Uid) ON UPDATE CASCADE ON DELETE SET NULL,
        FOREIGN KEY (Cid) REFERENCES Contest(Cid) ON UPDATE CASCADE ON DELETE SET NULL
    )
    """
    cursor.execute(create_participation_table)
    cursor.execute('INSERT INTO participation (Uid, cid, PPscore) VALUES (%s,%s,%s)',
                   ('001', '001', 1000))

    """
    connection.commit()
    # 关闭连接
    cursor.close()
    connection.close()
    """
    connection.commit()
    feedback('Init database successfully')


def init_gui():
    pass


def main_board():
    printline()
    printf('< Welcome to Code Manager >')
    printf('tourist', '(T/0)')
    printf('login', '(L/1)')
    printf('register', '(R/2)')
    printf('Exit', '(Q)')
    printf('Useless', '(others)')
    printline()


def login():
    printline('Input your User id:')
    zh = input()

    print_('Input your Password:')
    pwd = input()

    try:
        cursor.execute('SELECT Uname, Upwd FROM User WHERE Uid = %s', (zh,))
        get = cursor.fetchone()
        if get and pwd == get[1]:
            name = get[0]
            print_(f'Welcome: {name}')
            now_info.nowUser = now_info.User(zh, name)
            body.body()
        else:
            feedback('Incorrect username or password')
    except pymysql.Error as e:
        feedback(f"An error occurred: {e}")


def register():
    printline('Now create your account!')
    print_('Input your User id:')
    zh = input()

    print_('Input your User name:')
    name = input()

    print_('Input your Password:')
    pwd = input()

    print_('Confirm your Password:')
    pwd2 = input()

    try:
        cursor.execute('SELECT Uname FROM User WHERE Uid = %s', (zh,))
        get = cursor.fetchone()
        if get:
            feedback('This User id is already exists, please change your User id while do it again.')
        elif pwd != pwd2:
            feedback('Two Password is different, confirm your password while do it again.')
        else:
            cursor.execute('INSERT INTO User (Uid, Uname, Upwd) VALUES (%s,%s,%s)', (zh, name, pwd))
            connection.commit()
            feedback('register successfully')
    except pymysql.Error as e:
        feedback(f"An error occurred: {e}")


def un_register():

    def board():
        printline()
        printf('Your are Tourist, register a account now?')
        printf('Login', '(L/1)')
        printf('Register', '(R/2)')
        printf('Back', '(B/3)')
        printf('Useless', '(others)')

    while True:
        board()
        ch = input()
        if ch == 'L' or ch == '1':
            login()
        elif ch == 'R' or ch == '2':
            register()
            return
        elif ch == 'B' or ch == '3':
            return
        else:
            print_('useless.')


def new_rating():
    # 使用 UPDATE 和子查询来更新 User 表中的 Urating 列
    update_query = """
        UPDATE User U
        SET U.Urating = (
            CASE
                WHEN (
                    SELECT MAX(PPscore) 
                    FROM Participation P 
                    WHERE P.Uid = U.Uid
                ) > U.Urating THEN (
                    SELECT MAX(PPscore) 
                    FROM Participation P 
                    WHERE P.Uid = U.Uid
                )
                ELSE U.Urating
            END
        )
        """
    cursor.execute(update_query)
    connection.commit()


if __name__ == '__main__':
    # init_database()
    new_rating()
    # init_gui()
    while True:
        main_board()
        print_('Input your order:')
        ch = input()
        if ch == '0' or ch == 'T':
            body.body()
        elif ch == '1' or ch == 'L':
            login()
        elif ch == '2' or ch == 'R':
            register()
            pass
        elif ch == 'Q':
            break
        else:
            print_('Useless.')

    connection.commit()
    cursor.close()
    connection.close()
