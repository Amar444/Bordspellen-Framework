import time
import threading
from gac.client.client import *


class AstleySpammer(threading.Thread):
    astley = ["We're no strangers to love, you know the rules and so do I",
                "A full commitments what I'm thinking of",
                "You wouldn't get this from any other guy.",
                "I just wanna tell you how I'm feeling, gotta make you understand.",
                "Never gonna give you up, never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry, never gonna say goodbye",
                "Never gonna tell a lie and hurt you.",
                "We've known each other for so long",
                "Your heart's been aching, but you're too shy to say it",
                "Inside we both know what's been going on",
                "We know the game and we're gonna play it.",
                "And if you ask me how I'm feeling, don't tell me you're too blind to see.",
                "Never gonna give you up, never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry, never gonna say goodbye",
                "Never gonna tell a lie and hurt you.",
                "Never gonna give you up, never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry, never gonna say goodbye",
                "Never gonna tell a lie and hurt you.",
                "(Ooh, give you up, ooh, give you up)",
                "Never gonna give, never gonna give (Give you up)",
                "Never gonna give, never gonna give (Give you up)",
                "We've known each other for so long",
                "Your heart's been aching, but you're too shy to say it",
                "Inside we both know what's been going on",
                "We know the game and we're gonna play it.",
                "I just wanna tell you how I'm feeling, gotta make you understand.",
                "Never gonna give you up, never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry, never gonna say goodbye",
                "Never gonna tell a lie and hurt you.",
                "Never gonna give you up, never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry, never gonna say goodbye",
                "Never gonna tell a lie and hurt you.",
                "Never gonna give you up, never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry, never gonna say goodbye",
                "Never gonna tell a lie and hurt you."]
    client = None
    receiver = None

    def __init__(self, client, receiver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.receiver = receiver

    def run(self):
        length = len(self.astley)
        counter = 0

        while True:
            # print(self.astley[counter])
            self.client.send(OutgoingCommand('message', '"' + self.receiver + '"', '"' + self.astley[counter] + '"'))
            counter = counter + 1
            if counter >= length:
                # counter = 0
                break
            time.sleep(3)

# AstleySpammer().start()
