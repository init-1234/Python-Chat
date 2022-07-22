import socket
from os import system
from time import sleep
from threading import Thread
from datetime import datetime


def clear():
    system("clear")

def banner_console():

    print(f"\033[0;37m[*] Listening on {HOST}:{PORT}")
    print("=========================================================")

# 0.0.0.0 is the localhost
# recommend open a port in your router
HOST = "0.0.0.0"
# select the port
PORT = 63123

sep = "<SEP>"
# modify or add users and password 
users_dic = {"user_1":"password_1", "user_2":"password_2"}
users_list = ["user_1", "user_2"]

conect = []
clients = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind( (HOST, PORT) )
s.listen()


def users():
    
    for client in clients:
        try:
            client.send("c".encode())
            sleep(0.1)
        except:
            pass

    sleep(1)

    for u in users_list:

        if u in conect:
            print(f"\033[0;32m[+] {u} -> Connected\033[0;37m")

        else:
            print(f"\033[0;31m[+] {u} -> Disconnected\033[0;37m")

    for r in conect:
        conect.remove(r)
        
def console():
    clear()
    banner_console()

    while True:

        command = input("Command-> ")

        if command == "send":
            while True:
                message = input("Message to send ('quit' to exit)-> ")

                if message != "quit":

                    message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] |SERVER@HOST|: {message}"

                    for client in clients:
                        try:
                            client.send(message.encode())
                        except:
                            pass
                    print("Message sent suscessful")
                else:
                    break

        elif command == "users":
            users()

        elif command == "clear":
            clear()
            banner_console()

        elif command == "help":
            print("""
Console Commands
-----------------------------------
help - print console commands
clear - clean the screen
users - print connected and disconnected users
send - send message 
""")
        else:
            print(f"\033[0;31mError: Command {command} not found\033[0;37m")

def listener(cl):

    while True:

        g = ""
        try:
            message = cl.recv(1024).decode()
        except:
            continue
        else:
            message = message.replace(sep, ": ")

        if len(message) == 0:
            cl.close()

        message_list = list(message)
        
        try:
            if message_list[0] == "c":
                count1 = 0
                for x in  message_list:
                    if count1 >= 2:
                          g += x
                    else:
                        count1 += 1
                conect.append(g)
        except:
            continue
        
        else:
            for client in clients:
                try:
                    client.send(message.encode())
                except:
                    pass


t2 = Thread(target = console)
t2.daemon = True
t2.start()                    

while True:
    c, a = s.accept()

    try:
        name = c.recv(1024).decode()
    except:
        continue
    
    try:
        passw = c.recv(1024).decode()
    except:
        continue

    sleep(3)
    
    if name in users_dic and users_dic[name] == passw:

        auth = "True"
        c.send(auth.encode())
        clients.add(c)

        t1 = Thread(target = listener, args=(c,))
        t1.daemon = True
        t1.start()
        
    else:

        auth = "False"
        c.send(auth.encode())
        
