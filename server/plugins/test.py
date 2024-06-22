from plugins.pluginParser import Plugin, User

# Plugin info
name = 'Test'
filename = __file__.split('\\')[-1]
priority = 1

# Create plugin object
plugin: Plugin = Plugin(name, filename)

@plugin.event.onServerStart
def onServerStart(event,ip,port):
    global update
    update = plugin.import_var('update_perm')
    has_perm = plugin.import_var('has_perm')
    update('test',{"hello":True})
    print(has_perm('test','hello'))








