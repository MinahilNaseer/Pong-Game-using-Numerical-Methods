import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


paddle_width = 10
paddle_height = 100
ball_radius = 13
base_ball_speed = 5
base_paddle_speed = 6
ai_smoothness = 0.1
winning_score_10 = 10
winning_score_5 = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



pygame.init()
font = pygame.font.Font(None, 36)
