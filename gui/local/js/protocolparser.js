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
    }
  }
}

console.log(protocol.parser.createChallenge("nameplayer", "namegame", 5));
