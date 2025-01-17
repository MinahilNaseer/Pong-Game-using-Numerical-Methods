import pygame
import sys
import subprocess

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (100, 149, 237)
SHADOW_COLOR = (50, 50, 50)

background_image = pygame.image.load("pong_BG.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 36)


def draw_text():
    pong_text = font.render("PONG", True, WHITE)
    game_text = font.render("GAME", True, WHITE)
    pong_text_rect = pong_text.get_rect(center=(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 3))
    game_text_rect = game_text.get_rect(center=(SCREEN_WIDTH // 3.2 + 190, SCREEN_HEIGHT // 2 + 100))
    screen.blit(pong_text, pong_text_rect)
    screen.blit(game_text, game_text_rect)


def draw_buttons():
    button_width = 180
    button_height = 60
    shadow_offset = 5
    border_radius = 20
    
    single_player_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 200, button_width, button_height)
    single_player_shadow_rect = single_player_button_rect.move(shadow_offset, shadow_offset)
    pygame.draw.rect(screen, SHADOW_COLOR, single_player_shadow_rect, border_radius=border_radius)
    pygame.draw.rect(screen, ORANGE, single_player_button_rect, border_radius=border_radius)
    single_player_text = button_font.render("Single Player", True, BLACK)
    single_player_text_rect = single_player_text.get_rect(center=single_player_button_rect.center)
    screen.blit(single_player_text, single_player_text_rect)

    
    multiplayer_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, button_width, button_height)
    multiplayer_shadow_rect = multiplayer_button_rect.move(shadow_offset, shadow_offset)
    pygame.draw.rect(screen, SHADOW_COLOR, multiplayer_shadow_rect, border_radius=border_radius)
    pygame.draw.rect(screen, ORANGE, multiplayer_button_rect, border_radius=border_radius)
    multiplayer_text = button_font.render("Multiplayer", True, BLACK)
    multiplayer_text_rect = multiplayer_text.get_rect(center=multiplayer_button_rect.center)
    screen.blit(multiplayer_text, multiplayer_text_rect)

    return single_player_button_rect, multiplayer_button_rect


def wait_for_button_click():
    single_player_button_rect, multiplayer_button_rect = draw_buttons()
    waiting = True
    hovering_over_button = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if single_player_button_rect.collidepoint(mouse_pos):
                    print("Single Player selected")
                    
                    subprocess.Popen(["python", "main.py", "single"])  
                    waiting = False
                elif multiplayer_button_rect.collidepoint(mouse_pos):
                    print("Multiplayer selected")
                    
                    subprocess.Popen(["python", "main.py", "multi"])  
                    waiting = False

        
        mouse_pos = pygame.mouse.get_pos()
        if single_player_button_rect.collidepoint(mouse_pos) or multiplayer_button_rect.collidepoint(mouse_pos):
            if not hovering_over_button:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                hovering_over_button = True
        else:
            if hovering_over_button:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                hovering_over_button = False

        screen.blit(background_image, (0, 0))
        draw_text()
        draw_buttons()
        pygame.display.flip()


def start_screen():
    screen.blit(background_image, (0, 0))
    draw_text()
    draw_buttons()
    pygame.display.flip()
    wait_for_button_click()

start_screen()
pygame.quit()
