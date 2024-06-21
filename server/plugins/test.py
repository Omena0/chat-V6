from plugins.pluginParser import Plugin

# Plugin info
name = 'help Plugin'
filename = __file__.split('\\')[-1]
priority = 1

# Create plugin object
plugin: Plugin = Plugin(name, filename)


@plugin.event.onServerStart
def start(event,ip,port):
    event.startMsg = '[!] Server has been started! [{ip}:{port}] Running TestPlugin'

