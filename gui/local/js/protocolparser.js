var protocol = {

  "createParser": {
  "createChallenge" : function(challengedPlayer, gameName, turnTime) {
          if(gameName != null && challengedPlayer != null) {
            if(gameName != "" && challengedPlayer != "") {
              var protocol = "challenge \"";
              protocol += challengedPlayer + "\" ";
              protocol += "\"" + gameName + "\" ";

              if(turnTime != "" && turnTime != null) {
                protocol += turnTime;
              }

              return protocol;
            }
            return null;
          }
          return null;
    },
    "createLogin" : function(playerName) {
        if(playerName != null && playerName != "") {
          var protocol = "login ";
          protocol += "\"" + playerName + "\"";
          return protocol;
        }
        return null;
    },
    "getPlayerList" :function() {
      return protocol.createParser.getProtocol("playerlist");
    },
    "getGameList" : function() {
      return protocol.createParser.getProtocol("gamelist");
    },
    "getProtocol": function(name) {
      if(name != null && name != "") {
        return "get " + name;
      } else {
        return null;
      }
    }
  }
}

console.log(protocol.createParser.createChallenge("nameplayer", "namegame", 5));
console.log(protocol.createParser.createLogin("nameplayer"));
console.log(protocol.createParser.getPlayerList());
