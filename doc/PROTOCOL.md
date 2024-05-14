
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

    Name     - Unique identifier
    Username - Display name
    Password - MD5 hash of password
    Token    - MD5 hash we use for identification.

### Errors

Protocol errors

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

    <REQUEST_NAME>
      <DESCRIPTION>
      <CONVERSATION>
  
### Requests

Everything that the client and server can send to eachother

#### Client to server

<details open>
<summary>LOGIN</summary>

    Exchange valid user details for token.
    CLIENT-> name && hashed psw
    SERVER-> token || INVALID
</details>

<details open>
<summary>SET_USER</summary>

    Request server to change our display name.
    CLIENT-> name && token && newUsername
    SERVER-> newUsername || INVALID
</details>

<details open>  
<summary>SEND_MESSAGE</summary>

    Request server to deliver our message.
    CLIENT-> name && token && message
    SERVER-> DONE || INVALID
</details>

<details open>  
<summary>SEND_COMMAND</summary>

    Request server to execute a / command.
    CLIENT-> name && token && command
    SERVER-> commandResponse || UNKNOWN_COMMAND || INVALID
</details>

<details open>
<summary>SEND_DM</summary>

    Send a private (direct) message to a user.
    CLIENT-> name && token && user && msg
    SERVER-> DONE || INVALID
</details>

#### Server to client

<details open>
<summary>DISPLAY</summary>

    Request the client to display a message.
    SERVER-> message
    CLIENT-> DONE
</details>

<details open>
<summary>DISPLAY_NAME</summary>

    Request the client to set the clientside username.
    SERVER-> name
    CLIENT-> DONE
</details>
