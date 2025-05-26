import unittest
from tkinter import Tk, BOTH, Canvas
from Graphics import Window, Point, Line
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(None, num_rows, num_cols)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    
    def test_maze_get_cell(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(None, num_rows, num_cols)
        cell = m1.get_cell(5, 5)
        self.assertIsNotNone(cell)
        self.assertEqual(cell.get_location(), (5, 5))
        
        # Test out of bounds
        cell_out_of_bounds = m1.get_cell(15, 15)
        self.assertIsNone(cell_out_of_bounds)

    def test_maze_draw(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(None, num_rows, num_cols)
        m1.draw()
        # Since we cannot visually verify the drawing, we will just check if the method runs without error.
        self.assertTrue(True)

    def test_maze_cell_draw(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(None, num_rows, num_cols)
        cell = m1.get_cell(5, 5)
        self.assertIsNotNone(cell)
        cell.draw()
        # Again, we cannot visually verify the drawing, so we will just check if the method runs without error.
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()