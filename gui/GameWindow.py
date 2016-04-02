import gi
import os
from gi.repository import Gtk, Gdk, WebKit

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')


class Browser(Gtk.Window):

    full_screen = True

    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        # Set title application
        self.set_title("GameView GAC")

        # Init the web-view
        webView = WebKit.WebView()

        # Gets project dir:
        BASE_DIR = self.get_project_path()

        # Add folder to project dir:
        BASE_DIR += "/gui/local/index.html"

        # Open the file on given location in a web-view:
        webView.load_uri('file:///' + BASE_DIR)

        # Create a scrollable window:
        scrolled_window = Gtk.ScrolledWindow()

        # Add web-view to the scrollable window:
        scrolled_window.add(webView)

        # Add the scrollable window to the main window:
        self.add(scrolled_window)

        # Set minimal size window:
        self.set_size_request(1000, 800)

        # Add listener:
        self.connect("key-release-event", self.on_key_release)

        # Set window to full screen:
        self.fullscreen()

    def on_key_release(self, widget, ev):
        if ev.keyval == Gdk.KEY_F11 or ev.keyval == Gdk.KEY_Escape:
            if self.full_screen:
                self.unfullscreen()
                self.full_screen = False
            else:
                self.fullscreen()
                self.full_screen = True


    def get_project_path(self):

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        return BASE_DIR


if __name__ == "__main__":
    win = Browser()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
