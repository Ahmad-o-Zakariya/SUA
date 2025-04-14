import pygame
import random

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GREEN   = (0, 200, 0)    # Default Player Snake
BLUE    = (0, 0, 200)    # Default AI Snake
RED     = (200, 0, 0)    # Food (Triangle)

# Extra Colors for Selection
PURPLE  = (128, 0, 128)
YELLOW  = (255, 255, 0)
ORANGE  = (255, 165, 0)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
BROWN   = (139, 69, 19)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Player vs AI")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 40)

# --- Main Menu ---
def main_menu():
    while True:
        screen.fill(WHITE)
        title = title_font.render("🐍 Snake Game - Player vs AI 🐍", True, BLACK)
        instructions = font.render("1. Use Arrow Keys to Move", True, BLACK)
        rules_title = font.render("📜 Rules 📜", True, BLACK)
        rules = [
            "1. Don't hit the walls (duh).",
            "2. Don't eat yourself, you're not that delicious.",
            "3. AI can go through walls. Life isn't fair.",
            "4. Survive longer than AI. Or lose like a champ.",
            "5. Good luck! You'll need it."
        ]
        play_button = font.render("Press ENTER to Play", True, GREEN)
        
        screen.blit(title, (WIDTH // 6, HEIGHT // 10))
        screen.blit(instructions, (WIDTH // 6, HEIGHT // 5))
        screen.blit(rules_title, (WIDTH // 3, HEIGHT // 3))
        for i, rule in enumerate(rules):
            screen.blit(font.render(rule, True, BLACK), (WIDTH // 6, HEIGHT // 3 + 30 + i * 30))
        screen.blit(play_button, (WIDTH // 4, HEIGHT - 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# --- Difficulty Selection ---
def choose_difficulty():
    while True:
        screen.fill(WHITE)
        texts = ["Choose Difficulty:", "1. Easy", "2. Medium", "3. Hard", "4. Expert"]
        for i, text in enumerate(texts):
            label = font.render(text, True, BLACK)
            screen.blit(label, (WIDTH // 4, HEIGHT // 4 + i * 40))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Adjust AI move delays:
                # Easy: AI moves every 6 ticks
                if event.key == pygame.K_1:
                    return 8, 7, False  # player_speed=8, AI moves every 6 ticks
                # Medium: AI moves every 5 ticks
                elif event.key == pygame.K_2:
                    return 10, 6, False  # player_speed=10, AI moves every 5 ticks
                # Hard: AI moves every 2 ticks (slightly slower than every tick)
                elif event.key == pygame.K_3:
                    return 12, 4, False  # player_speed=12, AI moves every 2 ticks
                # Expert: AI moves every tick
                elif event.key == pygame.K_4:
                    return 14, 3, True   # player_speed=14, AI moves every tick

# --- Game Duration Selection (in seconds) ---
def choose_game_duration():
    # Minimum 30 seconds, maximum 15 minutes (900 seconds), increments of 15 seconds.
    duration = 30  
    while True:
        screen.fill(WHITE)
        title = title_font.render("Choose Game Duration (seconds):", True, BLACK)
        duration_text = font.render(f"Duration: {duration} second(s)", True, BLACK)
        instructions = font.render("Use UP/DOWN to adjust, ENTER to confirm", True, BLACK)
        screen.blit(title, (WIDTH // 6, HEIGHT // 4))
        screen.blit(duration_text, (WIDTH // 6, HEIGHT // 4 + 50))
        screen.blit(instructions, (WIDTH // 6, HEIGHT // 4 + 100))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Increase by 15 seconds until maximum 900 seconds.
                if event.key == pygame.K_UP and duration < 900:
                    duration += 15
                # Decrease by 15 seconds until minimum 30 seconds.
                elif event.key == pygame.K_DOWN and duration > 30:
                    duration -= 15
                elif event.key == pygame.K_RETURN:
                    return duration

# --- Color Selection ---
def choose_colors():
    # Select Player Snake Color
    while True:
        screen.fill(WHITE)
        title = title_font.render("Select Player Snake Color:", True, BLACK)
        option1 = font.render("1. Green", True, GREEN)
        option2 = font.render("2. Red", True, RED)
        option3 = font.render("3. Blue", True, BLUE)
        option4 = font.render("4. Yellow", True, YELLOW)
        option5 = font.render("5. Orange", True, ORANGE)
        
        screen.blit(title, (WIDTH // 6, HEIGHT // 6))
        screen.blit(option1, (WIDTH // 6, HEIGHT // 6 + 50))
        screen.blit(option2, (WIDTH // 6, HEIGHT // 6 + 90))
        screen.blit(option3, (WIDTH // 6, HEIGHT // 6 + 130))
        screen.blit(option4, (WIDTH // 6, HEIGHT // 6 + 170))
        screen.blit(option5, (WIDTH // 6, HEIGHT // 6 + 210))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    mapping = {
                        pygame.K_1: GREEN,
                        pygame.K_2: RED,
                        pygame.K_3: BLUE,
                        pygame.K_4: YELLOW,
                        pygame.K_5: ORANGE
                    }
                    player_color = mapping[event.key]
                    break
        else:
            continue
        break

    # Select AI Snake Color
    while True:
        screen.fill(WHITE)
        title = title_font.render("Select AI Snake Color:", True, BLACK)
        option1 = font.render("1. Blue", True, BLUE)
        option2 = font.render("2. Purple", True, PURPLE)
        option3 = font.render("3. Cyan", True, CYAN)
        option4 = font.render("4. Magenta", True, MAGENTA)
        option5 = font.render("5. Brown", True, BROWN)
        
        screen.blit(title, (WIDTH // 6, HEIGHT // 6))
        screen.blit(option1, (WIDTH // 6, HEIGHT // 6 + 50))
        screen.blit(option2, (WIDTH // 6, HEIGHT // 6 + 90))
        screen.blit(option3, (WIDTH // 6, HEIGHT // 6 + 130))
        screen.blit(option4, (WIDTH // 6, HEIGHT // 6 + 170))
        screen.blit(option5, (WIDTH // 6, HEIGHT // 6 + 210))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    mapping_ai = {
                        pygame.K_1: BLUE,
                        pygame.K_2: PURPLE,
                        pygame.K_3: CYAN,
                        pygame.K_4: MAGENTA,
                        pygame.K_5: BROWN
                    }
                    ai_color = mapping_ai[event.key]
                    break
        else:
            continue
        break

    return player_color, ai_color

# --- Outro Panels ---
def collision_panel():
    """Outro panel when the player collides."""
    while True:
        screen.fill(WHITE)
        title = title_font.render("Game Over! You collided.", True, BLACK)
        option1 = font.render("1. Main Menu", True, BLACK)
        option2 = font.render("2. Quit", True, BLACK)
        screen.blit(title, (WIDTH // 6, HEIGHT // 4))
        screen.blit(option1, (WIDTH // 6, HEIGHT // 4 + 50))
        screen.blit(option2, (WIDTH // 6, HEIGHT // 4 + 90))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "main_menu"
                elif event.key == pygame.K_2:
                    pygame.quit()
                    exit()

def time_over_panel(winner):
    """Outro panel when time expires, showing the winner and giving options."""
    while True:
        screen.fill(WHITE)
        title = title_font.render(f"Time's Up! {winner}", True, BLACK)
        option1 = font.render("1. Main Menu", True, BLACK)
        option2 = font.render("2. Quit", True, BLACK)
        screen.blit(title, (WIDTH // 6, HEIGHT // 4))
        screen.blit(option1, (WIDTH // 6, HEIGHT // 4 + 50))
        screen.blit(option2, (WIDTH // 6, HEIGHT // 4 + 90))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "main_menu"
                elif event.key == pygame.K_2:
                    pygame.quit()
                    exit()

# --- Snake Classes ---
class Snake:
    def __init__(self, x, y, color, shape="rectangle"):
        self.body = [(x, y)]
        self.direction = (CELL_SIZE, 0)  # Moves right initially
        self.growing = False
        self.color = color
        self.shape = shape

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if not self.growing:
            self.body.pop()
        self.growing = False
        self.body.insert(0, new_head)

    def grow(self):
        self.growing = True

    def draw(self):
        for segment in self.body:
            x, y = segment
            if self.shape == "rectangle":
                pygame.draw.rect(screen, self.color, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.circle(screen, self.color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)

    def change_direction(self, new_direction):
        if (new_direction[0], new_direction[1]) != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

    def check_collision(self):
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or head_x >= WIDTH or 
            head_y < 0 or head_y >= HEIGHT or 
            (head_x, head_y) in self.body[1:]
        )

class AI_Snake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, shape="circle")

    def move_ai(self, food_pos, player_snake):
        head_x, head_y = self.body[0]
        food_x, food_y = food_pos
        possible_moves = [(CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)]
        best_move = self.direction
        min_distance = float("inf")
        for move in possible_moves:
            new_x, new_y = head_x + move[0], head_y + move[1]
            distance = abs(new_x - food_x) + abs(new_y - food_y)
            if (new_x, new_y) not in self.body and (new_x, new_y) not in player_snake.body and distance < min_distance:
                best_move = move
                min_distance = distance
        self.change_direction(best_move)
        self.move()
        self.teleport_through_walls()

    def teleport_through_walls(self):
        head_x, head_y = self.body[0]
        new_x = head_x % WIDTH
        new_y = head_y % HEIGHT
        self.body[0] = (new_x, new_y)

def generate_food(snake1, snake2):
    while True:
        food = (
            random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        )
        if food not in snake1.body and food not in snake2.body:
            return food

# --- Main Game Function ---
def play_game():
    player_speed, ai_move_delay, expert_mode = choose_difficulty()
    game_duration = choose_game_duration()  # game_duration is now in seconds
    player_color, ai_color = choose_colors()
    
    player = Snake(100, 100, player_color, shape="rectangle")
    ai_snake = AI_Snake(400, 100, ai_color)
    food = generate_food(player, ai_snake)
    
    food_move_counter = 0
    running = True
    game_duration_ms = game_duration * 1000  # convert seconds to milliseconds
    start_ticks = pygame.time.get_ticks()
    
    while running:
        screen.fill(WHITE)
        
        elapsed_time = pygame.time.get_ticks() - start_ticks
        remaining_time = max(0, (game_duration_ms - elapsed_time) // 1000)
        time_display = font.render(f"Time Left: {remaining_time}s", True, BLACK)
        screen.blit(time_display, (10, 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    player.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    player.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    player.change_direction((CELL_SIZE, 0))
                    
        player.move()
        if food_move_counter % ai_move_delay == 0:
            ai_snake.move_ai(food, player)
        
        if expert_mode:
            food_move_counter += 1
            if food_move_counter >= 8:
                food = generate_food(player, ai_snake)
                food_move_counter = 0
        
        if player.check_collision():
            choice = collision_panel()
            return choice
        
        if player.body[0] == food:
            player.grow()
            food = generate_food(player, ai_snake)
        
        if ai_snake.body[0] == food:
            ai_snake.grow()
            food = generate_food(player, ai_snake)
        
        player.draw()
        ai_snake.draw()
        pygame.draw.polygon(screen, RED, [(food[0] + 10, food[1]), (food[0], food[1] + 20), (food[0] + 20, food[1] + 20)])
        
        pygame.display.flip()
        clock.tick(player_speed)
        
        if elapsed_time >= game_duration_ms:
            if len(ai_snake.body) > len(player.body):
                winner = "AI Wins!"
            else:
                winner = "Player Wins!"
            choice = time_over_panel(winner)
            return choice

# --- Main Program Flow ---
def main():
    while True:
        main_menu()
        choice = play_game()
        if choice == "main_menu":
            continue
        else:
            pygame.quit()
            exit()

if __name__ == "__main__":
    main()
