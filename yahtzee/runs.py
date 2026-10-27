#!/usr/bin/env python3
"""
Try to roll five of a kind in five dice.
"""
import math
from yahtzee import hand, perc

def stats(cnts):
    tot = len(cnts)

    # count how many counts fall into each power of two bin.
    bins = [0 for _ in range(15)]
    for cnt in cnts:
        bin = int(math.log(cnt, 2))
        bins[bin] += 1

    # display the non-empty bin counts
    for bin,cnt in enumerate(bins):
        lower = math.pow(2, bin)
        upper = math.pow(2, bin+1)
        if cnt:
            print(f"from {lower} to {upper-1}: {cnt} {perc(cnt, tot)}")

def simulate_runs(N, noisy=False):
    cnts = []
    for n in range(N):
        handnum = 0
        while True:
            handnum += 1
            if noisy:
                print(f"game {handnum}")
            if hand(noisy=noisy):
                break
        cnts.append(handnum)
        if noisy:
            print(f"sim {n} got yahtzee in hand {handnum}")
    stats(cnts)

if __name__ == '__main__':
    simulate_runs(1000)
