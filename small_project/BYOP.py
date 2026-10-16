# (B)ring (Y)our (O)wn (P)et - is a python program that will let you draw a friend for your computer.
# It will follow you everywhere, whether it wants to or not.
# It might have some nice things to say, or maybe some NOT such nice things to says sometimes.

# Main program loop:
# Check mouse inputs.
# Check whether 6 seconds have passed to comment.
# Draws drawing onto the screen.
# Use flip() to show updated frame.
# tick() limits the fps aka maximum while loops.

# Sources: https://www.pygame.org/docs/

import pygame
import random

pygame.init()

# Window settings
WIDTH, HEIGHT = 450, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BYOP")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
comment_font = pygame.font.SysFont(None, 26)

# Colors
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
BACKGROUND = (245, 245, 245)

# Drawing canvas
canvas_rect = pygame.Rect(20, 60, 410, 235)
canvas = pygame.Surface(canvas_rect.size)
canvas.fill(WHITE)

# Buttons
clear_button = pygame.Rect(85, 305, 120, 35)
start_button = pygame.Rect(225, 305, 140, 35)

# Comments
comments = [
    "Nice!",
    "Good job!",
    "That's actually good!",
    "I believe in you!",
    "Positive Aura+",
    "Keep going!",
    "The horse is here.",
    "Nice weather we are having today."
    "What is that?",
    "Bro...",
    "Interesting...",
    "Aura Loss-",
    "Delete me",
    "On my chungus what are we doing here?",
    "Who are you anyways?",
    "Why are we here? Just to suffer?"
]

# Drawing settings
drawing = False
last_pos = None
brush_size = 4

# Comment settings
judging = False
current_comment = ""
last_comment_time = 0

# 6 seconds is 6,000 milliseconds
COMMENT_INTERVAL = 6000

def draw_button(rect, text, dark=False):
    color = BLACK if dark else WHITE
    text_color = WHITE if dark else BLACK

    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 1, border_radius=6)

    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))

running = True

while running:
    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if canvas_rect.collidepoint(event.pos):
                drawing = True

                last_pos = (
                    event.pos[0] - canvas_rect.x,
                    event.pos[1] - canvas_rect.y
                )

                pygame.draw.circle(canvas, BLACK, last_pos, brush_size)

            elif clear_button.collidepoint(event.pos):
                canvas.fill(WHITE)
                current_comment = ""

            elif start_button.collidepoint(event.pos):
                judging = not judging

                if judging:
                    current_comment = "Hello"
                    last_comment_time = pygame.time.get_ticks()
                else:
                    current_comment = ""

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            last_pos = None

        elif event.type == pygame.MOUSEMOTION and drawing:

            x = event.pos[0] - canvas_rect.x
            y = event.pos[1] - canvas_rect.y

            # Keep drawing inside canvas
            x = max(0, min(x, canvas_rect.width - 1))
            y = max(0, min(y, canvas_rect.height - 1))

            current_pos = (x, y)

            pygame.draw.line(
                canvas,
                BLACK,
                last_pos,
                current_pos,
                brush_size * 2
            )

            pygame.draw.circle(
                canvas,
                BLACK,
                current_pos,
                brush_size
            )

            last_pos = current_pos

    # Random comment every 6 seconds
    if judging:
        current_time = pygame.time.get_ticks()

        if current_time - last_comment_time >= COMMENT_INTERVAL:
            current_comment = random.choice(comments)
            last_comment_time = current_time

    # Draw interface
    screen.fill(BACKGROUND)

    # Title
    title = font.render("Draw your helpful friend", True, BLACK)
    screen.blit(title, (20, 20))

    # Canvas
    screen.blit(canvas, canvas_rect.topleft)

    # Comment bubble
    if current_comment:
        bubble_width = min(
            410,
            max(150, comment_font.size(current_comment)[0] + 30)
        )

        bubble = pygame.Rect(
            WIDTH // 2 - bubble_width // 2,
            8,
            bubble_width,
            48
        )

        pygame.draw.rect(
            screen, WHITE, bubble, border_radius=10
        )
        pygame.draw.rect(
            screen, BLACK, bubble, 2, border_radius=10
        )

        text = comment_font.render(current_comment, True, BLACK)
        screen.blit(text, text.get_rect(center=bubble.center))

    # Buttons
    draw_button(clear_button, "Clear")
    draw_button(
        start_button,
        "Stop" if judging else "Start Judging",
        dark=True
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
