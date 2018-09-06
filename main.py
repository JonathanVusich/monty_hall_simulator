import time
from numba import jit, int8, int64, int32, prange, vectorize
import numpy as np

"""
This project simulates the Monty Hall door problem in code.
It allows the user to select the strategy and the number of
iterations to simulate. Results are printed after the simulation
has been completed.
"""


def main():
    while True:
        while True:
            switch = input("Should the player switch (y/n)?")
            if switch.lower() == "y" or switch.lower() == "yes":
                switch = 1
                break
            elif switch.lower() == "n" or switch.lower() == "no":
                switch = 0
                break
            else:
                print("Not a valid choice!")
        while True:
            try:
                number = int(input("How many times should the simulation be run?"))
                break
            except ValueError:
                print("Please enter an integer value!")
        if number > 100000000:
            start = time.perf_counter()
            success = calculate_results(switch, 1000000)
            benchmark = time.perf_counter() - start
            iterations = number/1000000.0
            confirm = input("Estimated time to run this simulation is {} seconds. "
                            "Are you sure you want to continue (y/n)?".format(str(iterations*benchmark)))
            if not confirm.lower() == "y" and not confirm.lower() == "yes":
                continue
        print("Starting...")
        start = time.perf_counter()
        success = calculate_results(switch, number)
        end = time.perf_counter() - start
        percentage = (float(success)/float(number))*100
        print("The simulation was run a total of {0} times and was completed in {1} seconds.".format(str(number),
                                                                                                     str(end)))
        print("This strategy has a " + str(percentage) + "% win rate.")
        while True:
            play_again = input("Would you like to run the simulation again (y/n)?")
            if play_again.lower() == "y" or play_again.lower() == "yes":
                play_again = True
                break
            elif play_again.lower() == "n" or play_again.lower() == "no":
                play_again = False
                break
            else:
                print("Not a valid choice!")
        if not play_again:
            break


def calculate_results(switch, number):
    success = 0
    if number > 10000000:
        iterations = int(number/10000000)
        leftover = number % 10000000
        for x in range(iterations):
            if switch == 1:
                success += switch_results(10000000)
            else:
                success += noswitch_results(10000000)
        if switch == 1:
            success += switch_results(leftover)
        else:
            success += noswitch_results(leftover)
    else:
        if switch == 1:
            success += switch_results(number)
        else:
            success += noswitch_results(number)
    return success


@jit(int64(int64), nopython=True, parallel=True)
def switch_results(number):
    success = 0
    doors = np.reshape(np.array([1, 1, 0, 1, 0, 1, 0, 1, 1]), (3, 3))
    door_set = np.random.randint(0, high=3, size=number)
    door_choices = np.random.randint(0, high=3, size=number)
    for x in prange(number):
        if doors[door_set[x], door_choices[x]] == 1:
            success += 1
    return success


@jit(int64(int64), nopython=True, parallel=True)
def noswitch_results(number):
    success = 0
    doors = np.reshape(np.array([1, 1, 0, 1, 0, 1, 0, 1, 1]), (3, 3))
    door_set = np.random.randint(0, high=3, size=number)
    door_choices = np.random.randint(0, high=3, size=number)
    for x in prange(number):
        if doors[door_set[x], door_choices[x]] == 0:
            success += 1
    return success


if __name__ == "__main__":
    main()
