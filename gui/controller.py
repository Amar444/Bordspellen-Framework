import json
import copy

from gui.commands import CommandLogin, CommandLogout, CommandPlayerlist, CommandGamelist, CommandCreateChallenge, \
    CommandAcceptChallenge, CommandSubscribe, CommandUnsubscribe, CommandMove, CommandBoard, CommandForfeit
from tictactoe.game import TicTacToeGame
from reversi.game import ReversiGame
from gac.players import NamedPlayerMixin, BoardPlayerMixin
from gac.client import Client
from tictactoe.ai import TicTacToeAIPlayer
from reversi.ai import ReversiAIPlayer


class GUIController:
    """ Provides a controller to link the GUI and a Client (so essentially the server) together """
    gui = None
    client = Client()
    nickname = None
    commands = None
    challenges = {}
    own_player = None
    opponent_player = None
    first_yourturn = True

    def __init__(self, gui):
        """ Initializes a new controller to be used by the GUI """
        super().__init__()
        self.gui = gui

        # every command that needs to be used should be listed here
        # placing this outside a method does not seem to work, that is why its initialized here
        self.commands = (
            CommandLogin,
            CommandLogout,
            CommandPlayerlist,
            CommandGamelist,
            CommandCreateChallenge,
            CommandAcceptChallenge,
            CommandSubscribe,
            CommandUnsubscribe,
            CommandMove,
            CommandBoard,
            CommandForfeit
        )

    def handle_message(self, message):
        """ handles every incoming messege from the GUI """
        # make JSON from the message
        message = self.handle_json(message)

        # try to get the command from the message
        try:
            command = message['command']
        except Exception as e:
            print("JSON does not contain a command")
            command = 'No command found'

        # iterate through every known command and create every command that listens to the command
        for current_command in self.commands:
            if current_command.command == command:
                try:
                    current_command(self, self.client, message)
                except Exception as e:
                    print("Command error, exception: {}", e)


    def handle_json(self, json_str):
        """ generates a dictionary from a given JSON string """
        try:
            json_str = json.loads(str(json_str))
        except Exception as e:
            json_str = None
            print("Could not convert JSON, exception: {}", e)
        return json_str

    def send_to_gui(self, listener, details, status=None, status_message=None):
        """ sends information to the GUI of the controller """
        if status is not None:
            details['status'] = status
        if status_message is not None:
            details['statusMessage'] = status_message

        self.gui.send_to_client(json.dumps(
            {
                'listener': listener,
                'detail': details
            }
        ))

#--------------------------------------------
#NOTE  listeners have yet to be made abstract (and everything else below this point)
#--------------------------------------------
    def start_listeners(self):
        self.client.on('GAME', self.handle_game)

    def handle_game(self, data):
        type = data.arguments[0]

        if type == 'MATCH':
            self.handle_match(data.arguments[1:])
        elif type == 'YOURTURN':
            self.handle_yourturn(data.arguments[1:])
        elif type == 'CHALLENGE':
            self.handle_challenge(data.arguments[1:])
        elif type == 'MOVE':
            self.handle_move(data.arguments[1:])
        elif type == 'HELP':
            print("We ain't accepting no help!")
        else:
            self.game_ended(data.arguments[0:])

    def handle_match(self, args):
        data = args[0]
        gametype = data['GAMETYPE']
        opponent = data['OPPONENT']
        player_to_move = data['PLAYERTOMOVE']
        self.send_to_gui('match', {'gametype': gametype, 'opponent': opponent, 'playerToMove': player_to_move})
        self.create_game(gametype, opponent, player_to_move)

    def handle_yourturn(self, args):
        if self.first_yourturn is not True:
            # self.own_player.play(args[0]['TURNMESSAGE'])
            self.own_player.play()
        else:
            self.first_yourturn = False

    def handle_move(self, args):
        data = args[0]
        if data['PLAYER'] == self.opponent_player.name:
            x = data['MOVE'] / self.opponent_player.board.size[0]
            y = data['MOVE'] % self.opponent_player.board.size[1]
            self.own_player.game.execute_move(self.opponent_player, int(x), int(y))


        board = self.own_player.board
        board_to_send = [[None for r in range(0, board.size[0])] for r in range(0, board.size[1])]
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                if board.state[row][col] is self.own_player:
                    board_to_send[row][col] = self.own_player.name
                elif board.state[row][col] is self.opponent_player:
                    board_to_send[row][col] = self.opponent_player.name
                else:
                    board_to_send[row][col] = None
        self.send_to_gui('boardListener', {'board': board_to_send})

    def handle_challenge(self, args):
        data = args[0]

        if data == 'CANCELLED':
            challenge_number = args[1]['CHALLENGENUMBER']
            del self.challenges[challenge_number]
            self.send_to_gui('challengeCancelled', {'challengeNumber': challenge_number})
        else:
            challenger = data['CHALLENGER']
            game_name = data['GAMETYPE']
            challenge_number = data['CHALLENGENUMBER']
            turntime = data['TURNTIME']
            self.send_to_gui('challenged', {'challenger': challenger, 'gameName': game_name,
                                            'challengeNumber': challenge_number, 'turnTime': turntime})

    def game_ended(self, args):
        game_status = args[0].lower()
        data = args[1]
        player_one_score = data['PLAYERONESCORE']
        player_two_score = data['PLAYERTWOSCORE']
        comment = data['COMMENT']
        self.send_to_gui('gameStatus', {'status': game_status, 'playerOneScore': player_one_score,
                                        'playerTwoScore': player_two_score, 'comment': comment})

        self.opponent_player = None
        self.own_player = None
        self.first_yourturn = True

    def create_game(self, gametype, opponent, player_to_move):
        self.first_yourturn = True
        if gametype == 'Reversi':
            game = ReversiGame()
        elif gametype == 'Tic-tac-toe':
            game = TicTacToeGame()

        try:
            player_type = self.challenges[str(opponent)]
            del self.challenges[str(opponent)]
        except Exception as e:
            player_type = 'AI'

        if player_type == 'AI':
            if gametype == 'Reversi':
                self.own_player = GUIReversiAIPlayer(controller=self, name=self.nickname, game=game)
            elif gametype == 'Tic-tac-toe':
                self.own_player = GUITicTacToeAIPlayer(controller=self, name=self.nickname, game=game)
        elif player_type == 'HUMAN':
            self.own_player = UIPlayer(controller=self, name=self.nickname, game=game)

        self.opponent_player = ServerPlayer(name=opponent, game=game)

        if self.own_player.name == player_to_move:
            players = (self.opponent_player, self.own_player)
        elif self.opponent_player.name == player_to_move:
            players = (self.own_player, self.opponent_player)

        game.set_players(players)
        self.opponent_player.setup()

        if self.own_player.name == player_to_move:
            self.own_player.play()
        elif self.opponent_player.name == player_to_move:
            self.first_yourturn = False
            self.opponent_player.play()

        print('{ \
            "command": "getBoard" \
          }')


class ClientPlayer(NamedPlayerMixin, BoardPlayerMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ServerPlayer(ClientPlayer):
    opponent = None

    def play(self):
        super().play()

    def setup(self):
        """ Sets up any initial properties """
        if self.opponent is None:
            for player in self.game.players:
                if player != self:
                    self.opponent = player
                    break


class UIPlayer(ClientPlayer):
    controller = None
    check_move = True

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller

    def play(self):
        super().play()
        self.controller.send_to_gui('doMove', {'turnmessage': ''})


class GUITicTacToeAIPlayer(TicTacToeAIPlayer):
    controller = None
    check_move = False

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller

    def play(self):
        super().play()

        x, y, p = self.board.last_turn
        self.controller.handle_message('{ \
            "command": "move", \
            "moveX": ' + str(x) + ', \
            "moveY": ' + str(y) + ' \
          }')


class GUIReversiAIPlayer(ReversiAIPlayer):
    controller = None
    check_move = False

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller

    def play(self):
        super().play()

        x, y, p = self.board.last_turn

        print('{ \
                "command": "move", \
                "moveX": ' + str(x) + ', \
                "moveY": ' + str(y) + ' \
              }'
        )
        self.controller.handle_message('{ \
                "command": "move", \
                "moveX": ' + str(x) + ', \
                "moveY": ' + str(y) + ' \
              }')
