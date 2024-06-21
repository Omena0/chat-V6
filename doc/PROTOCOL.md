
# Protocol

This file contains the specifics of exactly how the client and server communicate.

## Reading

This section regards all the formating that I've used in this document.

### Data types

The types of data used in this document

    lowerCamelCase = Variable
    UPPERCASE = Static string
    <WRAPPEDSTR> = The "replace me with X"

### Variables

Variable information

    display_name     - Display name
    name - Unique identifier
    Password - MD5 hash of password
    Token    - MD5 hash we use for identification.

### Errors

Protocol responses

    INVALID         - Invalid token
    UNKNOWN_COMMAND - User tried executing a nonexistent command
    NOT_IMPLEMENTED - Feature is not implemented or enabled
    DONE            - Sender marks operation as completed.

### Operators

Logical operators used in this document

    && - And   - Different pieces of data separated by "|"
    || - Or    - Server will respond with either of the specified responses
  
### Format

Request format

    <REQUEST_display_name>
      <DESCRIPTION>
      <CONVERSATION>
  
### Requests

Everything that the client and server can send to eachother

#### Client -> server

<details open>
<summary>LOGIN</summary>

    Exchange valid user details for token.
    CLIENT-> display_name && hashed psw
    SERVER-> token || INVALID
</details>

<details open>
<summary>SET_USER</summary>

    Request server to change our display display_name.
    CLIENT-> display_name && token && newname
    SERVER-> newname || INVALID
</details>

<details open>  
<summary>SEND_MESSAGE</summary>

    Request server to deliver our message.
    CLIENT-> display_name && token && message
    SERVER-> DONE || INVALID
</details>

<details open>  
<summary>SEND_COMMAND</summary>

    Request server to execute a / command.
    CLIENT-> display_name && token && command
    SERVER-> commandResponse || UNKNOWN_COMMAND || INVALID
</details>

<details open>
<summary>SEND_DM</summary>

    Send a private (direct) message to a user.
    CLIENT-> display_name && token && user && msg
    SERVER-> DONE || INVALID
</details>

#### Server -> client

<details open>
<summary>DISPLAY</summary>

    Request the client to display text.
    SERVER-> message
    CLIENT-> DONE
</details>

<details open>
<summary>SET_display_name</summary>

    Request the client to set the client display_name.
    SERVER-> display_name
    CLIENT-> DONE
</details>

<details open>
<summary>MESSAGE</summary>

    Send a message to the client
    SERVER-> display_name && name && message
    CLIENT-> DONE
</details>

<details open>
<summary>DM</summary>

    Request the client to set the client display_name.
    SERVER-> display_name
    CLIENT-> DONE
</details>
