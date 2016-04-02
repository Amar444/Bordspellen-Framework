/* Initialize */

var view = {
  title : document.getElementById("game-name"),
  content : document.getElementById("game-main-content"),
  frameContent : document.querySelector(".content"),
  frameBackground : document.querySelector(".background"),
}

view.frameContent.classList.remove('hideElem');
view.frameBackground.classList.remove('hideElem');

/* Application */
var app = {
  "main" : {
    "unloadPage" : function(dest, button) {
      view.frameContent.classList.add('hideElem');
      view.frameBackground.classList.add('hideElem');
      setTimeout(function() {
        window.location=dest;
      }, 1000);
    }
  }
};
