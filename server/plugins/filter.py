from plugins.pluginParser import Plugin, User
import time as t

# Plugin info
name = 'ChatFilter'
filename = __file__.split('\\')[-1]
priority = 999

### Config

# How long is rate limit
DELAY = 0.5

# Create plugin object
plugin: Plugin = Plugin(name, filename)

# Last message times
lastMsg:dict[str,int] = {}

@plugin.event.onServerStart
def onServerStart(event,ip,port):
    global has_perm
    has_perm = plugin.import_var('has_perm')

@plugin.event.beforeMessage
def beforeMessage(event,msg:str,sender:User):
    if has_perm(sender,'filter.bypass'): return
    if not has_perm(sender,'filter.bypass.printable'):
        event.msg = ''.join([i for i in msg if i.isprintable()])
        if not event.msg:
            event.cancel = True
            return
    
    if has_perm(sender,'filter.bypass.spam'):
        return

    if sender.name not in lastMsg:
        lastMsg[sender.name] = t.time()

    if lastMsg[sender.name] + DELAY > t.time():
        event.cancel = True
        plugin.sendMsg('Please slow the fuck down already',sender)
        print('[!] Message was rate-limited.')
        
    lastMsg[sender.name] = t.time()




