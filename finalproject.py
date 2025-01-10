import tkinter as tk
import random

SNAKE_SIZE = 40
FOOD_SIZE = 40
direction = 'Right'
next_direction = 'Right'
speed = 130 # Higher Number = Slower Snake
score = 0
DIRECTIONS = {
    'Left':(-SNAKE_SIZE, 0),
    'Right':(SNAKE_SIZE, 0),
    'Up':(0, -SNAKE_SIZE),
    'Down':(0, SNAKE_SIZE)
}

def create_window():
    window = tk.Tk()
    window.title("Snake Game")
    window.resizable(False, False)  # Prevent window resizing
    canvas = tk.Canvas(window, bg="black", height=800, width=800)
    canvas.pack()
    return window, canvas

def create_snake(canvas):
    initial_positions = [(200, 200), (160, 200), (120, 200)]  # Initial positions of the snake segments
    snake = [canvas.create_rectangle(pos[0], pos[1], pos[0] + SNAKE_SIZE, pos[1] + SNAKE_SIZE, fill='green') for pos in initial_positions]
    return snake

def draw_snake(snake):
    for segment in snake:
        canvas.itemconfig(segment, fill='green')

def create_food(canvas):
    canvas.update()
    x = random.randint(0, (canvas.winfo_width() // FOOD_SIZE) - 1) * FOOD_SIZE
    y = random.randint(0, (canvas.winfo_height() // FOOD_SIZE) - 1) * FOOD_SIZE
    food = canvas.create_rectangle(x, y, x + FOOD_SIZE, y + FOOD_SIZE, fill = 'red')
    return food

def move_snake(canvas, window, snake, food):
    global direction, next_direction, score

    direction = next_direction
    x_offset, y_offset = DIRECTIONS[direction]
    head_x, head_y, _, _ = canvas.coords(snake[0])
    new_head_x = head_x + x_offset
    new_head_y = head_y + y_offset
    new_head = canvas.create_rectangle(new_head_x, new_head_y, new_head_x + SNAKE_SIZE, new_head_y + SNAKE_SIZE, fill="green")
    snake.insert(0, new_head)
    if check_border_collision(new_head) or check_self_collision(snake):
        game_over(canvas)
        return

    if check_collision(new_head, food):
        canvas.delete(food)
        food = create_food(canvas)
        score += 10
        update_score(canvas, score)
    else:
        canvas.delete(snake.pop())

    window.after(speed, move_snake, canvas, window, snake, food)
    
def change_direction(new_direction):
    global direction, next_direction
    if (direction == "Left" and new_direction != "Right") or \
       (direction == "Right" and new_direction != "Left") or \
       (direction == "Up" and new_direction != "Down") or \
       (direction == "Down" and new_direction != "Up"):
        next_direction = new_direction

def check_border_collision(head):
    x, y, _, _ = canvas.coords(head)
    return x < 0 or x >= canvas.winfo_width() or y < 0 or y >= canvas.winfo_height()

def check_self_collision(snake):
    head = snake[0]
    return any(check_collision(head, segment) for segment in snake[1:])

def check_collision(item1, item2):
    if isinstance(item2, list):
        return any(check_collision(item1, segment) for segment in item2)
    x1, y1, x2, y2 = canvas.coords(item1)
    x3, y3, x4, y4 = canvas.coords(item2)
    return x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3

def update_score(canvas, score):
    canvas.delete('score')
    canvas.create_text(50, 10, text=f'Score: {score}', fill='white', font=('Arial', 18), tags="score")

def game_over(canvas):
    canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2, text='Game Over!', fill='white', font=('Arial', 45))


if __name__ == "__main__":
    window, canvas = create_window()
    snake = create_snake(canvas)
    food = create_food(canvas)
    draw_snake(snake)
    move_snake(canvas, window, snake, food)
    update_score(canvas, score)
    window.bind("<Left>", lambda event: change_direction("Left"))
    window.bind("<Right>", lambda event: change_direction("Right"))
    window.bind("<Up>", lambda event: change_direction("Up"))
    window.bind("<Down>", lambda event: change_direction("Down"))

    window.mainloop()
