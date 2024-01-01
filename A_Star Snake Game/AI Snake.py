import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()
        self.obstacles = []
        # Player snake initialization
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        # AI snake initialization
        self.ai_snake = [(300, 300), (310, 300), (320, 300)]
        self.ai_direction = "Left"

        self.food = self.create_food()

        self.master.bind("<KeyPress>", self.change_direction)
        self.score_label = tk.Label(self.master, text="Snake Length:  3")  # Initialize score_label
        self.score_label.pack()
        self.score_display = self.canvas.create_text(25, 22.5, text="Snake Length:  3", fill="white", anchor="nw")
        self.score=0
        # Player snake
        self.create_boundaries()
        self.update()
        self.ai_snake = [(300, 300), (310, 300), (320, 300)]  # Initial position for AI snake
        self.ai_direction = "Left"  # Initial direction for AI snake
    
    def move_ai_snake(self):
        # Implement logic for AI snake's movement
        # Example: Move towards the player snake
        ai_head = self.ai_snake[0]
        player_head = self.snake[0]

        # Implement basic logic to move AI snake towards player snake
        if ai_head[0] < player_head[0]:
            self.ai_direction = "Right"
        elif ai_head[0] > player_head[0]:
            self.ai_direction = "Left"
        elif ai_head[1] < player_head[1]:
            self.ai_direction = "Down"
        elif ai_head[1] > player_head[1]:
            self.ai_direction = "Up"

        # Update AI snake's position based on the determined direction
        # Implement collision avoidance logic for AI snake

        # ... (additional logic to move AI snake, avoid collisions, etc.)

    # Update method incorporating AI snake's movement

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
        
    def move_snake(self, snake, direction):
        head = snake[0]
        new_head = self.get_new_head_position(head, direction)

        # Check for self-collision or boundary collision
        if new_head in snake or not 0 <= new_head[0] < 380 or not 0 <= new_head[1] < 380:
            return False

        snake.insert(0, new_head)
        snake.pop()
        return True

    def get_new_head_position(self, head, direction):
        if direction == "Right":
            return (head[0] + 20, head[1])
        elif direction == "Left":
            return (head[0] - 20, head[1])
        elif direction == "Up":
            return (head[0], head[1] - 20)
        elif direction == "Down":
            return (head[0], head[1] + 20)

    def ai_logic(self):
        head = self.ai_snake[0]
        food_coords = self.canvas.coords(self.food)
        new_directions = []

        # Check for direct line of sight to food
        if head[0] == food_coords[0]:
            if head[1] > food_coords[1]:
                new_directions.append("Up")
            else:
                new_directions.append("Down")
        elif head[1] == food_coords[1]:
            if head[0] > food_coords[0]:
                new_directions.append("Left")
            else:
                new_directions.append("Right")

        # Avoiding collisions
        for direction in ["Left", "Right", "Up", "Down"]:
            new_head = self.get_new_head_position(head, direction)
            if 0 <= new_head[0] < 400 and 0 <= new_head[1] < 400 and new_head not in self.ai_snake:
                new_directions.append(direction)

        # Choose a new direction
        if new_directions:
            self.ai_direction = random.choice(new_directions)

    def update(self):
        if not self.move_snake(self.snake, self.direction):
            self.game_over()
            return
        head = self.snake[0]
        self.ai_logic()

        if not self.move_snake(self.ai_snake, self.ai_direction):
            self.ai_snake = [(300, 300), (310, 300), (320, 300)]  # Reset AI snake

        # Update player snake on canvas
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        # Update AI snake on canvas
        self.canvas.delete("ai_snake")
        for segment in self.ai_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="orange", tags="ai_snake")

        # Food logic
        self.update_food()
        self.score_label.config(text=f"Snake Length: {len(self.snake)}")  # Update score_label text
        self.master.after(200, self.update)


        if random.random() < 0.03:  # Adjust probability to create obstacles
            obstacle = self.create_obstacle()
            self.obstacles.append(obstacle)

        # Check collision with obstacles
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if head[0] == obstacle_coords[0] and head[1] == obstacle_coords[1]:
                self.game_over()
        

    def update_food(self):
        head = self.snake[0]
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))  # Increase the length
            self.score=+1
            self.score_label.config(text=f"Snake Length: {len(self.snake)}")  # Update score_label text
            self.canvas.delete(self.food)
            self.food = self.create_food()
            
            
            
    def change_direction(self, event):
        if event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"

    def game_over(self):
        print("Game Over!")
        self.master.destroy()
    
    def create_boundaries(self):
        # Create boundaries on the canvas
        for i in range(0, 400, 20):
            self.canvas.create_rectangle(0, i, 20, i + 20, fill="grey")  # Left boundary
            self.canvas.create_rectangle(i, 0, i + 20, 20, fill="grey")  # Top boundary
            self.canvas.create_rectangle(i, 380, i + 20, 400, fill="grey")  # Bottom boundary
            self.canvas.create_rectangle(380, i, 400, i + 20, fill="grey")  # Right boundary
    
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

        obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="white")
        return obstacle
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
