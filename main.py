import pygame

class LifeGame:

    def __init__(self):

        # Settings
        self.WIDTH = 800
        self.HEIGHT = 800
        self.TILE_SIZE = 20
        self.GRID_WIDTH = self.WIDTH // self.TILE_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.TILE_SIZE
        self.FPS = 60

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

    def run_game(self):
        run = True
        alive_cells = set()
        alive_cells.add((10, 10))
        while run:
            self.clock.tick(self.FPS)

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

            self.screen.fill((50, 50, 50))
            self.draw_grid(alive_cells)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = LifeGame()
    game.run_game()