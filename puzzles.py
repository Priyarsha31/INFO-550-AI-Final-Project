import pygame
import random
from settings import *
import sys
from utils import load_and_slice_image, draw_tiles
from constraint import Problem, AllDifferentConstraint
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AI CSP Escape Room Challenge')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def csp_constraints(tile_order):
    problem = Problem()
    problem.addVariables(range(len(tile_order)), range(len(tile_order)))
    problem.addConstraint(AllDifferentConstraint())
    return problem.getSolutions()

def jigsaw_puzzle(window, font):
    tiles, tile_width, tile_height = load_and_slice_image('C:/Users/Administrator/INFO-550-AI-Final-Project/scary.jpg', 3, 3)
    tile_order = list(range(9))
    random.shuffle(tile_order)

    # Apply CSP to ensure all tiles have unique positions
    solutions = csp_constraints(tile_order)
    if not solutions:
        print("No valid tile arrangements found.")
        return

    selected_tile = None
    solved = False  # To check if the puzzle has been solved

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if not solved:  # Only allow interaction if not solved
                    if selected_tile is None:
                        mouse_x, mouse_y = event.pos
                        selected_index = (mouse_y - (WINDOW_HEIGHT - 300) // 2) // tile_height * 3 + (mouse_x - (WINDOW_WIDTH - 300) // 2) // tile_width
                        if 0 <= selected_index < len(tile_order):
                            selected_tile = selected_index
                    else:
                        mouse_x, mouse_y = event.pos
                        clicked_index = (mouse_y - (WINDOW_HEIGHT - 300) // 2) // tile_height * 3 + (mouse_x - (WINDOW_WIDTH - 300) // 2) // tile_width
                        if 0 <= clicked_index < len(tile_order):
                            tile_order[selected_tile], tile_order[clicked_index] = tile_order[clicked_index], tile_order[selected_tile]
                            selected_tile = None
                            if tile_order == sorted(tile_order):
                                solved = True
                                print("Puzzle solved! Proceeding to the final stage...")
                                pygame.display.set_caption("Puzzle solved! Proceeding to the final stage...")
                                window.fill(BACKGROUND_COLOR)
                                message_line1 = "  Amazing! You've pieced together the third puzzle."
                                message_line2 = "But the tension mounts as you approach the final hurdle."
                                render_line1 = font.render(message_line1, True, FONT_COLOR)
                                render_line2 = font.render(message_line2, True, FONT_COLOR)

                                # Determine the vertical position for each line
                                line_spacing = 20  # Adjust as needed
                                line1_y = WINDOW_HEIGHT // 2 - 30
                                line2_y = line1_y + render_line1.get_height() + line_spacing

                                window.blit(render_line1, (100, line1_y))
                                window.blit(render_line2, (100, line2_y))
                                pygame.display.update()
                                pygame.time.wait(3500)
                                return True

        if not solved:
            window.fill(BACKGROUND_COLOR)
            draw_tiles(tile_order, tiles, tile_width, tile_height, window)
            pygame.display.update()

        clock.tick(FPS)


#####################################################################3

def color_mapping_puzzle(window, font):
    tile_count = 16  # 4x4 grid
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
    tile_width = 100
    tile_height = 100
    tile_positions = [(i % 4 * tile_width + (WINDOW_WIDTH - 4 * tile_width) // 2,
                       i // 4 * tile_height + (WINDOW_HEIGHT - 4 * tile_height) // 2) for i in range(tile_count)]

    # Initial random color assignment
    color_index = [random.randint(0, len(colors) - 1) for _ in range(tile_count)]

    def check_solution():
        adjacency_list = [
            (0, 1), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7),
            (4, 5), (4, 8), (5, 6), (5, 9), (6, 7), (6, 10), (7, 11),
            (8, 9), (8, 12), (9, 10), (9, 13), (10, 11), (10, 14), (11, 15),
            (12, 13), (13, 14), (14, 15)
        ]
        return all(colors[color_index[a]] != colors[color_index[b]] for a, b in adjacency_list)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for idx, pos in enumerate(tile_positions):
                    rect = pygame.Rect(pos[0], pos[1], tile_width, tile_height)
                    if rect.collidepoint(x, y):
                        color_index[idx] = (color_index[idx] + 1) % len(colors)  # Cycle through colors

        window.fill(BACKGROUND_COLOR)

        # Draw instructions
        instructions_1 = "Click tiles to change colors. "
        instructions_2 = "No two adjacent tiles should have the same color."
        instruction_text_1 = font.render(instructions_1, True, FONT_COLOR)
        instruction_text_2 = font.render(instructions_2, True, FONT_COLOR)
        window.blit(instruction_text_1, (50, 30))
        window.blit(instruction_text_2, (50, 60))

        # Draw tiles
        for idx, pos in enumerate(tile_positions):
            pygame.draw.rect(window, colors[color_index[idx]], (pos[0], pos[1], tile_width, tile_height))

        pygame.display.update()
        clock.tick(FPS)

        if check_solution():
            pygame.time.wait(2000)
            message_1 = "Congratulations! You've successfully decoded the colors, "
            message_2 = "             but the room holds more challenges."
            message_render_1 = font.render(message_1, True, FONT_COLOR)
            message_render_2 = font.render(message_2, True, FONT_COLOR)
            line_spacing = 10
            window.fill(BACKGROUND_COLOR)
            window.blit(message_render_1, (50, WINDOW_HEIGHT // 2 - 40 - line_spacing))
            window.blit(message_render_2, (50, WINDOW_HEIGHT // 2 + line_spacing))
            pygame.display.update()
            pygame.time.wait(1000)  # Brief pause before continuing
            return True  # Exit the loop if puzzle is solved correctly

        
        

##########################################################################################

def generate_sudoku(mask_rate=0.5):
    """Generate a 9x9 Sudoku grid and mask it for a game."""
    base = 3
    side = base * base
    def pattern(r,c): return (base * (r % base) + r // base + c) % side
    def shuffle(s): return random.sample(s, len(s))
    rBase = range(base)
    rows  = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols  = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums  = shuffle(range(1, base*base+1))

    # Produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * mask_rate
    for p in range(int(empties)):
        board[random.randrange(side)][random.randrange(side)] = 0

    return board

def print_board(board):
    """Print the board in a 9x9 grid."""
    num_size = 2
    for line in board:
        print(" ".join(f"{num: {num_size}}" for num in line))

def sudoku_csp_solver(board):
    """Solve the Sudoku puzzle using Constraint Satisfaction Problem."""
    problem = Problem()
    
    # Define variables
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                problem.addVariable((i, j), range(1, 10))

    # Define constraints
    for i in range(9):
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for j in range(9)])
        problem.addConstraint(AllDifferentConstraint(), [(j, i) for j in range(9)])

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [(i + x, j + y) for x in range(3) for y in range(3)]
            problem.addConstraint(AllDifferentConstraint(), square)

    # Solve the problem
    solutions = problem.getSolutions()

    if solutions:
        return solutions[0]
    else:
        return None

def sudoku_game(window, font):
    window.fill(BACKGROUND_COLOR)
    board = generate_sudoku(mask_rate=0.05)  # Generate a board with some cells empty
    initial_board = [row[:] for row in board]  # Keep a copy to avoid changing the initial numbers

    block_size = 50  # Size of each Sudoku block
    grid_origin = ((WINDOW_WIDTH - block_size * 9) // 2, (WINDOW_HEIGHT - block_size * 9) // 2)  # Center the grid
    selected_cell = None
    running = True
    font = pygame.font.Font(None, 40)  # Ensure the font is visible

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if grid_origin[0] <= pos[0] <= grid_origin[0] + 9 * block_size and \
                   grid_origin[1] <= pos[1] <= grid_origin[1] + 9 * block_size:
                    selected_cell = ((pos[0] - grid_origin[0]) // block_size, (pos[1] - grid_origin[1]) // block_size)
            elif event.type == KEYDOWN:
                if selected_cell and initial_board[selected_cell[1]][selected_cell[0]] == 0:  # Ensure the cell is editable
                    if event.unicode.isdigit():
                        num = int(event.unicode)
                        if 1 <= num <= 9:
                            board[selected_cell[1]][selected_cell[0]] = num

        # Clear screen and redraw grid and numbers after any event to update the view correctly
        window.fill(BACKGROUND_COLOR)
        draw_sudoku_grid(window, grid_origin, block_size)
        draw_numbers(window, board, grid_origin, block_size, font, initial_board)

        # Check if the puzzle is solved
        if all(all(row[col] != 0 for col in range(9)) for row in board) and is_sudoku_correct(board):
            message = "You've made it out alive... this time. But beware, the next escape room might not be so forgiving"
            message_words = message.split()
            # Split the message into three lines based on word count
            line1 = ' '.join(message_words[:7])  # Adjust the number of words for each line
            line2 = ' '.join(message_words[7:14])
            line3 = ' '.join(message_words[14:])
            # Render each line
            render_line1 = font.render(line1, True, FONT_COLOR)
            render_line2 = font.render(line2, True, FONT_COLOR)
            render_line3 = font.render(line3, True, FONT_COLOR)
            # Determine vertical positions for each line
            line_spacing = 10  # Adjust as needed
            line1_y = WINDOW_HEIGHT // 2 - 40
            line2_y = line1_y + render_line1.get_height() + line_spacing
            line3_y = line2_y + render_line2.get_height() + line_spacing
            # Clear the window and render the lines
            window.fill(BACKGROUND_COLOR)
            window.blit(render_line1, ((WINDOW_WIDTH - render_line1.get_width()) // 2, line1_y))
            window.blit(render_line2, ((WINDOW_WIDTH - render_line2.get_width()) // 2, line2_y))
            window.blit(render_line3, ((WINDOW_WIDTH - render_line3.get_width()) // 2, line3_y))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

        pygame.display.update()
        clock.tick(FPS)

def draw_sudoku_grid(window, grid_origin, block_size):
    for i in range(10):
        line_thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(window, FONT_COLOR, (grid_origin[0] + i * block_size, grid_origin[1]),
                         (grid_origin[0] + i * block_size, grid_origin[1] + 9 * block_size), line_thickness)
        pygame.draw.line(window, FONT_COLOR, (grid_origin[0], grid_origin[1] + i * block_size),
                         (grid_origin[0] + 9 * block_size, grid_origin[1] + i * block_size), line_thickness)

def draw_numbers(window, board, grid_origin, block_size, font, initial_board):
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                color = FONT_COLOR if initial_board[row][col] == 0 else (255, 235, 45)  # Different color for initial numbers
                digit = font.render(str(board[row][col]), True, color)
                digit_rect = digit.get_rect(center=(grid_origin[0] + col * block_size + block_size // 2,
                                                    grid_origin[1] + row * block_size + block_size // 2))
                window.blit(digit, digit_rect)

def is_sudoku_correct(board):
    # Check if the board is correctly filled
    base = 3
    side = base * base
    def check_group(group):
        return set(group) == set(range(1, side + 1))
    for row in board:
        if not check_group(row):
            return False
    for col in range(side):
        if not check_group([board[row][col] for row in range(side)]):
            return False
    for row in range(0, side, base):
        for col in range(0, side, base):
            square = [board[r][c] for r in range(row, row + base) for c in range(col, col + base)]
            if not check_group(square):
                return False
    return True


######################################################################################

def logic_puzzle(window, font):
    window.fill(BACKGROUND_COLOR)
    # CSP problem setup
    problem = Problem()
    problem.addVariables('LOCKPEN', range(1, 10))  # Assuming you want digits from 1 to 9
    problem.addConstraint(AllDifferentConstraint())
    problem.addConstraint(lambda L, O, C, K, P, E, N: (L*1000 + O*100 + C*10 + K) * 2 == (O*1000 + P*100 + E*10 + N), 'LOCKPEN')
    solutions = problem.getSolutions()

    input_values = {char: '' for char in 'LOCKPEN'}
    selected_index = None
    texts = [
        "SOLVE: LOCK + LOCK = OPEN",
        "Click to select a box and type to enter a number.",
        "Press ENTER to submit your answer.",
        "Match the alphabet to the numbers to solve it.",
        "Each letter represents a unique number."
    ]

    y_offset = 30
    for text in texts:
        text_surface = font.render(text, True, FONT_COLOR)
        window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 40

    start_x = (WINDOW_WIDTH - 7 * 50) // 2
    start_y = y_offset + 20
    box_width = 40
    box_height = 40
    spacing = 10

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, letter in enumerate('LOCKPEN'):
                    box_rect = pygame.Rect(start_x + i * (box_width + spacing), start_y, box_width, box_height)
                    if box_rect.collidepoint(mouse_x, mouse_y):
                        selected_index = letter
                        break
            elif event.type == KEYDOWN:
                if selected_index is not None:
                    if event.key == pygame.K_BACKSPACE:
                        input_values[selected_index] = ''
                    elif event.unicode.isdigit():
                        # Replace existing digit or set new one if there's no digit yet
                        input_values[selected_index] = event.unicode
                    if event.key == pygame.K_RETURN:
                        if check_solution(input_values, solutions):
                            print("Correct!")
                            pygame.time.wait(1000)
                            return True
                        else:
                            print("Incorrect solution. Please try again.")

        window.fill(BACKGROUND_COLOR)
        y_offset = 30
        for text in texts:
            text_surface = font.render(text, True, FONT_COLOR)
            window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 40

        for i, letter in enumerate('LOCKPEN'):
            pygame.draw.rect(window, INPUT_BOX_COLOR, (start_x + i * (box_width + spacing), start_y, box_width, box_height))
            letter_text = font.render(input_values[letter], True, TEXT_COLOR)
            window.blit(letter_text, (start_x + i * (box_width + spacing) + (box_width - letter_text.get_width()) // 2, start_y + (box_height - letter_text.get_height()) // 2))
            letter_label = font.render(letter, True, FONT_COLOR)
            window.blit(letter_label, (start_x + i * (box_width + spacing), start_y - 30))

        pygame.display.update()
        clock.tick(FPS)

def check_solution(input_values, solutions):
    try:
        user_solution = {k: int(v) for k, v in input_values.items() if v.isdigit()}
        for sol in solutions:
            if all(sol[k] == user_solution[k] for k in 'LOCKPEN'):
                return True
        return False
    except ValueError:
        return False
