import tkinter as tk
import random
import heapq
import sys

sys.setrecursionlimit(10000)
# Constants
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = "white"
GREEN = "green"
RED = "red"
BLACK = "black"

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    def __lt__(self, other):
        return False

def generate_grid():
    return [[Node(row, col) for col in range(COLS)] for row in range(ROWS)]

def heuristic(node, target):
    return abs(node.row - target.row) + abs(node.col - target.col)

def get_neighbours(grid, node):
    neighbours = []
    if node.row > 0:
        neighbours.append(grid[node.row - 1][node.col])
    if node.row < ROWS - 1:
        neighbours.append(grid[node.row + 1][node.col])
    if node.col > 0:
        neighbours.append(grid[node.row][node.col - 1])
    if node.col < COLS - 1:
        neighbours.append(grid[node.row][node.col + 1])
    return neighbours

def reconstruct_path(current):
    path = []
    while current is not None:
        path.append((current.row, current.col))
        current = current.parent
    return path[::-1]

def astar_search(grid, start, target):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g_cost = 0

    while open_set:
        _, current_node = heapq.heappop(open_set)

        if current_node == target:
            return reconstruct_path(current_node)

        for neighbour in get_neighbours(grid, current_node):
            temp_g_cost = current_node.g_cost + 1

            if temp_g_cost < neighbour.g_cost:
                neighbour.parent = current_node
                neighbour.g_cost = temp_g_cost
                neighbour.h_cost = heuristic(neighbour, target)
                heapq.heappush(open_set, (neighbour.g_cost + neighbour.h_cost, neighbour))

    return None

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A* Snake Game")
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg=BLACK)
        self.canvas.pack()

        self.grid = generate_grid()
        self.snake = [(ROWS // 2, COLS // 2), (ROWS // 2, COLS // 2 - 1), (ROWS // 2, COLS // 2 - 2)]
        self.direction = (0, -1)
        self.food = self.generate_food()

        self.draw()
        self.game_loop()

    def generate_food(self):
        while True:
            food = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            if food not in self.snake:
                return food


    def move_snake(self):
        head = self.snake[0]
        path = astar_search(self.grid, self.grid[head[0]][head[1]], self.grid[self.food[0]][self.food[1]])

        if path:
            next_move = path[1]
            direction = (next_move[0] - head[0], next_move[1] - head[1])
            self.direction = direction

        # new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # # Keep the snake within the canvas boundaries
        # if 0 <= new_head[0] < ROWS and 0 <= new_head[1] < COLS:
        #     self.snake.insert(0, new_head)
        #     if new_head == self.food:
        #         self.food = self.generate_food()
        #     else:
        #         self.snake.pop()
        # else:
        #     # If the snake hits the wall, end the game
        #     print("Game Over")
        #     return

        self.draw()
        self.after(100, self.game_loop)

    def check_collision(self):
        head = self.snake[0]
        return (
            head in self.snake[1:] or
            head[0] < 0 or head[0] >= ROWS or
            head[1] < 0 or head[1] >= COLS
        )

    def draw(self):
        self.canvas.delete("all")
        for segment in self.snake:
            x, y = segment[1] * CELL_SIZE, segment[0] * CELL_SIZE
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=GREEN)
        x, y = self.food[1] * CELL_SIZE, self.food[0] * CELL_SIZE
        self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=RED)
        self.update()

    def game_loop(self):
        if not self.check_collision():
            self.move_snake()
            self.draw()
            self.after(1000, self.game_loop)
        else:
            print("Game Over")


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
