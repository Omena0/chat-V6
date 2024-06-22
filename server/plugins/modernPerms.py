from plugins.pluginParser import Plugin, User

# Plugin info
name = 'ModernPerms'
filename = __file__.split('\\')[-1]
priority = 5

version = '1.0.0'

helpMsg = """
-- Permissions Plugin --
 - Commands -
  /perm set|view <user> <perm> [<value>] - Manage permissions

"""

# Create plugin object
plugin: Plugin = Plugin(name, filename)

## Permissions
perms:dict[dict] = {}

def update_perm(user,newperms:dict):
    if isinstance(user,str): user = plugin.getUser(user)
    perms[user.name].update(newperms)
    user.perms = perms[user.name]

def has_perm(user,permission:str):
    """Will be None if no permission is set.
        Otherwise bool
    """
    if isinstance(user,str):
        user = plugin.getUser(user)
    
    if user.name not in perms:
        return

    for perm,value in perms[user.name].items():
        if perm == '*': continue
        if perm == permission: return value
        if permission.startswith(perm.removesuffix('*')): return value

    if '*' in perms[user.name]:
        if perms[user.name]['*']: return True
        if permission == '*':
            return False


@plugin.event.onServerStart
def onServerStart(event, ip, port):
    event.startMsg = f'Server started on [{ip}:{port}] - Running modernPerm V{version}'

@plugin.event.onPluginLoad
def onPluginLoad(event):
    plugin.export_var({'update_perm':update_perm})
    plugin.export_var({'has_perm':has_perm})
    plugin.export_var({'perms':perms})

@plugin.event.onLogin
def onLogin(event, user, psw):
    if user.name not in perms.keys():
        perms[user.name] = {}
    else:
        user.perms = perms[user.name]

@plugin.event.beforeCommand
def beforeCommand(event,user,cmd):
    if cmd.startswith('/perm '):
        event.handled = True
        cmd = cmd.split('/perm ')[1]
        if cmd.startswith('set '):
            user_ = cmd.split(' ')[1]
            perm = cmd.split(' ')[2]
            value = cmd.split(' ')[3].lower() == 'true'
            update_perm(user_,{perm:value})
            plugin.sendMsg(f'Updated permissions for {user_}.',user)
    
    
    if cmd == '/help':
        for line in helpMsg.splitlines(): plugin.sendDm(line,user_)

