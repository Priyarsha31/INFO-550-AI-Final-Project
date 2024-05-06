import pygame
from settings import *
pygame.init()
from puzzles import jigsaw_puzzle, color_mapping_puzzle, sudoku_game, logic_puzzle


def welcome_screen(window, font):
    window.fill(BACKGROUND_COLOR)
    welcome_text_1 = "Welcome to the ultimate escape room challenge."
    welcome_text_2 = "Can you unlock the mysteries within and break free?"
    render_1 = font.render(welcome_text_1, True, FONT_COLOR)
    render_2 = font.render(welcome_text_2, True, FONT_COLOR)
    window.blit(render_1, (WINDOW_WIDTH // 2 - render_1.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
    window.blit(render_2, (WINDOW_WIDTH // 2 - render_2.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
    pygame.display.update()
    pygame.time.wait(3000)  # Display for 3 seconds

def run_game():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('AI CSP Escape Room Challenge')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Adjust font size and style as needed

    welcome_screen(window, font)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Call your game functions here, pass window and font
        color_mapping_puzzle(window, font)
        logic_puzzle(window, font)
        jigsaw_puzzle(window, font)
        sudoku_game(window, font)

        running = False


        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    run_game()