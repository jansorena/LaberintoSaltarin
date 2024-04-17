import argparse
import pygame
from agente import Agente

# Constantes globales
MARGIN = 10
WIDTH = 100
HEIGHT = 100
START_COLOR = (255, 255, 0)
END_COLOR = (255, 0, 0)
VISITED_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 0, 255)
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40

class Laberinto:
    def __init__(self, m, n, start_x, start_y, end_x, end_y, grid):
        self.m = m
        self.n = n
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.grid = grid
        self.agente = Agente()
        self.visited = [[False for _ in range(n)] for _ in range(m)]

    @staticmethod
    def parse_input(filename):
        mazes = []
        with open(filename, "r") as file:
            while True:
                header = file.readline().strip()
                if header == '0':
                    break
                m, n, start_x, start_y, end_x, end_y = map(int, header.split())
                grid = []
                for _ in range(m):
                    row = list(map(int, file.readline().strip().split()))
                    row = ['G' if x == 0 else x for x in row]
                    grid.append(row)
                mazes.append(Laberinto(m, n, start_x, start_y, end_x, end_y, grid))
        return mazes

    @classmethod
    def parse_arguments(cls):
        parser = argparse.ArgumentParser(description="Parse and solve jumping mazes.")
        parser.add_argument("filename", type=str, help="The filename of the maze input.")
        args = parser.parse_args()

        try:
            return cls.parse_input(args.filename)
        except FileNotFoundError:
            print(f"Error: El archivo '{args.filename}' no se encuentra.")
            exit()

    def draw_grid(self, screen):
        for row in range(self.m):
            for column in range(self.n):
                if (row, column) == (self.start_x, self.start_y):
                    color = START_COLOR
                elif (row, column) == (self.end_x, self.end_y) and self.visited[row][column]:
                    color = END_COLOR
                elif self.visited[row][column]:
                    color = (0, 255, 0)  # Green
                else:
                    color = WHITE
                pygame.draw.rect(screen,
                            color,
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT])

    def draw_buttons(self, screen):
        WINDOW_SIZE = [WIDTH * self.n + MARGIN * (self.n - 1), HEIGHT * self.m + MARGIN * (self.m - 1) + 100]
        button_font = pygame.font.Font(None, 50)

        # Draw the buttons with a border
        pygame.draw.rect(screen, BLACK, (50 - 2, WINDOW_SIZE[1] - 75 - 2, 200 + 4, 50 + 4))
        pygame.draw.rect(screen, BLACK, (300 - 2, WINDOW_SIZE[1] - 75 - 2, 200 + 4, 50 + 4))
        self.dfs_button = pygame.draw.rect(screen, BUTTON_COLOR, (50, WINDOW_SIZE[1] - 75, 200, 50))
        self.cu_button = pygame.draw.rect(screen, BUTTON_COLOR, (300, WINDOW_SIZE[1] - 75, 200, 50))

        # Render the button text
        dfs_text = button_font.render('DFS', True, WHITE)
        cu_text = button_font.render('CU', True, WHITE)

        # Draw the button text
        screen.blit(dfs_text, (50 + (200 - dfs_text.get_width()) // 2, WINDOW_SIZE[1] - 75 + (50 - dfs_text.get_height()) // 2))
        screen.blit(cu_text, (300 + (200 - cu_text.get_width()) // 2, WINDOW_SIZE[1] - 75 + (50 - cu_text.get_height()) // 2))

    def draw_numbers(self, screen):
        font = pygame.font.Font(None, 100)
        for row in range(self.m):
            for column in range(self.n):
                # Render the number
                text = font.render(str(self.grid[row][column]), True, BLACK)
                # Calculate the position of the text
                text_rect = text.get_rect(center=((MARGIN + WIDTH) * column + MARGIN + WIDTH // 2,
                                                (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2))
                screen.blit(text, text_rect)

    def draw_arrow(self,prev,screen,x, y):
        if prev is not None:
                prev_x, prev_y = prev
                pygame.draw.line(screen, BLACK, 
                                    ((MARGIN + WIDTH) * prev_y + MARGIN + WIDTH // 2, 
                                    (MARGIN + HEIGHT) * prev_x + MARGIN + HEIGHT // 2), 
                                    ((MARGIN + WIDTH) * y + MARGIN + WIDTH // 2, 
                                    (MARGIN + HEIGHT) * x + MARGIN + HEIGHT // 2), 
                                    5)

    def draw(self):
        # Initialize the font module
        pygame.font.init()

        # Set the HEIGHT and WIDTH of the screen
        WINDOW_SIZE = [WIDTH * self.n + MARGIN * (self.n - 1), HEIGHT * self.m + MARGIN * (self.m - 1) + 100]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Set title of screen
        pygame.display.set_caption("Laberinto Saltarín")

        # Event loop
        self.draw_grid(screen)
        self.draw_numbers(screen)
        self.draw_buttons(screen)
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dfs_button.collidepoint(pygame.mouse.get_pos()):
                        print("DFS")
                        self.agente.solveDFS(self, screen)
                        self.visited = [[False for _ in range(self.n)] for _ in range(self.m)]
                    elif self.cu_button.collidepoint(pygame.mouse.get_pos()):
                        self.agente.solveCostoUniforme(self, screen)
                        self.visited = [[False for _ in range(self.n)] for _ in range(self.m)]