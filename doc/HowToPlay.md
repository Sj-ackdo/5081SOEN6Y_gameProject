# Setup and playing guide

### Client side

Simply run the program with,
```
$ python play.py
```
if playing with localhost,
```
$ python play.py --ip {ip given by server}
```
to play with a remote lan.

### Server side

For the host make sure the port ***6767*** is not blocked by your firewall,<br>
host the server with the following command,
```
$ python src/init_server.py arg1 arg2
```

where *arg1* and *arg2* can be any of the following:<br>
`--player-amount {int}`, is used to set the amount of players allowed to connect to the server (standard is 2)<br>
`--map {int}`, is used to choose which map to use in the game (1 or 2)
