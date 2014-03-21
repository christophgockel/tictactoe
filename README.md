# Tic Tac Toe

A single player Tic Tac Toe implementation with an unbeatable computer opponent, using Python and a terminal ui.

## Playing the Game
Game interface is located in `tictactoe.py`.

To play the game, you can execute this file using the Python interpreter:

```
python tictactoe.py
```

When the game is started, you will be asked which symbol you want to play and who should take the first turn (you or the computer).

## Requirements
* Python >= 2.7 (tested with 2.7.5)
* `mock` >= 1.0.1

`mock` is not needed for playing the game, only when running the tests.
Install with the package manager of your choice.

When using [pip](http://www.pip-installer.org), you can do this via

```
pip install -r requirements.txt
```

Running the tests then is as simple as executing

```
python -m unittest discover
```