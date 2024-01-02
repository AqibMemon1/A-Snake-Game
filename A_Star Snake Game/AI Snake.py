import tkinter as tk
import random
import heapq
import math


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
        self.enemy_snake = [(300, 300), (310, 300), (320, 300)]
        self.ai_direction = "Left"
        self.food = self.create_food()
        self.master.bind("<KeyPress>", self.change_direction)
        self.score_label_player = tk.Label(self.master, text="Player Score:  3")  # Initialize score_label
        self.score_label_player.pack()
        self.score_display_player = self.canvas.create_text(25, 22.5, text="Player Score:  3", fill="light blue",  anchor="nw")
        self.score_label_ai = tk.Label(self.master, text="Enemy Score:  3")  # Initialize score_label
        self.score_label_ai.pack()
        self.score_display_ai = self.canvas.create_text(285, 22.5, text="Enemy Score:  3", fill="light blue",  anchor="nw")
        self.player_score=3
        self.score_ai=3
        self.create_boundaries()
        self.update()
        self.enemy_snake = [(300, 300), (310, 300), (320, 300)]  # Initial position for AI snake
        self.ai_direction = "Left"  # Initial direction for AI snake
        # Adding Timer in the Canvas
        self.timer_label = tk.Label(self.master, text="Time Left: 60")
        self.timer_label.pack()
        self.timer_display = self.canvas.create_text(175, 22.5, text="Time Left: 60", fill="light blue", anchor="nw")
        self.time_left = 18
        self.update_timer()
    
    def move_enemy_snake(self):
        ai_head = self.enemy_snake[0]
        food_coords = self.canvas.coords(self.food)
        # Move towards food if it's to the right
        if food_coords[0] > ai_head[0]:
            self.ai_direction = "Right"
        # Move towards food if it's to the left
        elif food_coords[0] < ai_head[0]:
            self.ai_direction = "Left"
        # Move towards food if it's below
        elif food_coords[1] > ai_head[1]:
            self.ai_direction = "Down"
        # Move towards food if it's above
        elif food_coords[1] < ai_head[1]:
            self.ai_direction = "Up"

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
        if new_head in snake or not 20 <= new_head[0] < 380 or not 20 <= new_head[1] < 380:
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
        head = self.enemy_snake[0]
        food_coords = self.canvas.coords(self.food)
        new_directions=[]
        path = self.astar_pathfinding(head, (food_coords[0], food_coords[1]))

        if len(path) > 1:
            next_step = path[1]
            if next_step[0] > head[0]:
                self.ai_direction = "Right"
            elif next_step[0] < head[0]:
                self.ai_direction = "Left"
            elif next_step[1] > head[1]:
                self.ai_direction = "Down"
            elif next_step[1] < head[1]:
                self.ai_direction = "Up"

        # Avoiding collisions
        for direction in ["Left", "Right", "Up", "Down"]:
            new_head = self.get_new_head_position(head, direction)
            if 0 <= new_head[0] < 400 and 0 <= new_head[1] < 400 and new_head not in self.enemy_snake:
                new_directions.append(direction)

        # Choose a new direction
        if new_directions:
            self.ai_direction = random.choice(new_directions)
            

    def update(self):
        if not self.move_snake(self.snake, self.direction):
            self.game_over()
            return
        else:
            pass

        head = self.snake[0]
        self.ai_logic()
        self.move_enemy_snake()  # Add this line to invoke AI movement

        if not self.move_snake(self.enemy_snake, self.ai_direction):
            self.enemy_snake = [(300, 300), (310, 300), (320, 300)]  # Reset AI snake

        # Update player snake on canvas
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        # Update AI snake on canvas
        self.canvas.delete("enemy_snake")
        for segment in self.enemy_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="orange", tags="enemy_snake")

        # Food logic
        self.update_food()
        self.master.after(200, self.update)

        if random.random() < 0.1:  # Adjust probability to create obstacles
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
            self.player_score += 1  # Increment the player score
            self.score_label_player.config(text=f"Player Score: {self.player_score}")  # Update player score_label text
            self.canvas.itemconfig(self.score_display_player, text=f"Player Score: {self.player_score}",)
            self.canvas.delete(self.food)
            self.food = self.create_food()

        # Update AI snake on canvas
        self.canvas.delete("enemy_snake")
        for segment in self.enemy_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="orange", tags="enemy_snake")

        # Food logic for AI snake
        self.update_food_ai()
        self.score_label_ai.config(text=f"Enemy Score: {len(self.enemy_snake)}")  # Update AI score_label text

    def update_food_ai(self):
        head = self.enemy_snake[0]
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.enemy_snake.append((0, 0))  # Increase the length
            self.score_ai += 1  # Increment the AI snake score
            self.score_label_ai.config(text=f"Enemy Score: {len(self.enemy_snake)}")  # Update AI score_label text
            self.canvas.itemconfig(self.score_display_ai, text=f"Enemy Score: {self.score_ai}")
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
        # Unbind keyboard events
            # self.master.unbind("<KeyPress>")
            # # Stop any scheduled updates
        self.master.after_cancel(self.update_timer)
        self.master.after_cancel(self.update)
        self.canvas.delete(tk.ALL)
        self.end_game_message()

    
    def create_boundaries(self):
        # Create boundaries on the canvas
        for i in range(0, 400, 20):
            self.canvas.create_rectangle(0, i, 20, i + 20, fill="grey")  # Left boundary
            self.canvas.create_rectangle(i, 0, i + 20, 20, fill="grey")  # Top boundary
            self.canvas.create_rectangle(i, 380, i + 20, 400, fill="grey")  # Bottom boundary
            self.canvas.create_rectangle(380, i, 400, i + 20, fill="grey")  # Right boundary

    # Random Obstacle Creation 
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
    def astar_pathfinding(self, start, goal):
        def heuristic(a, b):
            return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)  # Manhattan distance as the heuristic function
        # Define potential movement directions (up, down, left, right)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # Initialize data structures for the algorithm
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start))  # Priority queue for nodes to be evaluated
        came_from = {}
        g_score = {position: float("inf") for position in self.obstacles}
        g_score.update({(i, j): float("inf") for i in range(0, 400, 20) for j in range(0, 400, 20)})
        g_score[start] = 0
        f_score = {position: float("inf") for position in self.obstacles}
        f_score.update({(i, j): float("inf") for i in range(0, 400, 20) for j in range(0, 400, 20)})
        f_score[start] = heuristic(start, goal)

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            closed_set.add(current)

            for direction in directions:
                new_position = (current[0] + direction[0] * 20, current[1] + direction[1] * 20)

                if not (0 <= new_position[0] < 400 and 0 <= new_position[1] < 400):
                    continue

                if new_position in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[new_position]:
                    came_from[new_position] = current
                    g_score[new_position] = tentative_g_score
                    f_score[new_position] = tentative_g_score + heuristic(new_position, goal)
                    heapq.heappush(open_set, (f_score[new_position], new_position))
        return []
    
    def end_game_message(self):
        if self.player_score > self.score_ai:
            winner = "Player Snake Wins!"
            print(winner)
            self.canvas.create_text(135, 160, text="YOU WIN!", fill="red", font="Arial 25",anchor="nw")
        elif self.player_score < self.score_ai:
            winner = "Enemy Snake Wins!"
            print(winner)
            self.canvas.create_text(135, 160, text="ENEMY WINS!", fill="red", font="Arial 25",anchor="nw")
        else:
            winner = "It's a tie!"
            print(winner)
            self.canvas.create_text(135, 160, text="Its a TIE!", fill="red", font="Arial 25",anchor="nw")
        end_text = f"{winner} wins! Player Score: {self.player_score}, Enemy Score: {self.score_ai}"
        end_label = tk.Label(self.master, text=end_text, font=("Arial", 18))
        end_label.place(x=100, y=180)  # Adjust x and y as needed
        end_label.pack()    
    # Timer Count-Down Fucntion
        
    def update_timer(self):
        self.time_left -= 1
        self.timer_label.config(text=f"Time Left: {self.time_left}")
        self.canvas.itemconfig(self.timer_display, text=f"Time Left: {self.time_left}")
        if self.time_left > 0:
            self.master.after(1000, self.update_timer)
        else:
            self.game_over()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
