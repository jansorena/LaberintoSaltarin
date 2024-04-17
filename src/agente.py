import heapq
import pygame

class Agente:
    def solveDFS(self,maze,screen):
        stack = [(maze.start_x, maze.start_y, 0, None, [])]
        print('Explorando ...')
        while stack:
            x, y, steps, prev, path = stack.pop()
            maze.visited[x][y] = True
            
            if x == maze.end_x and y == maze.end_y:
                path.append((x,y))
                maze.draw_grid(screen)
                maze.draw_buttons(screen)
                maze.draw_numbers(screen)
                print(f'{prev} --> {x,y}')
                print(f'Pasos: {steps}')
                print(f'Camino {path}')
                return
            
            path = path.copy()
            path.append((x,y))
            maze.draw_grid(screen)
            maze.draw_buttons(screen)
            maze.draw_numbers(screen)
            maze.draw_arrow(prev, screen, x ,y)
            pygame.display.update()
            print(f'{prev} --> {x,y}')
            pygame.time.wait(200)
            
            for dx, dy in [(maze.grid[x][y], 0), (-maze.grid[x][y], 0), (0, maze.grid[x][y]), (0, -maze.grid[x][y])]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < maze.m and 0 <= new_y < maze.n and not maze.visited[new_x][new_y]:
                    stack.append((new_x, new_y, steps + 1, (x,y), path))
            
        
        print("No hay solución")

    def solveCostoUniforme(self,maze,screen):
        queue = [(0,0, maze.start_x, maze.start_y, None, [])]
        heapq.heapify(queue)
        print('Explorando ...')
        while queue:
            costo, steps, x, y, prev, path = heapq.heappop(queue)  # Pop the smallest item off the heap
            maze.visited[x][y] = True
            if x == maze.end_x and y == maze.end_y:
                path.append((x,y))
                maze.draw_grid(screen)
                maze.draw_buttons(screen)
                maze.draw_numbers(screen)
                print(f'{prev} --> {x,y}')
                print(f'Pasos: {steps}')
                print(f'Camino {path}')
                return
            
            path = path.copy()
            path.append((x,y))
            maze.draw_grid(screen)
            maze.draw_buttons(screen)
            maze.draw_numbers(screen)
            maze.draw_arrow(prev, screen, x ,y)
            pygame.display.update()
            print(f'{prev} --> {x,y}')
            pygame.time.wait(200)

            for dx, dy in [(maze.grid[x][y], 0), (-maze.grid[x][y], 0), (0, maze.grid[x][y]), (0, -maze.grid[x][y])]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < maze.m and 0 <= new_y < maze.n and not maze.visited[new_x][new_y]:
                    heapq.heappush(queue, (costo+maze.grid[x][y],steps + 1, new_x, new_y, (x,y), path))  # Push the new item on the heap
        print("No hay solución")