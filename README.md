# Sokoban-AI

# Start the Game
```shell
cd sokoban
python3 run.py
```

# API Usage
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
- `'up'`
- `'down'`
- `'left'`
- `'right'`