# BUNDLE FILES:
#
#     cd pong
#     Python -m PyInstaller --onefile --windowed --add-data "pong.png:." --add-data "hit.wav:." multi.py    
#
#

try:
    import pygame
    from pygame.locals import QUIT, KEYDOWN
    import sys
    import os

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
            

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


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

    ICON: pygame.Surface = pygame.image.load(resource_path("pong.png"))

    HIT: pygame.mixer.Sound = pygame.mixer.Sound(resource_path('hit.wav'))

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
    volume: float = 0.45
    ball = Ball(PLAYER_WIDTH, OFFSET, SCREEN_HEIGHT, BALL_WIDTH, BALL_HEIGHT)
    paused: bool = False

    # Set the window name to 'Pong'
    pygame.display.set_caption("Pong")
    pygame.display.set_icon(ICON)
    HIT.set_volume(volume)

    def pause():
        global paused, start
        paused = True

        if not start:
            while paused:

                KEY: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
                text_pause: pygame.Surface = FONT.render("PAUSED", True, WHITE)
                text_rect: pygame.Rect = text_pause.get_rect()
                text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

                text_info: pygame.Surface = START.render("PRESS 'P' TO CONTINUE", True, WHITE)
                info_rect: pygame.Rect = text_info.get_rect()
                info_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + text_pause.get_height() + OFFSET)

                SCREEN.blit(text_pause, text_rect)
                SCREEN.blit(text_info, info_rect)

                if KEY[pygame.K_p]:
                    paused = False
                    break

                for event in pygame.event.get():

                    # If the window's 'x' button is pressed
                    if event.type == QUIT:
                        paused = False
                        pygame.quit()
                pygame.display.update()



    # Game
    while run:
        HIT.set_volume(volume)
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
        if KEY[pygame.K_UP]:
            if not OPPONENT.top <= 0:
                OPPONENT.move_ip(0, -1)
        
        if KEY[pygame.K_s]:
            if not PLAYER.bottom >= SCREEN_HEIGHT:
                PLAYER.move_ip(0, 1)
                if start:
                    ball.rect.move_ip(0, 1)
        
        if KEY[pygame.K_DOWN]:
            if not OPPONENT.bottom >= SCREEN_HEIGHT:
                OPPONENT.move_ip(0, 1)
        
        if KEY[pygame.K_m]:
            if volume == 0:
                volume = 0.45
            else:
                volume = 0

        if KEY[pygame.K_ESCAPE]:
            pause()

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
except pygame.error:
    pass
