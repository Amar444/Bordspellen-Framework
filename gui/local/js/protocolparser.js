var protocol = {

  "parser": {
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
      return protocol.parser.getProtocol("playerlist");
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

console.log(protocol.parser.createChallenge("nameplayer", "namegame", 5));
console.log(protocol.parser.createLogin("nameplayer"));
console.log(protocol.parser.getPlayerList());
