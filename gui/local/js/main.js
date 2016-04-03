/* Application */
var app = {
  "_utilities" : {
    "fadeOutVolume" : function(audio) {
      var vol = audio.volume;
      var fadeout = setInterval(
        function() {
          // Reduce volume by 0.05 as long as it is above 0
          // This works as long as you start with a multiple of 0.05!
          if (vol > 0) {
            vol -= 0.05;
            audio.volume = vol;
          }
          else {
            // Stop the setInterval when 0 is reached
            clearInterval(fadeout);
          }
        }, 50);
      },
      "fadeInVolume" : function(audio) {
        var vol = audio.volume;
        var fadeout = setInterval(
          function() {
            // Reduce volume by 0.05 as long as it is above 0
            // This works as long as you start with a multiple of 0.05!
            if (vol < 1) {
              vol += 0.05;
              audio.volume = vol;
            }
            else {
              // Stop the setInterval when 0 is reached
              clearInterval(fadeout);
            }
          }, 50);
        }
    },
  "main" : {
    "unloadPage" : function(dest, button) {
      view.frameContent.classList.add('hideElem');
      view.frameBackground.classList.add('hideElem');

      app._utilities.fadeOutVolume(window.playAudio);

      setTimeout(function() {
        if(sessionStorage != null) {
          sessionStorage.musicTime = window.playAudio.currentTime;
        }
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

if(sessionStorage != null && window.home != true) {
  window.playAudio.currentTime = sessionStorage.musicTime;
}

window.playAudio.volume = 0;
app._utilities.fadeInVolume(window.playAudio);
window.playAudio.play();

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}