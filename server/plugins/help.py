from plugins.pluginParser import Plugin

# Plugin info
name = 'help Plugin'
filename = __file__.split('\\')[-1]
priority = 999

# Create plugin object
plugin: Plugin = Plugin(name, filename)


helpHeader = '--- Help ---'


@plugin.event.beforeCommand
def command(event,user,command):
    if command == '/help':
        event.handled = True
        plugin.sendDm(helpHeader,user)

