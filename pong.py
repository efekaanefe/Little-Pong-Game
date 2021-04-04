import pygame
import random
import os

pygame.init()
pygame.mixer.init()


ROCKET_SPEED = 7
BALL_SPEED = 6

ROCKET_WIDTH, ROCKET_HEIGHT = 12, 75
BALL_WIDTH, BALL_HEIGHT = 9, 9

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

SCORE_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)


LEFT_PLAYER_ROCKET_IMAGE = pygame.image.load(
    os.path.join("left_player_rocket.png"))
RIGHT_PLAYER_ROCKET_IMAGE = pygame.image.load(
    os.path.join("right_player_rocket.png"))

LEFT_PLAYER_ROCKET = pygame.transform.rotate(
    pygame.transform.scale(LEFT_PLAYER_ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT)), 0)
RIGHT_PLAYER_ROCKET = pygame.transform.rotate(
    pygame.transform.scale(RIGHT_PLAYER_ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT)), 0)

HIT_SOUND = pygame.mixer.Sound(
    os.path.join("hit_sound.mp3"))
HIT_SOUND.set_volume(0.1)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


FPS = 75


def draw_window(left_player, right_player, ball, score_left, score_right):

    WIN.fill(BLACK)
    left_score = SCORE_FONT.render(
        "LEFT: " + str(score_left), 1, RED)
    right_score = SCORE_FONT.render(
        "RIGHT: " + str(score_right), 1, RED)

    WIN.blit(left_score, (left_score.get_width() - 40, 40))
    WIN.blit(right_score, (WIDTH - right_score.get_width() - 40, 40))

    pygame.draw.rect(WIN, WHITE, ball)

    WIN.blit(LEFT_PLAYER_ROCKET, (left_player.x, left_player.y))
    WIN.blit(RIGHT_PLAYER_ROCKET, (right_player.x, right_player.y))

    pygame.display.update()


# I COULDN´T HANDLE IT IN A FUNCTION, BECAUSE I WASN´T ABLE TO CHANGE THE GLOBAL VEL_X, VEL_Y
def handle_ball_movement(ball, left, right, VEL_X, VEL_Y):
    #global VEL_X
    #global VEL_Y

    if ball.y < 0:
        VEL_Y *= -1
    if ball.y + BALL_HEIGHT > HEIGHT:
        VEL_Y *= -1

    ball.x += VEL_X
    ball.y += VEL_Y

    if ball.colliderect(left):
        VEL_X *= -1
    if ball.colliderect(right):
        VEL_X *= -1

    pass


def ball_start_direction(BALL_SPEED):
    VEL_X = BALL_SPEED
    VEL_Y = -BALL_SPEED
    ball_start_direction_x = ["left", "right"]
    start_direction_x = random.choice(ball_start_direction_x)
    ball_start_direction_y = ["up", "down"]
    start_direction_y = random.choice(ball_start_direction_y)

    if start_direction_x == "right":
        VEL_X *= 1
    if start_direction_x == "left":
        VEL_X *= -1
    if start_direction_y == "up":
        VEL_Y *= -1
    if start_direction_y == "up":
        VEL_Y *= 1

    return (VEL_X, VEL_Y)


def handle_left_rocket(keys_pressed, left):
    if keys_pressed[pygame.K_s] and left.y + ROCKET_SPEED + ROCKET_HEIGHT < HEIGHT:
        left.y += ROCKET_SPEED
    if keys_pressed[pygame.K_w] and left.y > 0:
        left.y -= ROCKET_SPEED


def handle_right_rocket(keys_pressed, right):
    if keys_pressed[pygame.K_DOWN] and right.y + ROCKET_SPEED + ROCKET_HEIGHT < HEIGHT:
        right.y += ROCKET_SPEED
    if keys_pressed[pygame.K_UP] and right.y > 0:
        right.y -= ROCKET_SPEED


def draw_winner(winner_text):
    winner = WINNER_FONT.render(winner_text, 1, RED)
    WIN.blit(winner, (WIDTH/2 - winner.get_width() /
                      2, HEIGHT/2 - winner.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    winner_text = ""

    score_left = 0
    score_right = 0

    ball_directions = ball_start_direction(BALL_SPEED)
    VEL_X = ball_directions[0]
    VEL_Y = ball_directions[1]

    left = pygame.Rect(0, 200, ROCKET_WIDTH, ROCKET_HEIGHT)
    right = pygame.Rect(WIDTH - ROCKET_WIDTH, 200, ROCKET_WIDTH, ROCKET_HEIGHT)

    ball = pygame.Rect(WIDTH/2 - BALL_WIDTH, HEIGHT/2 -
                       BALL_HEIGHT, BALL_WIDTH, BALL_HEIGHT)

    clock = pygame.time.Clock()

    run = True

    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        handle_left_rocket(pygame.key.get_pressed(), left)
        handle_right_rocket(pygame.key.get_pressed(), right)

        # I COULDN´T HANDLE IT IN A FUNCTION, BECAUSE I WASN´T ABLE TO CHANGE THE GLOBAL VEL_X, VEL_Y
        #   handle_ball_movement(ball, left, right, VEL_X, VEL_Y)
        #   print(VEL_X, VEL_Y)

        # HITTIN UP OR DOWN
        if ball.y < 0:
            VEL_Y *= -1
        if ball.y + BALL_HEIGHT > HEIGHT:
            VEL_Y *= -1

        ball.x += VEL_X
        ball.y += VEL_Y

        # hitting to rocket
        if ball.colliderect(left) and VEL_X < 0:
            if abs(ball.left - left.right) < 10:
                VEL_X *= -1
                HIT_SOUND.play()
            elif abs(ball.bottom - left.top) < 10 and VEL_Y > 0:
                VEL_Y *= -1
                HIT_SOUND.play()
            elif abs(ball.top - left.bottom) < 10 and VEL_Y < 0:
                VEL_Y *= -1
                HIT_SOUND.play()

        if ball.colliderect(right) and VEL_X > 0:
            if abs(ball.right - right.left) < 10:
                VEL_X *= -1
                HIT_SOUND.play()
            elif abs(ball.bottom - right.top) < 10 and VEL_Y > 0:
                VEL_Y *= -1
                HIT_SOUND.play()
            elif abs(ball.top - right.bottom) < 10 and VEL_Y < 0:
                VEL_Y *= -1
                HIT_SOUND.play()

        # SCORE FOR RIGHT
        if ball.x < 0:
            ball.x = WIDTH/2 - BALL_WIDTH
            ball.y = HEIGHT/2 - BALL_HEIGHT
            score_right += 1
            ball_directions = ball_start_direction(BALL_SPEED)
            VEL_X = ball_directions[0]
            VEL_Y = ball_directions[1]
            pygame.time.delay(1000)

        # SCORE FOR LEFT
        if ball.x + BALL_WIDTH > WIDTH:
            ball.x = WIDTH/2 - BALL_WIDTH
            ball.y = HEIGHT/2 - BALL_HEIGHT
            score_left += 1
            ball_directions = ball_start_direction(BALL_SPEED)
            VEL_X = ball_directions[0]
            VEL_Y = ball_directions[1]
            pygame.time.delay(1000)

        if score_left == 5:
            winner_text = "LEFT PLAYER WINS"
            draw_winner(winner_text)
            main()
        if score_right == 5:
            winner_text = "RIGHT PLAYER WINS"
            draw_winner(winner_text)
            main()

        draw_window(left, right, ball, score_left, score_right)


main()
