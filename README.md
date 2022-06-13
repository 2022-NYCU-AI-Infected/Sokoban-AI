# Sokoban-AI

# Environment
The environment is tested on Python 3.10
```shell
pip3 install numpy pygame
```

# Play the Game
`run.py` will run the game and can be controlled by user with keyboard input.
```shell
cd sokoban
python3 run.py
```
- Arrow keys to move the character
- `q`: quit the game
- `d`: undo

# Solve the Sokoban!
Run `ans.py` to auto run selected methods to solve the puzzle.

## Available Methods
- `dfs`
- `bfs`
- `ucs`
- `astar`

## Output
It will output the result with following format:
```python3
{Level},{Method name},{endTime - startTime},{cache size},{Answer}
```
It can be copied to Google Sheets and be formated correctly.

# API Usage
`sokobanAPI.py` consists of functions let `solver.py` to interact the game.

## Import
```python3
from sokobanAPI import API

game = API(1) # 1 is for game level
game.start() # Start the game
```

## Move
```
game.move(direction)
```
`direction` can be one of these:
- `'U'`
- `'D'`
- `'L'`
- `'R'`

## Auto Run
```python3
game.playSeq(sequence, delay=0.5)
```
`sequence` is a string that consist of a sequence of movement.
> e.g. `'UULDR'` will move Up, Up, Left, Down, Right