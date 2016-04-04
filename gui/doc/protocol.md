The communication-protocol between the GUI and the main GameApplication:
=====

## When the GUI is in need for the player-list:
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

## When the GUI is in need for the game-list:

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
