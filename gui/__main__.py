"""
Starts the server and opens a webbrowser
"""

import webbrowser

from gui.server import RunServer
from gui.controller import GUIController

rs = RunServer()
RunServer.set_instance(rs)
cs = GUIController(rs)

rs.start()
webbrowser.open_new('http://localhost:63342/Bordspellen-Framework/gui/local/index.html')\
