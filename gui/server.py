#########   ###    ###    ########
##     ##   ##  ##  ##    ##         Mijn PEP8 dinges bugged. Als je dit netjes kan maken, graag!
##     ##   ##      ##    ##    ##
#########   ##      ##    ########

import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import threading


class WebsocketConnection(tornado.websocket.WebSocketHandler):
    """ Every new connection becomes an instance of this class """

    def open(self):
        """ Method for a new connection. Subscribe to list. """
        RunServer.connection.append(self);
        print("Client connection established! Yeeeehaaaa!!");

    def on_message(self, message):
        """ Method for an incomming message """
        print(message);

    def on_close(self):
        """ Method on closing the connection. Removes from list. """
        RunServer.connection.remove(self);

    def check_origin(self, origin):
        """ Method for connection handshake. """
        return True


class RunServer(threading.Thread):
    """ This is the class that runs the server and pushes messages. """

    # The array that will hold all the active connections
    connection = [];

    @staticmethod
    def run():
        """ This method will start the thread and sets up the server """
        app = tornado.web.Application([(r"/", WebsocketConnection)])
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

    @staticmethod
    def sendToClient(data):
        """ This method allows you to send messages to all subscribers """
        if(len(RunServer.connection) > 0) :
            for singleServer in RunServer.connection:
                singleServer.write_message(data)


if __name__ == '__main__':
    rs = RunServer()
    rs.start()