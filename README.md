# Async chat Minecraft


Test chat for Minecraft lovers.



# How to install

Download the repository

Open the folder in the terminal:
```bash
cd async_minecraft_chat
```
Install requirements libraries and packages:
```bash
pip3 install -r requirements.txt
```


## Setting up with `cli`:

### get_messages.py

`--host` - host;

`--port` - port;

`--history` - path to the file, where will save a history of the chat;

### sending_messages.py

`--host` - host;

`--port` - port;

`--token` - user authorisation key for server;

`--username` - username for new user;

`--message` - message to send;


# Example to run the code

```bash
python3 sending_messages.py --username=TestUser --message=Hello World!!!
``` 
