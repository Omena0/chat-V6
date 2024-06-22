from plugins.pluginParser import Plugin, User

# Plugin info
name = 'Ignore Plugin'
filename = __file__.split('\\')[-1]
priority = 10

# Create plugin object
plugin: Plugin = Plugin(name, filename)

# Dictionary to store ignored users per user
ignorelist:dict[str,list] = {}
blocklist:dict[str,list] = {}

helpMsg = """
-- Ignore Plugin --
 - Commands -
  /ignore     - Ignore a user  (t)
  /block      - Block a user   (t)
 (t) = Toggle"""

@plugin.event.beforeMessage
def beforeMessage(event,msg:str,sender:User):
    event.cancel = True
    print(f'[{sender.name}] <{sender.display_name}> {msg}')
    for user in plugin.getUsers():
        
        if sender.name in ignorelist[user]:
            msg = '[You have ignored this user]'
        if user.name in blocklist[sender]:
            msg = '[This user has blocked you]'
        plugin.sendMsg(msg,recipient=user,user=sender)


@plugin.event.beforeDm
def beforeDm(event,sender:User,recipient:User,msg:str):
    if sender.name in ignorelist[recipient]:
        plugin.sendMsg(f'{recipient} Has ignored you.',sender)
        event.cancel = True
    if sender.name in blocklist[recipient]:
        plugin.sendMsg(f'{recipient} Has blocked you.',sender)
        event.cancel = True


@plugin.event.beforeCommand
def beforeCommand(event,user,cmd):
    if cmd.startswith("/ignore "):
        event.handled = True
        ignored = cmd.split("/ignore ")[1]
        if ignored not in ignorelist[user]:
            ignorelist[user].append(ignored)
            plugin.sendMsg(f'You will no longer see messages from {ignored}.',user)
        else:
            ignorelist[user].remove(ignored)
            plugin.sendMsg(f'You will now see messages from {ignored}',user)
            
    if cmd.startswith("/block "):
        event.handled = True
        blocked = cmd.split("/block ")[1]
        if blocked not in blocklist[user]:
            blocklist[user].append(blocked)
            plugin.sendMsg(f'{blocked} Can no longer see your messages.',user)
        else:
            blocklist[user].remove(blocked)
            plugin.sendMsg(f'{blocked} Can now see your messages again.',user)
        
    if cmd == '/help':
        event.handled = True
        for line in helpMsg.splitlines(): plugin.sendDm(line,user)


@plugin.event.onLogin
def onLogin(event,user,password):
    if user not in ignorelist.keys():
        ignorelist[user] = []

    if user not in blocklist.keys():
        blocklist[user] = []


