import pygame
import time
from config import *

def countdown(screen):
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        countdown_text = font.render(str(i), True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

def display_winner(screen, winner):
    screen.fill(BLACK)
    win_text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)

def draw(screen, player_paddle, ai_paddle, ball, player_score, ai_score, elapsed_time):
    screen.fill(BLACK)
    pygame.draw.line(screen, BLUE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
    pygame.draw.rect(screen, RED, screen.get_rect(), 4)

    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
    ai_text = font.render(str(ai_score), True, WHITE)
    screen.blit(ai_text, (SCREEN_WIDTH * 3 // 4, 20))

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 50, 20))
