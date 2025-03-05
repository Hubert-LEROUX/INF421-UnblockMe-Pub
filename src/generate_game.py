"""
Le but de ce fichier est de générer des jeux de données

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

"""

from tools import * 
from visualisation import *
import random
import argparse

def save_game(game_state, file):
    """
    Save a game to a file.
    
    :param game_state: dict, the game state
    :param file: str, the file path
    """
    with open(file, "w") as f:
        f.write(f"{game_state['size']}\n")
        for car in game_state["cars"]:
            f.write(f"{car['id_car']} {car['length']} {car['orientation']} {car['x_topleft']} {car['y_topleft']}\n")

def create_game(nb_cars=10, size=6, limite_nb_tentatives=1_000):
    """
    Create a game.
    
    :param nb_cars: int, the number of cars in the game
    :param size: int, the size of the grid
    :param limite_nb_tentatives: int, the maximum number of attempts to place a car
    :return: dict, the game state
    """
    def create_new_car(game_state, id_car):
        """
        Create a car.
        
        :param id_car: int, the car ID
        :param length: int, the car length
        :param orientation: str, the car orientation
        :return: dict, the car
        """
        length = random.randint(2,3) if id_car != 1 else 2 # la première voiture est toujours de longueur 2
        orientation = random.choice(["h", "v"]) if id_car != 1 else "h" # la première voiture est toujours horizontale

        # Il faut chercher de la place. Si on y arrive pas on renvoie None
        lines_indices = list(range(size)) if orientation == "h" else list(range(size-length+1))
        columns_indices = list(range(size)) if orientation == "v" else list(range(size-length+1))

        random.shuffle(lines_indices)
        random.shuffle(columns_indices)

        # On tire au hasard les coordonnées
        for i in lines_indices:
            for j in columns_indices:
                if orientation == "h":
                    if all(game_state["grid"][i][j+k] == 0 for k in range(length)):
                        return {"id_car": id_car, "length": length, "orientation": orientation, "x_topleft":j, "y_topleft":i}
                else:
                    if all(game_state["grid"][i+k][j] == 0 for k in range(length)):
                       return {"id_car": id_car, "length": length, "orientation": orientation, "x_topleft":j, "y_topleft":i}
                    
        return None

    def trace_grid(orientation, length, x, y, value=0):
        """
        Trace a car on the grid.
        
        :param orientation: str, the car orientation
        :param length: int, the car length
        :param y: int, the y coordinate of the top-left corner of the car
        :param x: int, the x coordinate of the top-left corner of the car
        :param value: int, the value to write
        """
        for j in range(length):
            if orientation == "h":
                game_state["grid"][y][x+j] = value
            else:
                game_state["grid"][y+j][x] = value
    
    game_state = {"size":size, "grid": [[0 for _ in range(size)] for _ in range(size)], "cars": []}
    nb_tentatives = 0 # Parfois ce n'est pas réalisable, on limite le nombre de tentatives
    for i in range(nb_cars):

        car = create_new_car(game_state, i+1)

        if car is None: # Si on n'arrive pas à placer une voiture, on recommence
            nb_tentatives += 1
            if nb_tentatives > limite_nb_tentatives:
                raise exception("Impossible de placer les voitures")
            return create_game(nb_cars, size)
        

        game_state["cars"].append(car)

        # On écrit la voiture dans la grille
        trace_grid(car["orientation"], car["length"], car["x_topleft"], car["y_topleft"], car["id_car"])


        while heuristic_BFS(copy_game_state(game_state))[1] == float("inf"): # On vérifie que le jeu est solvable
            nb_tentatives += 1
            if nb_tentatives > limite_nb_tentatives:
                raise exception("Impossible de placer les voitures")
            # On efface la voiture
            trace_grid(car["orientation"], car["length"], car["x_topleft"], car["y_topleft"])

            car = create_new_car(game_state, i+1) # on recrée la voiture
            game_state["cars"][-1] = car # on la remplace

            # on la réécrit dans la grille
            trace_grid(car["orientation"], car["length"], car["x_topleft"], car["y_topleft"], car["id_car"])

            
    return game_state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Rush Hour game.",
                                      epilog="""Examples:
        generate_game.py -n 12 -s 8 -o game.txt
        generate_game.py --nb_cars 15 --size 10 --output game.txt
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--nb_cars", type=int, default=10, help="Number of cars in the game")
    parser.add_argument("-s", "--size", type=int, default=6, help="Size of the grid")
    parser.add_argument("-o", "--output", type=str, help="Output file to save the game")
    parser.add_argument("-l", "--limite_nb_tentatives", type=int, default=1000, help="Maximum number of attempts to place a car")

    args = parser.parse_args()

    print(f"Generating a game with {args.nb_cars} cars and a grid of size {args.size}x{args.size}")
    game_state = create_game(nb_cars=args.nb_cars, size=args.size, limite_nb_tentatives=args.limite_nb_tentatives)

    if args.output:
        save_game(game_state, args.output)

    show_grid(game_state["grid"])