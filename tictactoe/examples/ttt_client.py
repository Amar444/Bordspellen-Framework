from client import Client, EVENT_GAME, EVENT_CONNECTED
from client.commands import OutgoingCommand
from gamekit.players import Player, NamedPlayerMixin, BoardPlayerMixin

from ai import AIPlayer
from game import TicTacToeGame


class ClientPlayer(NamedPlayerMixin, BoardPlayerMixin, Player):
    client = None

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client


class RemotePlayer(ClientPlayer):
    def on_move(self, move):
        move = int(move.arguments[1]['MOVE'])
        x, y = int(move / self.board.size[0]), move % self.board.size[1]
        self.board.set(x, y, self)


class ClientAIPlayer(ClientPlayer, AIPlayer):
    def play(self):
        super().play()

        x, y, p = self.board.last_turn
        move = str(x * self.board.size[0] + y % self.board.size[1])

        self.client.send(OutgoingCommand('MOVE', move))


class TicTacToeClient(Client):
    game_class = TicTacToeGame

    game = None
    our_player = None
    their_player = None
    nickname = None

    def __init__(self):
        super().__init__()

        self.on(EVENT_CONNECTED, self.on_connected)
        self.on(EVENT_GAME, self.on_game)

        self.game = self.game_class()
        self.our_player = ClientAIPlayer(name='X', client=self, game=self.game)
        self.their_player = RemotePlayer(name='O', client=self, game=self.game)
        self.game.set_players((self.our_player, self.their_player))

    def on_connected(self, e):
        while self.nickname is None:
            nickname = input('nickname? ')
            result = self.send_sync(OutgoingCommand('LOGIN', nickname))
            if result.type == 'OK':
                self.nickname = nickname

        # e = self.send_sync(OutgoingCommand('SUBSCRIBE', self.game.name))
        # if e.type == 'OK':
        #     print("Waiting for a challenge...")
        # else:
        #     self.disconnect()

    def on_game(self, e):
        if e.arguments[0] == 'MATCH' and e.arguments[1]['GAMETYPE'] == 'TicTacToe':
            print("A new match has started!")
            print("Opponent will be {}".format(e.arguments[1]['OPPONENT']))

        elif e.arguments[0] == 'YOURTURN':
            self.our_player.play()

        elif e.arguments[0] == 'MOVE':
            if e.arguments[1]['PLAYER'] != self.nickname:
                self.their_player.on_move(e)


c = TicTacToeClient()
c.connect()
