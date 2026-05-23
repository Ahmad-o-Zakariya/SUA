
import random
from collections import deque
from dataclasses import dataclass
import pygame

pygame.init()
pygame.display.set_caption("Snake Arena: Player vs AI")

WIDTH, HEIGHT = 800, 600
CELL = 20
GRID_W, GRID_H = WIDTH // CELL, HEIGHT // CELL
FPS = 60

# Colors
BG = (12, 14, 24)
PANEL = (20, 24, 38)
PANEL_2 = (28, 33, 52)
TEXT = (240, 244, 255)
MUTED = (160, 170, 195)
ACCENT = (98, 193, 255)
ACCENT_2 = (127, 255, 212)
DANGER = (255, 102, 102)
FOOD = (255, 187, 84)
GRID = (26, 31, 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_SWATCHES = [
    ("Emerald", (46, 204, 113)),
    ("Ruby", (231, 76, 60)),
    ("Azure", (52, 152, 219)),
    ("Gold", (241, 196, 15)),
    ("Amber", (230, 126, 34)),
    ("Violet", (155, 89, 182)),
]
AI_SWATCHES = [
    ("Neon Blue", (82, 169, 255)),
    ("Orchid", (196, 113, 237)),
    ("Cyan", (68, 221, 255)),
    ("Magenta", (255, 77, 166)),
    ("Brown", (160, 110, 74)),
    ("Teal", (46, 204, 187)),
]

DIFFICULTIES = {
    "Easy": {"tick_rate": 7, "ai_bias": 0.45, "label": "Easy"},
    "Medium": {"tick_rate": 9, "ai_bias": 0.62, "label": "Medium"},
    "Hard": {"tick_rate": 11, "ai_bias": 0.78, "label": "Hard"},
    "Expert": {"tick_rate": 13, "ai_bias": 0.92, "label": "Expert"},
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 22)
small = pygame.font.SysFont("Segoe UI", 18)
title_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
subtitle_font = pygame.font.SysFont("Segoe UI", 30, bold=True)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def grid_to_px(cell):
    return cell[0] * CELL, cell[1] * CELL

def px_to_grid(px):
    return px[0] // CELL, px[1] // CELL

def draw_text(text, x, y, fnt=font, color=TEXT, center=False):
    surf = fnt.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)
    return rect

def draw_rounded_panel(rect, color, radius=18, border=None):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(screen, border, rect, width=2, border_radius=radius)

def draw_grid():
    screen.fill(BG)
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)

@dataclass
class Button:
    rect: pygame.Rect
    label: str
    value: object = None

    def draw(self, hovered=False, active=False):
        base = PANEL_2 if not hovered else (36, 42, 66)
        border = ACCENT if active else (70, 80, 110)
        draw_rounded_panel(self.rect, base, radius=16, border=border)
        draw_text(self.label, self.rect.centerx, self.rect.centery, font, TEXT, center=True)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

class Snake:
    def __init__(self, start_cell, color, wrap=False):
        self.body = deque([start_cell])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.color = color
        self.wrap = wrap
        self.grow_pending = 0

    @property
    def head(self):
        return self.body[0]

    def set_direction(self, direction):
        if direction == (-self.direction[0], -self.direction[1]):
            return
        self.next_direction = direction

    def move(self):
        self.direction = self.next_direction
        x, y = self.head
        dx, dy = self.direction
        nx, ny = x + dx, y + dy
        if self.wrap:
            nx %= GRID_W
            ny %= GRID_H
        new_head = (nx, ny)
        self.body.appendleft(new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def occupies(self, cell):
        return cell in self.body

    def self_collision(self):
        return self.head in list(self.body)[1:]

    def wall_collision(self):
        x, y = self.head
        return not self.wrap and (x < 0 or x >= GRID_W or y < 0 or y >= GRID_H)

    def draw(self, head_color=None):
        body_list = list(self.body)
        for i, cell in enumerate(body_list):
            px, py = grid_to_px(cell)
            rect = pygame.Rect(px + 2, py + 2, CELL - 4, CELL - 4)
            if i == 0 and head_color:
                color = head_color
            else:
                color = self.color
            pygame.draw.rect(screen, color, rect, border_radius=6)
        # eyes on head for polish
        hx, hy = grid_to_px(self.head)
        eye_color = WHITE
        ex1 = hx + CELL // 4
        ex2 = hx + (CELL * 3) // 4
        ey = hy + CELL // 3
        pygame.draw.circle(screen, eye_color, (ex1, ey), 2)
        pygame.draw.circle(screen, eye_color, (ex2, ey), 2)

def wrap_neighbors(cell):
    x, y = cell
    candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    wrapped = [((cx % GRID_W), (cy % GRID_H)) for cx, cy in candidates]
    return wrapped

def neighbors(cell, wrap=False):
    x, y = cell
    candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    result = []
    for cx, cy in candidates:
        if wrap:
            result.append((cx % GRID_W, cy % GRID_H))
        elif 0 <= cx < GRID_W and 0 <= cy < GRID_H:
            result.append((cx, cy))
    return result

def shortest_path(start, goal, blocked, wrap=False):
    if start == goal:
        return [start]
    q = deque([start])
    parent = {start: None}
    while q:
        node = q.popleft()
        for nxt in neighbors(node, wrap=wrap):
            if nxt in blocked or nxt in parent:
                continue
            parent[nxt] = node
            if nxt == goal:
                path = [goal]
                cur = goal
                while parent[cur] is not None:
                    cur = parent[cur]
                    path.append(cur)
                path.reverse()
                return path
            q.append(nxt)
    return None

def flood_fill_area(start, blocked, wrap=False, limit=300):
    if start in blocked:
        return 0
    seen = {start}
    q = deque([start])
    count = 0
    while q and count < limit:
        node = q.popleft()
        count += 1
        for nxt in neighbors(node, wrap=wrap):
            if nxt not in seen and nxt not in blocked:
                seen.add(nxt)
                q.append(nxt)
    return count

def generate_food(player, ai):
    occupied = set(player.body) | set(ai.body)

    while True:
        # Prevent spawning too close to walls
        cell = (
            random.randint(2, GRID_W - 3),
            random.randint(2, GRID_H - 3)
        )

        if cell not in occupied:
            return cell

def ai_choose_move(ai, player, food, difficulty_bias):
    head = ai.head
    blocked = set(player.body) | set(list(ai.body)[1:])
    path = shortest_path(head, food, blocked, wrap=True)
    if path and len(path) >= 2 and random.random() < difficulty_bias:
        return (path[1][0] - head[0], path[1][1] - head[1])

    candidates = []
    for nxt in neighbors(head, wrap=True):
        if nxt in blocked:
            continue
        area = flood_fill_area(nxt, blocked | {head}, wrap=True, limit=350)
        dist = min(abs(nxt[0] - food[0]), GRID_W - abs(nxt[0] - food[0])) + \
               min(abs(nxt[1] - food[1]), GRID_H - abs(nxt[1] - food[1]))
        score = area * 12 - dist * 5
        candidates.append((score, nxt))

    if candidates:
        candidates.sort(reverse=True)
        best = candidates[0][1]
        return (best[0] - head[0], best[1] - head[1])

    # last resort: keep moving, even if suboptimal
    return ai.direction

def draw_food(food, pulse):
    px, py = grid_to_px(food)

    # Center of food
    cx = px + CELL // 2
    cy = py + CELL // 2

    # Smooth pulsing size
    scale = 8 + int(2 * pulse)

    # Prevent absurd growth
    scale = min(scale, 14)

    # Keep food safely inside arena visually
    margin = 18
    cx = clamp(cx, margin, WIDTH - margin)
    cy = clamp(cy, margin, HEIGHT - margin)

    # Triangle points
    points = [
        (cx, cy - scale),
        (cx - scale, cy + scale),
        (cx + scale, cy + scale)
    ]

    # Main triangle
    pygame.draw.polygon(screen, FOOD, points)

    # Outline glow
    pygame.draw.polygon(screen, (255, 240, 210), points, 2)

    # CENTER MARKER
    pygame.draw.circle(screen, WHITE, (cx, cy), 3)

    # Small inner glow
    pygame.draw.circle(screen, (255, 230, 170), (cx, cy), 6, 1)

def draw_hud(duration_left, score, high_score, difficulty_label):
    panel = pygame.Rect(14, 14, 320, 90)
    draw_rounded_panel(panel, (18, 22, 34), radius=18, border=(60, 70, 100))
    draw_text(f"Time Left: {duration_left:>3}s", 30, 28, font, TEXT)
    draw_text(f"Score: {score}", 30, 52, font, ACCENT_2)
    draw_text(f"Best: {high_score}", 170, 52, font, ACCENT)
    draw_text(f"Mode: {difficulty_label}", 170, 28, font, MUTED)

def main_menu():
    buttons = [
        Button(pygame.Rect(WIDTH // 2 - 120, 300, 240, 52), "Start Game"),
        Button(pygame.Rect(WIDTH // 2 - 120, 365, 240, 52), "Controls"),
        Button(pygame.Rect(WIDTH // 2 - 120, 430, 240, 52), "Quit"),
    ]
    while True:
        draw_grid()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((6, 9, 18, 150))
        screen.blit(overlay, (0, 0))

        title = title_font.render("Snake Arena", True, TEXT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 130)))
        draw_text("Player vs AI", WIDTH // 2, 180, subtitle_font, ACCENT_2, center=True)
        draw_text("BeAt the AI if you CAN .", WIDTH // 2, 220, font, MUTED, center=True)

        mouse = pygame.mouse.get_pos()
        for b in buttons:
            b.draw(hovered=b.hit(mouse))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "start"
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons[0].hit(mouse):
                    return "start"
                if buttons[1].hit(mouse):
                    return "controls"
                if buttons[2].hit(mouse):
                    return "quit"

        pygame.display.flip()
        clock.tick(FPS)

def controls_screen():
    back = Button(pygame.Rect(WIDTH // 2 - 90, 500, 180, 48), "Back")
    while True:
        draw_grid()
        card = pygame.Rect(120, 110, 560, 320)
        draw_rounded_panel(card, PANEL, radius=24, border=(60, 70, 100))
        draw_text("Controls", card.centerx, 155, subtitle_font, TEXT, center=True)
        lines = [
            "Arrow keys: move",
            "Enter / Space: confirm",
            "Escape: pause or go back",
            "The AI wraps around walls.",
            "You do not.",
        ]
        for i, line in enumerate(lines):
            draw_text(line, card.centerx, 215 + i * 36, font, MUTED, center=True)

        mouse = pygame.mouse.get_pos()
        back.draw(hovered=back.hit(mouse))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back.hit(mouse):
                return "menu"

        pygame.display.flip()
        clock.tick(FPS)

def difficulty_screen():
    buttons = []
    start_y = 220
    for i, (name, spec) in enumerate(DIFFICULTIES.items()):
        buttons.append(Button(pygame.Rect(WIDTH // 2 - 125, start_y + i * 70, 250, 52), name, spec))
    while True:
        draw_grid()
        draw_text("Choose Difficulty", WIDTH // 2, 120, title_font, TEXT, center=True)
        draw_text("This controls speed and how aggressively the AI commits to the path.", WIDTH // 2, 170, small, MUTED, center=True)
        mouse = pygame.mouse.get_pos()
        for b in buttons:
            b.draw(hovered=b.hit(mouse))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return list(DIFFICULTIES.values())[0]
                if event.key == pygame.K_2:
                    return list(DIFFICULTIES.values())[1]
                if event.key == pygame.K_3:
                    return list(DIFFICULTIES.values())[2]
                if event.key == pygame.K_4:
                    return list(DIFFICULTIES.values())[3]
                if event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    if b.hit(mouse):
                        return b.value
        pygame.display.flip()
        clock.tick(FPS)

def duration_screen():
    duration = 60
    plus = Button(pygame.Rect(WIDTH // 2 + 75, 290, 54, 54), "+")
    minus = Button(pygame.Rect(WIDTH // 2 - 129, 290, 54, 54), "−")
    confirm = Button(pygame.Rect(WIDTH // 2 - 90, 390, 180, 48), "Confirm")
    while True:
        draw_grid()
        draw_text("Set Match Duration", WIDTH // 2, 120, title_font, TEXT, center=True)
        card = pygame.Rect(WIDTH // 2 - 170, 220, 340, 200)
        draw_rounded_panel(card, PANEL, radius=22, border=(60, 70, 100))
        draw_text("Minutes", WIDTH // 2, 255, font, MUTED, center=True)
        draw_text(f"{duration} s", WIDTH // 2, 310, subtitle_font, ACCENT_2, center=True)
        draw_text("Range: 30 to 900 seconds.", WIDTH // 2, 360, small, MUTED, center=True)

        mouse = pygame.mouse.get_pos()
        plus.draw(hovered=plus.hit(mouse))
        minus.draw(hovered=minus.hit(mouse))
        confirm.draw(hovered=confirm.hit(mouse))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    duration = clamp(duration + 15, 30, 900)
                elif event.key == pygame.K_DOWN:
                    duration = clamp(duration - 15, 30, 900)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return duration
                elif event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if plus.hit(mouse):
                    duration = clamp(duration + 15, 30, 900)
                elif minus.hit(mouse):
                    duration = clamp(duration - 15, 30, 900)
                elif confirm.hit(mouse):
                    return duration

        pygame.display.flip()
        clock.tick(FPS)

def color_screen(title, swatches):
    buttons = []
    start_x = WIDTH // 2 - 220
    start_y = 230
    gap_x = 150
    gap_y = 96
    for idx, (name, color) in enumerate(swatches):
        row, col = divmod(idx, 3)
        rect = pygame.Rect(start_x + col * gap_x, start_y + row * gap_y, 130, 70)
        buttons.append((Button(rect, name, color), color))
    while True:
        draw_grid()
        draw_text(title, WIDTH // 2, 120, title_font, TEXT, center=True)
        draw_text("Click a swatch or use number keys 1–6.", WIDTH // 2, 170, small, MUTED, center=True)
        mouse = pygame.mouse.get_pos()
        for idx, (btn, color) in enumerate(buttons):
            hovered = btn.hit(mouse)
            draw_rounded_panel(btn.rect, PANEL_2 if not hovered else (36, 42, 66), radius=16, border=color if hovered else (75, 85, 115))
            pygame.draw.circle(screen, color, (btn.rect.x + 28, btn.rect.centery), 14)
            label = f"{idx + 1}. {btn.label}"

            # Auto-resize if text is too long
            dynamic_font = small
            text_width = dynamic_font.size(label)[0]

            if text_width > 70:
                dynamic_font = pygame.font.SysFont("Segoe UI", 15)

            draw_text(
                label,
                btn.rect.x + 50,
                btn.rect.centery - 9,
                dynamic_font,
                TEXT
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                idx = event.key - pygame.K_1
                if 0 <= idx < len(buttons):
                    return buttons[idx][1]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn, color in buttons:
                    if btn.hit(mouse):
                        return color

        pygame.display.flip()
        clock.tick(FPS)

def pause_screen(score, duration_left):
    while True:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        box = pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 - 110, 360, 220)
        draw_rounded_panel(box, PANEL, radius=24, border=(80, 90, 125))
        draw_text("Paused", box.centerx, box.y + 42, subtitle_font, TEXT, center=True)
        draw_text(f"Score: {score}", box.centerx, box.y + 90, font, ACCENT_2, center=True)
        draw_text(f"Time left: {duration_left}s", box.centerx, box.y + 120, font, MUTED, center=True)
        draw_text("Press Esc to resume", box.centerx, box.y + 160, font, TEXT, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"
        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(result_text, score, high_score):
    retry = Button(pygame.Rect(WIDTH // 2 - 120, 345, 240, 52), "Play Again")
    menu = Button(pygame.Rect(WIDTH // 2 - 120, 410, 240, 52), "Main Menu")
    quit_btn = Button(pygame.Rect(WIDTH // 2 - 120, 475, 240, 52), "Quit")
    while True:
        draw_grid()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((6, 9, 18, 150))
        screen.blit(overlay, (0, 0))
        card = pygame.Rect(WIDTH // 2 - 220, 150, 440, 270)
        draw_rounded_panel(card, PANEL, radius=26, border=(85, 95, 130))
        draw_text("Match Complete", WIDTH // 2, 205, subtitle_font, TEXT, center=True)
        draw_text(result_text, WIDTH // 2, 250, font, DANGER if "AI" in result_text else ACCENT_2, center=True)
        draw_text(f"Score: {score}", WIDTH // 2, 290, font, TEXT, center=True)
        draw_text(f"Best: {high_score}", WIDTH // 2, 320, font, ACCENT, center=True)

        mouse = pygame.mouse.get_pos()
        for b in (retry, menu, quit_btn):
            b.draw(hovered=b.hit(mouse))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "retry"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry.hit(mouse):
                    return "retry"
                if menu.hit(mouse):
                    return "menu"
                if quit_btn.hit(mouse):
                    return "quit"
        pygame.display.flip()
        clock.tick(FPS)

def play_match(difficulty, duration, player_color, ai_color, high_score):
    player = Snake((5, GRID_H // 2), player_color, wrap=False)
    ai = Snake((GRID_W - 6, GRID_H // 2), ai_color, wrap=True)
    ai.direction = (-1, 0)
    ai.next_direction = (-1, 0)

    food = generate_food(player, ai)
    step_clock = 0.0
    elapsed = 0.0
    ai_step_timer = 0.0
    pulse = 0.0
    score = 0

    step_interval = 1.0 / difficulty["tick_rate"]
    ai_interval = step_interval * 0.72

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        elapsed += dt
        step_clock += dt
        ai_step_timer += dt
        pulse += dt * 5

        remaining = max(0, int(duration - elapsed))
        if remaining <= 0:
            if len(ai.body) > len(player.body):
                result = "AI wins by length."
            elif len(ai.body) < len(player.body):
                result = "You win by length."
            else:
                result = "Draw."
            return result, score, high_score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, high_score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = pause_screen(score, remaining)
                    if paused == "quit":
                        return "quit", score, high_score
                elif event.key == pygame.K_UP:
                    player.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    player.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    player.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    player.set_direction((1, 0))

        while step_clock >= step_interval:
            step_clock -= step_interval
            player.move()
            if player.wall_collision() or player.self_collision() or player.head in list(ai.body):
                return "You crashed.", score, max(high_score, score)
            if player.head == food:
                player.grow(1)
                score += 10
                if score > high_score:
                    high_score = score
                food = generate_food(player, ai)

            if ai_step_timer >= ai_interval:
                ai_step_timer = 0.0
                move = ai_choose_move(ai, player, food, difficulty["ai_bias"])
                ai.set_direction(move)
                ai.move()

                if ai.head == food:
                    ai.grow(1)
                    food = generate_food(player, ai)

                # AI can collide into player; if it does, player wins that exchange
                if ai.head in list(player.body):
                    return "AI crashed.", score + 15, max(high_score, score + 15)

        draw_grid()
        draw_food(food, pulse)
        draw_hud(remaining, score, max(high_score, score), difficulty["label"])
        player.draw(head_color=WHITE)
        ai.draw(head_color=WHITE)

        # subtle center divider
        pygame.draw.line(screen, (70, 80, 115), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
        pygame.display.flip()

    return "Done", score, high_score

def main():
    high_score = 0
    while True:
        choice = main_menu()
        if choice == "quit":
            break
        if choice == "controls":
            result = controls_screen()
            if result == "quit":
                break
            continue

        difficulty = difficulty_screen()
        if difficulty is None:
            continue
        duration = duration_screen()
        if duration is None:
            continue
        player_color = color_screen("Choose Player Color", PLAYER_SWATCHES)
        if player_color is None:
            continue
        ai_color = color_screen("Choose AI Color", AI_SWATCHES)
        if ai_color is None:
            continue

        result_text, score, high_score = play_match(difficulty, duration, player_color, ai_color, high_score)
        if result_text == "quit":
            break

        action = game_over_screen(result_text, score, high_score)
        if action == "quit":
            break
        if action == "retry":
            result_text, score, high_score = play_match(difficulty, duration, player_color, ai_color, high_score)
            if result_text == "quit":
                break
            action = game_over_screen(result_text, score, high_score)
            if action == "quit":
                break

    pygame.quit()

if __name__ == "__main__":
    main()
