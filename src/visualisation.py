from tools import *

import os
import time
from matplotlib import pyplot as plt

examples_dir = os.path.join(".", "examples")

def show_grid(grid):
    """
    Display the grid in a readable format.
    
    :param grid: List of lists representing the grid.
    """
    max_id_car = max(max(line) for line in grid)
    nb_digits = len(str(max_id_car))
    for line in grid:
        print('|' + '|'.join('%0*d' % (nb_digits, cell) if cell != 0 else '_'*nb_digits for cell in line) + '|')

def print_solution(game_state, solution):
    """
    Print the solution of a game.
    
    :param game_state: dict, the game state
    :param solution: dict, the solution
    """
    print(f"Initial state:")
    show_grid(game_state["grid"])
    print(f"Solution:")
    for i, step in enumerate(solution):
        print(f"Step {i+1}:")
        show_grid(step["grid"])
        # print(f"Move car {step['id_car']} {step['direction']} by {step['distance']} steps")
        print()


def write_solution(game_state, solution, file):
    """
    Write the solution of a game to a file.
    
    :param game_state: dict, the game state
    :param solution: dict, the solution
    :param file: str, the file path
    """
    with open(file, "w") as f:
        f.write(f"Initial state:\n")
        for line in game_state["grid"]:
            f.write('|' + '|'.join(str(cell) if cell != 0 else '_' for cell in line) + '|\n')
        f.write(f"Solution:\n")
        for i, step in enumerate(solution):
            f.write(f"Step {i+1}:\n")
            for line in step["grid"]:
                f.write('|' + '|'.join(str(cell) if cell != 0 else '_' for cell in line) + '|\n')
            # f.write(f"Move car {step['id_car']} {step['direction']} by {step['distance']} steps\n\n")

def generate_results_BFS(nb_games=40):
    depths = []
    nodes_visiteds = []
    nb_cars= []
    temps=[]
    for i in range(1, nb_games + 1):
        file = os.path.join(examples_dir, f"GameP{i:02}.txt")
        game_state = set_game_from_file(file)

        t = time.time()
        depth, nodes_visited= brute_foce_BFS(game_state)

        temps.append(time.time()-t)
        depths.append(depth)
        nodes_visiteds.append(nodes_visited)
        nb_cars.append(len(game_state["cars"]))
    
    return nb_cars, depths, nodes_visiteds, temps

def plot_BFS(nb_games=40):
    """
    Plots the results of a Breadth-First Search (BFS) algorithm for a given number of games.
    Parameters:
    nb_games (int): The number of games to generate results for. Default is 40.
    The function generates four subplots:
    1. Time vs Number of cars
    2. Time vs Depth of the solution
    3. Nodes visited vs Number of cars
    4. Nodes visited vs Depth
    The data for these plots is obtained from the `generate_results_BFS` function, which returns
    the number of cars, depths, nodes visited, and times for the given number of games.
    The plots are displayed in a 2x2 grid layout.
    """
    nb_cars, depths, nodes_visiteds, temps = generate_results_BFS(nb_games)

    plt.figure(figsize=(8, 8))

    plt.subplot(221)
    plt.plot(nb_cars, temps, 'o')
    plt.title("Time vs Number of cars")
    plt.xlabel("Number of cars")
    plt.ylabel("Time (s)")

    plt.subplot(222)
    plt.plot(depths, temps, 'o')
    plt.title("Time vs Depth of the solution")
    plt.xlabel("Depth")
    plt.ylabel("Time (s)")

    plt.subplot(223)
    plt.plot(nb_cars, nodes_visiteds, 'o')
    plt.title("Nodes visited vs Number of cars")
    plt.xlabel("Number of cars")
    plt.ylabel("Number of nodes visited")

    plt.subplot(224)
    plt.plot(depths, nodes_visiteds, 'o')
    plt.title("Nodes visited vs Depth")
    plt.xlabel("Depth")
    plt.ylabel("Number of nodes visited")
               
    plt.grid()
    plt.tight_layout()
    plt.show()

def get_data_from_different_heuristic(heuristics_list, nb_games=40):
    """
    Collect data from different heuristics on a set of games.

    Parameters:
    heuristics_list (list): List of heuristic functions to evaluate.
    nb_games (int): Number of games to evaluate. Default is 40.

    Returns:
    list: A list of dictionaries containing the number of explored nodes, minimum distance, grid size, and time taken for each heuristic.
    """
    data = [[] for i in range(len(heuristics_list))]

    for i in range(1, nb_games + 1):
        print(f"{i:2d}", end=" ")
        start_time = time.time()

        file = os.path.join(examples_dir, f"GameP{i:02}.txt")
        game_state = set_game_from_file(file)
        n = game_state["size"]
        
        for j, h in enumerate(heuristics_list):
            start_time_heuristic = time.time()
            nb_explored, min_dist, _ = heuristic_BFS(game_state, h)
            
            data[j].append({"nb_explored": nb_explored, "min_dist": min_dist, "n": n, "time": time.time() - start_time_heuristic})
        
        print(f"{time.time() - start_time:5.2f} s - Done")

    return data


def plot_compare_BFS_vs_heuristic(heuristic, nb_games=40):
    """
    Compare the performance of Breadth-First Search (BFS) and a given heuristic algorithm.
    This function generates four plots:
    1. Execution time comparison between BFS and the heuristic algorithm.
    2. Number of explored nodes comparison between BFS and the heuristic algorithm.
    3. Ratio of execution time (Heuristic/BFS) vs Number of the problem.
    4. Ratio of explored nodes (Heuristic/BFS) vs Number of the problem.
    Parameters:
    heuristic (function): A heuristic function to be compared against BFS.
    nb_games (int, optional): The number of games/problems to solve for comparison. Default is 40.
    Returns:
    None
    """
    heuristics_list = [lambda x: 0, heuristic]
    data = get_data_from_different_heuristic(heuristics_list, nb_games)

    plt.figure(figsize=(16, 16))

    plt.subplot(121)
    plt.plot([data[0][i]["time"] for i in range(nb_games)], [data[1][i]["time"]/ data[0][i]["time"] for i in range(nb_games)], 'o')
    plt.axhline(y=1, color='r', linestyle='-')
    plt.title("Ratio of execution time (Heuristic/BFS) ")
    plt.xlabel("Execution time of BFS")
    plt.ylabel("Ratio of execution time")
    plt.grid()

    plt.subplot(122)
    plt.plot([data[0][i]["nb_explored"] for i in range(nb_games)], [data[1][i]["nb_explored"] / data[0][i]["nb_explored"] for i in range(nb_games)], 'o')
    plt.axhline(y=1, color='r', linestyle='-')
    plt.title("Ratio of explored nodes (Heuristic/BFS) vs Number of the problem")
    plt.xlabel("Execution time of BFS")
    plt.ylabel("Ratio of explored nodes")
    plt.grid()

    plt.tight_layout()
    plt.show()


def plot_compare_heuristics(heuristics_list, nom_heuristiques, nb_games=40):
    heuristics_list.append(lambda x: 0)

    data = get_data_from_different_heuristic(heuristics_list, nb_games)
    
    plt.figure(figsize=(16, 16))

    plt.subplot(121)
    for j in range(len(heuristics_list)-1):
        plt.plot([data[-1][i]["time"] for i in range(nb_games)], [data[j][i]["time"]/ data[-1][i]["time"] for i in range(nb_games)], 'o', label=nom_heuristiques[j])
    plt.legend()
    plt.axhline(y=1, color='r', linestyle='-')
    plt.title("Ratio of execution time (Heuristic/BFS) ")
    plt.xlabel("Execution time of BFS")
    plt.ylabel("Ratio of execution time")
    plt.grid()

    plt.subplot(122)
    for j in range(len(heuristics_list)-1):
        plt.plot([data[-1][i]["nb_explored"] for i in range(nb_games)], [data[j][i]["nb_explored"]/ data[-1][i]["nb_explored"] for i in range(nb_games)], 'o', label=nom_heuristiques[j])
    plt.legend()
    plt.axhline(y=1, color='r', linestyle='-')
    plt.title("Ratio of explored nodes (Heuristic/BFS) vs Number of the problem")
    plt.xlabel("Execution time of BFS")
    plt.ylabel("Ratio of explored nodes")
    plt.grid()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    #plot_BFS(40)
    #plot_compare_BFS_vs_heuristic (number_cars_blocking, 40)
    liste_heuristiques = [distance_to_goal,number_cars_blocking,number_cars_indirectly_blocking]
    nom_heuristiques = ["distance à l'objectif","nombre de voitures blocant directement","nombre de voitures blocant indirectement (version 2)"]
    plot_compare_heuristics(liste_heuristiques, nom_heuristiques, nb_games=40)