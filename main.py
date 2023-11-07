from random import randint as rr, shuffle, choices


class Domino:
    HEADING = "=" * 70
    UP_KEY = 7
    DRAW_CRIT = 8
    SNAKE_MASK = '...'
    MASK_CRIT = 6

    def __init__(self, hand):
        self.hand = hand
        self.player = self.computer = []
        self.left_end = self.right_end = self.snake_ends = self.no_draw = None
        self.snake = choices(doubles := [
            [i] * 2 for i in range(self.UP_KEY)], [2 ** i for i in range(len(doubles))])
        self.stock = [[i, j] for i in range(self.UP_KEY) for j in range(i, self.UP_KEY)]

    def get_cmd(self):
        while True:
            try:
                dom_num = input()
                if not dom_num.lstrip('-').isdigit() and len(dom_num) or \
                        abs(int(dom_num)) > len(self.player):
                    print('Invalid input. Please try again.')
                    continue
                return int(dom_num)
            except ValueError:
                return self.get_ai_cmd()

    def get_ai_cmd(self):
        return rr(-len(self.computer), len(self.computer))

    def allocate(self):
        while any(dom >= self.snake[0] for dom in self.stock[self.hand * 2:]
                  if len(set(dom)) == 1) or self.stock.remove(self.snake[0]):
            shuffle(self.stock)
        self.stock, self.player, self.computer = \
            [self.stock[:self.hand * 2]] + [self.stock[i: i + self.hand] \
                                            for i in range(self.hand * 2, len(self.stock), self.hand)]
        self.player, self.computer = [self.player, self.computer][::choices([-1, 1])[0]]

    def stats(self, playing, game, serp_end=MASK_CRIT // 2):
        player_data = '\n'.join(f'{i}: {dom}' for i, dom in enumerate(self.player, 1))

        print('{heading}\nStock size: {}\nComputer size: {}\n\n{snake}\n\nPlayer pieces:\n{}\n{}Status:'
              .format(len(self.stock), len(self.computer), player_data, '\n'[:len(self.player) ^ 0],
                      heading=self.HEADING,
                      snake=''.join(map(str, self.snake))
                      .replace(('-1', ''.join(map(str, self.snake[serp_end:len(self.snake) - serp_end]))
                                )[len(self.snake) > self.MASK_CRIT], self.SNAKE_MASK)), end=' ')

        if game:
            print(('It\'s your turn to make a move. Enter your command.',
                   'Computer is about to make a move. Press Enter to continue...'
                   )[playing == self.computer])
        else:
            print(' '.join(('The game is over.', (
                ('It\'s a draw!',) * 2, ('The computer won!', 'You won!')
            )[self.no_draw][len(self.player) < len(self.computer)])))

    def make_move(self, playing, dom_num):
        if dom_num:
            self.snake.insert((0, len(self.snake))[dom_num > 0], playing.pop(abs(dom_num) - 1))
        elif self.stock:
            playing.append(self.stock.pop())

    def check_game_status(self):
        crit = (-1, self.left_end)[len({self.left_end, self.right_end}) % 2]
        self.no_draw = sum(self.snake, []).count(crit) < self.DRAW_CRIT
        return all((self.player, self.computer, self.no_draw))

    def update_snake_ends(self):
        self.left_end, *_, self.right_end = sum(self.snake, [])
        self.snake_ends = self.left_end, self.right_end

    def run(self, game=True):
        self.allocate()
        curr_player = (self.player, self.computer)[len(self.player) < len(self.computer)]

        while game:
            self.stats(curr_player, game)

            self.make_move(playing=curr_player, dom_num=self.get_cmd())
            self.update_snake_ends()
            game = self.check_game_status()

            curr_player = (self.player, self.computer)[curr_player == self.player]
        self.stats(curr_player, game)


my_game = Domino(7)
my_game.run()
