import time
import random
from Graphics import Window, Point, Line
from enum import Flag, auto

class Walls(Flag):
    WEST = auto()    # Gets value 1 (0b0001)
    EAST = auto()   # Gets value 2 (0b0010)
    NORTH = auto()     # Gets value 4 (0b0100)
    SOUTH = auto()  # Gets value 8 (0b1000)
    ALL = WEST | EAST | NORTH | SOUTH  # Combined value: 15
    NONE = 0
    def __str__(self):
        return f"Walls({self.name})"

class Cell:
    
    visited = False

    def __init__(self, window = None, x=0, y=0, cellwidth = 20, cellheight = 20, walls=Walls.ALL, buffer=50):
        self.has_west_wall  = bool(walls & Walls.WEST)
        self.has_east_wall  = bool(walls & Walls.EAST)
        self.has_north_wall = bool(walls & Walls.NORTH)
        self.has_south_wall = bool(walls & Walls.SOUTH)
        self.__x = x
        self.__y = y
        self.cellwidth = cellwidth
        self.cellheight = cellheight
        self.__nw_corner = Point(x * self.cellwidth + 1 + buffer, y * self.cellheight + buffer)
        self.__se_corner = Point((x + 1) * self.cellwidth + 1 + buffer, (y + 1) * self.cellheight + buffer)
        self.__ne_corner = Point((x + 1) * self.cellwidth + 1 + buffer, y * self.cellheight + buffer)
        self.__sw_corner = Point(x * self.cellwidth + 1 + buffer, (y + 1) * self.cellheight + buffer)
        if window != None:
            self.__window = window
        else:
            self.__window = None
        self.draw()

    def draw(self):
        if self.__window is None:
            return
        
        # Draw West wall
        line = Line(self.__nw_corner, self.__sw_corner)
        if self.has_west_wall:
            self.__window.drawLine(line)
        else:
            self.__window.drawLine(line, fill_color="white")
        # Draw the East wall
        line = Line(self.__ne_corner, self.__se_corner)
        if self.has_east_wall:
            self.__window.drawLine(line)
        else:
            self.__window.drawLine(line, fill_color="white")
        # Draw the North wall
        line = Line(self.__nw_corner, self.__ne_corner)
        if self.has_north_wall:
            self.__window.drawLine(line)
        else:
            self.__window.drawLine(line, fill_color="white")
        # Draw the South wall
        line = Line(self.__sw_corner, self.__se_corner)
        if self.has_south_wall:
            self.__window.drawLine(line)
        else:
            self.__window.drawLine(line, fill_color="white")
    
    def get_location(self):
        return (self.__x, self.__y)

    def draw_to_cell(self, other_cell, backtrack = False, buffer=50):
        if other_cell is None or not isinstance(other_cell, Cell):
            raise ValueError("other_cell must be a valid Cell instance.")
        if self.__window is None:
            return
        color = "red" if not backtrack else "gray"
        line = Line(self.__x * self.cellwidth + self.cellwidth // 2 + buffer,
                    self.__y * self.cellheight + self.cellheight // 2 + buffer,
                    other_cell.__x * self.cellwidth + self.cellwidth // 2 + buffer,
                    other_cell.__y * self.cellheight + self.cellheight // 2 + buffer)
        self.__window.drawLine(line, fill_color=color)

class Maze:
    def __init__(self, window=None, width=2, height=3, cellwidth = 20, cellheight = 20, buffer=50, entrance=(0,0), exit=None, seed=None, check_interrupt=None):
        if window != None:
            self.__window = window
        else:
            self.__window = None
        
        if seed != None:
            random.seed(seed)
        else:
            random.seed()

        self.__width = width
        self.__height = height
        self.__cells = [[Cell(window, x, y, cellwidth, cellheight) for x in range(width)] for y in range(height)]
        
        # If entrance is "random", pick a random position on top row or west side
        if entrance == "random":
            if random.choice([True, False]):  # Choose top row
                entrance = (random.randint(0, width - 1), 0)
            else:  # Choose west side
                entrance = (0, random.randint(0, height - 1))
        
        if entrance[0] < 0 or entrance[0] >= width or entrance[1] < 0 or entrance[1] >= height:
            raise ValueError("Entrance coordinates must be within the maze dimensions.")
        self.entrance = entrance
        
        # Handle exit positioning
        if exit == "random":
            if random.choice([True, False]):  # Choose bottom row
                exit = (random.randint(0, width - 1), height - 1)
            else:  # Choose east side
                exit = (width - 1, random.randint(0, height - 1))
        
        if exit is not None:
            if exit[0] < 0 or exit[0] >= width or exit[1] < 0 or exit[1] >= height:
                raise ValueError("Exit coordinates must be within the maze dimensions.")
            self.exit = self.__cells[exit[1]][exit[0]]
            self.exit_coords = exit
        else:
            self.exit = self.__cells[height - 1][width - 1]
            self.exit_coords = (width - 1, height - 1)
        
        self.__buffer = buffer
        self.__check_interrupt = check_interrupt
        self.__break_entrance()
        self.__break_exit()
        self.__reset_visited()
        self.__break_walls_r(entrance[0], entrance[1])
    
    def draw(self):
        for row in self.__cells:
            for cell in row:
                cell.draw()

    def clear(self):
        if self.__window is None:
            return
        self.__window.clear()
        
    
    def get_cell(self, x, y):
        return self.__cells[y][x] if 0 <= x < self.__width and 0 <= y < self.__height else None
    
    def _create_cells(self):
        self.__cells = [[Cell(self.__window, x, y) for x in range(self.__width)] for y in range(self.__height)]
    
    def _draw_cells(self):
        for row in self.__cells:
            for cell in row:
                cell.draw()

    def __draw_cell(self, i, j):
        if 0 <= i < self.__width and 0 <= j < self.__height:
            self.__cells[j][i].draw()
            self.__animate(0.0)
        else:
            raise IndexError("Cell index out of bounds")

    def __animate(self, delay=0.05):
        if self.__window is None:
            return
        if self.__check_interrupt and not self.__check_interrupt():
            raise InterruptedError("Animation interrupted")
        self.__window.redraw()
        time.sleep(delay)

    def __break_entrance(self):
        # Allow entrance on any position on the top row or west side
        if self.entrance[1] == 0:  # Top row
            self.__cells[0][self.entrance[0]].has_north_wall = False
            self.__cells[0][self.entrance[0]].draw()
            self.__draw_cell(self.entrance[0], 0)
        elif self.entrance[0] == 0:  # West side
            self.__cells[self.entrance[1]][0].has_west_wall = False
            self.__cells[self.entrance[1]][0].draw()
            self.__draw_cell(0, self.entrance[1])
        else:
            raise ValueError("Entrance must be on the top row or west side.")

    def __break_exit(self, exit=None):
        # Use the stored exit coordinates
        exit_x, exit_y = self.exit_coords
        
        # Allow exit on any position on the bottom row or east side
        if exit_y == self.__height - 1:  # Bottom row
            self.__cells[exit_y][exit_x].has_south_wall = False
            self.__cells[exit_y][exit_x].draw()
            self.__draw_cell(exit_x, exit_y)
        elif exit_x == self.__width - 1:  # East side
            self.__cells[exit_y][exit_x].has_east_wall = False
            self.__cells[exit_y][exit_x].draw()
            self.__draw_cell(exit_x, exit_y)
        else:
            raise ValueError("Exit must be on the bottom row or east side.")

    def __break_walls_r(self, i, j):
        self.__cells[j][i].visited = True
        while True:
            if j < 0 or j >= self.__height or i < 0 or i >= self.__width:
                return
            to_visit = []
            if j > 0 and not self.__cells[j - 1][i].visited:
                to_visit.append((i, j - 1))
            if j < self.__height - 1 and not self.__cells[j + 1][i].visited:
                to_visit.append((i, j + 1))
            if i > 0 and not self.__cells[j][i - 1].visited:
                to_visit.append((i - 1, j))
            if i < self.__width - 1 and not self.__cells[j][i + 1].visited:
                to_visit.append((i + 1, j))
            if not to_visit:
                return
            next_cell = random.choice(to_visit)
            if next_cell[0] == i and next_cell[1] == j - 1:
                self.__cells[j][i].has_north_wall = False
                self.__cells[next_cell[1]][next_cell[0]].has_south_wall = False
            elif next_cell[0] == i and next_cell[1] == j + 1:
                self.__cells[j][i].has_south_wall = False
                self.__cells[next_cell[1]][next_cell[0]].has_north_wall = False
            elif next_cell[0] == i - 1 and next_cell[1] == j:
                self.__cells[j][i].has_west_wall = False
                self.__cells[next_cell[1]][next_cell[0]].has_east_wall = False
            elif next_cell[0] == i + 1 and next_cell[1] == j:
                self.__cells[j][i].has_east_wall = False
                self.__cells[next_cell[1]][next_cell[0]].has_west_wall = False
            self.__draw_cell(i, j)
            self.__draw_cell(next_cell[0], next_cell[1])
            self.__break_walls_r(next_cell[0], next_cell[1])

    def __reset_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        self.__reset_visited()
        try:
            # Draw Starting line from entrance edge to center
            entrance_cell = self.__cells[self.entrance[1]][self.entrance[0]]
            x = self.entrance[0]
            y = self.entrance[1]
            buffer = self.__buffer
            cellwidth = entrance_cell.cellwidth
            cellheight = entrance_cell.cellheight
            # Calculate cell center
            center_x = x * cellwidth + cellwidth // 2 + buffer
            center_y = y * cellheight + cellheight // 2 + buffer
            cell_center = Point(center_x, center_y)
            # Determine which edge to start from
            if y == 0 and entrance_cell.has_north_wall == False:
                # Entrance is on the top row (north wall is open)
                start_point = Point(center_x, y * cellheight + buffer // 2)
            elif x == 0 and entrance_cell.has_west_wall == False:
                # Entrance is on the west side (west wall is open)
                start_point = Point(x * cellwidth + buffer // 2, center_y)
            else:
                # Fallback: just use the cell center
                start_point = cell_center

            line = Line(start_point, cell_center)
            self.__window.drawLine(line, "red")
            self.__animate(0.05)

            result = self.__solve_r(self.entrance[0], self.entrance[1])
            
            # Draw the exit line if the exit is reached
            if result:
                exit_cell = self.exit
                exit_x = exit_cell.get_location()[0]
                exit_y = exit_cell.get_location()[1]
                exit_center_x = exit_x * cellwidth + cellwidth // 2 + buffer
                exit_center_y = exit_y * cellheight + cellheight // 2 + buffer
                exit_center = Point(exit_center_x, exit_center_y)
                

                # Determine which edge to end at
                if exit_y == self.__height - 1 and exit_cell.has_south_wall == False:
                    # Exit is on the bottom row (south wall is open)
                    end_point = Point(exit_center_x, (exit_y + 1) * cellheight + 1.5 * buffer)
                elif exit_x == self.__width - 1 and exit_cell.has_east_wall == False:
                    # Exit is on the east side (east wall is open)
                    end_point = Point((exit_x + 1) * cellwidth + 1.5 * buffer, exit_center_y)
                else:
                    # Fallback: just use the cell center
                    end_point = exit_center
                
                line = Line(exit_center, end_point)
                self.__window.drawLine(line, "red")
                self.__animate(0.05)
            
            return result
        except InterruptedError:
            return False

    def __solve_r(self, i, j, animateTime=0.03, backtrackTime=0.1):
        self.__animate(animateTime)
        self.__cells[j][i].visited = True
        if self.__cells[j][i] == self.exit:
            return True
        # Check North
        if j > 0 and not self.__cells[j - 1][i].visited and not self.__cells[j][i].has_north_wall:
            self.__cells[j][i].draw_to_cell(self.__cells[j - 1][i])
            if self.__solve_r(i, j - 1):
                return True
            else:
                self.__cells[j][i].draw_to_cell(self.__cells[j - 1][i], backtrack=True)
                self.__animate(backtrackTime)
        # Check South
        if j < self.__height - 1 and not self.__cells[j + 1][i].visited and not self.__cells[j][i].has_south_wall:
            self.__cells[j][i].draw_to_cell(self.__cells[j + 1][i])
            if self.__solve_r(i, j + 1):
                return True
            else:
                self.__cells[j][i].draw_to_cell(self.__cells[j + 1][i], backtrack=True)
                self.__animate(backtrackTime)
        # Check West
        if i > 0 and not self.__cells[j][i - 1].visited and not self.__cells[j][i].has_west_wall:
            self.__cells[j][i].draw_to_cell(self.__cells[j][i - 1])
            if self.__solve_r(i - 1, j):
                return True
            else:
                self.__cells[j][i].draw_to_cell(self.__cells[j][i - 1], backtrack=True)
                self.__animate(backtrackTime)
        # Check East
        if i < self.__width - 1 and not self.__cells[j][i + 1].visited and not self.__cells[j][i].has_east_wall:
            self.__cells[j][i].draw_to_cell(self.__cells[j][i + 1])
            if self.__solve_r(i + 1, j):
                return True
            else:
                self.__cells[j][i].draw_to_cell(self.__cells[j][i + 1], backtrack=True)
                self.__animate(backtrackTime)
        
        # If no path found, return False
        return False
