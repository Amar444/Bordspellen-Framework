$(function () {

  /* EVENTS */

  $(document).on("click", "[data-position]", function() {
    var placed = $(this).attr("data-placed");
    if(placed == "") {
      var xy = app._utilities.getXY(parseInt($(this).attr("data-position")), window.gameWidth);
      console.log(xy);
      window.activeWebSocket.send(JSON.stringify({
        "command" : "move",
        "moveX" : xy[0],
        "moveY" : xy[1]
      }));
      window.placed = true;
    }

  });

  $(".back-button").click(function() {
    window.location = "gameroom.html";
  });




  /* API EVENTS */

  $(document).on("boardListener", function(e) {
    var board = e.detail.board;
    for(var i = 0; i < board.length; i++) {
      for(var j = 0; j < board[i].length; j++) {
        var pos = app._utilities.getPos([i, j], window.gameWidth),
            item;
        if(board[i][j] == app._utilities.storage.get('localName')) {
          item = "cross";
        } else if(board[i][j] == null) {
          item = "";
        } else {
          item = "circle";
        }
        $('[data-position="'+pos+'"]').attr("data-placed", item);
      }
    }
  });

  $(document).on("moveListener", function(e) {
    if(e.detail.status == "error") {
      $("#result").text(e.detail.status);
      $("#player1-points").text("");
      $("#player2-points").text("");
      $("#player1").text("");
      $("#player2").text("");
      $("#result-message").text(e.detail.message);
      $(".match-overlay").remove();
      $(".challenge-overlay").removeClass('hidden');
    }
  });

  $(document).on("match", function(e) {
    console.log(e.detail);
    app._utilities.storage.set("playerToMove", e.detail.playerToMove);
    if(e.detail.gametype == "Tic-tac-toe") {
      window.location="tictactoe.html";
    }
    if(e.detail.gametype == "Reversi") {
      window.location="reversion.html";
    }
  });

  $(document).on("doMove", function(e) {
    $(".match-overlay").hide();
    app.main.setGameTimer("It's your turn", app._utilities.storage.get("turnTime"), function() {
      $(".match-overlay").show();
    });
  });

  $(document).on("gameStatus", function(e) {
    $("#result").text(e.detail.status.capitalizeFirstLetter());
    $("#player1-points").text(e.detail.playerOneScore);
    $("#player2-points").text(e.detail.playerTwoScore);
    $("#player1").text("You");
    $("#player2").text("Opponent");
    $("#result-message").text(e.detail.comment);
    $(".match-overlay").remove();
    $(".challenge-overlay").removeClass('hidden');
  });


  /* INITIALISATION */

  if(app._utilities.storage.get("playerToMove") == app._utilities.storage.get("localName")) {
    $(".match-overlay").hide();
    app.main.setGameTimer("It's your turn", app._utilities.storage.get("turnTime"), function() {
      $(".match-overlay").show();
    });
  }
  window.activeWebSocket.onopen = function() {
    window.activeWebSocket.send(JSON.stringify({
      "command" : "getBoard"
    }));
  }

});
