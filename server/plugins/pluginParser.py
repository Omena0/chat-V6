"""Module that parses plugins for various applications."""

import importlib
import os
import socket
from random import randrange
from hashlib import md5
from types import ModuleType

try: os.chdir('server')
except: ...

# Had to do this shit for type hints
class User:
    def __init__(self, display_name, psw, cs):
        self.name:str         = display_name         # Unique Identifier
        self.display_name:str     = self.name    # Customisable display display_name
        self.password:str     = psw          # Hashed password
        self.token:str        = self.genToken()
        self.cs:socket.socket = cs

    def genToken(self):
        return md5(f'{self.name}|{self.display_name}|{randrange(-32767,32767)}'.encode()).hexdigest()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

class Dummy: ...

class Plugin:
    def __init__(self,display_name,filename):
        self.name = display_name
        self.filename = filename
        
        # Methods (set by server)
        self.sendMsg = None
        self.sendDm = None
        self.brodcast = None
        self.load_plugins = None
        
        # Import & export
        self.export_var = None
        self.import_var = None
        
        # Get-Methods (set by server)
        self.getUser = None
        self.getUsers = None
        self.getIp = None
        self.getCS = None
        self.getHost = None
        self.getPlugins = None
        
        # Events (defined per plugin)
        self.event = Event()
    


        

class EventReturn:
    def __init__( # Dont mind this mess LMAO
            self,
            plugin:Plugin,
            cancel:bool          = False,
            valid:bool           = False,
            joinMsg:str          = None,
            newname:str          = None,
            broadcast:str        = None,
            broadcastMessage:str = None,
            msg:str              = None,
            name:str             = None,
            display_name:str     = None,
            recipient:str        = None,
            leaveMsg:str         = None,
            startMsg:str         = None,
            silent:bool          = False,
            handled:bool         = False
        ):
        
        self.plugin = plugin
        
        # All returns from various events
        self.cancel:bool          = cancel
        self.valid:bool           = valid
        self.joinMsg:str          = joinMsg
        self.newname:str          = newname
        self.broadcast:str        = broadcast
        self.broadcastMessage:str = broadcastMessage
        self.msg:str              = msg
        self.display_name:str     = name
        self.name:str             = display_name
        self.recipient:str        = recipient
        self.leaveMsg:str         = leaveMsg
        self.startMsg:str         = startMsg
        self.silent:bool          = silent
        self.handled              = handled

class Event:
    def __init__(self): ...
    def beforeMessage(self,func,*args,**__): # Theese docstrings r a life saver FR
        """BeforeMessageEvent
        
        Params: msg:str, user:User
        Return: cancel:bool, msg:str, name:str, display_name:str
        """
        if not args:
            self.beforeMessage = func
    def beforeDm(self,func,*args,**__):
        """BeforeDmEvent
        
        Params: sender:User, recipient:User, msg:str
        Return: cancel:bool, recipient:str|User, msg:str, name:str, display_name:str
        """
        if not args:
            self.beforeDm = func
    def beforeNick(self,func,*args,**__):
        """BeforeNickEvent
        
        Params: olddisplay_name, newdisplay_name
        Return: cancel, newdisplay_name, broadcastMsg
        """
        if not args:
            self.beforeNick = func
    def beforeCommand(self,func,*args,**__):
        """BeforeCommandEvent
        
        Params: user, command
        Return: handled
        """
        if not args:
            self.beforeCommand = func
    def onLogin(self,func,*args,**__):
        """OnLoginEvent
        
        Params: user, password
        Return: cancel
        """
        if not args:
            self.onLogin = func
    def onLeave(self,func,*args,**__):
        """OnLeaveEvent
        
        Params: user
        Return: silent, leaveMsg
        """
        if not args:
            self.onLeave = func
    def onServerStart(self,func,*args,**__):
        """OnServerStartEvent
        
        Params: ip, port
        Return: startMsg
        """
        if not args:
            self.onServerStart = func
    def onPluginLoad(self,func,*args,**__):
        """OnPluginLoadEvent
        
        When this is called you can use plugin methods
        
        Params: None
        Return: None
        """
        if not args:
            self.onPluginLoad = func



def loadPlugin(name) -> ModuleType:
    """Loads a plugin"""
    try:
        name = name.replace('.py','')
        plugin:ModuleType = importlib.import_module(f'plugins.{name}')
        
        print(f'[.] Loaded plugin "{plugin.name}"')
        return plugin

    except Exception as e:
        print(f'[!] [{name}] Failed to load plugin. {f'[{e}]'.replace('module','plugin') if debug else ''}')
        if debug: raise e

debug = True

if __name__ == '__main__':
    loadPlugin('testPlugin')
