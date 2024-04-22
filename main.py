import pygame
import random

class LifeGame:

    def __init__(self):

        # Settings
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.TILE_SIZE = 20
        self.GRID_WIDTH = self.WIDTH // self.TILE_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.TILE_SIZE
        self.FPS = 5

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_grid(self, alive_cells):
        for cell in alive_cells:
            col, row = cell
            top_left = (col * self.TILE_SIZE, row * self.TILE_SIZE)
            pygame.draw.rect(self.screen, 'white', (*top_left, self.TILE_SIZE, self.TILE_SIZE))
        for row in range(self.GRID_HEIGHT):
            pygame.draw.line(self.screen, 'black', (0, row * self.TILE_SIZE), (self.WIDTH, row * self.TILE_SIZE))
        for col in range(self.GRID_WIDTH):
            pygame.draw.line(self.screen, 'black', (col * self.TILE_SIZE, 0), (col * self.TILE_SIZE, self.HEIGHT))

    def get_neighbours(self, cell):
        neighbours = []
        col, row = cell
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if col + x == col and row + y == row:
                    continue
                neighbours.append((col + x, row + y))

        return neighbours

    def update_grid(self, alive_cells):
        new_alive_cells = set()
        all_neighbours = set()

        for cell in alive_cells:
            neighbours = self.get_neighbours(cell)
            all_neighbours.update(neighbours)
            alive_neighbours = [neighbour for neighbour in neighbours if neighbour in alive_cells]

            if len(alive_neighbours) in [2, 3]:
                new_alive_cells.add(cell)

        for cell in all_neighbours:
            neighbours = self.get_neighbours(cell)
            alive_neighbours = [neighbour for neighbour in neighbours if neighbour in alive_cells]

            if len(alive_neighbours) == 3:
                new_alive_cells.add(cell)

        return new_alive_cells
    def generate_random(self):
        cells = set()
        for i in range(1, 100):
            x = random.randint(0, 800)
            y = random.randint(0, 800)
            cells.add((x, y))

        return cells

    def run_game(self):
        run = True
        paused = True
        alive_cells = set()
        while run:

            if not paused:
                self.clock.tick(self.FPS)
                alive_cells = self.update_grid(alive_cells)
            #print(alive_cells)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    position = (x // self.TILE_SIZE, y // self.TILE_SIZE)

                    if position in alive_cells:
                        alive_cells.remove(position)
                    else:
                        alive_cells.add(position)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if paused:
                            paused = False
                        else:
                            paused = True

            self.screen.fill((50, 50, 50))
            self.draw_grid(alive_cells)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = LifeGame()
    game.run_game()