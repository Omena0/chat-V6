from plugins.pluginParser import Plugin, User
from time import sleep

# Plugin info
name = 'Ignore Plugin'
filename = __file__.split('\\')[-1]
priority = 10

# Create plugin object
plugin: Plugin = Plugin(name, filename)

# Dictionary to store ignored users per user
ignorelist:dict[str,list] = {}
blocklist:dict[str,list] = {}

@plugin.event.onPluginLoad
def onPluginLoad(event,*_):
    global helpMsg
    # Help plugin integration
    helpMsg = plugin.import_var('helpMsg')
    helpMsg += """
    -- Ignore Plugin --
     - Commands -
     /ignore     - Ignore a user  (t)
     /block      - Block a user   (t)
     (t) = Toggle
    """.strip().replace('\t','')
    plugin.export_var({'helpMsg':helpMsg})

@plugin.event.beforeMessage
def beforeMessage(event,msg:str,sender:User):
    event.cancel = True
    print(f'[{sender.name}] <{sender.username}> {msg}')
    for user in plugin.getUsers():
        
        if sender.name in ignorelist[user]:
            msg = '[You have ignored this user]'
        if user.name in blocklist[sender]:
            msg = '[This user has blocked you]'
        plugin.sendMessageAs(msg,recipient=user,user=sender)


@plugin.event.beforeDm
def beforeDm(event,sender:User,recipient:User,msg:str):
    if sender.name in ignorelist[recipient]:
        plugin.sendDmAs(f'{recipient} Has ignored you.',sender)
        event.cancel = True
    if sender.name in blocklist[recipient]:
        plugin.sendDmAs(f'{recipient} Has blocked you.',sender)
        event.cancel = True


@plugin.event.beforeCommand
def beforeCommand(event,user,cmd):
    if cmd.startswith("/ignore "):
        ignored = cmd.split("/ignore ")[1]
        if ignored not in ignorelist[user]:
            ignorelist[user].append(ignored)
            plugin.sendDmAs(f'You will no longer see messages from {ignored}.',user)
        else:
            ignorelist[user].remove(ignored)
            plugin.sendDmAs(f'You will now see messages from {ignored}',user)
            
    if cmd.startswith("/block "):
        blocked = cmd.split("/block ")[1]
        if blocked not in blocklist[user]:
            blocklist[user].append(blocked)
            plugin.sendDmAs(f'{blocked} Can no longer see your messages.',user)
        else:
            blocklist[user].remove(blocked)
            plugin.sendDmAs(f'{blocked} Can now see your messages again.',user)

@plugin.event.onJoin
def onJoin(event,user):
    if user not in ignorelist.keys():
        ignorelist[user] = []
    if user not in blocklist.keys():
        blocklist[user] = []


