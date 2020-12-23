# -*- coding: utf-8 -*-
#  @FileName  Client.py
#  @Author    MJH
#  @Email     jiahui.mao@foxmail.com
#  @Version   v1.0
#  @Date      2020/12/14
import json
import socket
import threading

stop_flag = 0


def login(sock, server_ip, server_port):
    choice = input("please login or register\r\n"
                   "login    -- 1\r\n"
                   "register -- 2\r\n")
    print("please input the username and password")
    username = input("username:\r\n")
    password = input("password:\r\n")
    # choice = int(choice)
    if choice == "1":
        message_send_str = {"operate": "login", "username": str(username), "password": str(password)}
        message_send_json = json.dumps(message_send_str)
        sock.sendto(message_send_json.encode(), (server_ip, server_port))
    elif choice == "2":
        message_send_str = {"operate": "register", "username": str(username), "password": str(password)}
        message_send_json = json.dumps(message_send_str)
        sock.sendto(message_send_json.encode(), (server_ip, server_port))
        print("register sent")
    message_recv_str = sock.recvfrom(1024)
    message_recv_json = json.loads(message_recv_str[0].decode())
    if message_recv_json["state"] == "success":
        return username
    else:
        print("username or password is not correct, please retry")
        login(sock, server_ip, server_port)


def send_message_p2p(sock, server_ip, server_port, my_username):
    dest_username = input("please input the destination username:\n")
    while True:  
        content = input()
        if stop_flag:
            break
        print("I say to " + str(dest_username) + ": " + str(content))
        message_send_str = {"operate": "p2p", "my_username": my_username,
                            "dest_username": dest_username, "content": content}
        message_send_json = json.dumps(message_send_str)
        sock.sendto(message_send_json.encode(), (server_ip, server_port))
        if content == "END":
            break
    print("Stop point-to-point communication")
    return True


def send_message_p2g(sock, server_ip, server_port, my_username):
    while True:
        content = input()
        if stop_flag:
            break
        print("I say to all: " + str(content))
        message_send_str = {"operate": "p2g", "my_username": my_username, "content": content}
        message_send_json = json.dumps(message_send_str)
        sock.sendto(message_send_json.encode(), (server_ip, server_port))
        if content == "END":
            break
    print("Stop point-to-group communication")
    return True


def recv_message(sock):
    global stop_flag
    while True:
        message_recv_str = sock.recvfrom(1024)
        message_recv_json = json.loads(message_recv_str[0].decode())
        operate = str(message_recv_json["operate"])
        dest_username = str(message_recv_json["my_username"])
        if str(message_recv_json["content"]) == "END":
            stop_flag = 1
            print("stop communication? ")
        elif operate == "p2p":
            content = str(message_recv_json["content"])
            print(dest_username + " say to me: " + content)
        elif operate == "p2g":
            content = str(message_recv_json["content"])
            print(dest_username + " say to all: " + content)
        else:
            pass


def menu():
    print("please choose the function\r\n"
          "p2p    -- 1\r\n"
          "p2g    -- 2\r\n"
          "exit   -- 3\r\n")
    fun = input("please input the number:\r\n")
    return fun


# def p2p_comm(sock, server_ip, server_port, my_username):
#     dest_username = input("please input the destination username: ")
#     # 创建发送消息线程
#     thread_send = threading.Thread(target=send_message_p2p,
#                                    args=(sock, server_ip, server_port, my_username, dest_username))
#     thread_send.start()
#     return thread_send
#
#
# def p2g_comm(sock, server_ip, server_port, my_username):
#     # 创建发送消息线程
#     thread_send = threading.Thread(target=send_message_p2g, args=(sock, server_ip, server_port, my_username))
#     thread_send.start()
#     return thread_send


def main():
    # 创建socket连接
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # 确定目标IP地址和端口，即服务器IP地址和端口
    server_ip = "6001::1a7"
    server_port = 20000

    my_username = login(sock, server_ip, server_port)
    recv_thread = threading.Thread(target=recv_message, args=(sock,))
    recv_thread.start()
    while True:
        fun = menu()
        # fun = int(fun)
        if fun == "1":
            send_message_p2p(sock, server_ip, server_port, my_username)
        elif fun == "2":
            send_message_p2g(sock, server_ip, server_port, my_username)
        elif fun == "3":
            print("exit client")
            break
        else:
            pass


if __name__ == '__main__':
    main()
