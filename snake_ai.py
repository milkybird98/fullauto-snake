import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_B1, KEY_B2
from random import randint

def shift_array(arr, size):
    for i in range(size, 0, -1):
        arr[i] = arr[i-1]

##################################################################
#
# View Model # for snake game render and view
#
##################################################################

class snake_game_view:
    HEIGTH = 10
    WIDTH = 20
    FIELD_SIZE = HEIGTH * WIDTH
    win = None

    def __init__(self,HEIGTH,WIDTH):
        self.HEIGTH=HEIGTH
        self.WIDTH=WIDTH
        self.FIELD_SIZE=HEIGTH*WIDTH
        curses.initscr()
        self.win = curses.newwin(HEIGTH+2, WIDTH+2, 0, 0)
        self.win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.win.border(0)
        self.win.nodelay(1)
    
    def draw_timeout(self,time):
        self.win.timeout(time)

    def draw_menu(self):
        self.win.addstr(self.HEIGTH//2-1, 2, "UP: AI")
        self.win.addstr(self.HEIGTH//2, 2, "DOWN: Manuly")
        self.win.addstr(self.HEIGTH//2+1, 2, "Press to choose")

    def close(self):
        curses.endwin()

    def draw_food(self,food):
        self.win.addch(food//self.WIDTH+1, food%self.WIDTH+1, '@')

    def draw_info(self, info):
        self.win.border(0)
        self.win.addstr(0, 2, ' ' + str(info))

    def draw_snake(self,snake,snake_size):
        self.win.addch(snake[snake_size]//self.WIDTH+1, snake[snake_size]%self.WIDTH+1, ' ')
        

        for i in range(snake_size):
            position = snake[i]
            self.win.addch(position//self.WIDTH+1, position%self.WIDTH+1, '*')
            if i > 2:
                break
        
        self.win.addch(snake[0]//self.WIDTH+1, snake[0]%self.WIDTH+1, '#')

    def get_key_input(self):
        event = self.win.getch()
        return event

##################################################################
#
# Game Model # for snake game ruler and operation
#
##################################################################

class snake_game_model:
    HEIGTH = 15
    WIDTH = 30
    FIELD_SIZE = HEIGTH * WIDTH

    HEAD = 0

    FOOD = 0
    UNDEFINED = (HEIGTH + 1) * (WIDTH + 1)
    SNAKE = 2 * UNDEFINED

    LEFT = -1
    RIGHT = 1
    UP = -WIDTH
    DOWN = WIDTH

    mov = []

    ERR = -999

    board = []
    snake = []
    snake_size = 0
    food = 0
    
    def __init__(self,HEIGTH=15,WIDTH=30):
        self.HEIGTH=HEIGTH
        self.WIDTH=WIDTH
        self.FIELD_SIZE=HEIGTH*WIDTH    

        self.board = [0] * self.FIELD_SIZE
        self.snake = [0] * (self.FIELD_SIZE+1)
        self.snake[self.HEAD] = 1*WIDTH+1
        self.snake_size = 1 
        self.food = 3 * WIDTH + 3

        self.UNDEFINED = (HEIGTH + 1) * (WIDTH + 1)
        self.SNAKE = self.UNDEFINED + 1
        
        self.UP = -WIDTH
        self.DOWN = WIDTH
        self.mov = [self.LEFT, self.RIGHT, self.UP, self.DOWN]

    def get_move_length(self,direction):
        return self.mov[direction]

    def is_cell_free(self, cell_position):
        return not (cell_position in self.snake[:self.snake_size]) 

    def is_move_possible(self, cell_position, move):
        flag = False
        if move == self.LEFT:
            flag = True if cell_position%self.WIDTH > 0 else False
        elif move == self.RIGHT:
            flag = True if cell_position%self.WIDTH < (self.WIDTH-1) else False
        elif move == self.UP:
            flag = True if cell_position > (self.WIDTH-1) else False
        elif move == self.DOWN:
            flag = True if cell_position < (self.FIELD_SIZE-self.WIDTH) else False
        return flag

    def new_food(self):
        cell_free = False
        while not cell_free:
            w = randint(0, self.WIDTH-1)
            h = randint(0, self.HEIGTH-1)
            self.food = h * self.WIDTH + w
            cell_free = self.is_cell_free(self.food)

    def make_move(self, move):
        shift_array(self.snake, self.snake_size+1)

        if self.is_move_possible(self.snake[self.HEAD],move) == False:
            return 'die'

        self.snake[0] += move

        if self.snake[self.HEAD] == self.food:
            self.board[self.snake[self.HEAD]] = self.SNAKE 
            self.snake_size += 1
            if self.snake_size < self.FIELD_SIZE: self.new_food()
            return 'eat'
        elif self.snake[self.HEAD] in self.snake[1:self.snake_size]:
            return 'die'
        else:
            self.board[self.snake[self.HEAD]] = self.SNAKE
            self.board[self.snake[self.snake_size]] = self.UNDEFINED
            return None

##################################################################
#
# AI Model # for snake game inside AI implementation
#
##################################################################

class snake_game_ai(snake_game_model):
    virtual_board = []
    virtual_snake = []
    virtual_snake_size = 0
    follow_step = 0

    def update_data(self,board,food,snake,snake_size):
        self.board = board[:]
        self.food = food
        self.snake = snake[:]
        self.snake_size = snake_size

    def is_cell_free(self, cell_position, snake, snake_size):
        return not (cell_position in snake[:snake_size]) 

    def reset_virtual_board(self):
        for i in range(self.FIELD_SIZE):
            if i == self.food:
                self.virtual_board[i] = self.FOOD
            elif self.is_cell_free(i, self.virtual_snake,self.virtual_snake_size):
                self.virtual_board[i] = self.UNDEFINED
            else:
                self.virtual_board[i] = self.SNAKE   

    def reset_board(self):
        for i in range(self.FIELD_SIZE):
            if i == self.food:
                self.board[i] = self.FOOD
            elif self.is_cell_free(i, self.snake, self.snake_size):
                self.board[i] = self.UNDEFINED
            else:
                self.board[i] = self.SNAKE

    def calculate_food_distance_DFS(self):
        DFSqueue = []
        DFSqueue.append(self.food)
        inDFSqueue = [0] * self.FIELD_SIZE
        found = False
        while len(DFSqueue)!=0: 
            cell_position = DFSqueue.pop(0)
            if inDFSqueue[cell_position] == 1: continue
            inDFSqueue[cell_position] = 1
            for i in range(4):
                if self.is_move_possible(cell_position, self.mov[i]):
                    if cell_position + self.mov[i] == self.snake[self.HEAD]:
                        found = True
                    if self.board[cell_position+self.mov[i]] < self.SNAKE:
                        
                        if self.board[cell_position+ self.mov[i]] > self.board[cell_position]+1:
                            self.board[cell_position+ self.mov[i]] = self.board[cell_position] + 1
                        if inDFSqueue[cell_position+ self.mov[i]] == 0:
                            DFSqueue.append(cell_position+ self.mov[i])

        return found

    def calculate_food_distance_DFS_invirtual(self, food):
        DFSqueue = []
        DFSqueue.append(food)
        inDFSqueue = [0] * self.FIELD_SIZE
        found = False
        while len(DFSqueue)!=0: 
            cell_position = DFSqueue.pop(0)
            if inDFSqueue[cell_position] == 1: continue

            inDFSqueue[cell_position] = 1
            for i in range(4):
                if self.is_move_possible(cell_position, self.mov[i]):
                    if cell_position + self.mov[i] == self.virtual_snake[self.HEAD]:
                        found = True
                    if self.virtual_board[cell_position+self.mov[i]] < self.SNAKE:
                        
                        if self.virtual_board[cell_position+ self.mov[i]] > self.virtual_board[cell_position] + 1:
                            self.virtual_board[cell_position+ self.mov[i]] = self.virtual_board[cell_position] + 1
                        if inDFSqueue[cell_position+ self.mov[i]] == 0:
                            DFSqueue.append(cell_position+ self.mov[i])

        return found

    def choose_shortest_move(self, psnake, pboard):
        move = self.ERR
        min = self.SNAKE
        for i in range(4):
            if self.is_move_possible(psnake[self.HEAD], self.mov[i]) and pboard[psnake[self.HEAD]+self.mov[i]]<min:
                min = pboard[psnake[self.HEAD]+self.mov[i]]
                move = self.mov[i]
        return move

    def choose_longest_move(self, psnake, pboard):
        move = self.ERR
        max = -1
        for i in range(4):
            if self.is_move_possible(psnake[self.HEAD], self.mov[i]) and pboard[psnake[self.HEAD]+self.mov[i]]<self.UNDEFINED and pboard[psnake[self.HEAD]+self.mov[i]]>max:
                max = pboard[psnake[self.HEAD]+self.mov[i]]
                move = self.mov[i]
        return move

    def is_tail_reachable(self):
        self.virtual_board[self.virtual_snake[self.virtual_snake_size-1]] = 0 
        self.virtual_board[self.food] = self.SNAKE 
        result = self.calculate_food_distance_DFS_invirtual(self.virtual_snake[self.virtual_snake_size-1]) 
        if result:
            for i in range(4):
                if self.is_move_possible(self.virtual_snake[self.HEAD], self.mov[i]) and self.virtual_snake[self.HEAD]+self.mov[i]==self.virtual_snake[self.virtual_snake_size-1] and self.virtual_snake_size>3:
                    result = False

        return result

    def follow_body_node(self,index):
        self.virtual_snake_size = self.snake_size
        self.virtual_snake = self.snake[:]

        self.reset_virtual_board() 

        self.virtual_board[self.virtual_snake[self.virtual_snake_size-1-index]] = self.FOOD
        self.virtual_board[self.food] = self.SNAKE

        if self.calculate_food_distance_DFS_invirtual(self.virtual_snake[self.virtual_snake_size-1-index]) == False:
            return self.ERR

        self.virtual_board[self.virtual_snake[self.virtual_snake_size-1-index]] = self.SNAKE 

        return self.choose_longest_move(self.virtual_snake, self.virtual_board)

    def make_any_move(self):
        move = self.ERR
        self.virtual_snake_size = self.snake_size
        self.virtual_snake = self.snake[:]

        self.reset_virtual_board()
        self.calculate_food_distance_DFS_invirtual(self.food)

        min = self.SNAKE
        for i in range(4):
            if self.is_move_possible(self.virtual_snake[self.HEAD], self.mov[i]) and self.virtual_board[self.virtual_snake[self.HEAD]+self.mov[i]] < min:
                min = self.virtual_board[self.virtual_snake[self.HEAD]+self.mov[i]]
                move = self.mov[i]

        return move

    def simulate_shortest_move(self):
        self.virtual_board = self.board[:]
        self.virtual_snake = self.snake[:]
        self.virtual_snake_size = self.snake_size

        self.reset_virtual_board()
        
        while True:
            if self.calculate_food_distance_DFS_invirtual(self.food) == False:
                return False 

            move = self.choose_shortest_move(self.virtual_snake, self.virtual_board)
            shift_array(self.virtual_snake, self.virtual_snake_size)
            self.virtual_snake[self.HEAD] += move 

            if self.virtual_snake[self.HEAD] == self.food:
                self.virtual_snake_size += 1
                self.reset_virtual_board()
                self.virtual_board[self.food] = self.SNAKE
                return True
            else:
                self.virtual_board[self.virtual_snake[self.HEAD]] = self.SNAKE
                self.virtual_board[self.virtual_snake[self.virtual_snake_size]] = self.UNDEFINED

    def simulate_find_way(self,game,view):
        next_move = self.ERR
        ai_operation = ''

        if game.snake_size == self.FIELD_SIZE-1:
            self.reset_board()
            self.calculate_food_distance_DFS()
            next_move = self.choose_shortest_move(self.snake,self.board)
            ai_operation = 'final_eat'
        elif self.simulate_shortest_move() and self.is_tail_reachable():
            self.reset_board()
            self.calculate_food_distance_DFS()
            next_move = self.choose_shortest_move(self.snake,self.board)
            self.follow_step = 0
            ai_operation = 'eat'
        elif self.follow_step < (20 * self.FIELD_SIZE): 
            for i in range(1):
                next_move = self.follow_body_node(i)
                if next_move != self.ERR:
                    ai_operation = 'tail: '+ str(i)
                    self.follow_step += 2
                    break

        if next_move == self.ERR:
            next_move = self.make_any_move()
            self.follow_step -= 1
            ai_operation = 'any'

        view.draw_info(ai_operation)

        return next_move

##################################################################
#
# Controler Layer # for snake game input data choose
#
##################################################################

def ai_move(game,view,ai):
    ai.update_data(game.board,game.food,game.snake,game.snake_size)
    next_move = ai.simulate_find_way(game,view)
    return next_move

def key_move(game,view,key):
    if key == KEY_LEFT:
        next_move = game.get_move_length(0)
    if key == KEY_RIGHT:
        next_move = game.get_move_length(1)
    if key == KEY_UP:
        next_move = game.get_move_length(2)
    if key == KEY_DOWN:
        next_move = game.get_move_length(3)
    return next_move

WIDTH = 15
HEIGTH = 30

AI_STEP_DELAY = 0
MAN_STEP_DELAY = 500

AI_MODE = 1
MANULY_MODE = 2

Mode = None

view = snake_game_view(WIDTH,HEIGTH)
game = snake_game_model(WIDTH,HEIGTH)
ai = snake_game_ai(WIDTH,HEIGTH)

view.draw_info('Choose Mode')
view.draw_menu()
view.draw_timeout(-1)

while True:
    event = view.get_key_input()
    if event == KEY_UP:
        Mode = AI_MODE
        view.draw_timeout(AI_STEP_DELAY)
        break
    elif event == KEY_DOWN:
        Mode = MANULY_MODE
        view.draw_timeout(MAN_STEP_DELAY)
        break
    elif event == 27:
        view.close()
        exit()

view.win.erase()

key = KEY_RIGHT
next_move = game.get_move_length(1)

game.new_food()
view.draw_food(game.food)

while True:
    # receive keyboard input
    event = view.get_key_input()
    key = key if event == -1 else event
    if key == 27:
        break

    if Mode == AI_MODE:
        next_move = ai_move(game,view,ai)
    elif Mode == MANULY_MODE:
        view.draw_info("Length: " + str(game.snake_size))
        next_move = key_move(game,view,key)

    if next_move == game.ERR:
        #view.draw_info('game over, press ESC to exit')
        break        

    res = game.make_move(next_move)
    if res != 'die':
        view.draw_snake(game.snake,game.snake_size)

    if res == 'die':
        view.draw_info('game over, press ESC to exit')
        break
    elif res == 'eat':
        view.draw_food(game.food)
    if game.snake_size == game.FIELD_SIZE :
        view.draw_info('game success, press ESC to exit')


while key != 27:
    event = view.get_key_input()
    key = key if event == -1 else event


view.close()
print("\nScore - " + str(game.snake_size))
