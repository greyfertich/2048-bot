# 2048-bot
AI bot written in Python that can play 2048 both locally and in the browser

## Running
### Local (command line) version
```
python3 play2048.py
```

### Browser version
To run the bot in the browser, open www.play2048.co in your browser and update x_coords and y_coords in tiles.py with the pixel indices for each row and column of the game. A more robust system will be coming in the future.
Then, run play2048.py in the command line with the browser window fully visible:
```
python3 play2048.py --mode=browser
```

## Performance
In its default configuration, the AI can achieve the 2048 tile __ percent of the time.
Here are the proportions of games which ended with the specific tile as the highest value:
256: 2%
512: 6%
1024: 33%
2048: 46%
4096: 12%

## Implementation
My implementation uses the Expectimax algorithm which is used to maximize the chances of winning for a player assuming that the opponent does not play optimally. In the case of 2048, the player is the user playing the game and the opponent is the computer that randomly generates a tile of size 2 or 4 and places it on an empty spot on the board after ever move the user makes.
