from random import randint as rr, shuffle, choice, choices


class Domino:
  UP_KEY = 7
  ENDS_CRIT = 8

  def __init__(self, hand):
    self.hand = hand
    self.player = self.computer = []
    self.snake = choices(doubles := [[i] * 2 for i in range(self.UP_KEY)], [2 ** i for i in range(len(doubles))])
    self.left_end = self.right_end = self.snake_ends = None
    self.stock = [[i, j] for i in range(self.UP_KEY) for j in range(i, self.UP_KEY)]


  def get_cmd(self):
    while True:
      try:
        dom_num = input()
        if not dom_num.strip().lstrip('-').isdigit() and len(dom_num) or abs(int(dom_num)) > len(self.player):
          print('Invalid input. Please try again.')
          continue
        return int(dom_num)
      except ValueError:
        return self.get_ai_cmd()

  
  def get_ai_cmd(self):
    return rr(-len(self.computer), len(self.computer))

  
  def allocate(self):
    while any(dom >= self.snake[0] for dom in self.stock[self.hand * 2:] if len(set(dom)) == 1) or self.stock.remove(self.snake[0]):
      shuffle(self.stock)
    self.stock, self.player, self.computer = [self.stock[:self.hand * 2]] + [self.stock[i: i + self.hand] for i in range(self.hand * 2, len(self.stock), self.hand)]
    self.player, self.computer = [self.player, self.computer][::choices((-1, 1))[0]] 
    
  def stats(self, playing):
    print("=" * 70)
    player_data = '\n'.join(f'{i}: {dom}' for i, dom in enumerate(self.player, 1))
    print('Stock size: {}\nComputer size: {}\n\n{}\n\nPlayer pieces: \n{}\n'.format(
      len(self.stock), 
      len(self.computer), 
      ''.join(map(str, (self.snake[3:], '...', self.snake[-3:]))), 
      player_data))
    print(('It\'s your turn to make a move. Enter your command.', 'Computer is about to make a move. Press Enter to continue...')[playing == self.computer])


  def make_move(self, playing, dom_num):
    if dom_num:
      self.snake.insert(
        (0, len(self.snake))[dom_num > 0], 
        playing.pop(abs(dom_num) - 1)
      ) 
    else:
      playing.append(self.stock.pop())

  def check_game_status(self):
    crit = [-1, self.right_end][len({self.left_end, self.right_end}) % 2]
    snake_ends_8 = sum(self.snake, []).count(crit) < self.ENDS_CRIT
    return all((self.player, self.computer, snake_ends_8))

  def update_snake_ends(self):
    self.left_end, *_, self.right_end = sum(self.snake, [])
    self.snake_ends = [self.left_end, self.right_end]

  def main(self, game=True):
    self.allocate()
    curr_player = (self.player, self.computer)[len(self.player) < len(self.computer)]

    while game:
      self.update_snake_ends()
      
      self.stats(curr_player)
      self.make_move(playing=curr_player, dom_num=self.get_cmd())
      
      curr_player = (self.player, self.computer)[curr_player == self.player]
      game = self.check_game_status()
    

my_game = Domino(7)
my_game.main()
