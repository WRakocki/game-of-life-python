import pygame
import random


class LifeGame:
    """General class for managing resources and game behaviour"""
    def __init__(self):
        """Initialization of the game and creation of resources"""

        # Settings
        self.WIDTH = 1600
        self.HEIGHT = 1000
        self.TILE_SIZE = 10
        self.GRID_WIDTH = self.WIDTH // self.TILE_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.TILE_SIZE
        self.FPS = 10

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_grid(self, alive_cells):
        """Drawing the grid with alive cells"""
        for cell in alive_cells:
            col, row = cell
            top_left = (col * self.TILE_SIZE, row * self.TILE_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 255), (*top_left, self.TILE_SIZE, self.TILE_SIZE))
        for row in range(self.GRID_HEIGHT):
            pygame.draw.line(self.screen, (0, 0, 0), (0, row * self.TILE_SIZE), (self.WIDTH, row * self.TILE_SIZE))
        for col in range(self.GRID_WIDTH):
            pygame.draw.line(self.screen, (0, 0, 0), (col * self.TILE_SIZE, 0), (col * self.TILE_SIZE, self.HEIGHT))

    def get_neighbours(self, cell):
        """Getting the neighbours of the specific cell"""

        neighbours = []
        col, row = cell
        for x in [-1, 0, 1]:
            # Grid size restriction
            if col + x < 0 or col + x >= self.GRID_WIDTH:
                continue
            for y in [-1, 0, 1]:
                # Grid size restriction
                if row + y < 0 or row + y >= self.GRID_HEIGHT:
                    continue
                # Avoiding adding the initial cell
                if x == 0 and y == 0:
                    continue

                neighbours.append((col + x, row + y))

        return neighbours

    def update_grid(self, alive_cells):
        """Calculating which cell will stay alive and which cell will become alive"""

        new_alive_cells = set()
        all_neighbours = set()

        for cell in alive_cells:
            neighbours = self.get_neighbours(cell)
            all_neighbours.update(neighbours)
            alive_neighbours = [neighbour for neighbour in neighbours if neighbour in alive_cells]
            # Staying alive
            if len(alive_neighbours) in [2, 3]:
                new_alive_cells.add(cell)

        for cell in all_neighbours:
            neighbours = self.get_neighbours(cell)
            alive_neighbours = [neighbour for neighbour in neighbours if neighbour in alive_cells]
            # Becoming alive
            if len(alive_neighbours) == 3:
                new_alive_cells.add(cell)

        return new_alive_cells

    def generate_random(self):
        """Generating random alive cells"""

        cells = set()
        for i in range(random.randint(1, self.GRID_HEIGHT * self.GRID_WIDTH)):
            x = random.randint(0, self.GRID_WIDTH)
            y = random.randint(0, self.GRID_HEIGHT)
            cells.add((x, y))

        return cells

    def run_game(self):
        """Start of the game and main loop"""

        pygame.display.set_caption("Game Of Life - PAUSED")
        run = True
        paused = True
        alive_cells = set()
        while run:

            if not paused:
                self.clock.tick(self.FPS)
                alive_cells = self.update_grid(alive_cells)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # Mouse input handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    position = (x // self.TILE_SIZE, y // self.TILE_SIZE)
                    if position in alive_cells:
                        alive_cells.remove(position)
                    else:
                        alive_cells.add(position)
                # Key handling
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if paused:
                            pygame.display.set_caption("Game Of Life - PLAYING")
                            paused = False
                        else:
                            pygame.display.set_caption("Game Of Life - PAUSED")
                            paused = True
                    if event.key == pygame.K_q:
                        alive_cells = set()

                    if event.key == pygame.K_r:
                        alive_cells = self.generate_random()

            self.screen.fill((50, 50, 50))
            self.draw_grid(alive_cells)
            pygame.display.update()

        pygame.quit()


def main():
    game = LifeGame()
    game.run_game()


if __name__ == '__main__':
    main()
