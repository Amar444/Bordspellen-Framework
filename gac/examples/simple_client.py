from client import Client, EVENT_CONNECTED

print("Warning: this will loop forever waiting for incoming messages")
print("from the server. You may want to stop this script using Ctrl-C")
print("")

client = Client()
client.connect()
client.on(EVENT_CONNECTED, lambda m: client.login('Robert'))