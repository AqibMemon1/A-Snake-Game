import tkinter as tk
import random

class SnakeGame:
    def create_obstacle(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20

            overlapping = False
            if (
            x < 20 or x >= 380 or y < 20 or y >= 380
        ):
                overlapping = True

            if not overlapping:
                break

        obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="blue")
        return obstacle

    def create_boundaries(self):
        # Create boundaries on the canvas
        for i in range(0, 400, 20):
            self.canvas.create_rectangle(0, i, 20, i + 20, fill="grey")  # Left boundary
            self.canvas.create_rectangle(i, 0, i + 20, 20, fill="grey")  # Top boundary
            self.canvas.create_rectangle(i, 380, i + 20, 400, fill="grey")  # Bottom boundary
            self.canvas.create_rectangle(380, i, 400, i + 20, fill="grey")  # Right boundary

    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")

        self.master.resizable(False, False)
        
        

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()
        self.score_label = tk.Label(self.master, text="Snake Length:  3")  # Initialize score_label
        self.score_label.pack()
        self.score_display = self.canvas.create_text(25, 22.5, text="Snake Length:  3", fill="white", anchor="nw")
        self.snake = [(100, 100), (90, 100), (80, 100)]
       
        self.direction = "Right"
        
        
        self.score = 0  # Added score variable
        self.obstacles = []
        
        self.master.bind("<KeyPress>", self.change_direction)
        self.create_boundaries()
        self.food = self.create_food()
        self.update()

    
        self.ai_snake = [(300, 300), (310, 300), (320, 300)]  # Initial position for AI snake
        self.ai_direction = "Left"  # Initial direction for AI snake

    
    def update(self):
        self.move_snake()



    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            food_coords = (x, y, x + 20, y + 20)
            # Check if food overlaps with boundaries or obstacles
            overlapping = False
        
            # Check boundaries
            if (
                x < 20 or x >= 380 or y < 20 or y >= 380
            ):
                overlapping = True

            # Check obstacles
            for obstacle in self.obstacles:
                obstacle_coords = self.canvas.coords(obstacle)
                if self.canvas.bbox(obstacle) == food_coords:
                    overlapping = True
                    break
            if not overlapping:
                break
    
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")

        return food
    
    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)

        
       
        head_coords = self.snake[0]
        food_coords = self.canvas.coords(self.food)

    # Calculate the cell position of the head and food
        head_cell = (head_coords[0] // 20, head_coords[1] // 20)
        food_cell = (food_coords[0] // 20, food_coords[1] // 20)

    # Check collision with food
        if head_cell == (food_cell[0] // 20, food_cell[1] // 20):  # Compare cell positions
            self.score += 1
            self.master.title(f"Snake Game - Score: {self.score}")
            self.snake.append(self.snake[-1])  # Add a new segment to the snake
            self.canvas.delete(self.food)  # Delete the eaten food
            self.food = self.create_food()  # Create new food

        else:
            self.snake.pop()

    def check_boundary_collision(self, position):
        # Check collision with grey boundaries
        x, y = position
        return (
            x < 20 or x >= 380 or y < 20 or y >= 380
    )  

    def update(self):
        self.move_snake()
        
        head = self.snake[0]
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")
        
        self.master.after(200, self.update)
        
        if len(self.snake) > 3:  # Check to avoid initial length display
            self.score_label.config(text=f"Snake Length: {len(self.snake)}")  # Update score_label text

        self.canvas.delete("food")
        food_coords = self.canvas.coords(self.food)
        
        if head[0] == food_coords[0] and head[1] == food_coords[1]:

            self.snake.append((0, 0))  # Just to increase the length
            self.canvas.delete("food")
            x, y = food_coords[0], food_coords[1]
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="black")
            self.food = self.create_food()

        if len(self.snake) > 3:  
            self.canvas.itemconfig(self.score_display, text=f"Snake Length: {len(self.snake)}")

        if random.random() < 0.03:  # Adjust probability to create obstacles
            obstacle = self.create_obstacle()
            self.obstacles.append(obstacle)

        if (
            head[0] < 0
            or head[0] >= 400
            or head[1] < 0
            or head[1] >= 400
            or head in self.snake[1:]
            or self.check_boundary_collision(head)
        ):
            self.game_over()

        # Check collision with obstacles
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if head[0] == obstacle_coords[0] and head[1] == obstacle_coords[1]:
                self.game_over()

        self.score_label.config(text=f"Snake Length: {len(self.snake)}")  # Updated score_label text

    def game_over(self):
        self.master.title(f"Snake Game - Game Over! Final Score: {len(self.snake)}")
        self.canvas.delete(tk.ALL)
            


    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

