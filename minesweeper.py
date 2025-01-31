import tkinter
import random
import math


board_size = 9
mine_number = 15
game_over_flag = False
number_of_clicks = 0

class square:
    def __init__(self):
        self.is_mine = False
        self.neighbour_mines = 0
        self.is_flagged = False
        self.is_visible = False

def reset_board_numbers(board):
    for j in range(1,len(board)-1):
        for k in range(1,len(board[0])-1):
            board[j][k].neighbour_mines = 0

        
def count_neighbours(board):
    for j in range(1,len(board)-1):
        for k in range(1,len(board[0])-1):
            l = board[j][k]
            if board[j-1][k-1].is_mine: l.neighbour_mines += 1
            if board[j-1][k].is_mine: l.neighbour_mines += 1
            if board[j-1][k+1].is_mine: l.neighbour_mines += 1
            if board[j][k-1].is_mine: l.neighbour_mines += 1
            if board[j][k+1].is_mine: l.neighbour_mines += 1
            if board[j+1][k-1].is_mine: l.neighbour_mines += 1
            if board[j+1][k].is_mine: l.neighbour_mines += 1
            if board[j+1][k+1].is_mine: l.neighbour_mines += 1
            
            
def generate_random_board(size, mine_count):
    global board
    board = []
    for i in range(size+2):
        board.append([])
        for j in range(size+2):
            board[i].append(square())

    
    for i in range(mine_count):
        is_clear = False
        while not is_clear:
            x = random.randint(1,len(board)-2)
            y = random.randint(1,len(board[0])-2)
            if board[x][y].is_mine == False:
                board[x][y].is_mine= True
                is_clear = True
            else: continue
    count_neighbours(board)
    return board


def draw_board():
    global board
    global game_over_flag
    global colour_list
    canv.delete("all")
    for i in range(len(board)-2):
        for j in range(len(board[0])-2):
            b = board[i+1][j+1]
            if b.is_visible:
                canv.create_rectangle(600/board_size*j,600/board_size*i,600/board_size*(j+1),600/board_size*(i+1),fill='#ffffff')
                canv.create_text(600/board_size*(j+0.5),600/board_size*(i+0.5),text=str(b.neighbour_mines), fill=colour_list[b.neighbour_mines], font=("Arial", 25))
                if b.is_mine:
                    canv.create_oval(600/board_size*j,600/board_size*i,600/board_size*(j+1),600/board_size*(i+1),fill='#000000')

            elif b.is_flagged:
                canv.create_polygon(600/board_size*j,600/board_size*i,600/board_size*(j),600/board_size*(i+1),600/board_size*(j+1),600/board_size*(i+0.5), fill="#ff0000")
            else: canv.create_rectangle(600/board_size*j,600/board_size*i,600/board_size*(j+1),600/board_size*(i+1),fill='#aaaaaa')
    if game_over_flag:
        canv.create_rectangle(0,0,600,600, fill="#000000")
        canv.create_text(300,300,text="useless pathetic tranny")
    elif check_winstate(board):
        canv.create_rectangle(0,0,600,600, fill="#ffffff")
        canv.create_text(300,300,text="Congartulatuongs!1")
        
            
def toggle_visibility(loc):
    global game_over_flag
    global number_of_clicks
    if str(loc.widget) != ".canv": return
    
    y=math.ceil(loc.y/600*(len(board)-2))
    x=math.ceil(loc.x/600*(len(board)-2))
    if number_of_clicks == 0:
        if board[y][x].is_mine == True:
            board[y][x].is_mine = False
            reset_board_numbers(board)
            count_neighbours(board)
            draw_board()
            print("was mine")
    
    
    
    elif board[y][x].is_mine:
        game_over_flag = True

    flood_fill_clear(board, [y,x])
    number_of_clicks += 1
    draw_board()

    
def flag(loc):
    global number_of_clicks
    y=math.ceil(loc.y/600*(len(board)-2))
    x=math.ceil(loc.x/600*(len(board)-2))
    
    if number_of_clicks == 0:
        if node.is_mine == True:
            node_is_mine = False
            count_neighbours(board)
    number_of_clicks += 1
    
    
    if (not node.is_visible):
        node.is_flagged = not node.is_flagged
        mine_counter_stringvar.set(str(mine_number-1))
    draw_board()


def check_winstate(board):
    count = 0
    while count <= (board_size ** 2)-mine_number:
        for j in range(1,len(board)-1):
            for k in range(1,len(board[0])-1):
                if board[j][k].is_visible == True:
                    count += 1
        return False 
    return True        


def new_game(*args):
    global game_over_flag
    global board_size
    global mine_number
    global board
    global number_of_clicks
    number_of_clicks = 0
    game_over_flag = False
    board = generate_random_board(board_size, mine_number)
    draw_board()



def flood_fill_clear(board, node_pos):
    stack = []
    check_stack = []
    stack.append(node_pos)
    while stack: #look i know okay
        n = stack[0]
        if n in check_stack:
            stack.pop(0)
        check_stack.append(n)
        board[n[0]][n[1]].is_visible = True
        if board[n[0]][n[1]].neighbour_mines == 0:
            stack.append([n[0],n[1]-1])
            stack.append([n[0],n[1]+1])
            stack.append([n[0]-1,n[1]])
            stack.append([n[0]+1,n[1]])
            stack.append([n[0]-1,n[1]-1])
            stack.append([n[0]+1,n[1]+1])
            stack.append([n[0]-1,n[1]+1])
            stack.append([n[0]+1,n[1]-1])
        stack.pop(0)
            
            
    """
    Flood-fill (node):
  1. Set Q to the empty queue or stack.
  2. Add node to the end of Q.
  3. While Q is not empty:
  4.   Set n equal to the first element of Q.
  5.   Remove first element from Q.
  6.   If n is Inside:
         Set the n
         Add the node to the west of n to the end of Q.
         Add the node to the east of n to the end of Q.
         Add the node to the north of n to the end of Q.
         Add the node to the south of n to the end of Q.
  7. Continue looping until Q is exhausted.
  8. Return.
  JUST FILL THEN ADD NEW NODE, SO THAT IT FILLS THE NUMBERS BUT DOESNT USE THEM AS A NODE!!!!!!!!!
"""

root = tkinter.Tk()
colour_list = ["#FFFFFF", "#0000FF", "#209020", "#FF0000", "#000080", "#800000", "#00baca", "#000000", "#666666"]
nav_bar = tkinter.Frame(root)
mine_counter_stringvar = tkinter.StringVar(nav_bar, str(mine_number))
mine_counter = tkinter.Label(nav_bar, textvariable=mine_counter_stringvar)
test_button = tkinter.Button(nav_bar, text="start again", command=new_game)
nav_bar.pack()
mine_counter.pack()
test_button.pack()
canv = tkinter.Canvas(master=root,width=600,height=600, name="canv")
new_game()


root.bind("<Button-1>", toggle_visibility)
root.bind("<Button-3>", flag)

canv.pack()

root.mainloop()
