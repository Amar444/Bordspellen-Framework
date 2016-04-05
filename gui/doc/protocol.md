The communication-protocol between the GUI and the main GameApplication:
=====

<br>
<br>

GUI CALLS:
-----
#### When the GUI is in need for the player-list:
```
GUI -> : gui get playerlist
GUI <- : <playerlist>
GUI -> : OK    
```
- This player list needs to be of the following format (JSON):

```json
{
  "playerList": [
    {
      "playerName": "PlayerOne"
    },
    {
      "playerName": "PlayerTwo"
    },
    {
      "playerName": "PlayerThree"
    }
  ]
}
```

<br>
<br>
<br>

---
#### When the GUI is in need for the game-list:

```
GUI -> : gui get gamelist
GUI <- : <gamelist>
GUI -> : OK
```
- This game list needs to be of the following format (JSON):

```json
{
  "gameList": [
    {
      "gameName": "GameOne"
    },
    {
      "gameName": "GameTwo"
    },
    {
      "gameName": "GameThree"
    }
  ]
}
```

<br>
<br>
<br>

---
#### When the GUI is in need to challenge a player:

```
GUI -> : gui challenge <playerName> <gameName> <n>
GUI <- : OK
```
- n can be included or excluded, but will almost certainly be included when playing
in the GUI environment. The n parameter stands for the turn time of the game in seconds and
if not given, the server will use it's default time. 'n' must be given without quotationmarks.


<br>
<br>
<br>
<br>

GUI UPDATES:
-----

The GUI's sockets also listens to certain command i.e. for updating the view. The
following protocols needs to used when communication with the GUI.

#### Game update
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
