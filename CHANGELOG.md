
# Changes since V1.0.0 B1

## V1.1.1 B4

Plugin api bugfixes

Changes:

- Rename sendBroadcast to broadcast
- Rename sendMessageAs to sendMsg in plugin api and internally
- Rename sendDmAs to sendDm
- Remove already removed event defenitions from being checked
- Plugin event errors are now logged
- Changed how direct messages look like
- Updates to plugins
- Changes to documentation and other .md files

## V1.1.0 B3

Client & protocol update

Changes:

- Protocol now supports server -> client requests
- Added new `DISPLAY` and `DISLPLAY_display_name` packets.
- Fixed client not running in /client directory when debugging
- Fixed default config being invalid
- Fixed apiGet function not working without http scheme
- Fixed config types being always strings
- Fixed store credentials and online mode config options
- Implemented protocol changes on server
- Fixed server not broadcasting messages from client if a plugin used the onMessage event
- Random bugfixes

## V1.0.1 B2

Bugfixes & config

Changes:

- Add config
- Fixed potential bug where by forgetting to send \t in a raw data send would result in the client not parsing it
- Remove bans & topics from server
- Loading of plugins is now in a function
- Fix some plugins
- Random bugfixes

## V1.0.0 B1

Everything before this is UNDOCUMENTED

Changes:

- Publish source.