from plugins.pluginParser import Plugin, User

# Plugin info
name = 'Bans Plugin'
filename = __file__.split('\\')[-1]
priority = 2

# Create plugin object
plugin: Plugin = Plugin(name, filename)

# People with perms to mute & ban
opList:list[str] = ['Omena0']

# Muted users cannot send messages.
muteList:set[str] = set()

# Banned users cannot connect.
banList:set[str] = set()

@plugin.event.onPluginLoad
def onPluginLoad(event,*_):
    plugin.export_var({"opList":opList})
    plugin.export_var({"muteList":muteList})
    plugin.export_var({"banList":banList})
    
    # Help plugin integration
    helpMsg = plugin.import_var('helpMsg')
    helpMsg = ''
    helpMsg += """
-- Bans Plugin --
- Commands -
 /ban*    - Ban a user
 /unban*  - Unban a user
 /mute*   - Mute a user
 /unmute* - Unmute a user
 * - Admin only
    """.strip().replace('\t','')
    plugin.export_var({'helpMsg':helpMsg})

@plugin.event.beforeMessage
def beforeMessage(event,msg:str,sender:User):
    if sender.name in muteList:
        plugin.sendDmAs('You have been muted.',sender)
        event.cancel = True


@plugin.event.beforeDm
def beforeDm(event,sender:User,recipient:User,msg:str):
    if sender.name in muteList:
        plugin.sendDmAs('You have been muted.',sender)
        event.cancel = True


@plugin.event.beforeCommand
def beforeCommand(event,user,cmd):
    if cmd.startswith("/mute "):
        punished = cmd.split("/mute ")[1]
        plugin.sendDmAs(f'You have been muted by {user.name}.',punished)
        muteList.add(punished)
        
    if cmd.startswith("/unmute "):
        punished = cmd.split("/unmute ")[1]
        plugin.sendDmAs(f'You have been unmuted by {user.name}.',punished)
        muteList.remove(punished)
        
    elif cmd.startswith("/ban "):
        punished = cmd.split("/ban ")[1]
        plugin.sendDmAs(f'You have been banned by {user.name}.',punished)
        banList.add(punished)
        plugin.getCS(punished).close()
    
    elif cmd.startswith("/unban "):
        punished = cmd.split("/unban ")[1]
        plugin.sendDmAs(f'You have been unbanned by {user.name}.',punished)
        banList.remove(punished)
        

@plugin.event.onLogin
def onJoin(event,user,password):
    if user.name in banList:
        plugin.sendDmAs(f'You have been banned by {user.name}.',user)
        event.cancel = True

    if user.name in muteList:
        plugin.sendDmAs(f'You have been muted by {user.name}.',user)

