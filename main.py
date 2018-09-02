import time
from numba import jit, int8, int64, prange
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
        if number > 1000000:
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


@jit(int64(int8, int64), nopython=True)
def calculate_results(switch, number):
    success = 0
    doors = np.array([1, 1, 0])
    if number > 1000000:
        iterations = number/1000000
        leftover = number % 1000000
        for x in prange(iterations):
            random_numbers = np.random.randint(0, high=3, size=1000000)
            for y in prange(1000000):
                np.random.shuffle(doors)
                choice = doors[random_numbers[y]]
                if switch == 0 and choice == 0:
                    success += 1
                if switch == 1 and choice == 1:
                    success += 1
        random_numbers = np.random.randint(0, high=3, size=leftover)
        for y in prange(leftover):
            np.random.shuffle(doors)
            choice = doors[random_numbers[y]]
            if switch == 0 and choice == 0:
                success += 1
            if switch == 1 and choice == 1:
                success += 1
    else:
        random_numbers = np.random.randint(0, high=3, size=number)
        for x in prange(number):
            np.random.shuffle(doors)
            choice = doors[random_numbers[x]]
            if switch == 0 and choice == 0:
                success += 1
            if switch == 1 and choice == 1:
                success += 1
    return success


if __name__ == "__main__":
    main()
