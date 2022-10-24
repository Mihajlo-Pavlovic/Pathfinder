import pygame
import os
import config
import heapq
import sys

class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path

class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)


    def get_agent_path(self, game_map, goal):
        def getPrice(x):
            c = game_map[x[0]][x[1]]

            if type(c) is Road: return 2
            if type(c) is Grass: return 3
            if type(c) is Mud: return 5
            if type(c) is Dune: return 7
            if type(c) is Water: return 500
            if type(c) is Stone: return 1000

            return -1

        def getTaxiDistance(x):
            return (abs(x[0] - goal[0]) + abs(x[1] - goal[1])) * 2

        start = [[self.row, self.col]]
        heap = []
        heapq.heappush(heap, (0, start))

        while heap:
            while heap:
                path = heapq.heappop(heap)
                cur = path[1][-1]
                print(cur)
                if cur[0] is goal[0] and cur[1] is goal[1]:
                    path_ret = []
                    for p in path[1]:
                        path_ret.append(game_map[p[0]][p[1]])
                    return path_ret
                neighbour = []
                # pokupi susedne i sortiraj
                if cur[0] != 0:
                    neighbour.append([cur[0] - 1, cur[1]])
                if cur[1] != len(game_map[0]) - 1:
                    neighbour.append([cur[0], cur[1] + 1])
                if cur[0] != len(game_map) - 1:
                    neighbour.append([cur[0] + 1, cur[1]])
                if cur[1] != 0:
                    neighbour.append([cur[0], cur[1] - 1])
                for neigh in neighbour:
                    if neigh not in path[1]:
                        new_path = list(path[1])
                        new_path.append(neigh)
                        heapq.heappush(heap, (path[0] + getPrice(neigh) + getTaxiDistance(neigh) - getTaxiDistance(cur), new_path))

class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)


    def get_agent_path(self, game_map, goal):
        def getPrice(x):
            c = game_map[x[0]][x[1]]

            if type(c) is Road: return 2
            if type(c) is Grass: return 3
            if type(c) is Mud: return 5
            if type(c) is Dune: return 7
            if type(c) is Water: return 500
            if type(c) is Stone: return 1000

            return -1

        # class Partial_path:
        #     def __init__(self, start, cost):
        #         self.path = [start]
        #         self.cost = cost
        #
        #     def add_vertex(self, v):
        #         self.path.append(v)
        #         self.cost += getPrice(v)

        start = [[self.row, self.col]]
        heap = []
        heapq.heappush(heap, (0, start))

        while heap:
            #treba da uzme onu sa najmanjim brojem cvorova na putanji
            pot_path = []
            pot_path.append(heapq.heappop(heap))
            while(len(heap) != 0 and heap[0][0] is pot_path[0][0]):
                pot_path.append(heapq.heappop(heap))
            min = sys.maxsize
            path = (0, [0, 0])
            for p in pot_path:
                if len(p[1]) < min:
                    path = p
            for p in pot_path:
                if p is not path:
                    heapq.heappush(heap, p)
            cur = path[1][-1]
            print(cur)
            if cur[0] is goal[0] and cur[1] is goal[1]:
                path_ret = []
                for p in path[1]:
                    path_ret.append(game_map[p[0]][p[1]])
                return path_ret
            neighbour = []
            # pokupi susedne i sortiraj
            if cur[0] != 0:
                neighbour.append([cur[0]-1, cur[1]])
            if cur[1] != len(game_map[0]) - 1:
                neighbour.append([cur[0], cur[1]+1])
            if cur[0] != len(game_map) - 1:
                neighbour.append([cur[0]+1, cur[1]])
            if cur[1] != 0:
                neighbour.append([cur[0], cur[1]-1])
            for neigh in neighbour:
                if neigh not in path[1]:
                    new_path = list(path[1])
                    new_path.append(neigh)
                    heapq.heappush(heap, (path[0]+getPrice(neigh), new_path))

class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):

        def getPrice(x):
            c = game_map[x[0]][x[1]]

            if type(c) is Road: return 2
            if type(c) is Grass: return 3
            if type(c) is Mud: return 5
            if type(c) is Dune: return 7
            if type(c) is Water: return 500
            if type(c) is Stone: return 1000

            return -1

        def getAvgPrice(y, cur):
            ret = 0
            x = 0
            #Ako postoji severni i nije prosli
            if y[0] != 0 and y != cur:
                ret += getPrice([y[0]-1, y[1]])
                x+=1
            #Ako postoji istocni i nije prosli
            if y[1] != len(game_map[0]) - 1 and y != cur:
                ret += getPrice([y[0], y[1]+1])
                x+=1
            #Ako postoji juzni i nije prosli
            if y[0] != len(game_map) - 1 and y != cur:
                ret += getPrice([y[0]+1, y[1]])
                x+=1
            #Ako postoji zapadni i nije prosli
            if y[1] != 0 and y != cur:
                ret += getPrice([y[0], y[1]-1])
                x+=1
            if(x != 0):
                return ret/x
            else:
                return sys.maxsize
        start = []
        start.append(self.row)
        start.append(self.col)

        queue = [[start]]
        visited = []

        while queue:
            path = queue.pop(0)
            cur = path[-1]
            if cur[0] is goal[0] and cur[1] is goal[1]:
                path_ret = []
                for p in path:
                    path_ret.append(game_map[p[0]][p[1]])
                return path_ret
            if cur not in visited:
                neighbour = []
                #pokupi susedne i sortiraj
                if cur[0] != 0:
                    temp = []
                    temp.append(cur[0] - 1)
                    temp.append(cur[1])
                    neighbour.append(temp)
                if cur[1] != len(game_map[0]) - 1:
                    temp = []
                    temp.append(cur[0])
                    temp.append(cur[1] + 1)
                    for x in range(len(neighbour) + 1):
                        if x is len(neighbour):
                            neighbour.append(temp)
                            break
                        elif getAvgPrice(neighbour[x], cur) > getAvgPrice(temp,cur):
                            neighbour.insert(x, temp)
                            break
                        else:
                            pass
                if cur[0] != len(game_map) - 1:
                    temp = []
                    temp.append(cur[0] + 1)
                    temp.append(cur[1])
                    for x in range(len(neighbour) + 1):
                        if x is len(neighbour):
                            neighbour.append(temp)
                            break
                        elif getAvgPrice(neighbour[x], cur) > getAvgPrice(temp,cur):
                            neighbour.insert(x, temp)
                            break
                        else:
                            pass
                if cur[1] != 0:
                    temp = []
                    temp.append(cur[0])
                    temp.append(cur[1] - 1)
                    for x in range(len(neighbour) + 1):
                        if x is len(neighbour):
                            neighbour.append(temp)
                            break
                        elif getAvgPrice(neighbour[x], cur) > getAvgPrice(temp, cur):
                            neighbour.insert(x, temp)
                            break
                        else:
                            pass
                for neigh in neighbour:
                    new_path = list(path)
                    new_path.append(neigh)
                    queue.append(new_path)
                visited.append(cur)





class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        def DFS(self, v, path, game_map):

            def getPrice(x):
                c = game_map[x[0]][x[1]]

                if type(c) is Road: return 2
                if type(c) is Grass: return 3
                if type(c) is Mud: return 5
                if type(c) is Dune: return 7
                if type(c) is Water: return 500
                if type(c) is Stone: return 1000

                return -1

            neighbour = []
            path.append(v)
            if v[0] == goal[0] and v[1] == goal[1]:
                return path
            # napravi listu suseda, po ceni pa smeru
            if v[0] != 0:
                temp = []
                temp.append(v[0] - 1)
                temp.append(v[1])
                neighbour.append(temp)
            if v[1] != len(game_map[0]) - 1:
                temp = []
                temp.append(v[0])
                temp.append(v[1] + 1)
                for x in range(len(neighbour) + 1):
                    if x is len(neighbour):
                        neighbour.append(temp)
                        break
                    elif getPrice(neighbour[x]) > getPrice(temp):
                        neighbour.insert(x, temp)
                        break
                    else:
                        pass
            if v[0] != len(game_map) - 1:
                temp = []
                temp.append(v[0] + 1)
                temp.append(v[1])
                for x in range(len(neighbour) + 1):
                    if x is len(neighbour):
                        neighbour.append(temp)
                        break
                    elif getPrice(neighbour[x]) > getPrice(temp):
                        neighbour.insert(x, temp)
                        break
                    else:
                        pass
            if v[1] != 0:
                temp = []
                temp.append(v[0])
                temp.append(v[1] - 1)
                for x in range(len(neighbour) + 1):
                    if x is len(neighbour):
                        neighbour.append(temp)
                        break
                    elif getPrice(neighbour[x]) > getPrice(temp):
                        neighbour.insert(x, temp)
                        break
                    else:
                        pass
            for n in neighbour:
                if n not in path:
                    DFS(self, n, path, game_map)
                    end = []
                    end.append(goal[0])
                    end.append(goal[1])
                    if path[len(path) - 1][0] is end[0] and path[len(path) - 1][1] is end[1]:
                        return path

        start = []
        path = []
        start.append(self.row)
        start.append(self.col)
        path = DFS(self, start, path, game_map)
        path_ret = []
        for p in path:
            path_ret.append(game_map[p[0]][p[1]])
        return path_ret


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
