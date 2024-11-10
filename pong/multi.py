import pygame
from pygame.locals import QUIT
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Classes
class Ball:
    def __init__(self, player_width, offset, screen_height, ball_width, ball_height):
        self.start = True
        self.PLAYER_WIDTH = player_width
        self.OFFSET = offset
        self.SCREEN_HEIGHT = screen_height
        self.BALL_WIDTH = ball_width
        self.BALL_HEIGHT = ball_height
        self.rect: pygame.Rect = pygame.Rect(self.PLAYER_WIDTH + self.OFFSET, self.SCREEN_HEIGHT / 2 + self.BALL_WIDTH, self.BALL_WIDTH, self.BALL_HEIGHT)
        self.ballX: int = 1
        self.ballY: int = 1

    def move(self, player_rect, opponent_rect):
        if self.rect.top <= 0 or self.rect.bottom >= self.SCREEN_HEIGHT:
            self.ballY = -self.ballY
            HIT.play()

        if self.rect.colliderect(player_rect) or self.rect.colliderect(opponent_rect):
            self.ballX = -self.ballX

            if self.rect.colliderect(player_rect):
                self.rect.left = player_rect.right
            elif self.rect.colliderect(opponent_rect):
                self.rect.right = opponent_rect.left

            
            HIT.play()

        self.rect.move_ip(self.ballX, -self.ballY)

    def reset(self):
        self.start = True
        self.rect = pygame.Rect(SCREEN_WIDTH / 2, 0, self.BALL_WIDTH, self.BALL_HEIGHT)
        self.ballX = 1
        self.ballY = 1


# Constants
BLUE : list[int] = (0, 0, 255)
RED  : list[int] = (255, 0, 0)
GREEN: list[int] = (0, 255, 0)
BLACK: list[int] = (0, 0, 0)
WHITE: list[int] = (255, 255, 255)

OFFSET: int = 25

MISTAKE_OFFSET: int = 150
DIFFICULTY: float = 3.5

SCREEN_HEIGHT: int = 600
SCREEN_WIDTH: int = 800
SCREEN: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ICON: pygame.Surface = pygame.image.load("./pong/assets/icon/pong.png")

HIT: pygame.mixer.Sound = pygame.mixer.Sound('./pong/assets/sfx/hit.wav')
VOLUME: float = 0.45

PLAYER_HEIGHT: int = 100
PLAYER_WIDTH: int = 20
PLAYER: pygame.Rect = pygame.Rect((0 + OFFSET, SCREEN_HEIGHT / 2 - PLAYER_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT))

OPPONENT_HEIGHT: int = 100
OPPONENT_WIDTH: int = 20
OPPONENT: pygame.Rect = pygame.Rect((SCREEN_WIDTH - OPPONENT_WIDTH - OFFSET, SCREEN_HEIGHT / 2 - OPPONENT_WIDTH, OPPONENT_WIDTH, OPPONENT_HEIGHT))

BALL_HEIGHT: int = 20
BALL_WIDTH: int = 20

SPEED: int = 450
FPS: pygame.time.Clock = pygame.time.Clock()

FONT_SIZE: int = SCREEN_HEIGHT // 3
FONT_Y: int = 100
FONT_X: int = 100
FONT: pygame.font.Font = pygame.font.Font(None, FONT_SIZE)
START: pygame.font.Font = pygame.font.Font(None, FONT_SIZE // 3)

# Variables
start: bool = True
run: bool = True
ballY: int = 1
ballX: int = 1
score_player: int = 0
score_opponent: int = 0
text_start: pygame.Surface = FONT.render("PRESS SPACE TO START", True, WHITE)
text_player: pygame.Surface = FONT.render(str(score_player), True, WHITE)
text_opp: pygame.Surface = FONT.render(str(score_opponent), True, WHITE)

ball = Ball(PLAYER_WIDTH, OFFSET, SCREEN_HEIGHT, BALL_WIDTH, BALL_HEIGHT)

# Set the window name to 'Pong'
pygame.display.set_caption("Pong")
pygame.display.set_icon(ICON)
HIT.set_volume(VOLUME)


# Game
while run:
    if not start:
        ball.move(PLAYER, OPPONENT)


    

    SCREEN.fill(BLACK)
    KEY: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

    if start:
        text_start: pygame.Surface = START.render("PRESS SPACE TO START", True, WHITE)
        text_rect: pygame.Rect = text_start.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text_start, text_rect)

    text_opp: pygame.Surface = FONT.render(str(score_opponent), True, WHITE)
    text_player: pygame.Surface = FONT.render(str(score_player), True, WHITE)
    SCREEN.blit(text_player, (OFFSET * 3, FONT_Y))
    SCREEN.blit(text_opp, (SCREEN_WIDTH - text_opp.get_width() - OFFSET * 3, FONT_Y))

    # Draw player, ball and opponent
    pygame.draw.rect(SCREEN, WHITE, PLAYER)
    pygame.draw.rect(SCREEN, RED, ball.rect)
    pygame.draw.rect(SCREEN, WHITE, OPPONENT)

    if KEY[pygame.K_SPACE]:
        if start:
            start = False
    if KEY[pygame.K_w]:
        if not PLAYER.top <= 0:
            PLAYER.move_ip(0, -1)
            if start:
                ball.rect.move_ip(0, -1)
    elif KEY[pygame.K_UP]:
        if not OPPONENT.top <= 0:
            OPPONENT.move_ip(0, -1)
    
    elif KEY[pygame.K_s]:
        if not PLAYER.bottom >= SCREEN_HEIGHT:
            PLAYER.move_ip(0, 1)
            if start:
                ball.rect.move_ip(0, 1)
    
    elif KEY[pygame.K_DOWN]:
        if not OPPONENT.bottom >= SCREEN_HEIGHT:
            OPPONENT.move_ip(0, 1)

    if ball.rect.right >= SCREEN_WIDTH:
        ball.reset()
        score_player = score_player + 1
    elif ball.rect.left <= 0:
        ball.reset()
        score_opponent = score_opponent + 1

    # Execute the following code every event
    for event in pygame.event.get():

        # If the window's 'x' button is pressed
        if event.type == QUIT:
            run = False

    # Update the window
    pygame.display.update()

    # Limit FPS to the Player speed
    FPS.tick(SPEED)


# Close window when broken out of the while loop
pygame.quit()
