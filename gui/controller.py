from gac.client import *
from gui.commands import *
import json

"""
NOTE:
What still needs to be done:
- Add comments/documentation
"""


class GUIController:
    gui = None
    client = Client()
    nickname = None
    commands = None

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.commands = (
            CommandLogin,
            CommandLogout,
            CommandPlayerlist,
            CommandGamelist,
            CommandCreateChallange
        )

    def handle_message(self, message):
        message = self.handle_json(message)

        try:
            command = message['command']
        except Exception as e:
            print("JSON does not contain a command")
            command = 'No command found'

        for current_command in self.commands:
            if current_command.command == command:
                current_command(self, self.client, message)

    def handle_json(self, json_str):
        try:
            json_str = json.loads(str(json_str))
        except Exception as e:
            json_str = None
            print("Could not convert JSON, exception: {}", e)
        return json_str

    def send_to_gui(self, listener, details, status, status_message):
        details['status'] = status
        details['statusMessage'] = status_message

        self.gui.send_to_client(json.dumps(
            {
                'listener': listener,
                'detail': details
            }
        ))
