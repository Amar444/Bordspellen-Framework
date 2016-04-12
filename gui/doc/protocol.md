The communication-protocol between the GUI and the main GameApplication:
=====



GUI CALLS:
---

<br>

#### When the GUI wants to login:

-----
```
GUI -> : { "command": "login", "nickname": <nickname>}
GUI <- :
    {
        'detail': {
            'status': <status>
            'message': <mesage>
            'playerName': <nickname>
            'IP': <IP>
            'port': <port>
        },
        'listener': 'loginStatus',
    }
```

<br>
<br>
<br>

#### When the GUI wants to logout:

-----
```
GUI -> : { "command": "logout"}
```

<br>
<br>
<br>

#### When the GUI is in need for the player-list:

-----
```
GUI -> : { "command": "playerlist"}
GUI <- :
    {
        'detail': {
            'status': <status>
            'message': <mesage>
            'players': ['henk', 'Jur', 'Johankladder']
        },
        'listener': 'playerList',
    }
```
- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.

<br>
<br>
<br>



#### When the GUI is in need for the game-list:

---
```
GUI -> : { "command": "gamelist"}
GUI <- :
    {
        'detail': {
            'status': <status>
            'message': <mesage>
            'games': ['Game one', 'GameTwo', 'GameThree']
        },
        'listener': 'gameList',
    }
```
- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.
<br>
<br>
<br>


#### When the GUI is in need to challenge a player:

---
```
GUI -> :
    {
        "command": "challenge",
        "playername": <playerName>,
        "gamename" : <gameName>,
        "turntime" : <turntime>
    }

GUI <- :
    {
        'detail': {
            'status': <status>,
            'message': <message>
        },
        'listener': 'challenge'
    }
```
- The server returns the details of this request. With this returned request,
the server will also send a listener that needs to be invoked after the request was completed or
when an error occurred.
- The message contains the reason why this request could'nt be accepted. Message does'nt needs
to be set, so can also be null.

<br>
<br>
<br>


#### When the gui is in need to accept a challenge:

---

```
GUI -> : {
            "command" : "accept",
            "challenge" : <challengeNumber>
          }

GUI <- :
    {
        'detail': {
            'status': <status>,
            'message': <message>
        },
        'listener': 'accept'
    }
```

- Whereas n is the challenge number the GUI likes to accept.
- The response of the server includes the details of the 'request' and a listener. This
listener will be invoked when the accept-request was accepted by the main-server.
- The message contains the reason why this request could'nt be accepted. Message does'nt needs
to be set, so can also be null.

<br>
<br>
<br>



#### When the GUI wants to subscribe to a game:

---
```
GUI -> : {
            "command" : "subscribe",
            "game" : <game>
          }

GUI <- :
    {
        'detail': {
            'status': <status>
            'message': <mesage>
        },
        'listener': 'subscribe',
    }
```
- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.
<br>
<br>
<br>



#### When the GUI wants to unsubscribe from the current subscription:

---
```
GUI -> : { "command" : "unsubscribe" }
GUI <- :
    {
        'detail': {
            'status': <status>
            'message': <mesage>
        },
        'listener': 'unsubscribe',
    }
```
- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.
<br>
<br>
<br>

GUI UPDATES:
-----

The GUI's sockets also listens to certain command i.e. for updating the view. The
following protocols needs to used when communication with the GUI.

#### Challenged:

---

```
GUI <- :
    {
        'detail': {
            'challenger': <playerName>,
            'gameName': <gameName>,
            'challengeNumber': <challengeNumber>,
            'turnTime': <turnTime>
        },
        'listener': 'challenged'
    }

```

- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.


<br>
<br>

#### Challenge cancelled:

---

```
GUI <- :
    {
        'detail': {
            'challengeNumber': <challengeNumber>,
        },
        'listener': 'challengeCancelled'
    }

```

- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.


<br>
<br>

#### Match started:

---

```
GUI <- :
    {
        'detail': {
            'gametype': <gametype>,
            'opponent': <opponent>,
            'playerToMove': <playerToMove>
        },
        'listener': 'match'
    }

```

- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.


<br>
<br>
