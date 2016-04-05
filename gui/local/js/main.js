/*  WebSocket Connection */
window.activeWebSocket = new WebSocket("ws://127.0.0.1:8888/");
window.activeWebSocket.onmessage = function (e) {

  console.log(e.data)
  if(e.data=="challenge accepted") {
    var event = new Event('challengeAccepted')
    document.dispatchEvent(event);
  }

}



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
            return sessionStorage.getItem(name);
          },
          "set" : function(name, value) {
            sessionStorage.setItem(name, value);
          }
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
    }
  }
};


/* Initialize */

var view = {
  title : document.getElementById("game-name"),
  content : document.getElementById("game-main-content"),
  frameContent : document.querySelector(".content"),
  frameBackground : document.querySelector(".background"),
}

view.frameContent.classList.remove('hideElem');
view.frameBackground.classList.remove('hideElem');

window.playAudio = new Audio('sounds/sound.mp3');
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
