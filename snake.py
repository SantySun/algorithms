from collections import deque

class Snake:
  def __init__(self) -> None:
    board = [
      [
        { "fruit": False, "snake": False } for _ in range(100)
      ] for _ in range(100)
    ]
    self.board = board
    '''
    Initially, the snake has 3 pixels, moving from left to right
    '''
    self.direction = "right"
    snake_pixels = [[49, 49], [49, 50], [49, 51]]
    snake = deque()
    for x, y in snake_pixels:
      self.board[x][y]["snake"] = True
      snake.appendleft([x, y])
    self.snake = snake
  

  def down(self):
    # change direction
    if self.direction != "up":
      self.direction = "down"
  
  def up(self):
    if self.direction != "down":
      self.direction = "up"
  
  def right(self):
    if self.direction != "left":
      self.direction = "right"
  
  def left(self):
    if self.direction != "right":
      self.direction = "left"
  

  def move(self):
    # pop tail
    x, y = self.snake.pop()
    self.snake[x][y]["snake"] = False

    # check next pixel
    i, j = self.snake.popleft()
    self.snake.appendleft([i, j])
    next_pixel = None
    after_next = None
    if self.direction == "right":
      next_pixel = [i, j + 1]
      after_next = [i, j + 2]
    elif self.direction == "up":
      next_pixel = [i - 1, j]
      after_next = [i - 2, j]
    elif self.direction == "left":
      next_pixel = [i, j - 1]
      after_next = [i, j - 2]
    else:
      next_pixel = [i + 1, j]
      after_next = [i + 2, j]

    # check if the snake hits the wall
    i, j = next_pixel
    if i >= 100 or i < 0:
      raise Exception
    if j >= 100 or j < 0:
      raise Exception
    
    # check if the next pixel is within snake body
    if self.board[i][j]["snake"]:
      raise Exception
    
    # append head
    self.board[i][j]["snake"] = True
    self.snake.appendleft([i, j])

    # check if the next pixel has fruit

  def assign_fruit(self, x, y):
    pixel = self.board[x][y]
    if not pixel["snake"] and not pixel["fruit"]:
      pixel["fruit"] = True
