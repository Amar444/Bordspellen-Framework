All the logic for the visual side of the application is placed in this folder. 

TO DO
Coordinates of new move sent through javascript to Python application.
GUI obtains data from application(possible classes: Board, Game, Player?) to enrich the GUI
    includes:
        board data,
        game data,
        win or loss,
        Players in lobby,

Board data: gets updated after every move, or done on an interval?
Game data: same as board data.
Win or loss: is received after a game. signals the end of the game?
Players in lobby: Updated on short interval to insure up to date lobby list.(Removal of previous list? or missing players?)