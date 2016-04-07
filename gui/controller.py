from gui.commands import *
import json


class GUIController:
    """ Provides a controller to link the GUI and a Client (so essentially the server) together """
    gui = None
    client = Client()
    nickname = None
    commands = None

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
            CommandCreateChallange
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

    def send_to_gui(self, listener, details, status, status_message):
        """ sends information to the GUI of the controller """
        details['status'] = status
        details['statusMessage'] = status_message

        self.gui.send_to_client(json.dumps(
            {
                'listener': listener,
                'detail': details
            }
        ))
