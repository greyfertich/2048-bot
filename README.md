# 2048-bot
AI bot written in Python that can play 2048 both locally and in the browser

## Running the local (command line) version
```
python3 play2048.py
```

## Running the browser version
To run the bot in the browser, open www.play2048.co in your browser and update x_coords and y_coords in tiles.py with the pixel indices for each row and column of the game. A more robust system will be coming in the future.
Then, run play2048.py in the command line with the browser window fully visible:
```
python3 play2048.py --mode=browser
```
