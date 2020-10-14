#!/usr/bin/env python3

"""
Sorting algorithms visualiser.

Supported algorithms:
- Selection sort
- Bubble sort
- Quick sort

Note that this does not provide an accurate indicator of an algorithm's performance, as most of the time is spent on
drawing the data, not on sorting. Bubble sort, for example, doesn't show each swap, as that would take forever,
instead the resulting array after each iteration of the algorithm is shown, therefore giving the impression that 
it is more efficient than quick sort, when in reality quick sort is usually much more efficient.

Author: Norrotor
"""

import os
import sys
import time
import argparse
import sorting_algorithms as sa

# For best ratios, the width should be 2^n * height, where 'n' is a positive integer.
WINDOW_WIDTH = 1024  # Window width.
WINDOW_HEIGHT = 512  # Window height. Also represents the number of items in the array.

# RGB colours for the game
colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
}

item_colors = [colors["black"] for _ in range(WINDOW_HEIGHT)]

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Hide pygame message
import pygame

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW.fill(colors["white"])


def check_events():
    """Check window events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def update_window(algorithm: callable, window: pygame.display, item1: int = 0, item2: int = 0) -> None:
    """Draw the items in the array on the given window; also change the window's caption to current time.

    :param algorithm: algorithm instance
    :param item1: first item of swapping
    :param item2: other item of swapping
    :param window: window to draw on
    """

    global item_colors

    window.fill(colors["white"])
    pygame.display.set_caption(
        f"Sorting Visualiser    Time: {time.time() - algorithm.start_time:.3f}    Status: Sorting")

    item_width = WINDOW_WIDTH // len(algorithm.array)  # Width of each array item

    # Set appropriate item colors
    item_colors[item1] = colors["green"]
    item_colors[item2] = colors["red"]

    # Draw the items
    for i in range(len(algorithm.array)):
        pygame.draw.rect(window, item_colors[i], (i * item_width, WINDOW_HEIGHT, item_width, -algorithm.array[i]))

    # Set item color back to black
    item_colors[item1] = colors["black"]
    item_colors[item2] = colors["black"]

    check_events()  # Check events in case the user wants to quit early
    pygame.display.update()  # Update the pygame window to reflect the changes made


def update_caption(finish_time):
    """Update window caption with the finish time."""
    pygame.display.set_caption(
        f"Sorting Visualiser    Time: {finish_time:.3f}    Status: Done")
    while True:
        pygame.display.update()
        check_events()


def main():
    # Map of algorithm name to algorithm callable
    algorithms = {
        "selection": sa.SelectionSort(),
        "bubble": sa.BubbleSort(),
        "quick": sa.QuickSort(),
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", help="sorting algorithm", default="selection", nargs="?",
                        choices=algorithms.keys())
    parser.add_argument("--sleep", help="wait time after swap (s)", default=0.0, type=float)

    args = None
    try:
        args = parser.parse_args()
    except TypeError:
        parser.print_help()

    alg_name = args.algorithm
    algorithm = algorithms[alg_name]
    algorithm.set_sleep_time(args.sleep)
    algorithm.run()
    time_taken = algorithm.get_time_taken()
    update_caption(time_taken)


if __name__ == "__main__":
    main()
