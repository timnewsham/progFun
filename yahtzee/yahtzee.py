#!/usr/bin/env python3
"""
Try to roll five of a kind in five dice.
"""
import itertools
import secrets

def roll():
    """Roll one dice, picking a random value from 1 to 6."""
    return secrets.choice([1,2,3,4,5,6])

def rolln(N):
    """Roll N dice"""
    return [roll() for n in range(N)]

def reroll(keep):
    """Reroll keeps some dice and re-rolls the rest."""
    want = 5 - len(keep)
    #print("keep", keep, "reroll", want)
    return keep + rolln(want)

def strategy(dice):
    """Strategy: rank the dice into groups and keep the most matched dice, of the highest value."""
    # group same-value dice together
    grouped = [list(v) for k,v in itertools.groupby(sorted(dice))]

    # sort the longest group first, breaking ties with the group with the highest die value.
    ranked = sorted(grouped, key=lambda v: (len(v), v[0]), reverse=True)

    # keep the first one, the best one, with the longest group and highest value.
    return ranked[0]

def hand(noisy=False):
    """hand plays a yahtzee hand using strategy to pick which dice to keep, and returns true if a yahtzee was rolled."""
    keep = []
    for n in range(3):
        dice = reroll(keep)
        if noisy:
            print(f"roll {n} is {dice}")
        keep = strategy(dice)
    best = keep
    yahtzee = len(best) == 5
    #print("got", dice, "best", best, yahtzee)
    return yahtzee

def perc(n, m):
    """Return a percentage string for n of m."""
    p = 100.0 * n / m
    return f"{p:.1f}% ({n} of {m})"

def simulate_odds(CNT=10000):
    """simulate_odds plays CNT games and shows how often the strategy got a yahtzee."""
    cnt = sum(1 for _ in range(CNT) if hand())
    print(perc(cnt, CNT))

if __name__ == '__main__':
    simulate_odds()
