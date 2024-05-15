# Chat V6

 6th iteration of my chat app (most are gone)

## Usage

Run the client and enter your username & password in the prompt.

There are 2 (default) commands:

```syntax
/nick <name>       - Set your nickname
/msg  <user> <msg> - Send a private message
```

Other commands can be added via server plugins.

## Running a server

If you want to run your own server, follow this tutorial.

### Step 1

Download the repo and extract it

### Step 2

Run the server

### Step 3

If you dont want to use your own ip address, use ngrok:

```bash
ngrok tcp 5000
```

If you dont want to constantly tell people what your server ip is, set up a static api on github pages:

- Make a repository called \<yourusername\>.github.io and create a folder in it called "api"
- Then make a folder inside that folder called "chat-v6"
- Then create a file named "ip.html" in the chat-v6 folder
- Inside the file put your ngrok ip address
- Set up github pages

Now you can connect to the right server by changing

```py
# Api address
api_addr = "https://omena0.github.io/api/"
```

into

```py
# Api address
api_addr = "https://<yourusername>.github.io/api/"
```

inside the client config.txt file.

**If you want to customise your new server, read the plugin docs!**

## Docs

### [PLUGIN DOCS](doc/PLUGINS.md)

How to make plugins?!?!?! (tutorial) (working) (2024) (no clickbait)

### [PROTOCOL DOCS](doc/PROTOCOL.md)

How does the networking (net)work??!?!?!
