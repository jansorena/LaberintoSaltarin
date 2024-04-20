import pygame
from laberinto import Laberinto

def main():
    # Inicializar pygame
    pygame.init()
    
    # Parsear el input
    mazes = Laberinto.parse_arguments()
    
    # Iterar por los distintos laberintos
    for maze in mazes:
        Laberinto.draw(maze)
     
if __name__ == "__main__":
    main()