from gui.server import RunServer
from gui.controller import GUIController

rs = RunServer()
RunServer.set_instance(rs)
cs = GUIController(rs)

rs.start()
