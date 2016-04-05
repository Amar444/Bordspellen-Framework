from gui.server import RunServer
from players import ClientPlayer

rs = RunServer()
RunServer.setInstance(rs)
cs = ClientPlayer(rs)

rs.start()
