from threading import Thread
from hashlib import md5
import requests
import socket
import os
import sys

os.system('cls')

try: os.chdir('client')
except: ...

API_URL = 'https://omena0.github.io/api/'

def apiGet(path:str) -> str:
    """Get a string from api

    Args:
        path (str): api path

    Returns:
        str: string from api
    """
    return requests.request('get',API_URL+path).text

# Address from api
import pathlib
print('[.] Fetching ip from api...')

addr = apiGet('chat-v6/ip').split(':')
addr = ('127.0.0.1',5000)
print(addr)
ip   = addr[0]
port = int(addr[1])

# Read cached username, or ask user for one and cache that
try:
    name,psw = pathlib.Path('cache/credentials.txt').read_text().split('|')
except Exception:
    name = input('Username: ')
    psw = md5(input('Password: ').encode()).hexdigest()
    try: os.mkdir('cache')
    except: pass
    with open('cache/credentials.txt','w') as file: file.write(f'{name}|{psw}')
username = name

# Connect
print(f'[.] Connecting to {ip}:{port}')

s = socket.socket()
try: s.connect((ip,port))
except ConnectionRefusedError:
    print('[!] Could not connect!')
    exit(0)

# Login
print('[.] Logging in...')

s.send(f'LOGIN|{name}|{psw}'.encode())
msg = s.recv(2048).decode().strip()
if msg == '': msg = '<NO TOKEN>'
print(msg)
if msg == 'INVALID_PSW':
    print('[!] Invalid Password')
    os.remove('cache/username.txt')
    raise SystemExit()
else:
    token = msg
    print('[!] Logged in!')

to_set = ''
def handler():
    while True:
        try: msg = s.recv(1024).decode()
        except Exception as e:
            print(f'\nServer Has either crashed, or closed our socket.\n{e}')
            return
        for i in msg.split('\t'):
            handlePacket(i)

def handlePacket(msg):
    global username, to_set
    msg = msg.strip()
    if msg == '': return
    if msg == 'DONE': return

    if msg == 'INVALID': # Invalid
        print('[!] Invalid Token!')
        print(f'[{name}] <{username}> ',end='')
    
    elif msg == 'INVALID_PSW': # Invalid password
        print('[!] Invalid Password!')
        print(f'[{name}] <{username}> ',end='')

    elif msg == 'UNKNOWN_COMMAND': # Invalid command
        print('[!] Unknown Command!')
        print(f'[{name}] <{username}> ',end='')

    elif msg == 'NOT_IMPLEMENTED': # NotImplementedError
        print('[!] Feature Not Implemented!')
        print(f'[{name}] <{username}> ',end='')

    elif to_set == 'username':
        username = msg
        to_set = ''
    else:
        if msg.startswith(f'[{name}] '): print(f'\r\x1b[1A\r',end='')
        
        print(f'\r{msg}{" "*50}\n[{name}] <{username}> ',end='')
        

Thread(target=handler).start()

print('[!] All done!')

print(f'Welcome, {username}')

#print(f'[{name}] <{username}> ',end='')
while True:
    msg = input(f'')
    if msg == '':
        print(f'[{name}] <{username}> ',end='')
        continue
    if msg.startswith('/'): # Command Handling
        # Client
        if msg.startswith('/nick'):
            s.send(f'SET_USER|{name}|{token}|{msg.replace("/nick","").strip()}'.encode())
            to_set = 'username'
            
        elif msg.startswith('/msg '):
            msg = msg.split(' ')
            s.send(f'SEND_DM|{name}|{token}|{msg[1]}|{' '.join(msg[2:])}'.encode())
            
        elif msg.startswith('/exit'):
            s.close()
            sys.exit()
        # Server
        else:
            s.send(f'SEND_COMMAND|{name}|{token}|{msg}'.encode())
    else:
        #print(f'SEND_MESSAGE|{name}|{token}|{msg}')
        s.send(f'SEND_MESSAGE|{name}|{token}|{msg}'.encode())
    
    