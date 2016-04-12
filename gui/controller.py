import json

from gui.commands import CommandLogin, CommandLogout, CommandPlayerlist, CommandGamelist, CommandCreateChallenge, \
    CommandAcceptChallenge, CommandSubscribe, CommandUnsubscribe, CommandMove
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
    first_turn = True

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
                current_command(self, self.client, message)

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
        self.create_game(gametype, opponent, player_to_move)
        self.send_to_gui('match', {'gametype': gametype, 'opponent': opponent, 'playerToMove': player_to_move})

    def handle_yourturn(self, args):
        if self.first_turn is not True:
            # self.own_player.play(args[0]['TURNMESSAGE'])
            self.own_player.play()

    def handle_move(self, args):
        data = args[0]
        if data['PLAYER'] == self.opponent_player.name:
            x = data['MOVE'] / self.opponent_player.board.size[0]
            y = data['MOVE'] % self.opponent_player.board.size[1]
            self.own_player.board.set(int(x), int(y), self.opponent_player.name)
        board = self.own_player.board.state
        self.send_to_gui('boardListener', {'board': board})

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
        print(str(args))
        game_status = args[0].lower()
        data = args[1]
        player_one_score = data['PLAYERONESCORE']
        player_two_score = data['PLAYERTWOSCORE']
        comment = data['COMMENT']
        self.send_to_gui('gameStatus', {'status': game_status, 'playerOneScore': player_one_score,
                                        'playerTwoScore': player_two_score, 'comment': comment})

        self.opponent_player = None
        self.own_player = None

    def create_game(self, gametype, opponent, player_to_move):
        self.first_turn = True

        if gametype == 'Reversi':
            game = ReversiGame()
        elif gametype == 'Tic-tac-toe':
            game = TicTacToeGame()

        player_type = self.challenges[str(opponent)]
        if player_type == 'AI':
            if gametype == 'Reversi':
                self.own_player = GUIReversiAIPlayer(controller=self, name=self.nickname, game=game)
            elif gametype == 'Tic-tac-toe':
                self.own_player = GUITicTacToeAIPlayer(controller=self, name=self.nickname, game=game)
        elif player_type == 'HUMAN':
            self.own_player = UIPlayer(controller=self, name=self.nickname, game=game)

        self.opponent_player = ServerPlayer(name=opponent, game=game)

        game.set_players((self.own_player, self.opponent_player))

        if self.own_player.name == player_to_move:
            self.own_player.play()
        elif self.opponent_player.name == player_to_move:
            self.opponent_player.play()
        self.first_turn = False


class ClientPlayer(NamedPlayerMixin, BoardPlayerMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ServerPlayer(ClientPlayer):
    def play(self):
        super().play()


class UIPlayer(ClientPlayer):
    controller = None

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller

    def play(self):
        super().play()
        self.controller.send_to_gui('doMove', {'turnmessage': ''})


class GUITicTacToeAIPlayer(TicTacToeAIPlayer):
    controller = None

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