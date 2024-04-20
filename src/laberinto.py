import argparse
import pygame
from agente import Agente

# Constantes globales
MARGIN = 5
WIDTH = 60
HEIGHT = 60
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
SIZE_FONT = 50
BUTTON_FONT = 25

# Colores
START_COLOR = (255, 255, 0)
END_COLOR = (255, 0, 0)
VISITED_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 0, 255)
GREEN = (0, 255, 0)

class Laberinto:
    # Constructor
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

    # Metodo que parsea el input
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

    # Leer la linea de entrada
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

    # Metodo que dibuja el laberinto
    def draw_grid(self, screen):
        for row in range(self.m):
            for column in range(self.n):
                if (row, column) == (self.start_x, self.start_y):
                    color = START_COLOR
                elif (row, column) == (self.end_x, self.end_y) and self.visited[row][column]:
                    color = END_COLOR
                elif self.visited[row][column]:
                    color = GREEN
                else:
                    color = WHITE
                pygame.draw.rect(screen,
                            color,
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT])

    # Metodo que dibuja los botones
    def draw_buttons(self, screen):
        button_font = pygame.font.Font(None, BUTTON_FONT)

        # Define the button positions
        # Define the button positions
        dfs_button_pos = ((WIDTH * self.n + MARGIN * (self.n - 1) - BUTTON_WIDTH) // 2, self.m * HEIGHT + 50)
        cu_button_pos = ((WIDTH * self.n + MARGIN * (self.n - 1) - BUTTON_WIDTH) // 2, self.m * HEIGHT + 100 + BUTTON_HEIGHT)



        # Draw the buttons
        self.dfs_button = pygame.draw.rect(screen, BUTTON_COLOR, (*dfs_button_pos, BUTTON_WIDTH, BUTTON_HEIGHT))
        self.cu_button = pygame.draw.rect(screen, BUTTON_COLOR, (*cu_button_pos, BUTTON_WIDTH, BUTTON_HEIGHT))

        # Render the button text
        dfs_text = button_font.render('DFS', True, WHITE)
        cu_text = button_font.render('CU', True, WHITE)

        # Draw the button text
        screen.blit(dfs_text, (dfs_button_pos[0] + (BUTTON_WIDTH - dfs_text.get_width()) // 2, dfs_button_pos[1] + (BUTTON_HEIGHT - dfs_text.get_height()) // 2))
        screen.blit(cu_text, (cu_button_pos[0] + (BUTTON_WIDTH - cu_text.get_width()) // 2, cu_button_pos[1] + (BUTTON_HEIGHT - cu_text.get_height()) // 2))
    
    def draw_numbers(self, screen):
        font = pygame.font.Font(None, SIZE_FONT)
        
        for row in range(self.m):
            for column in range(self.n):
                text = font.render(str(self.grid[row][column]), True, BLACK)
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
        WINDOW_SIZE = [WIDTH * self.n + MARGIN * (self.n - 1), HEIGHT * self.m + MARGIN * (self.m - 1) + 200]
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
                        print("Costo Uniforme")
                        self.agente.solveCostoUniforme(self, screen)
                        self.visited = [[False for _ in range(self.n)] for _ in range(self.m)]