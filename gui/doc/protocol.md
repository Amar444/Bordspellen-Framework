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
        'listener': 'playerList',
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
        'listener': 'playerList',
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
        'listener': 'challengeListener'
    }
```
- In this protocol the turn time does'nt need to be set, but the key will always be included.
When n is not included, than n will always be null.
- N will be always filled in without quotation's marks, since it will be handled by the external
server as an Integer.
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
        'listener': 'acceptListener'
    }
```

- Whereas n is the challenge number the GUI likes to accept.
- The response of the server includes the details of the 'request' and a listener. This
listener will be invoked when the accept-request was accepted by the main-server.
- The message contains the reason why this request could'nt be accepted. Message does'nt needs
to be set, so can also be null.

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
        'challenged': {
            'challenger': <playerName>,
            'gameName': <gameName>,
            'challengeNumber': <challengeNumber>,
            'turnTime': <turnTime>
        },
        'listener': 'challengedListener'
    }

```

- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.


<br>
<br>

#### Game update

- [ROW/ COLUMN  -> 0/2]
---
```json
{
  "game":
  {
    "players": [
      {
        "playerName": "playerOne"
      },
      {
        "playerName": "playerTwo"
      }
    ],
    "gameState": {
      "win": true,
      "board": {
        "rows": [
          {
            "columns": [
              {
                "playerName": "playerOne"
              },
              {
                "playerName": "playerTwo"
              },
              {
                "playerName": "playerTwo"
              }
            ]
          },
          {
            "columns": [
              {
                "playerName": "playerTwo"
              },
              {
                "playerName": "playerOne"
              },
              {
                "playerName": "playerOne"
              }
            ]
          },
          {
            "columns": [
              {
                "playerName": "playerTwo"
              },
              {
                "playerName": "playerOne"
              },
              {
                "playerName": "playerOne"
              }
            ]
          }
        ]
      }
    }
  }
}
```

- This protocol is based on the following tic-tac-toe situation:
<br>
![alt text](http://i.imgur.com/MBcncKw.png "Logo Title Text 1")

- When no move was set on a certain place on the board, a simple null will satisfy
 the protocol's need.
