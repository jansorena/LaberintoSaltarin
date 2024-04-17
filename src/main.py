import pygame
from laberinto import Laberinto
from agente import Agente

def main():
    pygame.init()
    
    mazes = Laberinto.parse_arguments()

    for maze in mazes:
        Laberinto.draw(maze)
     
if __name__ == "__main__":
    main()