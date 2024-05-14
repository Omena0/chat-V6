from plugins.pluginParser import Plugin, User
from time import sleep

# Plugin info
name = 'Reload Plugin'
filename = __file__.split('\\')[-1]
priority = 1

# Create plugin object
plugin: Plugin = Plugin(name, filename)

helpMsg = """
-- Reload Plugin --
 - Commands -
  /reload - Reload the server"""

@plugin.event.beforeCommand
def beforeCommand(event,user,cmd):
    if cmd == '/reload':
        plugin.load_plugins()
        plugin.sendDm('Reloading!',user)
        
    if cmd == '/help':
        for line in helpMsg.splitlines(): plugin.sendDm(line,user)

