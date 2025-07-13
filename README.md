# TCP

This is a simple TCP server/client messaging practice project. There are three versions of the server, the latest and greatest being `Server3`.

`Server2` supports multiple clients using Python's socket and threading modules. The original (`Server`) only supports one client that can only echo messages to itself.

`Server3` features end-to-end encryption, timestamped messages, and the ability to alias clients to nicknames, on top of all the things `Server2` can do.

- Start `Server3` using `python3 main.py 3` or `Server2` using `python3 main.py 2`, or `Server` using `python3 main.py 1`
- Start `Client` using `python3 main.py 0`

### Server2
There are three different ways a client can send a message with `Server2`:
- Echo: Simply enter your message as normal to echo it (Ex. `Hi, myself`)
- Broadcast: Prefix your message with `B-` to turn it into a broadcasted message that all connected clients will receive (Ex. `B-Yooooooo` or even something like `B- Jaxon Wuz Here -- 123(*&`
- DM: Prefix your message with `C<another client's port number>` to turn it into a direct message that only the specified client will receive (Ex. `C50244- This is a direct message`)
- Send an empty message to be prompted to quit

### Server3 (extends Server2)