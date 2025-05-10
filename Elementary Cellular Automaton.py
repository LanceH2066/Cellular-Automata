import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 4
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
BG_COLOR = (255, 255, 255)
ALIVE_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 0, 0)  # Red for visibility
SAVE_TEXT_COLOR = (0, 255, 0)  # Green for "Saved!" text

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elementary Cellular Automaton")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Font for rule display
small_font = pygame.font.Font(None, 28)  # Font for save message

# Function to convert rule number (0-255) into a lookup dictionary
def rule_to_dict(rule_number):
    rule_bin = f"{rule_number:08b}"  # Convert to 8-bit binary string
    keys = [(1, 1, 1), (1, 1, 0), (1, 0, 1), (1, 0, 0), 
            (0, 1, 1), (0, 1, 0), (0, 0, 1), (0, 0, 0)]
    return {keys[i]: int(rule_bin[i]) for i in range(8)}

# Function to apply a rule to generate the next row
def update_row(current_row, rule_dict):
    new_row = np.zeros_like(current_row)
    for i in range(len(current_row)):
        neighborhood = (current_row[(i-1)], current_row[i], current_row[(i+1)%(len(current_row))])
        new_row[i] = rule_dict.get(neighborhood, 0)
    return new_row

# Function to run the automaton simulation and draw the grid
def run_simulation(rule_number):
    screen.fill(BG_COLOR)
    rule_dict = rule_to_dict(rule_number)
    grid = np.zeros((ROWS, (ROWS*2)), dtype=int)        # Using ROWS*2 to ensure correct result for edge cells

    # Initialize first row with a single active cell in the center
    grid[0, (ROWS*2) // 2] = 1

    # Simulate the evolution
    for r in range(1, ROWS):
        grid[r] = update_row(grid[r-1], rule_dict)

    offset = ((ROWS*2) - COLS) // 2

    # Draw the grid
    for y in range(ROWS):
        for x in range((COLS)):
            if grid[y, x + offset] == 1:
                pygame.draw.rect(screen, ALIVE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Display the current rule number
    text_surface = font.render(f"Rule {rule_number}", True, TEXT_COLOR)
    screen.blit(text_surface, (10, 10))

    return grid  # Return the grid for saving

# Function to save the simulation as a PNG
def save_simulation(rule_number):
    filename = f"rule_{rule_number}.png"
    pygame.image.save(screen, filename)
    print(f"Saved: {filename}")
    return filename  # Return the filename for displaying confirmation

# Main function
def main():
    rule_number = 110  # Setup initial rule number
    running = True
    saved_text_timer = 0
    saved_text = None  # Store filename when saved

    while running:
        screen.fill(BG_COLOR)  # Clear the screen
        grid = run_simulation(rule_number)  # Run simulation and draw grid
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rule_number = (rule_number + 1) % 256
                elif event.key == pygame.K_DOWN:
                    rule_number = (rule_number - 1) % 256
                elif event.key == pygame.K_s:  
                    saved_text = save_simulation(rule_number)
                    saved_text_timer = 5

        # Display "Saved!" message if recently saved
        if saved_text and saved_text_timer > 0:
            saved_message = small_font.render(f"Saved: {saved_text}", True, SAVE_TEXT_COLOR)
            screen.blit(saved_message, (10, 50))
            saved_text_timer -= 1

        pygame.display.flip()  # Update the display

        clock.tick(2)

    pygame.quit()

if __name__ == '__main__':
    main()
