from gac.client import Client
import json

from gui.commands import CommandLogin, CommandLogout, CommandPlayerlist, CommandGamelist, CommandCreateChallenge, \
    CommandAcceptChallenge, CommandSubscribe, CommandUnsubscribe


class GUIController:
    """ Provides a controller to link the GUI and a Client (so essentially the server) together """
    gui = None
    client = Client()
    nickname = None
    commands = None
    challenges = {}

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
#NOTE  listeners have yet to be made abstract
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
        elif type == 'HELP':
            print("We ain't accepting no help!")
        else:
            self.game_ended(data.arguments[0:])

    def handle_match(self, args):
        data = args[0]
        gametype = data['GAMETYPE']
        opponent = data['OPPONENT']
        player_to_move = data['PLAYERTOMOVE']
        self.create_game(gametype, opponent)
        self.send_to_gui('match', {'gametype': gametype, 'opponent': opponent, 'playerToMove': player_to_move})

    def handle_yourturn(self, args):
        print(str(args))

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
            turntime = 10  # default for now
            self.send_to_gui('challenged', {'challenger': challenger, 'gameName': game_name,
                                            'challengeNumber': challenge_number, 'turnTime': turntime})

    def game_ended(self, args):
        print(str(args))

    def create_game(self, gametype, opponent):
        print(str(self.challenges))


class Match:
    game = None
    own_player = None
    opponent = None

    def __init__(self, game, own_player, opponent):
        self.game = game
        self.own_player = own_player,
        self.opponent = opponent


