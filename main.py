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
                number = int(input("How many times should the simulation be run? (max = 100,000,000)"))
                if number > 100000000:
                    print("Number is too large! Please enter a smaller value!")
                    continue
                elif number < 1:
                    print("Number is too small! Please enter a larger value!")
                    continue
                break
            except ValueError:
                print("Please enter an integer value!")
        start = time.perf_counter()
        door1 = 0
        door2 = 1
        door3 = 1
        success = calculate_results(door1, door2, door3, switch, number)
        end = time.perf_counter() - start
        percentage = (float(success)/float(number))*100
        print("The simulation was run a total of {0} times and was completed in {1} seconds.".format(str(number),
                                                                                                     str(end)))
        print("This strategy has a " + str(percentage) + "% win rate.")
        while True:
            play_again = input("Would you like to play again (y/n)?")
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


@jit(int64(int8, int8, int8, int8, int64), nopython=True)
def calculate_results(door1, door2, door3, switch, number):
    success = 0
    random_numbers = np.random.randint(0, high=3, size=number)
    for x in prange(number):
        num = random_numbers[x]
        if num == 0:
            choice = door1
        elif num == 1:
            choice = door2
        else:
            choice = door3
        if switch == 0 and choice == 0:
            success += 1
        if switch == 1 and choice == 1:
            success += 1
    return success


if __name__ == "__main__":
    main()
