from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.running = False
        self.__is_valid = True

    def redraw(self):
        if self.__is_valid and self.__root.winfo_exists():
            self.canvas.update_idletasks()
            self.canvas.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.__is_valid = False
        self.__root.destroy()
    
    def is_open(self):
        return self.__is_valid and self.__root.winfo_exists()

    def drawLine(self, Line, fill_color="black"):
        Line.draw(self.canvas, fill_color)
        self.redraw()

    def clear(self):
        self.canvas.delete("all")
        self.redraw()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return str(self)    
    
class Line:
    def __init__(self, *args, **kwargs):
      if len(args) == 1:
        line = args[0]
        if isinstance(line, Line):
          self.start = line.start
          self.end = line.end
        elif isinstance(line, tuple) and len(line) == 2:
          self.start = Point(*line[0])
          self.end = Point(*line[1])
        else:
          raise ValueError("Invalid input for Line initialization with 1 argument")

      elif len(args) == 2:
        start, end = args
        if isinstance(start, Point):
          self.start = start
        elif isinstance(start, tuple) and len(start) == 2:
          self.start = Point(*start)
        else:
          raise ValueError("Invalid 'start' input")

        if isinstance(end, Point):
          self.end = end
        elif isinstance(end, tuple) and len(end) == 2:
          self.end = Point(*end)
        else:
          raise ValueError("Invalid 'end' input")

      elif len(args) == 4:
        x1, y1, x2, y2 = args
        self.start = Point(x1, y1)
        self.end = Point(x2, y2)

      else:
        raise TypeError("Invalid number of arguments for Line initialization")

    def __str__(self):
        return f"Line({self.start}, {self.end})"

    def __repr__(self):
        return str(self)
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, width=2, fill=fill_color)

