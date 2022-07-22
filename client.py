import socket
from time import sleep
from os import system
from random import choice
from threading import Thread
from datetime import datetime


def clear():
    system("clear")


clear()    

colores = ["\033[;33m", "\033[;34m", "\033[;35m", "\033[;36m","\033[;37m", "\033[2;37m"]

color = choice(colores)

# write ip and port of server
HOST = "IP SERVER"
PORT = 63123

separator_token = "<SEP>"
auto_desconectar = [True]
nombre = ""
contra = ""
auth = "\033[;33mWaiting...\033[;37m"

banner_log1 = """
 ______________________________________________________________________________
|                                                                              |
|                                Security chat                                 |
|______________________________________________________________________________|
                                                                              
                                                                              
"""
banner_log2 = f"""
 ______________________________________________________________________________
|                                                                              |
|    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                                       |
|______________________________________________________________________________|"""


def timeout():
    v = "k"
    sleep(90)
    if auto_desconectar[0] == True:
        
        clear()
        print("automatically disconnected")
        s.close()
        s.send(v.encode())
        clear()

t2 = Thread(target=timeout)
t2.daemon = True
t2.start()

while True:
    op = input("Do you want to see your password(s/n): ")

    if op.lower() == "s":
        visi = "\033[0;37m"
        break

    elif op.lower() == "n":
        visi = "\033[8;37m"
        break

    else:
        print("Error: option incorrect")

clear()

t2 = Thread(target=timeout)
t2.daemon = True
t2.start()

s = socket.socket()

s.connect((HOST, PORT))

print(banner_log1)
nombre = input("\n                  User Name: ")
s.send(nombre.encode())
clear()
print(banner_log1)
print(f"\n                  User Name:        [{nombre}]")

contra = input(f"                  Password: {visi}")
print("\033[0;37m", end = "")
s.send(contra.encode())
clear()
print(banner_log1)
print(f"""
                  User Name:        [{nombre}]                               
                                                                              
                  Password:         [{visi}{contra}\033[0;37m]           
                                                                              
                                                                              
                                                                              
                                    [{auth}]""")
print(banner_log2)

var = s.recv(1024).decode()
auto_desconectar = [False]

if var == "False":
    clear()
    auth = "\033[0;31mDenied\033[0;37m"
    print(banner_log1)
    print(f"""
                  User Name:        [{nombre}]                               
                                                                              
                  Password:         [{visi}{contra}\033[0;37m]                
                                                                              
                                                                              
                                                                              
                                    [{auth}]""")
    print(banner_log2)
    input("\nPress ENTER to exit")
    exit()

else:
    clear()
    auth = "\033[0;32mSuscess\033[0;37m"
    print(banner_log1)
    print(f"""
                  User Name:        [{nombre}]                               
                                                                              
                  Password:         [{visi}{contra}\033[0;37m]              
                                                                              
                                                                              
                                                                              
                                    [{auth}]""")
    print(banner_log2)
    input("\nPress ENTER to connect")
    clear()
    n = f"\033[0;32m[+] User connected-> {nombre}\033[0;37m"
    s.send(n.encode())

def escucha_mensajes():
    while True:
        msg = s.recv(1024).decode()
        if len(msg) == 0:
            n = f"\033[0;31m[-] User disconnected-> {nombre}\033[0;37m"
            s.send(n.encode())
            clear()
            print("Ha ocurrido un error")
            break

        elif msg == "c":
            c = f"c-{nombre}"
            s.send(c.encode())
            
        else:
            print("\n" + msg)
    exit()

t = Thread(target=escucha_mensajes)

t.daemon = True

t.start()

while True:
    
    enviar =  input()
    
    if enviar.lower() == "exit":
        n = f"\033[0;31m[-] User disconnected-> {nombre}\033[0;37m"
        s.send(n.encode())
        clear()
        print("Has salido del chat")
        break

    elif enviar.lower() == "clear":
        clear()
    
    elif enviar.lower() == "color":
        color = choice(colores)
        print(f"{color}Color changed suscessfully\033[0;37")

    else:    
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        enviar = f"{color}[{date_now}] |{nombre}|{separator_token}{enviar}\033[0;37m"
    
        s.send(enviar.encode())

s.close()
