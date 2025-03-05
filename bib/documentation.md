# Documentation


- [Documentation](#documentation)
  - [Input/Output Functions](#inputoutput-functions)
    - [get\_input()](#get_input)
    - [get\_input\_from\_file(file)](#get_input_from_filefile)
    - [show\_grid(grid)](#show_gridgrid)
    - [set\_game\_from\_file(file)](#set_game_from_filefile)
  - [Game Logic Functions](#game-logic-functions)
    - [is\_point\_in\_grid(point, n)](#is_point_in_gridpoint-n)
    - [cars\_into\_grid(n, cars)](#cars_into_gridn-cars)
    - [is\_winning(game\_state)](#is_winninggame_state)
    - [copy\_game\_state(game\_state)](#copy_game_stategame_state)
    - [get\_next\_moves(game\_state)](#get_next_movesgame_state)
  - [Hashing Functions](#hashing-functions)
    - [generate\_primes(n)](#generate_primesn)
    - [distance\_top\_left(car)](#distance_top_leftcar)
    - [fast\_exp\_mod(base, exp, mod)](#fast_exp_modbase-exp-mod)
  - [Breadth-First Search Functions](#breadth-first-search-functions)
    - [brute\_foce\_BFS(game\_state)](#brute_foce_bfsgame_state)
    - [brute\_foce\_BFS\_from\_file(file)](#brute_foce_bfs_from_filefile)
    - [brute\_foce\_BFS\_with\_solution(game\_state)](#brute_foce_bfs_with_solutiongame_state)
  - [A\* Search Functions](#a-search-functions)
    - [heuristic\_BFS(game\_state, heuristic)](#heuristic_bfsgame_state-heuristic)
    - [distance\_to\_goal(game\_state)](#distance_to_goalgame_state)
    - [number\_cars\_blocking(game\_state)](#number_cars_blockinggame_state)
    - [number\_cars\_indirectly\_blocking(game\_state)](#number_cars_indirectly_blockinggame_state)
    - [improved\_blocking\_cars(game\_state)](#improved_blocking_carsgame_state)
  - [Run.py](#runpy)
  - [Visualisation](#visualisation)
    - [show\_grid(grid)](#show_gridgrid-1)
    - [print\_solution(game\_state, solution)](#print_solutiongame_state-solution)
    - [write\_solution(game\_state, solution, file)](#write_solutiongame_state-solution-file)
    - [generate\_results\_BFS(nb\_games=40)](#generate_results_bfsnb_games40)
    - [plot\_BFS(nb\_games=40)](#plot_bfsnb_games40)
    - [get\_data\_from\_different\_heuristic(heuristics\_list, nb\_games=40)](#get_data_from_different_heuristicheuristics_list-nb_games40)
    - [plot\_compare\_BFS\_vs\_heuristic(heuristic, nb\_games=40)](#plot_compare_bfs_vs_heuristicheuristic-nb_games40)
    - [plot\_compare\_heuristics(heuristics\_list, nom\_heuristiques, nb\_games=40)](#plot_compare_heuristicsheuristics_list-nom_heuristiques-nb_games40)
  - [generate\_game.py](#generate_gamepy)


## Input/Output Functions

### get_input()
Get the input from console for the Rush Hour game parameters.
- Returns: (n, cars) : tuple
    - cars: List of car dictionaries with properties:
        - id_car: Car ID number
        - orientation: 'h' for horizontal or 'v' for vertical
        - length: Length of the car
        - x_topleft: X coordinate of top-left position (0-indexed) 
        - y_topleft: Y coordinate of top-left position (0-indexed)
- Example:
```python
n, cars = get_input()
print(f"Grid size: {n}")
print(f"Cars: {cars}")
```
This example shows how to call `get_input()` and print the returned grid size and car list.

### get_input_from_file(file)
Gets input from a file for the Rush Hour game parameters.
- Parameters:
    - file: Path to input file
- Returns: Same as get_input()
- Example:
```python
n, cars = get_input_from_file("input.txt")
print(f"Grid size: {n}")
print(f"Cars: {cars}")
```
This example reads the game configuration from "input.txt" and prints the grid size and car list.


### show_grid(grid) 
Display the grid in a readable format.
- Parameters:
    - grid: 2D list representing game board with car IDs
- Example:
```python
grid = [[0, 1, 1, 0], [0, 0, 0, 0], [2, 2, 0, 3], [0, 0, 0, 3]]
show_grid(grid)
```
This example displays a sample game grid to the console.



### set_game_from_file(file)
Sets correctly the game from a file for the Rush Hour game parameters.
- Parameters:
    - file: Path to input file
- Returns: game_state : dictionary with 3 attributes:
    - size : size of the grid
    - cars : same as in get_input
    - grid : 2D list representing game board with car IDs
- Example:
```python
game_state = get_input_from_file("input.txt")
```
This example reads the game configuration from "input.txt" and puts it in the format used during the project.

## Game Logic Functions

### is_point_in_grid(point, n)
Checks if a point is within the grid boundaries.
- Parameters:
    - point: (x,y) tuple of coordinates
    - n: Size of grid
- Returns: Boolean indicating if point is in grid
- Example:
```python
n = 4
point = (2, 3)
is_in = is_point_in_grid(point, n)
print(f"Is point {point} in grid of size {n}? {is_in}")
```
This example checks if the point (2, 3) is within a 4x4 grid.



### cars_into_grid(n, cars)
Check the validity of the inputs and compute the grid
- Parameters:
    - n: Size of grid
    - cars: List of car dictionaries 
- Returns: (valid, grid) tuple where:
    - valid: Boolean indicating if configuration is valid
    - grid: 2D list representing game board with car IDs
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 0, 'y_topleft': 0}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
valid, grid = set_game(n, cars)
print(f"Game setup valid: {valid}")
if valid:
    print(f"Initial grid: {grid}")
```
This example sets up a 4x4 game with two cars and prints whether the setup is valid and the initial grid.

### is_winning(game_state)
Checks if current configuration is in winning state.
- Parameters:
    - game_state : dictionary 
- Returns: Boolean indicating if won
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

won = is_winning(game_state)
print(f"Is the game won? {won}")
```
This example checks if the given car configuration represents a winning state.

### copy_game_state(game_state)
Creates a deep copy of the game_state dictionary.
- Parameters:
    - game_state: dictionary
- Returns: New copy of game_state :  dictionary
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

copy_game_state = copy_game_state(cars)
```
This example demonstrates creating a deep copy of game_state dictionary.

### get_next_moves(game_state) 
Gets all valid next moves from current configuration.
- Parameters:
    - game_state: dictionary
- Returns: List of possible next game_state configurations
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

next_moves = get_next_moves(game_state)
print(f"Next possible moves: {next_moves}")
```
This example retrieves and prints the possible next moves from a given game configuration.

## Hashing Functions

### generate_primes(n)
Generates first n prime numbers.
- Parameters:
    - n: Number of primes to generate
- Returns: List of n prime numbers
- Example:
```python
n = 5
primes = generate_primes(n)
print(f"First {n} prime numbers: {primes}")
```
This example generates the first 5 prime numbers.

### distance_top_left(car)
Gets distance from car to top/left border.
- Parameters:
    - car: Car dictionary
- Returns: Distance from top/left border
- Example:
```python
car = {'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 1, 'y_topleft': 2}
distance = distance_top_left(car)
print(f"Distance to top/left: {distance}")
```
This example calculates the distance of a car from the top-left border.

### fast_exp_mod(base, exp, mod)
Calculates modular exponentiation efficiently.
- Parameters:
    - base: Base number
    - exp: Exponent
    - mod: Modulus
- Returns: (base^exp) mod mod
- Example:
```python
base = 2
exp = 10
mod = 100
result = fast_exp_mod(base, exp, mod)
print(f"({base}^{exp}) mod {mod} = {result}")
```
This example calculates (2^10) mod 100.

## Breadth-First Search Functions

### brute_foce_BFS(game_state)
Finds shortest solution using breadth-first search.
- Parameters:
    - game_state: dictionary
- Returns: Number of moves in shortest solution
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

moves = brute_foce_BFS(game_state)
print(f"Number of moves in shortest solution: {moves}")
```
This example finds the shortest solution for a given game configuration using BFS.

### brute_foce_BFS_from_file(file)
Finds shortest solution using breadth-first search from a file input.
- Parameters:
    - file: Path to input file
- Returns: Number of moves in shortest solution
- Example:
```python
file = "input.txt"

moves = brute_foce_BFS_from_file(file)
print(f"Number of moves in shortest solution: {moves}")
```
This example finds the shortest solution for a game configuration read from "input.txt" using BFS.



### brute_foce_BFS_with_solution(game_state)
Same as brute_foce_BFS but also returns solution path.
- Parameters:
    - game_state: dictionary
- Returns: (explored_nodes, min_dist, solution) tuple
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

explored_nodes, min_dist, solution = brute_foce_BFS_with_solution(game_state)
print(f"Explored nodes: {explored_nodes}, Minimum distance: {min_dist}, Solution: {solution}")
```
This example finds the shortest solution and the path using BFS.

## A* Search Functions 

### heuristic_BFS(game_state, heuristic)
A* search using provided heuristic function.
- Parameters:
    - game_state: dictionary
    - heuristic: Function mapping (n,cars) to estimate
- Returns: (explored_nodes, min_dist, solution) tuple
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}
heuristic = distance_to_goal

explored_nodes, min_dist, solution = heuristic_BFS(game_state, heuristic)
print(f"Explored nodes: {explored_nodes}, Minimum distance: {min_dist}, Solution: {solution}")
```
This example demonstrates A* search with a provided heuristic function.

### distance_to_goal(game_state)
Heuristic estimating the normalized distance to goal (between 0 and 1) .
- Parameters:
    - game_state: dictionary
- Returns: Distance estimate : float
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

distance = distance_to_goal(game_state)
print(f"Estimated distance to goal: {distance}")
```
This example calculates the estimated distance to the goal using the `distance_to_goal` heuristic.

### number_cars_blocking(game_state)
Heuristic counting blocking cars.
- Parameters:
    - game_state: dictionary
- Returns: Number of blocking cars
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

blocking_cars = number_cars_blocking(game_state)
print(f"Number of blocking cars: {blocking_cars}")
```
This example counts the number of cars blocking the path to the goal.


### number_cars_indirectly_blocking(game_state)
Heuristic counting indirectly blocking cars (simple heuristic).
- Parameters:
    - game_state: dictionary
- Returns: Number of blocking cars
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

blocking_cars = number_cars_indirectly_blocking(game_state)
print(f"Number of blocking cars: {blocking_cars}")
```
This example counts the number of cars indirectly blocking the path to the goal.


### improved_blocking_cars(game_state)
Heuristic counting indirectly blocking cars (complex heuristic).
- Parameters:
    - game_state: dictionary
- Returns: Number of blocking cars
- Example:
```python
n = 4
cars = [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}, {'id_car': 2, 'orientation': 'v', 'length': 3, 'x_topleft': 2, 'y_topleft': 0}]
grid = cars_into_grid(n, cars)[1]
game_state = {"size":n, "cars": cars, "grid": grid}

blocking_cars = improved_blocking_cars(game_state)
print(f"Number of blocking cars: {blocking_cars}")
```
This example counts the number of cars indirectly blocking the path to the goal.


## Run.py

```txt
usage: run.py [-h] [-i INPUT] [-H {distance_to_goal,number_cars_blocking,improved_blocking_cars}] [-o OUTPUT]

Solves the Rush Hour puzzle using a heuristic-based BFS.

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     File path for the game configuration.
  -H, --heuristic {distance_to_goal,number_cars_blocking,improved_blocking_cars}
                        Heuristic function.
  -o, --output OUTPUT   Output file path.

Examples:
        1. Run the solver with an input file and print the solution:
            python run.py -i input.txt
            
        2. Run with a specific heuristic, then print the solution:
            python run.py -i input.txt -H distance_to_goal

        3. Run with an input file, a specific heuristic, and save the solution:
            python run.py -i input.txt -H number_cars_blocking -o output.txt

        4. Run with user input and print the solution:
            python run.py

        5. Use a specific heuristic with user input:
            python run.py -H improved_blocking_cars
```

## Visualisation

### show_grid(grid)
Display the grid in a readable format.
- Parameters:
    - grid: 2D list representing game board with car IDs
- Example:
```python
grid = [[0, 1, 1, 0], [0, 0, 0, 0], [2, 2, 0, 3], [0, 0, 0, 3]]
show_grid(grid)
```
This example displays a sample game grid to the console.

### print_solution(game_state, solution)
Print the solution of a game.
- Parameters:
    - game_state: dictionary
    - solution: List of dictionaries representing solution steps
- Example:
```python
game_state = {"size": 4, "cars": [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}], "grid": [[0, 1, 1, 0], [0, 0, 0, 0], [2, 2, 0, 3], [0, 0, 0, 3]]}
solution = [{"move": "right", "car_id": 1}]
print_solution(game_state, solution)
```
This example prints the solution steps for a given game state.

### write_solution(game_state, solution, file)
Write the solution of a game to a file.
- Parameters:
    - game_state: dictionary
    - solution: List of dictionaries representing solution steps
    - file: Path to the output file
- Example:
```python
game_state = {"size": 4, "cars": [{'id_car': 1, 'orientation': 'h', 'length': 2, 'x_topleft': 2, 'y_topleft': 1}], "grid": [[0, 1, 1, 0], [0, 0, 0, 0], [2, 2, 0, 3], [0, 0, 0, 3]]}
solution = [{"move": "right", "car_id": 1}]
write_solution(game_state, solution, "solution.txt")
```
This example writes the solution steps to "solution.txt".

### generate_results_BFS(nb_games=40)
Generate results for a set of games using the Breadth-First Search (BFS) algorithm.
- Parameters:
    - nb_games: Number of games to generate results for (default is 40)
- Returns: Tuple containing lists of number of cars, depths, nodes visited, and times for the given number of games
- Example:
```python
results = generate_results_BFS(nb_games=10)
print(results)
```
This example generates BFS results for 10 games and prints them.

### plot_BFS(nb_games=40)
Plot the results of a Breadth-First Search (BFS) algorithm for a given number of games.
- Parameters:
    - nb_games: Number of games to generate results for (default is 40)
- Example:
```python
plot_BFS(nb_games=10)
```
This example plots BFS results for 10 games.

### get_data_from_different_heuristic(heuristics_list, nb_games=40)
Collect data from different heuristics on a set of games.
- Parameters:
    - heuristics_list: List of heuristic functions to evaluate
    - nb_games: Number of games to evaluate (default is 40)
- Returns: List of dictionaries containing the number of explored nodes, minimum distance, grid size, and time taken for each heuristic
- Example:
```python
heuristics = [distance_to_goal, number_cars_blocking]
data = get_data_from_different_heuristic(heuristics, nb_games=10)
print(data)
```
This example collects data from two heuristics for 10 games and prints the results.

### plot_compare_BFS_vs_heuristic(heuristic, nb_games=40)
Compare the performance of Breadth-First Search (BFS) and a given heuristic algorithm.
- Parameters:
    - heuristic: Heuristic function to be compared against BFS
    - nb_games: Number of games/problems to solve for comparison (default is 40)
- Example:
```python
plot_compare_BFS_vs_heuristic(distance_to_goal, nb_games=10)
```
This example compares BFS and the `distance_to_goal` heuristic for 10 games.

### plot_compare_heuristics(heuristics_list, nom_heuristiques, nb_games=40)
Compare the performance of multiple heuristic algorithms.
- Parameters:
    - heuristics_list: List of heuristic functions to evaluate
    - nom_heuristiques: List of names corresponding to the heuristic functions
    - nb_games: Number of games/problems to solve for comparison (default is 40)
- Example:
```python
heuristics = [distance_to_goal, number_cars_blocking]
names = ["Distance to Goal", "Number of Blocking Cars"]
plot_compare_heuristics(heuristics, names, nb_games=10)
```
This example compares the performance of two heuristics for 10 games.


## generate_game.py

```text
usage: generate_game.py [-h] [-n NB_CARS] [-s SIZE] [-o OUTPUT] [-l LIMITE_NB_TENTATIVES]

Generate a Rush Hour game.

options:
  -h, --help            show this help message and exit
  -n, --nb_cars NB_CARS
                        Number of cars in the game
  -s, --size SIZE       Size of the grid
  -o, --output OUTPUT   Output file to save the game
  -l, --limite_nb_tentatives LIMITE_NB_TENTATIVES
                        Maximum number of attempts to place a car

Examples:
        generate_game.py -n 12 -s 8 -o game.txt
        generate_game.py --nb_cars 15 --size 10 --output game.txt

```