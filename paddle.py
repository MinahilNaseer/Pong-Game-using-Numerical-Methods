import pygame
from config import *

def move_player_paddle(player_paddle, paddle_speed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += paddle_speed


def move_player2_paddle(player2_paddle, paddle_speed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player2_paddle.top > 0:
        player2_paddle.y -= paddle_speed  
    if keys[pygame.K_DOWN] and player2_paddle.bottom < SCREEN_HEIGHT:
        player2_paddle.y += paddle_speed  


def update_paddles(player_paddle, player2_paddle, paddle_speed):
    keys = pygame.key.get_pressed()  
    move_player_paddle(player_paddle, paddle_speed, keys)  
    move_player2_paddle(player2_paddle, paddle_speed, keys)  


def move_ai_paddle(ai_paddle, ball, predicted_y, paddle_speed):
    
    if ai_paddle.centery < predicted_y:
        ai_paddle.y += min(paddle_speed, (predicted_y - ai_paddle.centery) * ai_smoothness)
    elif ai_paddle.centery > predicted_y:
        ai_paddle.y -= min(paddle_speed, (ai_paddle.centery - predicted_y) * ai_smoothness)

    
    if ai_paddle.top < 0:
        ai_paddle.top = 0
    if ai_paddle.bottom > SCREEN_HEIGHT:
        ai_paddle.bottom = SCREEN_HEIGHT
