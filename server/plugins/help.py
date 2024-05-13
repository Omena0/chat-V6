from plugins.pluginParser import Plugin, User
from time import sleep

# Plugin info
name = 'help Plugin'
filename = __file__.split('\\')[-1]
priority = 1

# Create plugin object
plugin: Plugin = Plugin(name, filename)

helpMsg = '--- Help ---\n'

@plugin.event.onPluginLoad
def load(event):
    plugin.export_var({"helpMsg":helpMsg})

@plugin.event.beforeCommand
def command(event,user,command):
    if command == '/help':
        helpMsg = plugin.import_var('helpMsg')
        print(helpMsg)
        for i in helpMsg.splitlines():
            plugin.sendDmAs(i,user)


