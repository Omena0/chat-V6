from threading import Thread
from hashlib import md5
import requests
import pathlib
import socket
import os
import sys

defaultconfig = """
# Configuration file for the ChatV6 client

# !!! DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING !!!

############## Connection configuration ##############

# Fetches the ip from static api
# If this is enabled the ip and port bellow will be ignored.
fetch_ip = True

# Api address
api_addr = "omena0.github.io/api/chat-v6/ip"

# Custom address for the ChatV6 server
# Overridden if `fetch_ip` is true.
ip   = "127.0.0.1"
port = 5000

############## Login configuration ##############

# Whether to send a password during login.
online_mode = True

# Whether to stone the username and password (hash) so you dont have to type it every time
store_credentials = True
""".strip()

# Load config
def load_config(file='config.txt'):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(defaultconfig)
            
    with open(file, 'r') as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line.startswith(('#','//')): continue
            if not line: continue
            key,value = line.split('=')
            key,value = key.strip(), value.strip().replace("'",'').replace('"','')
            globals()[key] = value

# Defaults? (in case config doesent have the value)
fetch_ip = True
api_addr = "https://omena0.github.io/api/chat-v6/ip"
ip   = "127.0.0.1"
port = 5000
online_mode = True
store_credentials = True

# Load
load_config()

os.system('cls')

try: os.chdir('client')
except: ...

def apiGet(path:str) -> str:
    """Get a string from api

    Args:
        path (str): api path

    Returns:
        str: string from api
    """
    return requests.request('get',api_addr+path).text

# Address from api
if fetch_ip:
    print('[.] Fetching ip from api...')

    addr = apiGet('chat-v6/ip').split(':')
    addr = ('127.0.0.1',5000)
    print(addr)
    ip   = addr[0]
    port = int(addr[1])

if store_credentials:
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

if not online_mode: psw = '<OFFLINE>'

s.send(f'LOGIN|{name}|{psw}'.encode())
msg = s.recv(2048).decode().strip()
if msg == '': msg = '<NO TOKEN>'

if msg == 'INVALID_PSW':
    print('[!] Invalid Password')
    os.remove('cache/credentials.txt')
    exit(-1)

elif msg == '<NO TOKEN>':
    print('[!] Server did not return a token! Is the server in offline mode?')

else:
    token = msg
    print('[!] Logged in!')

to_set = ''
def handler():
    while True:
        try: msg = s.recv(1024).decode()
        except Exception as e:
            print(f'\n[!] Server Has either crashed, or closed our socket.\n{e}')
            return
        if '\t' not in msg: msg = '\t'+msg
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

while True:
    msg = input(f'')
    if msg == '':
        print(f'[{name}] <{username}> ',end='')
        continue
    if msg.startswith('/'): # Command Handling (clientside)
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
        s.send(f'SEND_MESSAGE|{name}|{token}|{msg}'.encode())
    
    