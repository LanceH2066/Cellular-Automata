import pygame
import numpy as np
import imageio
import collections

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
BG_COLOR = (0, 0, 0)
ON_COLOR = (0, 255, 255)  # Cyan for active cells
DYING_COLOR = (255, 165, 0)  # Orange for dying cells
TEXT_COLOR = (255, 255, 255)  # White
MAX_FRAMES = 100  # Only record first 100 frames

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brian's Brain Cellular Automaton")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)  # Small font for UI text

# Function to create a random grid
def create_grid():
    return np.random.choice([0, 1], (ROWS, COLS), p=[0.8, 0.2])

# Function to update the grid
def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for i in range(ROWS):
        for j in range(COLS):
            neighbors = np.sum(grid[max(0, i-1):min(ROWS, i+2), max(0, j-1):min(COLS, j+2)] == 1) - (grid[i, j] == 1)
            if grid[i, j] == 0 and neighbors == 2:
                new_grid[i, j] = 1  # OFF → ON if exactly two ON neighbors
            elif grid[i, j] == 1:
                new_grid[i, j] = 2  # ON → DYING
            elif grid[i, j] == 2:
                new_grid[i, j] = 0  # DYING → OFF
    return new_grid

# Function to draw the grid and UI text
def draw_grid(grid):
    screen.fill(BG_COLOR)
    
    # Draw cells
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i, j] == 1:
                pygame.draw.rect(screen, ON_COLOR, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[i, j] == 2:
                pygame.draw.rect(screen, DYING_COLOR, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw UI text at the top-left
    text_surface = font.render("Press S to Save | Press R to Restart", True, TEXT_COLOR)
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()

# Function to save GIF
def save_gif():
    if frames:  # Only save if we have frames
        imageio.mimsave("brians_brain.gif", list(frames), duration=0.1)
        print("GIF saved as brians_brain.gif")

# Function to restart simulation
def restart_simulation():
    global grid, frames, frame_count
    grid = create_grid()  # Generate new grid
    frames.clear()  # Clear previous frames
    frame_count = 0  # Reset frame count
    print("Simulation restarted.")

# Main function
def main():
    global grid, frames, frame_count
    grid = create_grid()
    frames = collections.deque()  # Stores frames until we hit MAX_FRAMES
    frame_count = 0  # Track frames recorded

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Press "S" to save the GIF
                    save_gif()
                elif event.key == pygame.K_r:  # Press "R" to restart
                    restart_simulation()

        grid = update_grid(grid)
        draw_grid(grid)

        # Capture frame only if we haven't hit MAX_FRAMES yet
        if frame_count < MAX_FRAMES:
            frame_surface = pygame.surfarray.array3d(pygame.display.get_surface())
            frame_surface = np.flipud(frame_surface)  # Flip the image vertically to correct orientation
            frame_surface = np.rot90(frame_surface, 3)  # Rotate for correct orientation
            frames.append(frame_surface)
            frame_count += 1  # Increment frame count

        clock.tick(10)  # Control simulation speed

    pygame.quit()

if __name__ == '__main__':
    main()
