from Graphics import Window, Point, Line
from maze import Walls, Cell, Maze
import sys
import signal

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    global running
    print("\nMaze solving interrupted by user.")
    running = False

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

screen_x = 1024
screen_y = 768
buffer = 50
num_cols = 12
num_rows = 8
cell_size_x = (screen_x - (2 * buffer)) / num_cols
cell_size_y = (screen_y - (2 * buffer)) / num_rows

win = Window(screen_x, screen_y)

def check_running():
    return running and win.is_open()

try:
    while running and win.is_open():
        try:
            # Process window events (including close button)
            win.redraw()
        except:
            # Window was closed
            running = False
            break
            
        maze = Maze(win, num_cols, num_rows, cell_size_x, cell_size_y, buffer, entrance="random", exit="random", check_interrupt=check_running)
        try:
            maze.solve()
        except InterruptedError:
            print("Maze solving interrupted")
            break
        except Exception as e:
            if "invalid command name" not in str(e):  # Ignore Tkinter errors when window is closing
                print(f"Error during solve: {e}")
            break
            
        if running and win.is_open():  # Check if we should continue
            maze.clear()
except Exception as e:
    if "invalid command name" not in str(e):  # Ignore Tkinter errors
        print(f"An error occurred: {e}")
finally:
    try:
        if win.is_open():
            win.close()
    except:
        pass  # Window might already be closed
    sys.exit(0)