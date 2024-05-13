import socket
from threading import Thread
from random import randrange
from hashlib import md5
import time as t
import os
import plugins.pluginParser as pluginParser
from types import ModuleType
from contextlib import suppress

try: os.chdir('server')
except: ...

ip   = '127.0.0.1'
port = 5000

debug = True

client_sockets:set[socket.socket] = set()

print('[.] Initializing...')

class User:
    def __init__(self, name, psw, cs):
        self.name:str         = name         # Unique Identifier
        self.username:str     = self.name    # Customisable display name
        self.password:str     = psw          # Hashed password
        self.token:str        = self.genToken()
        self.cs:socket.socket = cs
        users.add(self)

    def genToken(self):
        return md5(f'{self.name}|{self.username}|{randrange(-32767,32767)}'.encode()).hexdigest()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
    
users:set[User] = set()

def findUser(name) -> User:
    if isinstance(name,User): return name in users
    with suppress(IndexError): return [user for user in users if user.name == name][0]

def broadcast(msg:str, username='SYSTEM', name='SYSTEM') -> None:
    print(f'[{name}] <{username}> {msg}')
    for cs in client_sockets:
        with suppress(Exception): cs.send(f'\t[{name}] <{username}> {msg}'.encode())

def sendMsgAs(msg:str,recipient:str|User,user:str|User=None,username:str=None, name:str=None):
    """Sends a chat message that is only seen by the recipient unlike sendDmAs()

    Args:
        msg (str): _description_
        recipient (str | User): _description_
        user (str | User, optional): _description_. Defaults to None.
        username (str, optional): _description_. Defaults to None.
        name (str, optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_
    """
    if not findUser(recipient): return
    if user is None and (username is None or name is None):
        username = 'SYSTEM'
        name = 'SYSTEM'
    if isinstance(user,str): user = findUser(user)
    if isinstance(recipient,str): recipient = findUser(recipient)
    if username is None: username = user.username
    if name is None: name = user.name
    
    user.cs.send(f'\t[{name}] <{username}> {msg}'.encode())

def sendDmAs(msg:str, recipient:str|User,user:str|User=None, username='SYSTEM', name='SYSTEM'):
    """Sends a private message to someone.

    Args:
        msg (str): Message to send.
        recipient (str | User): The recipient of the DM.
        user (str | User, optional): The user to send as. Defaults to System.
        username (str, optional): The username to send as. Defaults to 'SYSTEM'.
        name (str, optional): The name to send as. Defaults to 'SYSTEM'.

    Raises:
        ValueError: _description_
    """
    if not findUser(recipient): return None
    if user is None and (username is None or name is None):
        username = 'SYSTEM'
        name = 'SYSTEM'
    if isinstance(user, str): user = findUser(user)
    if isinstance(recipient,str): recipient = findUser(recipient)
    if username is None: username = user.username
    if name is None: name = user.name
    if not recipient: return
    recipient.cs.send(f'\tPRIVATE [{name}] <{username}> {msg}'.encode())
    print(f'PRIVATE [{name} -> {recipient.name}]: {msg}')

def getIp(user:str): return findUser(user).cs.getpeername()

def getCs(user:str): return findUser(user).cs

def getHost(): return ip, port

def getUsers(): return users

def export_var(g):
    globals().update(g)
    
def import_var(var:str):
    return globals()[var]

def sortPlugins(_plugins) -> dict[int, ModuleType]:
    """Sort plugins into a dict based on priority

    Returns:
        dict[int, ModuleType]: Return dict where priority: module
    """
    sorted_ = []
    for plugin in _plugins:
        sorted_.insert(plugin.priority,plugin)
    return sorted_

def getPlugins() -> dict[int, ModuleType]: return plugins

def handleEvent(event, *args, **kwargs):
    global plugins
    for plugin in plugins:
        with suppress(Exception) as e:
            plugin:pluginParser.Plugin = plugin.plugin
            callback = getattr(plugin.event,event,None)

            event_return = pluginParser.EventReturn(plugin)
            callback(event_return,*args,**kwargs)
            for i in ["cancel","valid","joinMsg","newUsername","broadcast","broadcastMessage","msg","username","name","recipient","leaveMsg","startMsg","silent","reason","time"]:
                if getattr(event_return,i):
                    return event_return



def load_plugins():
    global plugins
    print('[!] Loading Plugins...')
    plugins = []
    pluginParser.location = 'plugins'
    for plugin in os.listdir(pluginParser.location):
        if not plugin.endswith('py'): continue
        if plugin.startswith('_'): continue
        if plugin == 'pluginParser.py': continue
        plugin:ModuleType = pluginParser.loadPlugin(plugin)
        if plugin is None:
            print('[!] Plugin failed to load!')
            continue
        plugins.append(plugin)
        # Methods
        plugin:pluginParser.Plugin = plugin.plugin
        plugin.sendMessageAs = sendMsgAs
        plugin.sendDmAs = sendDmAs
        plugin.sendBroadcast = broadcast
        plugin.load_plugins = load_plugins

        # Import & export
        plugin.export_var = export_var
        plugin.import_var = import_var

        # Get-Methods
        plugin.getUser = findUser
        plugin.getUsers = getUsers
        plugin.getIp = getIp
        plugin.getCS = getCs
        plugin.getHost = getHost
        plugin.getPlugins = getPlugins

    # Reverse plugins, so that plugins loaded first will maintain priority over ones that come later.
    # Assuming that all plugins have the same priority of course
    plugins = list(reversed(sortPlugins(plugins)))
    handleEvent('onPluginLoad')

load_plugins()

def csHandler(cs:socket.socket, addr:tuple):
    user = None
    while True:
        try:
            msg = cs.recv(2048).decode().split('|')
            if not msg: raise Exception('Recieved nothing')
            print(msg)
            
            if msg[0] == 'LOGIN':
                if findUser(msg[1]) is None:
                    print(f'[.] Creating new account: {msg[1]} [{addr[1]}]')
                    User(msg[1],msg[2],cs)
                user = findUser(msg[1])
                valid = user.password == msg[2]
                
                if not valid:
                    cs.send('\tINVALID_PSW'.encode())
                    print('INVALID')
                    return
                
                else:
                    user.token = user.genToken()
                    user.cs = cs
                        
                    cs.send(user.token.encode())

                    a:pluginParser.EventReturn = handleEvent('onLogin', user, [], msg[2])
                    if a and a.cancel:
                        client_sockets.remove(cs)
                        with suppress(Exception): cs.close()
                        return
                    
                    a:pluginParser.EventReturn = handleEvent('onJoin', user)
                    if a and a.cancel:
                        client_sockets.remove(cs)
                        with suppress(Exception): cs.close()
                        return
                    if a is None:
                        broadcast(f'{user.name} Logged in.', username='+')
                    elif not a.silent:
                        broadcast(a.joinMsg,username='+')
                continue

            user = findUser(msg[1])
            token = msg[2]

            if user.token != token:
                cs.send('\tINVALID'.encode())
                continue

            # If request = DONE, dont process any further.
            if msg[0] == 'DONE': continue

            elif msg[0] == 'SET_USER':
                a:pluginParser.EventReturn = handleEvent('beforeNick', user.username, msg[3])
                if a is not None:
                    if a.cancel:
                        cs.send(f'\t{user.username}'.encode())
                        continue
                    cs.send(f'\t{a.newName}'.encode())
                    if a.broadcast: broadcast(f'{a.broadcastMessage}', username='!')
                    user.username = a.newName
                else:
                    cs.send(f'\t{msg[3]}'.encode())
                    broadcast(f'{user.name} Changed their name. {user.username} -> {msg[3]}', username='!')
                    user.username = msg[3]
                continue

            elif msg[0] == 'SEND_MESSAGE':
                if msg[3] == '': continue # Drop empty messages (no point including them)
                a:pluginParser.EventReturn = handleEvent('beforeMessage', msg[3], user)
                if a is None:
                    broadcast(msg[3], username=user.username, name=user.name)
                elif a.cancel: continue
                else:
                    broadcast(a.msg, username=a.username, name=a.name)
                continue

            elif msg[0] == 'SEND_COMMAND':
                handleEvent('beforeCommand', user, msg[3]) # command event doesn't return anything so no point storing it

            elif msg[0] == 'SEND_DM':
                if not findUser(msg[3]):
                    sendDmAs(f'User does not exist. [{msg[3]}]',user)
                    continue
                a:pluginParser.EventReturn = handleEvent('beforeDm', user, findUser(msg[3]), msg[4])
                if a is None:
                    sendDmAs(msg[4], msg[3], username=user.username, name=user.name)
                elif a.cancel == True: continue
                else:
                    sendDmAs(a.msg, a.recipient, username=a.username, name=a.name)
        except Exception as e:
            if debug:
                print(e)
            try:client_sockets.remove(cs)
            except: ...
            cs.close()
            try:
                a:pluginParser.EventReturn = handleEvent('onLeave', user)
                if a is None and user is not None:
                    broadcast(f'[{user.name}] {user.username} Left. [{str(e).split("]")[0].replace("[","")}]', username='-')
                elif a is not None and not a.silent:
                    broadcast(a.leaveMsg, username='-')
                return
            except Exception as e:
                if debug: raise e
                return


print('[.] Setting up socket..')
s = socket.socket()
s.bind((ip, port))
s.listen(5)

a:pluginParser.EventReturn = handleEvent('onServerStart', ip, port)
if a is None: print(f'[!] Server started [{ip}:{port}]')
else: print(a.startMsg)

while True:
    cs, addr = s.accept()
    client_sockets.add(cs)
    print(f'[+] {addr[0]}:{addr[1]}')
    Thread(target=csHandler, args=[cs, addr]).start()
