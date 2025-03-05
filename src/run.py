"""
This script solves the Rush Hour puzzle using a heuristic-based Breadth-First Search (BFS).
Functions:
    main(): Parses command-line arguments and runs the Rush Hour solver with the specified options.
Usage examples:
"""

import argparse
from tools import (
    get_input, get_input_from_file, set_game_from_file, cars_into_grid,
    heuristic_BFS, distance_to_goal, number_cars_blocking, improved_blocking_cars
)
from visualisation import print_solution, write_solution

def main():
    
    parser = argparse.ArgumentParser(
        description="Solves the Rush Hour puzzle using a heuristic-based BFS.",
        epilog="""Examples:
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
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-i", "--input", help="File path for the game configuration.")
    parser.add_argument("-H", "--heuristic", help="Heuristic function.",
                        choices=["distance_to_goal","number_cars_blocking","improved_blocking_cars"])
    parser.add_argument("-o", "--output", help="Output file path.")
    args = parser.parse_args()

    if args.input:
        game_state = set_game_from_file(args.input)
    else:
        n, cars = get_input()
        valid, grid = cars_into_grid(n, cars)
        game_state = {"size": n, "cars": cars, "grid": grid} if valid else None

    if args.heuristic == "distance_to_goal":
        h = distance_to_goal
    elif args.heuristic == "number_cars_blocking":
        h = number_cars_blocking
    elif args.heuristic == "improved_blocking_cars":
        h = improved_blocking_cars
    else:
        h = lambda x: 0

    if game_state is not None:
        nb_nodes_explored, dist, solution = heuristic_BFS(game_state, heuristic=h)
        print(f"{nb_nodes_explored}, {dist}, {len(solution)}")
        if args.output:
            write_solution(game_state, solution, args.output)
        else:
            print_solution(game_state, solution)
    else:
        print("Invalid game configuration")

if __name__ == "__main__":
    main()
