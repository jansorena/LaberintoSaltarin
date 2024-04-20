import heapq
import pygame

class Agente:
    def solveDFS(self,maze,screen):
        stack = [(maze.start_x, maze.start_y, 0, None, [])]
        print('Explorando ...')
        while stack:
            x, y, steps, prev, path = stack.pop()
            
            if maze.visited[x][y]:
                continue
            
            maze.visited[x][y] = True
            
            if x == maze.end_x and y == maze.end_y:
                path.append((x,y))
                maze.draw_grid(screen)
                maze.draw_buttons(screen)
                maze.draw_numbers(screen)
                print(f'{prev} --> {x,y}'.ljust(20), end='\r')
               
                print(''.ljust(20), end='\r')
                print('Camino:')
                
                for i in range(1,len(path)):
                    if path[i-1][0] < path[i][0]:
                        print(f'{path[i-1]} --> {path[i]} Abajo')
                    elif path[i-1][0] > path[i][0]:
                        print(f'{path[i-1]} --> {path[i]} Arriba')
                    elif path[i-1][1] < path[i][1]:
                        print(f'{path[i-1]} --> {path[i]} Derecha')
                    elif path[i-1][1] > path[i][1]:
                        print(f'{path[i-1]} --> {path[i]} Izquierda')

                print(f'Pasos: {steps}')
                return
            
            path = path.copy()
            path.append((x,y))
            print(f'{prev} --> {x,y}'.ljust(20), end='\r')

            maze.draw_grid(screen)
            maze.draw_buttons(screen)
            maze.draw_numbers(screen)
            maze.draw_arrow(prev, screen, x ,y)
            
            pygame.display.update()
            pygame.time.wait(200)
            
            for dx, dy in [(maze.grid[x][y], 0), (-maze.grid[x][y], 0), (0, maze.grid[x][y]), (0, -maze.grid[x][y])]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < maze.m and 0 <= new_y < maze.n and not maze.visited[new_x][new_y]:
                    stack.append((new_x, new_y, steps + 1, (x,y), path))
            
        print(''.ljust(20), end='\r')
        print("No hay solución")

    def solveCostoUniforme(self,maze,screen):
        queue = [(0,0, maze.start_x, maze.start_y, None, [])]
        heapq.heapify(queue)
        print('Explorando ...')
        while queue:
            costo, steps, x, y, prev, path = heapq.heappop(queue)

            if maze.visited[x][y]:
                continue
            
            maze.visited[x][y] = True

            if x == maze.end_x and y == maze.end_y:
                path.append((x,y))
                maze.draw_grid(screen)
                maze.draw_buttons(screen)
                maze.draw_numbers(screen)
                print(''.ljust(20), end='\r')
                print('Camino:')
                
                for i in range(1,len(path)):
                    if path[i-1][0] < path[i][0]:
                        print(f'{path[i-1]} --> {path[i]} Abajo')
                    elif path[i-1][0] > path[i][0]:
                        print(f'{path[i-1]} --> {path[i]} Arriba')
                    elif path[i-1][1] < path[i][1]:
                        print(f'{path[i-1]} --> {path[i]} Derecha')
                    elif path[i-1][1] > path[i][1]:
                        print(f'{path[i-1]} --> {path[i]} Izquierda')

                print(f'Pasos: {steps}')
                return
            
            path = path.copy()
            path.append((x,y))
            print(f'{prev} --> {x,y}'.ljust(20), end='\r')

            maze.draw_grid(screen)
            maze.draw_buttons(screen)
            maze.draw_numbers(screen)
            maze.draw_arrow(prev, screen, x ,y)
            
            pygame.display.update()
            pygame.time.wait(200)

            for dx, dy in [(maze.grid[x][y], 0), (-maze.grid[x][y], 0), (0, maze.grid[x][y]), (0, -maze.grid[x][y])]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < maze.m and 0 <= new_y < maze.n and not maze.visited[new_x][new_y]:
                    heapq.heappush(queue, (costo+maze.grid[x][y],steps + 1, new_x, new_y, (x,y), path))  # Push the new item on the heap
        
        print(''.ljust(20), end='\r')
        print("No hay solución")