from threading import Thread
from hashlib import md5
import requests
import pathlib
import socket
import os
import sys

os.system()

try: os.chdir('client')
except: ...

os.system('cls')

defaultconfig = """
# Configuration file for the ChatV6 client

# !!! DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING !!!

############## Connection configuration ##############

# Fetches the ip from static api
# If this is enabled the ip and port bellow will be ignored.
fetch_ip = True

# Api address
api_addr = "https://omena0.github.io/api/"

# Custom address for the ChatV6 server
# Overridden if `fetch_ip` is true.
ip   = "127.0.0.1"
port = 5000

############## Login configuration ##############

# Whether to send a password during login.
online_mode = True

# Whether to stone the display_name and password (hash) so you dont have to type it every time
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
            if value.lower() == 'true': value = True
            elif value.lower() == 'false': value = False
            else:
                try: value = int(value)
                except: ...

            globals()[key] = value

# Defaults? (in case config doesent have the value)
fetch_ip = True
api_addr = "https://omena0.github.io/api/"
ip   = "127.0.0.1"
port = 5000
online_mode = True
store_credentials = True

# Load
load_config()


try: os.chdir('client')
except: ...

def apiGet(path:str) -> str:
    """Get a string from api

    Args:
        path (str): api path

    Returns:
        str: string from api
    """
    url = api_addr+path
    if not url.startswith('http'): url = f'https://{url}'
    return requests.request('get',url).text

# Address from api
if fetch_ip:
    print('[.] Fetching ip from api...')

    addr = apiGet('chat-v6/ip').split(':')
    print(addr)
    ip   = addr[0]
    port = int(addr[1])

if store_credentials:
    # Read cached display_name, or ask user for one and cache that
    try:
        name,psw = pathlib.Path('cache/credentials.txt').read_text().split('|')
    except Exception:
        name = input('display_name: ')
        psw = md5(input('Password: ').encode()).hexdigest()
        try: os.mkdir('cache')
        except: pass
        with open('cache/credentials.txt','w') as file: file.write(f'{name}|{psw}')

else:
    name = input('display_name: ')
    if online_mode: psw = md5(input('Password: ').encode()).hexdigest()
display_name = name

if name == 'console':
    psw = md5(input('Console Password: ').encode()).hexdigest()


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
    print('[.] Continuing anyways...')
    token = msg

else:
    token = msg
    print('[!] Logged in!')

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
    global display_name, to_set
    msg = msg.strip()
    if msg == '': return
    if msg == 'DONE': return
    msg = msg.split('|')
    
    if msg[0] == 'INVALID': # Invalid
        print('[!] Invalid Token!')
        print(f'[{name}] <{display_name}> ',end='')
    
    elif msg[0] == 'INVALID_PSW': # Invalid password
        print('[!] Invalid Password!')
        print(f'[{name}] <{display_name}> ',end='')

    elif msg[0] == 'UNKNOWN_COMMAND': # Invalid command
        print('[!] Unknown Command!')
        print(f'[{name}] <{display_name}> ',end='')

    elif msg[0] == 'NOT_IMPLEMENTED': # NotImplementedError
        print('[!] Feature Not Implemented!')
        print(f'[{name}] <{display_name}> ',end='')
    
    elif msg[0] == 'RATELIMIT':
        print('[!] Slow down!')

    elif msg[0] == 'SET_NAME':
        display_name = msg[1]

    elif msg[0] == 'DISPLAY':
        if msg[1].startswith(f'[{name}] '): print(f'\r\x1b[1A\r',end='')

        print(f'\r{msg[1]}{" "*50}\n[{name}] <{display_name}> ',end='')



print('[!] All done!\n')
print(f'[SYSTEM] <!> Welcome, {display_name}!')

Thread(target=handler).start()

while True:
    msg = input(f'')
    if msg == '':
        print(f'[{name}] <{display_name}> ',end='')
        continue

    if msg.startswith('/'): # Command Handling
        # Client
        if msg.startswith('/nick'):
            s.send(f'SET_USER|{name}|{token}|{msg.replace("/nick","").strip()}'.encode())
            print(f'[{name}] <{display_name}> ',end='')

        elif msg.startswith('/msg '):
            msg = msg.split(' ')
            s.send(f'SEND_DM|{name}|{token}|{msg[1]}|{' '.join(msg[2:])}'.encode())
            print(f'[{name}] <{display_name}> ',end='')

        elif msg.startswith('/exit'):
            s.send('QUIT'.encode())
            s.close()
            sys.exit()

        # Server
        else:
            s.send(f'SEND_COMMAND|{name}|{token}|{msg}'.encode())

    else:
        msg = msg.removeprefix('\\')
        s.send(f'SEND_MESSAGE|{name}|{token}|{msg}'.encode())
    
    