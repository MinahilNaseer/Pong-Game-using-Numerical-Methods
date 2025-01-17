from config import *
import random

def detect_collision(ball, paddle):
    return ball.colliderect(paddle)


def move_ball(ball, ball_dx, ball_dy, player_paddle, ai_paddle, player_score, ai_score, multi=False):
    ball.x += ball_dx
    ball.y += ball_dy
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_dy = -ball_dy
    if detect_collision(ball, player_paddle) or detect_collision(ball, ai_paddle):
        ball_dx = -ball_dx    
    if multi:
        
        if ball.left <= 0:
            player_score += 1
            reset_ball(ball, ball_dx, ball_dy)
        elif ball.right >= SCREEN_WIDTH:
            ai_score += 1
            reset_ball(ball, ball_dx, ball_dy)
    else:
        if ball.left <= 0:
            ai_score += 1
            reset_ball(ball, ball_dx, ball_dy)
        elif ball.right >= SCREEN_WIDTH:
            player_score += 1
            reset_ball(ball, ball_dx, ball_dy)

    return ball_dx, ball_dy, player_score, ai_score


def reset_ball(ball, ball_dx, ball_dy):
    ball.x = SCREEN_WIDTH // 2
    ball.y = SCREEN_HEIGHT // 2
    ball_dx = base_ball_speed * random.choice((1, -1))
    ball_dy = base_ball_speed * random.choice((1, -1))

