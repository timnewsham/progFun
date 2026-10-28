#!/usr/bin/env python3
"""
See how many hands are needed to roll a yahtzee.
"""
import math
import os
from yahtzee import hand_wins, perc

def print_histogram(cnts):
    """Print a histogram of how many hands were required to roll a yahtzee."""
    tot = len(cnts)

    # count how many counts fall into each power-of-two bin.
    bins = [0 for _ in range(15)]
    for cnt in cnts:
        pow2 = int(math.log(cnt, 2))
        bins[pow2] += 1

    # display the non-empty power-of-two bin counts
    for pow2,cnt in enumerate(bins):
        lower = math.pow(2, pow2)
        upper = math.pow(2, pow2+1)
        if cnt:
            print(f"from {lower} to {upper-1}: {cnt} {perc(cnt, tot)}")

def simulate_run(noisy=False):
    """Simulate a run of yahtzee hands until a yahtzee is rolled, returning how many hands it took to get a yahtzee."""
    handnum = 0
    while True:
        handnum += 1
        if noisy:
            print(f"game {handnum}")
        if hand_wins(noisy=noisy):
            return handnum

def simulate_runs(N, noisy=False):
    """Run N simulations, playing yahtzee hands until a yahtzee is rolled."""
    cnts = []
    for n in range(N):
        handnum = simulate_run(noisy)
        cnts.append(handnum)
        if noisy:
            print(f"sim {n} got yahtzee in hand {handnum}")

    print_histogram(cnts)

if __name__ == '__main__':
    noisy = os.environ.get("NOISY") is not None
    simulate_runs(1000, noisy)
