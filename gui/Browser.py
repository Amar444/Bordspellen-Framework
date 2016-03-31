import sys
from gi.repository import Gtk, Gdk, WebKit

class Browser(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        webView = WebKit.WebView()
        webView.load_uri("http://www.google.nl")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(webView)
        scrolled_window.show_all()

        self.add(scrolled_window)

        self.set_size_request(700, 600)




if __name__ == "__main__":
    win = Browser()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()