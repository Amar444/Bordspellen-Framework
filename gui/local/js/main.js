
/* Application */
var app = {
  "_utilities" : {
    "fadeOutVolume" : function(audio) {
      var vol = audio.volume;
      var fadeout = setInterval(
        function() {
          if (vol > 0) {
            vol -= 0.05;
            if(vol < 0)
              vol = 0;
            audio.volume = vol;
          } else {
            clearInterval(fadeout);
          }
        }, 50);
      },
      "fadeInVolume" : function(audio) {
        var vol = audio.volume;
        var fadeout = setInterval(
          function() {
            if (vol < 1) {
              vol += 0.05;
              if(vol > 1)
                vol = 1;
              audio.volume = vol;
            } else {
              clearInterval(fadeout);
            }
          }, 50);
        },
        "statusAudio" : function() {
            if(app._utilities.storage.get("mute-sound") == "" || app._utilities.storage.get("mute-sound") == "on") {
                return true;
            } else {
                return false
            }
        },
        "playMusic" : function() {
            if(app._utilities.statusAudio()) {
                window.playAudio.play();
            }
        },
        "toggleAudio" : function() {
            var status;
            if(app._utilities.statusAudio()) {
                app._utilities.storage.set('mute-sound', "off");
                app._utilities.fadeOutVolume(window.playAudio);
                status = false;
            } else {
                app._utilities.storage.set('mute-sound', "on");
                app._utilities.fadeInVolume(window.playAudio);
                window.playAudio.play();
                status = true;
            }
             return status;
        },
        "storage" : {
          "get" : function(name) {
            return typeof sessionStorage.getItem(name) !== "undefined" ? sessionStorage.getItem(name) : false;
          },
          "set" : function(name, value) {
            sessionStorage.setItem(name, value);
          }
        },
        getXY : function(pos, squareWidth) {
           row = Math.floor((pos - 1) / squareWidth);
           col = (pos - 1) % squareWidth;
           return [row, col];
        },
        getPos : function(xy, squareWidth) {
           return (xy[0] * squareWidth + xy[1] % squareWidth) + 1;
        }
    },
  "main" : {
    "unloadPage" : function(dest, button) {
      view.frameContent.classList.add('hideElem');
      view.frameBackground.classList.add('hideElem');

      app._utilities.fadeOutVolume(window.playAudio);

      setTimeout(function() {
        app._utilities.storage.set("musicTime", window.playAudio.currentTime);
        window.location=dest;
      }, 1000);
    },
    "setGameTimer" : function(message, timer, callback) {
      $(function() {
        window.placed = false;
        $(".message-text").html(message);
        $(".message-timer").html(timer);
        $(".message").addClass('visible');
        var i = setInterval(function() {
          if(window.moveMade == true) {
            timer = -1;
          }
          timer = timer - 1;
          if(timer < 0 || window.placed == false) {
            $(".message").removeClass("visible");
            clearInterval(i);
            callback();
          } else {
            $(".message-timer").html(timer);
          }
        }, 1000);
      });
    }
  }
};

/*  WebSocket Connection */
var name = app._utilities.storage.get("localName");
if(name != false) {
  window.activeWebSocket = new WebSocket("ws://127.0.0.1:8888/"+name);
} else {
  window.activeWebSocket = new WebSocket("ws://127.0.0.1:8888/");
}
window.activeWebSocket.onmessage = function (e) {
  try {
    var obj = JSON.parse(e.data);
    var event = new CustomEvent(obj.listener, {"detail" : obj.detail});
    document.dispatchEvent(event);
  } catch(e) {
    console.warn("Invalid JSON: " + e.data)
  }
}


/* Initialize */

var view = {
  title : document.getElementById("game-name"),
  content : document.getElementById("game-main-content"),
  frameContent : document.querySelector(".content"),
  frameBackground : document.querySelector(".background"),
}

view.frameContent.classList.remove('hideElem');
view.frameBackground.classList.remove('hideElem');

if(typeof window.song !== "undefined") {
  window.playAudio = new Audio('sounds/' + window.song);
} else {
  window.playAudio = new Audio('sounds/sound.mp3');
}
window.playAudio.addEventListener('ended', function() {
    this.currentTime = 0;
    this.play();
}, false);

if(window.home != true) {
  window.playAudio.currentTime = app._utilities.storage.get("musicTime");
}

window.playAudio.volume = 0;
app._utilities.fadeInVolume(window.playAudio);
app._utilities.playMusic();
