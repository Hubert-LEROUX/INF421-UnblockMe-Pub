import os
import queue
import heapq
import time
from hash_table import My_hash_table, My_set
from visualisation import show_grid

examples_dir = os.path.join("..", "examples")

def get_input():
    """
    Get the input from console 
    :return: the input
    @param n: the size of the grid
    @param nb_cars: the number of cars
    @param cars: the list of cars (dict list)
    """
    n = int(input())
    nb_cars = int(input())
    cars = []
    for _ in range(nb_cars):
        line = input().split()
        cars.append({"id_car" : int(line[0]), "orientation" : line[1], "length":int(line[2]), "x_topleft" : int(line[3])-1, "y_topleft" : int(line[4])-1})

    return n, cars # pas besoin de renvoyer nb_cars, on peut le calculer avec len(cars)

def get_input_from_file(file):
    """
    Get the input from file
    :return: the input
    @param n: the size of the grid
    @param nb_cars: the number of cars
    @param cars: the list of cars (dict list)
    """
    with open(file, 'r') as f:
        n = int(f.readline().strip())
        nb_cars = int(f.readline().strip())
        cars = []
        for _ in range(nb_cars):
            line = f.readline().strip().split()
            cars.append({
                "id_car": int(line[0]),
                "orientation": line[1],
                "length": int(line[2]),
                "x_topleft": int(line[3]) - 1,
                "y_topleft": int(line[4]) - 1
            })
    return n, cars

def is_point_in_grid(point, n):
    """
    Check if a point is in the grid
    :param point: tuple (x, y) representing the point
    :param n: size of the grid
    :return: True if the point is in the grid, False otherwise
    """
    return point[0] >= 0 and point[0] < n and point[1] >= 0 and point[1] < n

def cars_into_grid(n, cars):
    """
    Set the game
    1) Check that the configuration is correct
    2) Convert the grid encoding from a list of cars into a matrix form
    :param n: the size of the grid
    :param cars: the list of cars (dict list)
    :return: a tuple (bool, grid) where bool indicates if the configuration is correct and grid is the matrix form of the grid
    """
    def add_car(n, grid, car):
        """
        Add a car to the grid
        :param n: the size of the grid
        :param grid: the grid
        :param car: the car to add
        :return: True if the car can be added, False otherwise
        """
        if not is_point_in_grid((car["x_topleft"], car["y_topleft"]), n):
            return False  # the first point is not even in the grid, no need to go further
        
        # Differentiate based on the orientation of the car
        if car["orientation"] == "h":  # horizontal
            if not is_point_in_grid((car["x_topleft"] + car["length"] - 1, car["y_topleft"]), n):
                return False  # the car will not fit
            for i in range(car["length"]):
                if grid[car["y_topleft"]][car["x_topleft"] + i] != 0:  # there is already a car
                    return False
                grid[car["y_topleft"]][car["x_topleft"] + i] = car["id_car"]
        else:  # the car is vertical
            if not is_point_in_grid((car["x_topleft"], car["y_topleft"] + car["length"] - 1), n):
                return False
            for i in range(car["length"]):
                if grid[car["y_topleft"] + i][car["x_topleft"]] != 0:  # there is already a car
                    return False
                grid[car["y_topleft"] + i][car["x_topleft"]] = car["id_car"]
        return True  # the car was set correctly

    grid = [[0 for _ in range(n)] for _ in range(n)]
    for car in cars:
        if not add_car(n, grid, car):
            return False, None
    return True, grid
    
def set_game_from_file(file):
    """
    Set the game from a file
    :param file: the file containing the game configuration
    :return: the game state as a dictionary with keys "size", "cars", and "grid"
    """
    n, cars = get_input_from_file(file)
    b, grid = cars_into_grid(n, cars)
    if b:
        return {"size": n, "cars": cars, "grid": grid}
    else:
        print("The configuration is not correct")

def show_grid(grid):
    """
    Display the grid in a readable format.
    
    :param grid: List of lists representing the grid.
    """
    max_id_car = max(max(line) for line in grid)
    nb_digits = len(str(max_id_car))
    for line in grid:
        print('|' + '|'.join('%0*d' % (nb_digits, cell) if cell != 0 else '_'*nb_digits for cell in line) + '|')


def copy_game_state(game_state):
    """
    Create a deep copy of the game state.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: dict, a deep copy of the game state
    """
    n = game_state["size"]
    cars = game_state["cars"]
    grid = game_state["grid"]

    return {"size": n, "cars": [car.copy() for car in cars], "grid": [row[:] for row in grid]}


def get_next_moves(game_state):
    """
    Get all possible next moves from the current game state.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: list of dicts, each representing a new game state after a possible move
    """
    def get_next_moves_car(game_state, id_car):
        """
        Get all possible next moves for a specific car.
        
        :param game_state: dict, the current game state
        :param id_car: int, the ID of the car to move
        :return: list of dicts, each representing a new game state after a possible move of the car
        """
        def get_next_moves_car_in_one_direction(game_state, id_car, direction):
            """
            Get all possible next moves for a specific car in one direction.
            
            :param game_state: dict, the current game state
            :param id_car: int, the ID of the car to move
            :param direction: tuple, the direction to move the car (delta_x, delta_y)
            :return: list of dicts, each representing a new game state after a possible move of the car in the given direction
            """
            next_moves_car_one_direction = []
            new_game_state = copy_game_state(game_state)
            delta_x, delta_y = direction
            possible = True

            while possible:
                cars = new_game_state["cars"]
                car = cars[id_car]
                grid = new_game_state["grid"]
                n = new_game_state["size"]

                if delta_x + delta_y > 0: # mouvement vers la droite ou vers le bas
                    point_left = (car["x_topleft"], car["y_topleft"]) # case qui disparaît
                    point_to_check = (car["x_topleft"] + car["length"] * delta_x, car["y_topleft"] + car["length"] * delta_y) # case
                else: # mouvement vers la gauche ou vers le haut
                    point_left = (car["x_topleft"] - (car["length"] - 1) * delta_x, car["y_topleft"] - (car["length"] - 1) * delta_y)
                    point_to_check = (car["x_topleft"] + delta_x, car["y_topleft"] + delta_y)

                possible = is_point_in_grid(point_left, n) and is_point_in_grid(point_to_check, n) and grid[point_to_check[1]][point_to_check[0]] == 0

                if possible:
                    car["x_topleft"] += delta_x
                    car["y_topleft"] += delta_y
                    grid[point_left[1]][point_left[0]] = 0
                    grid[point_to_check[1]][point_to_check[0]] = car["id_car"]

                    next_moves_car_one_direction.append(new_game_state)
                    new_game_state = copy_game_state(new_game_state)

            return next_moves_car_one_direction

        next_moves_car = []
        car = game_state["cars"][id_car]
        if car["orientation"] == "h":
            next_moves_car.extend(get_next_moves_car_in_one_direction(game_state, id_car, (1, 0)))
            next_moves_car.extend(get_next_moves_car_in_one_direction(game_state, id_car, (-1, 0)))
        else:
            next_moves_car.extend(get_next_moves_car_in_one_direction(game_state, id_car, (0, 1)))
            next_moves_car.extend(get_next_moves_car_in_one_direction(game_state, id_car, (0, -1)))

        return next_moves_car

    next_moves = []
    for id_car in range(len(game_state["cars"])):
        next_moves.extend(get_next_moves_car(game_state, id_car))
    return next_moves


def distance_top_left(car):
    """
    Get the distance from the top left corner
    :param car: the car
    :return: the distance
    """
    if car["orientation"] == "h":
        return car["x_topleft"]
    else:
        return car["y_topleft"]
    

def is_winning(game_state):
    """
    Check if the current game state is a winning state.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: bool, True if the red car (car with id 1) has reached the right edge of the grid, False otherwise
    """
    cars = game_state["cars"]
    n = game_state["size"]
    
    return cars[0]["x_topleft"] == n - cars[0]["length"]

def brute_foce_BFS(game_state):
    """
    Perform a brute force Breadth-First Search (BFS) to solve the game.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: tuple, (int, int), the minimum number of moves to solve the game and the number of explored nodes, or (-1, int) if no solution is found
    """
    nb_cars = len(game_state["cars"])

    q = queue.Queue()
    q.put((0, game_state))

    seen = My_set(nb_cars)

    while q:
        depth, game_state = q.get()

        if seen.contains(game_state):  # if already processed, ...
            continue  # ... skip to the next

        seen.add(game_state)

        if is_winning(game_state):
            return depth, len(seen)
        
        for new_game_state in get_next_moves(game_state):
            if not seen.contains(new_game_state):
                q.put((depth+1, new_game_state))

    return -1, len(seen)

def brute_foce_BFS_from_file(file):
    """
    Perform a brute force Breadth-First Search (BFS) to solve the game from a file.
    
    :param file: str, the path to the file containing the game configuration
    :return: int, the minimum number of moves to solve the game or -1 if no solution is found
    """
    game_state = set_game_from_file(file)
    return brute_foce_BFS(game_state)

def deballe_solution(antecedent, game_state):
    """
    Unpack the solution path from the antecedent hash table.

    :param antecedent: My_hash_table, the hash table storing the antecedents of each game state
    :param game_state: dict, the final game state from which to start unpacking the solution
    :return: list of dicts, the solution path from the initial state to the final state
    """
    solution = []
    while game_state is not None:
        solution.append(game_state)
        game_state = antecedent.get(game_state)
    return solution[::-1]


def brute_foce_BFS_with_solution(game_state):
    """
    Perform a brute force Breadth-First Search (BFS) to solve the game and return the solution path.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: tuple, (number of explored nodes, minimum number of moves to solve the game, solution path)
    """
    nb_cars = len(game_state["cars"])

    q = queue.Queue()
    q.put((0, game_state))

    antecedent = My_hash_table(nb_cars)
    antecedent.add(game_state, None)  # The initial state has no antecedent

    while q:
        depth, game_state = q.get()

        if is_winning(game_state):
            return len(antecedent) - q.qsize(), depth, deballe_solution(antecedent, game_state)
        
        for new_game_state in get_next_moves(game_state):
            if not antecedent.contains(new_game_state):
                antecedent.add(new_game_state, game_state)
                q.put((depth + 1, new_game_state))

    return -1, None, None


class My_Cars(tuple):
    """
    A class to represent a game configuration as a tuple.

    The tuple contains:
    - distance_heuristique: The heuristic distance.
    - profondeur: The depth of the game state.
    - game_state: The current game state.
    - antecedent: The antecedent of the game state.

    The class overrides the less than operator to compare based on the sum of distance_heuristique and profondeur.
    """
    def __lt__(self, other):
        return self[0] + self[1] < other[0] + other[1]

def heuristic_BFS(game_state, heuristic = lambda x : 0):
    """
    Perform a heuristic Breadth-First Search (BFS) to solve the game.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :param heuristic: function, a heuristic function that takes a game state and returns a heuristic value
    :return: tuple, (number of explored nodes, minimum number of moves to solve the game, solution path)
    """
    nb_cars = len(game_state["cars"])

    q = [My_Cars((heuristic(game_state), 0, game_state, None))]
    heapq.heapify(q)

    seen = My_set(nb_cars)
    antecedent = My_hash_table(nb_cars)
    antecedent.add(game_state, None)  # The initial state has no antecedent

    while q:
        h, dist, game_state, antecedent_game_state = heapq.heappop(q)
        if not seen.contains(game_state):
            antecedent.add(game_state, antecedent_game_state)
            seen.add(game_state)  # Mark the state as seen

            if is_winning(game_state):
                solution = deballe_solution(antecedent, game_state)
                return len(seen), dist, solution
            
            for new_game_state in get_next_moves(game_state):
                heapq.heappush(q, My_Cars((heuristic(new_game_state), dist + 1, new_game_state, game_state)))

    return (len(seen), float("+inf"), None)


def number_cars_blocking(game_state):
    """
    Get the number of cars blocking the path of the main car.
    
    Note: All blocking cars are vertical; otherwise, the game is unsolvable.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: int, the number of cars blocking the path of the main car
    """
    cars = game_state["cars"]

    return sum(1 for car in cars[1:] if car["y_topleft"] <= cars[0]["y_topleft"] 
               and cars[0]["y_topleft"] < car["y_topleft"] + car["length"] 
               and cars[0]["x_topleft"] <= car["x_topleft"] and car["orientation"] == "v")


def distance_to_goal(game_state):
    """
    Calculate the normalized distance of the red car (car with id 1) to the goal.
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: float, the normalized distance to the goal
    """
    cars = game_state["cars"]
    n = game_state["size"]
    return (n - cars[0]["length"] - cars[0]["x_topleft"]) / n


def number_cars_indirectly_blocking(game_state):
    """
    Get the number of cars indirectly blocking the path of the main car.
    i.e 1 for the red car + 1 for each directly blocking car + the minimum number of cars to move to unblock directly blocking cars
    
    :param game_state: dict, the current game state containing the size of the grid, list of cars, and the grid itself
    :return: int, the number of cars indirectly blocking the path of the main car
    """
    if is_winning(game_state):
        return 0
    
    cars = game_state["cars"]
    n = game_state["size"]
    grid = game_state["grid"]

    directly_blocking = []
    blocking = [False] * len(cars)
    blocking[0] = True
    for car in cars[1:]:
        if car["y_topleft"] <= cars[0]["y_topleft"] and cars[0]["y_topleft"] < car["y_topleft"] + car["length"] and cars[0]["x_topleft"] <= car["x_topleft"] and car["orientation"] == "v":
            directly_blocking.append(car)
            blocking[car["id_car"] - 1] = True

    def num_blocking(blocking):
        return sum(1 for b in blocking if b)

    def update_blocking(cases, blocking):
        blocking = [b for b in blocking]
        for i, j in cases:
            if grid[j][i] != 0:
                blocking[grid[j][i] - 1] = True
        return blocking

    def min_blocking_cases(blocking, directly_blocking):
        if not directly_blocking:
            return num_blocking(blocking)
        else:
            new_directly_blocking = directly_blocking[1:]
            car = directly_blocking[0]

            if cars[0]["y_topleft"] - car["length"] >= 0:
                cases_top = [(car["x_topleft"], cars[0]["y_topleft"] - 1 - i) for i in range(car["length"])]
                blocking_top = update_blocking(cases_top, blocking)
            else:
                blocking_top = [True] * len(cars)
            
            if cars[0]["y_topleft"] + car["length"] < n:
                cases_bottom = [(car["x_topleft"], cars[0]["y_topleft"] + 1 + i) for i in range(car["length"])]
                blocking_bottom = update_blocking(cases_bottom, blocking)
            else:
                blocking_bottom = [True] * len(cars)

            return min(min_blocking_cases(blocking_top, new_directly_blocking), min_blocking_cases(blocking_bottom, new_directly_blocking))
    
    return min_blocking_cases(blocking, directly_blocking)


def improved_blocking_cars(game_state):
    """
    Calculate a lower bound to the number of cars that need to be moved to unblock the red car.

    Parameters:
    game_state (dict): The current state of the game, including the size of the grid and the positions of the cars.

    Returns:
    int: a lower bound to the number of cars that need to be moved.
    """
    cars = game_state["cars"]
    n = game_state["size"]

    def is_blocking_case(car, case):
        """
        Check if a car is blocking a specific case on the grid.

        Parameters:
        car (dict): The car to check.
        case (tuple): The case to check, represented as (i, j) coordinates.

        Returns:
        tuple: A tuple (bool, int or None) where the first element is True if the car is blocking the case, 
               and the second element is the relative position of the case within the car if it is blocking, 
               otherwise None.
        """
        i, j = case
        if car["orientation"] == "v" and car["x_topleft"] == i and car["y_topleft"] <= j and car["y_topleft"] + car["length"] > j:
            return True, j - car["y_topleft"]
        if car["orientation"] == "h" and car["y_topleft"] == j and car["x_topleft"] <= i and car["x_topleft"] + car["length"] > i:
            return True, i - car["x_topleft"]
        return False, None

    def is_blocking_red_car(car):
        """
        Check if a car is blocking the red car.

        Parameters:
        car (dict): The car to check.

        Returns:
        tuple: A tuple (bool, int or None) where the first element is True if the car is blocking the red car,
               and the second element is the relative position of the red car within the blocking car if it is blocking,
               otherwise None.
        """
        if car["y_topleft"] <= cars[0]["y_topleft"] and cars[0]["y_topleft"] < car["y_topleft"] + car["length"] and cars[0]["x_topleft"] <= car["x_topleft"] and car["orientation"] == "v":
            return True, cars[0]["y_topleft"] - car["y_topleft"]
        else:
            return False, None

    to_move = []  # List of cars to move and the case number to free (0 for top_left, length-1 for bottom_right)
    alive = len(cars) * [True]  # List of cars that have not disappeared
    alive[0] = False
    for i, car in enumerate(cars):
        b, case = is_blocking_red_car(car)
        if b:
            to_move.append((i, case))
            alive[i] = False

    def next_states(to_move, alive):
        list_next_states = []

        for num_move, (ind_car, case) in enumerate(to_move):
            car = cars[ind_car]
            if car["orientation"] == "v":
                # Move up (length - case)
                if car["y_topleft"] + case - car["length"] >= 0:
                    new_to_move = [x for i, x in enumerate(to_move) if i != num_move]
                    new_alive = [x for x in alive]
                    for j in range(car["y_topleft"] + case - car["length"], car["y_topleft"]):
                        for ind_car2, car2 in enumerate(cars):
                            b, case2 = is_blocking_case(car2, (car["x_topleft"], j))
                            if b and new_alive[ind_car2]:
                                new_alive[ind_car2] = False
                                new_to_move.append((ind_car2, case2))
                    list_next_states.append((new_to_move, new_alive))
                # Move down (case + 1)
                if car["y_topleft"] + car["length"] + case < n:
                    new_to_move = [x for i, x in enumerate(to_move) if i != num_move]
                    new_alive = [x for x in alive]
                    for j in range(car["y_topleft"] + car["length"], car["y_topleft"] + car["length"] + case + 1):
                        for ind_car2, car2 in enumerate(cars):
                            b, case2 = is_blocking_case(car2, (car["x_topleft"], j))
                            if b and new_alive[ind_car2]:
                                new_alive[ind_car2] = False
                                new_to_move.append((ind_car2, case2))
                    list_next_states.append((new_to_move, new_alive))
            if car["orientation"] == "h":
                # Move left (length - case)
                if car["x_topleft"] + case - car["length"] >= 0:
                    new_to_move = [x for i, x in enumerate(to_move) if i != num_move]
                    new_alive = [x for x in alive]
                    for i in range(car["x_topleft"] + case - car["length"], car["x_topleft"]):
                        for ind_car2, car2 in enumerate(cars):
                            b, case2 = is_blocking_case(car2, (i, car["y_topleft"]))
                            if b and new_alive[ind_car2]:
                                new_alive[ind_car2] = False
                                new_to_move.append((ind_car2, case2))
                    list_next_states.append((new_to_move, new_alive))
                # Move right (case + 1)
                if car["x_topleft"] + car["length"] + case < n:
                    new_to_move = [x for i, x in enumerate(to_move) if i != num_move]
                    new_alive = [x for x in alive]
                    for i in range(car["x_topleft"] + car["length"], car["x_topleft"] + car["length"] + case + 1):
                        for ind_car2, car2 in enumerate(cars):
                            b, case2 = is_blocking_case(car2, (i, car["y_topleft"]))
                            if b and new_alive[ind_car2]:
                                new_alive[ind_car2] = False
                                new_to_move.append((ind_car2, case2))
                    list_next_states.append((new_to_move, new_alive))

        return list_next_states

    q = queue.Queue()
    q.put((to_move, alive))
    while q:
        to_move, alive = q.get()
        if to_move == []:
            return sum(1 for b in alive if b == False)
        else:
            list_next_states = next_states(to_move, alive)
            for s in list_next_states:
                q.put(s)