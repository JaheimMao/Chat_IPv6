# -*- coding: utf-8 -*-
#  @FileName  Server.py
#  @Author    MJH
#  @Email     jiahui.mao@foxmail.com
#  @Version   v1.0
#  @Date      2020/12/14

import json
import socket
import sqlite3
import string


# 等待设备连接，在设备连接后，获取设备的IPv6地址和端口号，并作存储
def start_server(sock):
    print("start server")
    while True:
        data = sock.recvfrom(1024)
        print(data)
        message = json.loads(data[0].decode())
        ip = data[1][0]
        port = data[1][1]
        if message["operate"] == "login":
            print("login was called")
            state = User().login_check(message["username"], message["password"], ip, port)
            if state:
                sock.sendto(json.dumps({"operate": "login", "state": "success"}).encode(), (ip, port))
            else:
                sock.sendto(json.dumps({"operate": "login", "state": "fail"}).encode(), (ip, port))
        elif message["operate"] == "register":
            print("register was called")
            state = User().register(message["username"], message["password"], ip, port)
            if state:
                sock.sendto(json.dumps({"operate": "register", "state": "success"}).encode(), (ip, port))
        elif message["operate"] == "p2p":
            print("p2p was called")
            row = User().search_username(message["dest_username"])
            dest_ip = row[3]
            dest_port = row[4]
            if row[2] == 1:
                sock.sendto(json.dumps(message).encode(), (dest_ip, dest_port))
                print("send success")
            else:
                sock.sendto("user is not online or exits", (ip, port))
                print("error, send success")
        elif message["operate"] == "p2g":
            print("p2g was called")
            for row in User().select_all():
                if row[0] != message["my_username"] and row[2]:
                    sock.sendto(json.dumps(message).encode(), (row[3], row[4]))


class User:
    def __init__(self):
        self.connect = sqlite3.connect('user.db')
        print("Opened the database successfully")
        # cursor = self.connect.cursor()

    #  try:
    #      sql = '''CREATE TABLE USER_TABLE
    # (USERNAME           TEXT    NOT NULL,
    #  PASSWORD           TEXT    NOT NULL,
    #  STATE              INT     NOT NULL,
    #  IP                 TEXT    NOT NULL,
    #  PORT               INT     NOT NULL);'''
    #      cursor.execute(sql)
    #  except sqlite3.IntegrityError:
    #      self.connect.rollback()
    #      raise ValueError("The table already exists")
    #  self.connect.commit()

    def select_all(self):
        cursor = self.connect.cursor()
        sql = "SELECT * FROM USER_TABLE"
        row = cursor.execute(sql)
        return row

    def register(self, username, password, ip, port):
        cursor = self.connect.cursor()
        try:
            sql = "INSERT INTO USER_TABLE (USERNAME,PASSWORD,STATE, IP, PORT) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql, (username, password, 0, ip, port))
        except sqlite3.IntegrityError:
            self.connect.rollback()
            raise ValueError("The user name already exists")
        self.connect.commit()
        print("Registration success")
        cursor.close()
        return True

    def search_username(self, username):
        cursor = self.connect.cursor()
        sql = "SELECT USERNAME, PASSWORD, STATE, IP, PORT FROM USER_TABLE WHERE USERNAME = (?)"
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        print(row)
        cursor.close()
        return row

    def login_success(self, username, ip, port):
        cursor = self.connect.cursor()
        sql = "UPDATE USER_TABLE set STATE = 1 where USERNAME = (?)"
        cursor.execute(sql, (username,))
        self.connect.commit()
        sql = "UPDATE USER_TABLE set IP = (?) where USERNAME = (?)"
        cursor.execute(sql, (ip, username,))
        self.connect.commit()
        sql = "UPDATE USER_TABLE set PORT = (?) where USERNAME = (?)"
        cursor.execute(sql, (port, username,))
        self.connect.commit()
        print(self.search_username(username))

    def login_check(self, username, password, ip, port):
        row = self.search_username(username)
        if row == None:
            print("the user is not exist")
            return False
        if password != row[1]:
            print("password is not correct")
            return False
        print(row)
        self.login_success(username, ip, port)
        return True

    def logout_success(self, username):
        cursor = self.connect.cursor()
        sql = "UPDATE USER_TABLE set STATE = 0 where USERNAME = (?)"
        cursor.execute(sql, (username,))
        self.connect.commit()

    def db_close(self):
        self.connect.close()


def main():
    # 建立Socket连接
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    # 绑定端口号
    sock.bind(("6001::1a7", 20000))
    print("sock setup success")
    # sock.bind(("", 20000))
    start_server(sock)


if __name__ == '__main__':
    user = User()
    main()
