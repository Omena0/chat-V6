
# Plugins

This markdown file should provide you with enought information to make your first plugin! I suggest you skim all the docs and go read [The Tutorial](#plugin-tutorial) first and read all the links as they are mentioned.

Reading the [Protocol Docs](PROTOCOL.md#protocol) and source code might help the curious understand how all of this is implemented.

## The Plugin Object

### Methods

Theese arent defined untill the `onPluginLoad` event has been called.
<br><u>**ONLY** USE THEM AFTER the `onPluginLoad` event!</u>

##### Sry for the bad docs btw, i cant document all of them XD

<details open>
<summary>Click to contract</summary>

    sendMessage
    sendBroadcast

    export_var
    import_var

    getUser
    getUsers
    getIp
    getCS
    getHost
    getPlugins
</details>

---

### Events

Events are defined in plugins using the `@events` decorator.

#### BeforeEvents

BeforeEvents happen before the event happens and can be cancelled.

<details open>
<summary>Click to contract</summary>

    beforeMessage
    beforeDm
    beforeNick
    beforeCommand
</details>

#### AfterEvents

AfterEvent run after the event already happenned and cannot be cancelled.

<details open>
<summary>Click to contract</summary>

    onJoin
    onLeave
    onLogin
    onServerStart
    onPluginLoad
</details>

All event decorators specify what arguments will be passed to the function and what can be returned.

---

## EventReturn Object

The `eventReturn` object contains data returned from events.

### Properties

<details open>
<summary>Click to contract</summary>

    plugin (set on creation)

    cancel
    valid
    joinMsg
    newUsername
    broadcast
    broadcastMessage
    msg
    username
    name
    recipient
    leaveMsg
    startMsg
    silent
</details>

---

## Plugin Tutorial

First we need to import Plugin from plugins.pluginParser

```python
from plugins.pluginParser import Plugin
```

Then we need to set up basic information about the plugin

```python
# Plugin info
name = 'Test Plugin 1'
filename = __file__.split('\\')[-1] # BOILERPLATE; DO NOT CHANGE
priority = 1
```

This will be used by the server to identify the plugin and determine what plugin should override others. Increase priority if other plugins are overriding your events and you'd rather keep your events than theirs.
<br><br>
Then we will create the plugin object that handles communication between the plugin and the server. (all events are called but the eventReturn is always the one with the highest priority)

```python
# Create plugin object
plugin:Plugin = Plugin(name,filename)
```

The plugin object is used to control the server in different ways. After the `onPluginLoad` event has been called, we can use the methods that the Plugin object provides. [[Methods]](#methods)
<br><br>
Now let's add some events! Each event has a specific function associated with it which is called when that event occurs. [[Events]](#events)

```python
@plugin.event.onServerStart
def onServerStart(event,ip,port):
    # Set the new start message
    event.startMsg=f'[!] Server has been started! [{ip}:{port}] Running TestPlugin1'


@plugin.event.onPluginLoad
def onPluginLoad(*_): # Ignore args
    # Print how many plugins have been loaded
    print(f'[!] TestPlugin1 Loaded! Running {len(plugin.getPlugins())} plugins.')
```

Here we define 2 events, `onServerStart`, and `onPluginLoad`.
The `onServerStart` function can be used to modify the start text and thats exactly what we are doing.

The `onPluginLoad` event doesent recieve any arguments nor return anything. It is used to signal when the server is done loading the plugin and we can use the newly recieved functions to interface with the server. [[Methods]](#methods)
