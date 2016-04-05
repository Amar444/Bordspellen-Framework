The communication-protocol between the GUI and the main GameApplication:
=====



GUI CALLS:
---

<br>

#### When the GUI is in need for the player-list:

-----
```
GUI -> : playerlist
GUI <- : {'detail': {'players': ['henk', 'Jur', 'Johankladder']}, 'listener': 'playerList'}
```
- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.

<br>
<br>
<br>


#### When the GUI is in need for the game-list:

---
```
GUI -> : gamelist
GUI <- : {'detail': {'games': ['Game one', 'GameTwo', 'GameThree']}, 'listener': 'gameList'}
```
- The 'listener' entry in the return JSON String is the listener that needs to be invoked when
the GUI received the response of the server.
<br>
<br>
<br>


#### When the GUI is in need to challenge a player:

---
```
GUI -> :{
            "challenge":  {
              "playerName":  <playerName>,
              "gameName": <gameName>,
              "turnTime": <n>
            }
        }
GUI <- : OK
```
- In this protocol the turn time does'nt need to be set, but the key will always be included.
When n is not included, than n will always be null.
- N will be always filled in without quotation's marks, since it will be handled by the external
server as an Integer.

<br>
<br>
<br>


#### When the gui is in need to accept a challenge:

---

```
GUI -> : accept n
GUI <- : OK / ERR
```

- Whereas n is the challenge number the GUI likes to accept.
- Response OK, when the 'challenge-accept' is a valid command at the time of sending.
- Response ERR, when the challenged can't be found.

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
