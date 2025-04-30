# TCP

This is a simple TCP server/client messaging practice project. There are two versions of the server, the latest and greatest being `Server2`. 

`Server2` supports multiple clients using Python's socket and threading modules. The original (`Server`) only supports one client that can only ECHO messages to itself.

- Start `Server2` using `python3 main.py 3`, or start `Server` using `python3 main.py 1`
- Start `Client` using `python3 main.py 2`

There are three different ways a client can send a message with `Server2`:
- ECHO: Simply enter your message as normal to ECHO it (Ex. `Hi, myself`)
- Broadcast: Prefix your message with `B-` to turn it into a broadcasted message that all connected clients will receive (Ex. `B-Yooooooo` or even something like `B- Jaxon Wuz Here -- 123(*&`
- DM: Prefix your message with `C<another client's port number>` to turn it into a direct message that only the specified client will receive (Ex. `C50244- This is a direct message`)
