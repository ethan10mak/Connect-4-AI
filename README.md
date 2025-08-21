# Connect-4-AI

This project was completed as part of an assignment in UCSC CSE 140: Artificial Intelligence.

## Dependencies:
This code has been tested and run on Ubuntu WSL. The `numpy` package is required to run the files.

## Playing:
To run the game, go to the directory with the file `ConnectFour.py` and run the following:
`` 
python3 ConnectFour.py <arg1> <arg2>
``
`<arg1>` and `<arg2>` can be replaced with the following specifiers:
- `human`: A human controlled player
- `random`: A randomly controlled player
- `ai`: An AI player

Running this will display the game board and a button for the next move.

If you choose the human player, when you press the next move button, the terminal will prompt you for the player's move. The valid inputs are from 0-6, representing a column from right to left.
