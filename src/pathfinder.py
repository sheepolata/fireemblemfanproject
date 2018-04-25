import TileLogic
import math
import sys
import random
import settings as sett

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __hash__(self):
        return hash("foobar" * ((self.x/(self.y+1))))

#_start and _goal here are Coordinates
def heuristic_cost_estimate(_cell, _goal):
    res = 10 * (abs(_cell.x - _goal.x) + abs(_cell.y - _goal.y))
    return res

def distance_between(_cell, _other):
    res = abs(math.sqrt((float(_other.x) - float(_cell.x))**2 + (float(_other.y) - float(_cell.y))**2))
    return res + sett.logic_tiles[_other.x][_other.y].cost

def get_neighbours(_cell):
    """
    Returns adjacent cells to a cell. Clockwise starting
    from the one on the right.
    """
    cells = []
    if _cell.x < sett.nb_tiles_w - 1:
        cells.append(Coordinate(_cell.x+1, _cell.y))
    if _cell.y > 0:
        cells.append(Coordinate(_cell.x, _cell.y-1))
    if _cell.x > 0:
        cells.append(Coordinate(_cell.x-1, _cell.y))
    if _cell.y < sett.nb_tiles_h - 1:
        cells.append(Coordinate(_cell.x, _cell.y+1))
    return cells

def astar(_start, _goal):
    start = Coordinate(_start[0], _start[1])
    goal = Coordinate(_goal[0], _goal[1])

    #Path is a succession of coordinates
    path = []

    #Set of nodes already evaluated
    closed_set = []

    #The set of currently discovered nodes that are not evaluated yet.
    #Initially, only the start node is known.
    open_set = [start]

    #For each node, which node it can most efficiently be reached from.
    #If a node can be reached from many nodes, cameFrom will eventually contain the
    #most efficient previous step.
    came_from = {}

    #For each node, the cost of getting from the start node to that node.
    g_score = {}
    for i in range(len(sett.logic_tiles)):
        for j in range(len(sett.logic_tiles[i])):
            c = Coordinate(i, j)
            g_score[c] = float("inf")
    g_score[start] = 0.0

    #For each node, the total cost of getting from the start node to the goal
    #by passing by that node. That value is partly known, partly heuristic.
    f_score = {}
    for i in range(len(sett.logic_tiles)):
        for j in range(len(sett.logic_tiles[i])):
            c = Coordinate(i, j)
            f_score[c] = float("inf")
    f_score[start] = heuristic_cost_estimate(start, goal)

    sett.it_max_astar = 0
    while open_set:
        sett.it_max_astar += 1

        #current = Node in open_set with the lowest f_score
        mini = float("inf")
        list_curr = []
        current = None
        for elt in open_set:
            if mini >= f_score[elt]:
                mini = f_score[elt]
                current = elt
        
        if current == None:
            print("Error : current == None")
            sys.exit(0)

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.append(current)
        sett.logic_tiles[current.x][current.y].is_visited = True
        sett.logic_tiles[current.x][current.y].iteration_visit = sett.it_max_astar

        #For each neighbours of current
        for _neighbour in get_neighbours(current):
            if _neighbour in closed_set:
                continue

            if _neighbour not in open_set:
                open_set.append(_neighbour)

            #The distance from start to a neighbor
            #the "dist_between" function may vary as per the solution requirements.
            tentative_gScore = g_score[current] + distance_between(current, _neighbour)
            if tentative_gScore >= g_score[_neighbour]:
                continue

            came_from[_neighbour] = current
            g_score[_neighbour] = tentative_gScore
            f_score[_neighbour] = g_score[_neighbour] + heuristic_cost_estimate(_neighbour, goal)

    return -1

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path
