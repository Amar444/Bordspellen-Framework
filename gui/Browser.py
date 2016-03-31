import sys
from gi.repository import Gtk, Gdk, WebKit


class BrowserTab(Gtk.VBox):
    def __init__(self, *args, **kwargs):
        super(BrowserTab, self).__init__(*args, **kwargs)

        self.webview = WebKit.WebView()
        self.show()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.webview)

        self.pack_start(scrolled_window, True, True, 0)

        scrolled_window.show_all()

    def _load_url_string(self, url):
        if not "://" in url:
            url = "http://" + url
        self.webview.load_uri(url)



class Browser(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        # create notebook and tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)

        self.set_size_request(700, 600)

        # create a first, empty browser tab
        self.notebook.append_page(self._create_tab())

        self.add(self.notebook)

        # connect signals
        self.connect("destroy", Gtk.main_quit)

        self.notebook.show()
        self.show()


    def _create_tab(self):
        tab = BrowserTab()
        tab._load_url_string("google.nl")
        return tab



if __name__ == "__main__":
    Gtk.init(sys.argv)

    browser = Browser()

    Gtk.main()
