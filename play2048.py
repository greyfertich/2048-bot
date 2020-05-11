from gamecontroller import GameController
import time
from absl import app, flags
import sys

FLAGS = flags.FLAGS

flags.DEFINE_integer('n_games', 1, 'Number of games to play')
flags.DEFINE_integer('depth', 1, 'Depth of expectimax search')
flags.DEFINE_enum('opt', 'expectimax', ['expectimax', 'chain'],
                  'Specifies the type of move optimization')
flags.DEFINE_enum('mode', 'local', ['local','browser'],
                  'Species local or browser play')
flags.DEFINE_integer('move_delay', 0, 'Minimum wait time between moves')
flags.DEFINE_boolean('display_board', True, 'Display the board after each move')

def main(argv):
    loading_width = 50
    scores = []
    start = time.time()
    for i in range(FLAGS.n_games):
        controller = GameController(gameplayMode=FLAGS.mode, optimizer=FLAGS.opt,
                        depth=FLAGS.depth, display_board=FLAGS.display_board)
        grid = controller.run(moveDelay=FLAGS.move_delay)
        scores.append(max(grid))

    end = time.time() - start

    print('Highest score: {}'.format(0 if len(scores) == 0 else max(scores)))
    d = {}
    for i in scores:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    for i in sorted(list(d)):
        print('{}: {}'.format(i, d[i]/len(scores)))
    print('Average time per game: {} seconds'.format(end/(1 if FLAGS.n_games == 0 else FLAGS.n_games)))

if __name__ == '__main__':
    app.run(main)
