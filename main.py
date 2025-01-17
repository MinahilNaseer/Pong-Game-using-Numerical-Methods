import sys
import pygame
import time
import random
import math
from config import *
from paddle import move_player_paddle,move_player2_paddle, move_ai_paddle
from ball import move_ball
from numerical_methods import rk4_predict_position, bisection_method_for_collision, euler_predict_position,  ball_paddle_collision_predictor
from utils import countdown, draw, display_winner

pygame.init()


if len(sys.argv) > 1:
    game_mode = sys.argv[1]
else:
    game_mode = "single"  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")


def get_player_name():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ""
    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return name.strip() if name.strip() else "Guest"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        screen.fill((30, 30, 30))
        text_surface = font.render("Enter Name:", True, WHITE)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        txt_surface = font.render(name, True, WHITE)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))

        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        pygame.time.Clock().tick(30)


def get_player_name_multi():
    input_box_1 = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 25, 150, 50)
    input_box_2 = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 25, 150, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    name1 = ""
    name2 = ""
    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_1.collidepoint(event.pos):
                    active1 = not active1
                    active2 = False
                elif input_box_2.collidepoint(event.pos):
                    active2 = not active2
                    active1 = False
                else:
                    active1 = active2 = False
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN and name1.strip():
                        active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        name1 = name1[:-1]
                    else:
                        name1 += event.unicode
                elif active2:
                    if event.key == pygame.K_RETURN and name2.strip():
                        active2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        name2 = name2[:-1]
                    else:
                        name2 += event.unicode

        screen.fill((30, 30, 30))
        heading = font.render("Enter Player Names:", True, WHITE)
        screen.blit(heading, (SCREEN_WIDTH // 2 - heading.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        txt_surface1 = font.render(name1, True, WHITE)
        txt_surface2 = font.render(name2, True, WHITE)

        input_box_1.w = max(150, txt_surface1.get_width() + 10)
        input_box_2.w = max(150, txt_surface2.get_width() + 10)

        screen.blit(txt_surface1, (input_box_1.x + 5, input_box_1.y + 10))
        screen.blit(txt_surface2, (input_box_2.x + 5, input_box_2.y + 10))

        pygame.draw.rect(screen, color1, input_box_1, 2)
        pygame.draw.rect(screen, color2, input_box_2, 2)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

        if not active1 and not active2 and name1.strip() and name2.strip():
            return name1.strip(), name2.strip()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

if game_mode == "single":
    player_name = get_player_name()
    if player_name is None:
        pygame.quit()
        sys.exit()
    print("Player Name:", player_name)
else:
    player_name_1, player_name_2 = get_player_name_multi()
    if player_name_1 is None or player_name_2 is None:
        pygame.quit()
        sys.exit()
    print("Player 1 Name:", player_name_1)
    print("Player 2 Name:", player_name_2)


player_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
player2_paddle = pygame.Rect(SCREEN_WIDTH - 50 - paddle_width, SCREEN_HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_radius, ball_radius)
ball_dx = base_ball_speed * random.choice((1, -1))
ball_dy = base_ball_speed * random.choice((1, -1))
player_score = ai_score = 0
start_time = time.time()
clock = pygame.time.Clock()

countdown(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed_time = time.time() - start_time
    difficulty_factor = 1 + (elapsed_time / 60)
    paddle_speed = base_paddle_speed * difficulty_factor
    ball_dx = base_ball_speed * difficulty_factor * math.copysign(1, ball_dx)
    ball_dy = base_ball_speed * difficulty_factor * math.copysign(1, ball_dy)

    if game_mode == "single":
        
        move_player_paddle(player_paddle, paddle_speed)
        predicted_time = ball_paddle_collision_predictor(ball, ball_dx, ball_dy, player2_paddle.y) 
        predicted_x, predicted_y = rk4_predict_position(ball, ball_dx, ball_dy, predicted_time)
        move_ai_paddle(player2_paddle, ball, predicted_y, paddle_speed)
        ball_dx, ball_dy, player_score, ai_score = move_ball(ball, ball_dx, ball_dy, player_paddle, player2_paddle, player_score, ai_score)

        
        if player_score >= 10:
            display_winner(screen, f"{player_name}")
            running = False
        elif ai_score >= 10:
            display_winner(screen, "AI")
            running = False

    elif game_mode == "multi":
        
        move_player_paddle(player_paddle, paddle_speed)
        move_player2_paddle(player2_paddle, paddle_speed)  
        predicted_time = bisection_method_for_collision(ball, player2_paddle.x, ball_dx, ball_dy)
        _, predicted_y = euler_predict_position(ball, ball_dx, ball_dy, predicted_time)  
        ball_dx, ball_dy, player_score, ai_score = move_ball(ball, ball_dx, ball_dy, player_paddle, player2_paddle, player_score, ai_score)


        if player_score >= 10:
            display_winner(screen, f"{player_name_1}")
            running = False
        elif ai_score >= 10:
            display_winner(screen, f"{player_name_2}")
            running = False

    
    draw(screen, player_paddle, player2_paddle, ball, player_score, ai_score, elapsed_time)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
