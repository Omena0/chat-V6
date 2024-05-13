from plugins.pluginParser import Plugin, User
from time import sleep

# Plugin info
name = 'help Plugin'
filename = __file__.split('\\')[-1]
priority = 10

# Create plugin object
plugin: Plugin = Plugin(name, filename)

# IMPORTANT!!!
# THIS ONLY WORKS WHEN THE LAST LOADED PLUGIN HAS THE LOWEST PRIORITY!!!

helpMsg = '--- Help ---\n'

@plugin.event.onPluginLoad
def load(event):
    plugin.export_var({"helpMsg":helpMsg})

@plugin.event.beforeCommand
def command(event,user,command):
    if command == '/help':
        helpMsg = plugin.import_var('helpMsg')
        print(helpMsg)
        for line in helpMsg.split('\n'):
            plugin.sendDmAs(line,user)
            sleep(0.05)


