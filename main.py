import tkinter as tk
from tkinter import messagebox
import random as rnd
from PIL import Image, ImageTk


class Plot:
    # These are the core variables to control the game
    # I put them in the Plot class so that I wouldn't need to pass them through the function calls
    grid = []
    rows, cols, mines, revealed = 0, 0, 0, 0
    first_click = True
    b_size = 0
    sel = None
    t_start, secs, mins = False, 0, 0

    def __init__(self, row, col, val, flag, dug):
        self.row = row
        self.col = col
        self.val = val
        self.flag = flag
        self.dug = dug


def clear_game_frame():
    # grid_frame Frame sits in game_frame Frame and is created in the root but gridded in the create_board function
    # so to clear the game properly, I need to forget anything created in the root
    # and destroy everything else which will be created again later
    widgets = [i for i in grid_frame.grid_slaves()]
    for i in widgets:
        i.destroy()
    widgets = [i for i in game_frame.grid_slaves()]
    for i in widgets:
        i.grid_forget()


# This function takes the selected plot and returns the 8 surrounding plots discluding the original
# Since this function is called to return both instances of the Plot class and plot locations
# I felt it better that it returns a list of tuples rather than one or the other.
def find_neighbours(center):
    neighbours = []
    for x in range(center.row - 1, (center.row + 1) + 1):
        for y in range(center.col - 1, (center.col + 1) + 1):
            if x == -1 or x == Plot.rows or y == -1 or y == Plot.cols:
                pass
            elif (x, y) == (center.row, center.col) or Plot.grid[x][y].val == 'B' or Plot.grid[x][y].dug:
                pass
            else:
                neighbours.append((x, y))
    return neighbours


# This function detects if a plot is flagged or not and is called by a bind function on right click
# if there's no flag, it places a flag and disables the plot
# otherwise, it removes the flag and re-enables the plot
# r and c are the standard variables I used to represent Rows and Columns
# in both the Plot.grid instance array and finding the correct plot widget
def set_flag(event, r, c):
    flag_img_get = Image.open('assets/flag.png').resize((Plot.b_size, Plot.b_size))
    flag_img = ImageTk.PhotoImage(flag_img_get)
    blank_img_get = Image.open('assets/button.png').resize((Plot.b_size, Plot.b_size))
    blank_img = ImageTk.PhotoImage(blank_img_get)
    to_be_flagged = grid_frame.grid_slaves(row=r, column=c)[0]
    if not Plot.grid[r][c].flag and not Plot.grid[r][c].dug:
        to_be_flagged.config(image=flag_img)
        to_be_flagged.image = flag_img
        Plot.grid[r][c].flag = True
    elif Plot.grid[r][c].flag and not Plot.grid[r][c].dug:
        to_be_flagged.config(image=blank_img)
        to_be_flagged.image = blank_img
        Plot.grid[r][c].flag = False
    else:
        pass


# I created a function to return the clock number asset for whichever number is required
# without this, I would need to create 4 identical scripts for each of the numbers in the timer
def timer_num(x):
    timer_num_img_get = Image.open(f'assets/clock-{x}.png').resize((50, 60))
    timer_num_img = ImageTk.PhotoImage(timer_num_img_get)
    return timer_num_img


# I still needed to create 4 almost identical scripts to assign the assets to the 4 digits in the timer
# but I felt it was a good compromise since the timer_num function makes them shorter
def timer():
    secs_units_num = timer_num(str(Plot.secs).zfill(2)[1])
    timer_secs_units.config(image=secs_units_num)
    timer_secs_units.image = secs_units_num

    secs_tens_num = timer_num(str(Plot.secs).zfill(2)[0])
    timer_secs_tens.config(image=secs_tens_num)
    timer_secs_tens.image = secs_tens_num

    mins_units_num = timer_num(str(Plot.mins).zfill(2)[1])
    timer_mins_units.config(image=mins_units_num)
    timer_mins_units.image = mins_units_num

    mins_tens_num = timer_num(str(Plot.mins).zfill(2)[0])
    timer_mins_tens.config(image=mins_tens_num)
    timer_mins_tens.image = mins_tens_num

    # Ultra simple timer script. The timer is always running but only counts when t_start is True
    if Plot.t_start:
        Plot.secs += 1
        if Plot.secs == 60:
            Plot.mins += 1
            Plot.secs = 0
    ms.after(1000, timer)


# Upon winning or losing the game, this function reveals all of the mines on the board
# displaying an exploded mine on losing and a safe mine on winning
def reveal_all(x):
    # I felt it best to use an f-string rather than an if statement
    # to allow flexibility in retrieving the correct asset and keep the code shorter
    bomb_img_get = Image.open(f'assets/{x}.png').resize((Plot.b_size, Plot.b_size))
    bomb_img = ImageTk.PhotoImage(bomb_img_get)
    for r in Plot.grid:
        for c in r:
            if c.val == 'B':
                bomb = grid_frame.grid_slaves(row=c.row, column=c.col)[0]
                bomb.config(image=bomb_img)
                bomb.image = bomb_img


# If the player chooses to replay the game, this function resets all of the variables in the Plot class
# as well as resets the board weights for the set_difficulty function
# to restart the game and bypass the instructions
def reset_all():
    Plot.grid = []
    Plot.rows, Plot.cols, Plot.mines, Plot.revealed = 0, 0, 0, 0
    Plot.first_click = True
    Plot.sel = None
    Plot.t_start, Plot.secs, Plot.mins = False, 0, 0
    game_frame.columnconfigure(0, weight=1)
    game_frame.columnconfigure(1, weight=1)
    game_frame.columnconfigure(2, weight=1)
    game_frame.rowconfigure(0, weight=0)
    set_difficulty()


# Called when the win conditions are met
def win_cond():
    Plot.t_start = False
    reveal_all('mine')
    win_msg = """Congratulations! You found all the mines!
            Would you like to play again?
        """
    win_game = messagebox.askyesno('You won!', win_msg)
    if win_game:
        reset_all()
    else:
        quit()


# Called when the lose conditions are met
# It's essentially the same as the win_cond function but I felt it better to keep them separate
# rather than just have more if statements
def boom():
    Plot.t_start = False
    reveal_all('splode')
    boom_msg = """Too bad. Be careful of those mines.
            Would you like to play again?
        """
    splode = messagebox.askyesno('You sploded.', boom_msg)
    if splode:
        reset_all()
    else:
        quit()


# This function takes the coordinates of the clicked plot and detects if it's a mine or not
# if it's a mine, it meets the lose conditions and calls the boom function
# if there's no mine, it uses an f-string to find the correct number asset to assign to the plot
def reveal(r, c):
    # Plot.sel is the Plot instance which has been selected
    # otherwise, I'd need to type Plot.grid[r][c] every time. This just makes things a little easier
    if Plot.sel.val == 'B':
        boom()
    else:
        # I used Plot.grid[r][c] here rather than Plot.sel because it's not just the selected plot
        # that gets called but occasionally the full 3x3 around it. If I used Plot.sel, all 9 plots
        # would receive the value asset of the middle plot rather than their correct values
        value_img_get = Image.open(f'assets/{Plot.grid[r][c].val}.png').resize((Plot.b_size, Plot.b_size))
        value_img = ImageTk.PhotoImage(value_img_get)
        plot = grid_frame.grid_slaves(row=r, column=c)[0]
        plot.config(image=value_img)
        plot.image = value_img
        if not Plot.grid[r][c].dug:
            Plot.grid[r][c].dug = True
            Plot.revealed += 1
    if Plot.revealed == (Plot.rows * Plot.cols) - Plot.mines and not Plot.first_click:
        win_cond()


# I tried to create a recursion function to reveal all adjacent plots with value 0
# but I only ever got infinite loops even when putting in a break condition. I still find them a bit confusing
# I found a simple loop did the job just fine
def scrub(r, c):
    new_list = []
    # This line gets a list of the 8 neighbours surrounding the selected plot
    n_list = find_neighbours(Plot.grid[r][c])
    for _ in range(2):
        # For each of the 8 neighbouring plots, reveal them
        for n in n_list:
            reveal(n[0], n[1])
            # For each of the revealed plots check to see if it has a value of 0
            if Plot.grid[n[0]][n[1]].val == 0:
                # If it does, find the neighbours of that plot giving me 2 plots out
                # discluding the plot iself, any other revealed plots to avoid any repeats or any plots out of bounds
                for i in find_neighbours(Plot.grid[n[0]][n[1]]):
                    # Check to see if the new plot is already in the new list
                    if i not in new_list:
                        # Ultimately this creates a non-repeating list of adjacent plots with a value of 0
                        # and all surrounding plots regardless of the value
                        # since no plots with a value of 0 is next to a mine, I don't need to worry about that
                        new_list.append(i)
        # empty new list back into the original neighbour list and repeat
        n_list = new_list


# This function checks all instances pf the Plot class to find the mines
# if found, it uses the find_neighbours function to get a list of all 8 adjacent plots
# then it adds 1 to the value of any plots which aren't mines
def set_values():
    # I chose to use a generator here rather than list comprehension to save on memory
    # I know for a program this small, it's not necessary but I feel it's a good habit to get into
    plot = (Plot.grid[r][c] for r in range(Plot.rows) for c in range(Plot.cols))
    while True:
        try:
            center = plot.__next__()
            if center.val == 'B':
                neighbours = find_neighbours(center)
                for n in neighbours:
                    Plot.grid[n[0]][n[1]].val += 1

        except StopIteration:
            break


# This function takes the number of mines set in the set_difficulty function and randomly assigns
# that number of mines to plots, avoiding any repeats
def lay_mines(r, c):
    x, y, counter = 0, 0, 0
    while counter < Plot.mines:
        x = rnd.randint(0, Plot.rows - 1)
        y = rnd.randint(0, Plot.cols - 1)
        # This ensures that the first click is free by not laying a mine on the clicked plot
        # if first_click is True
        if Plot.grid[x][y].val != 0 or (x, y) == (r, c):
            pass
        else:
            Plot.grid[x][y].val = 'B'
            counter += 1

    # This function is only called on the first click so it sets the first_click variable to False
    # and then sets the values to adjacent plots as well as revealing the selected plot
    Plot.first_click = False
    set_values()
    reveal(r, c)


def clicked(effect, r, c):
    # This if statement is responsible for locking the flagged plots
    if Plot.grid[r][c].flag:
        pass
    else:
        # If it's the first click, the functions are called to populate the mines
        # and set t_start to True which starts the timer
        Plot.sel = Plot.grid[r][c]
        if Plot.first_click:
            Plot.t_start = True
            lay_mines(r, c)
            if Plot.sel.val == 0:
                scrub(r, c)
            else:
                reveal(r, c)
        else:
            # Otherwise, it just does this
            if Plot.sel.val == 0:
                reveal(r, c)
                scrub(r, c)
            else:
                reveal(r, c)


def create_board():
    # I set the column and row weights to center grid_frame so tha the board would be centered in game_frame
    game_frame.rowconfigure(0, weight=1)
    game_frame.columnconfigure(1, weight=0)
    game_frame.columnconfigure(2, weight=0)

    # grid_frame is called in the root but gridded here which is why I destroy everything in grid_frame on reset
    # but only forget everything in game_frame otherwise grid_frame will be destroyed and the reset doesn't work
    grid_frame.grid(row=0, column=0)

    # This sets the plot sizes. More plots means smaller plots to keep the game board more or less consistent
    # The larger and smaller numbers were also part of the easy and hard modes
    # making hard mode harder to see and vice versa with easy mode
    if Plot.rows == 10:
        Plot.b_size = 30
    if Plot.rows == 20:
        Plot.b_size = 20
    if Plot.rows == 30:
        Plot.b_size = 10

    plot_img_get = Image.open('assets/button.png').resize((Plot.b_size, Plot.b_size))
    plot_img = ImageTk.PhotoImage(plot_img_get)

    # This builds the game board, setting each button with a lambda to it's specific row and column
    # to make it able to pass on it's specific coordinates
    for row in range(Plot.rows):
        for col in range(Plot.cols):
            button = tk.Button(grid_frame, image=plot_img)
            button.image = plot_img
            button.grid(row=row, column=col)
            # even though I used a button, I still chose to bind the left and right mouse clicks
            # I just personally felt it more consistent
            button.bind('<Button-1>', lambda effect, r=row, c=col: clicked(None, r, c))
            button.bind('<Button-3>', lambda effect, r=row, c=col: set_flag(None, r, c))


# This builds Plot.grid which is a list of lists oriented to match the rows and columns of the game board
# that way I could use the same coordinates to call the plot or the corresponding Plot instance
def create_grid():
    for row in range(Plot.rows):
        row_list = []
        for col in range(Plot.cols):
            plot = Plot(row, col, 0, False, False)
            row_list.append(plot)
        Plot.grid.append(row_list)
    clear_game_frame()
    create_board()


def set_difficulty():
    clear_game_frame()

    # This nested function sets the number of rows and columns as well as the number of mines
    # depending on your choice of Easy, Medium or Hard
    def return_diff(*args):
        Plot.rows, Plot.cols, Plot.mines = args
        create_grid()

    # This sets the size and population of the game board. It took quite a bit of testing
    # until I had a population that I felt was comfortable and playable
    diff_label = tk.Label(game_frame, text='Please select difficulty', font='Helvetica 20', bg='white')
    diff_label.grid(row=0, column=0, columnspan=3)

    diff_easy_button = tk.Button(game_frame, text='EASY',  font='Helvetica 14',
                                 command=lambda x=10, y=10, z=15: return_diff(x, y, z))
    diff_easy_button.grid(row=1, column=0)

    diff_med_button = tk.Button(game_frame, text='MEDIUM',  font='Helvetica 14',
                                command=lambda x=20, y=20, z=50: return_diff(x, y, z))
    diff_med_button.grid(row=1, column=1)

    diff_hard_button = tk.Button(game_frame, text='HARD',  font='Helvetica 14',
                                 command=lambda x=30, y=30, z=150: return_diff(x, y, z))
    diff_hard_button.grid(row=1, column=2)


# Pretty self-explanatory
def instr():
    instructions = """
            Welcome to Minesweeper.
            The game is simple.
            Click on the plot to reveal the number beneath.
            Your first plot is free.
            The number beneath the plot will show the number of adjacent mines.
            Find all the mines to win the game.
            If you click on a mine, it will explode and you lose.
            Right click to plant a flag and disable the plot.
            Right click on a flag to remove it an re-enable the plot.
            Good luck.
        """
    inst_split = instructions.split('\n')
    for num, inst in enumerate(inst_split):
        inst_label = tk.Label(game_frame, text=inst.strip(), font='Helvetica 14 bold', bg='white')
        inst_label.grid(row=num, column=1)
    play_button = tk.Button(game_frame, text='PLAY', font='Helvetica 14', command=set_difficulty)
    play_button.grid(row=12, column=1, sticky='w')
    quit_button = tk.Button(game_frame, text='QUIT', font='Helvetica 14', command=lambda: quit())
    quit_button.grid(row=12, column=1, sticky='e')


# And finally (but first in the code) is to build the actual game window and related frames in tkinter
# I felt tkinter was probably a better choice for a game like Minesweeper partially because I'm more familiar with it
# but partially because it's been a Windows staple for so long
# and tkinter feels to me like it's pretty much designed to make windowed applications
ms = tk.Tk()
ms.title("Minesweeper")
ms.geometry("720x720")
ms.columnconfigure(0, weight=1)
ms.rowconfigure(2, weight=1)
ms.config(bg='white')

title_frame = tk.Frame(ms)
title_frame.grid(row=0, column=0, sticky='ew')
title_frame.columnconfigure(0, weight=1)

title_image_get = Image.open("assets/title.png").resize((720, 70))
title_img = ImageTk.PhotoImage(title_image_get)
title_label = tk.Label(title_frame, image=title_img)
title_label.grid(row=0, column=0)
title_label.image = title_img

time_frame = tk.Frame(ms, bg='white')
time_frame.grid(row=1, column=0, sticky='ew')

timer_base_canvas = tk.Canvas(time_frame, height=60, width=170, relief='groove', bd=3)
timer_base_canvas.pack(side='right')

timer_zero_get = Image.open('assets/clock-0.png').resize((50, 60))
timer_zero = ImageTk.PhotoImage(timer_zero_get)
timer_colon_get = Image.open('assets/clock-colon.png').resize((30, 60))
timer_colon = ImageTk.PhotoImage(timer_colon_get)

timer_secs_units = tk.Label(timer_base_canvas, image=timer_zero)
timer_secs_units.image = timer_zero
timer_secs_tens = tk.Label(timer_base_canvas, image=timer_zero)
timer_secs_tens.image = timer_zero
timer_mins_units = tk.Label(timer_base_canvas, image=timer_zero)
timer_mins_units.image = timer_zero
timer_mins_tens = tk.Label(timer_base_canvas, image=timer_zero)
timer_mins_tens.image = timer_zero
timer_colon_label = tk.Label(timer_base_canvas, image=timer_colon)
timer_colon_label.image = timer_colon

timer_secs_units.place(x=135, y=5, height=60, width=30)
timer_secs_tens.place(x=100, y=5, height=60, width=30)
timer_mins_units.place(x=45, y=5, height=60, width=30)
timer_mins_tens.place(x=10, y=5, height=60, width=30)
timer_colon_label.place(x=80, y=5, height=60, width=15)

game_frame = tk.Frame(ms, relief='sunken', bd=2, bg='white')
game_frame.grid(row=2, column=0, sticky='nsew')
game_frame.columnconfigure(0, weight=1)
game_frame.columnconfigure(1, weight=1)
game_frame.columnconfigure(2, weight=1)

grid_frame = tk.Frame(game_frame)

instr()
timer()

ms.mainloop()

# Thankyou for getting all the way through this. The opinions in these comments accurately represent my thoughts
# and opinions after finishing this program on the 22.9.2022
