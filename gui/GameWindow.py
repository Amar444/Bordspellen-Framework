import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk, WebKit


class Browser(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        # Set title application
        self.set_title("GameView GAC")

        # Init the web-view
        webView = WebKit.WebView()

        # Gets project dir:
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        # Add folder to project dir:
        BASE_DIR += "/gui/local"

        # Join begin file to project dir:
        BASE_DIR = os.path.join(BASE_DIR, 'index.html')

        # Open the file on given location in a web-view:
        webView.open('file://' + BASE_DIR)
        #bovenstaande methode returned file://c/Users/Jur/Documents/Bordspellen-Framework/gui/local/index.html op windows
        #webView.open('file:///C:/Users/Jur/Documents/Bordspellen-Framework/gui/local/index.html')
        # Create a scrollable window:
        scrolled_window = Gtk.ScrolledWindow()

        # Add web-view to the scrollable window:
        scrolled_window.add(webView)

        # Add the scrollable window to the main window:
        self.add(scrolled_window)

        # Set minimal size window:
        self.set_size_request(700, 700)


if __name__ == "__main__":
    win = Browser()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
