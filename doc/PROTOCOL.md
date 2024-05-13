
# Protocol

This file contains the specifics of exactly how the client and server communicate.
<br>
Yes i know it should be better..
<br>
No i wont fix it.

## Reading

This section regards all the formatting that I've used in this document.

### Data types

The types of data used in this document

    lowerCamelCase = Variable
    UPPERCASE = Static string
    <WRAPPEDSTR> = The "replace me with X"

### Variables

Variable information

    Name     - Unique identifier
    Username - Display name
    Licence  - Block signed with our privateKey, verifiable with publicKey
    Token    - MD5 hash we use for identification. Created with users name, username and a random number.

### Errors

Protocol errors

    INVALID         - Invalid token
    UNKNOWN_COMMAND - User tried executing a nonexistent command
    NOT_IMPLEMENTED - Feature is not implemented or enabled
    DONE            - Sender marks message as recieved, and completed.

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
