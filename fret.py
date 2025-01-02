#!/usr/bin/env python3
"""
Generate fretboard fingerings.

# Am on the guitar.
% ./fret.py -F 5 p1 min3 p5 
 5     3          
-o-|--|--|--|--||o 1=E
---|--|o-|--|--||o 2=A
---|--|--|o-|--||  3=D
-o-|--|--|o-|--||  4=G
-o-|--|--|--|o-||  5=B
-o-|--|--|--|--||o 6=E

# G on the ukulele
% ./fret.py -T "G C E A" -F 5 -t G p1 maj3 p5
 5     3          
---|o-|--|--|--||o 1=G
---|--|--|o-|--||  2=C
---|--|o-|--|--||  3=E
-o-|--|--|o-|--||  4=A

# C on open-D guitar
./fret.py  -T "D A D F# A D" -t C p1 maj3 p5
 12       9     7     5     3          
---|--|o-|--|--|--|--|o-|--|--|o-|--||  1=D
---|--|o-|--|--|o-|--|--|--|o-|--|--||  2=A
---|--|o-|--|--|--|--|o-|--|--|o-|--||  3=D
---|--|o-|--|--|--|o-|--|--|--|--|o-||  4=F#
---|--|o-|--|--|o-|--|--|--|o-|--|--||  5=A
---|--|o-|--|--|--|--|o-|--|--|o-|--||  6=D
"""

import argparse
import re
import sys

class Error(Exception):
    pass

def note(name):
    """
    return the half step corresponding to the note
    note: notes are noted in half steps starting with c = 0
    """
    name1 = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    name2 = ["c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "bb", "b"]
    l = name.lower()
    if l in name1:
        return name1.index(l)
    if l in name2:
        return name2.index(l)
    raise Error(f"unrecognized note {name}")

def interval(name):
    """return the number of half steps in an interval"""
    name1 = ["1", "min2", "maj2", "min3", "maj3", "p4", "aug4", "p5", "min6", "maj6", "min7", "maj7"]
    name2 = ["p1", "min2", "maj2", "aug2", "dim4", "aug3", "dim5", "dim6", "aug5", "dim7", "au6", "maj7"]

    m = re.match("^([a-z]*)([0-9]*)$", name)
    if m:
        pref = m.group(1)
        degree = int(m.group(2))
        norm = f"{pref.lower()}{degree % 8}"
        if norm in name1:
            return name1.index(norm)
        if norm in name2:
            return name2.index(norm)
    raise Error(f"unrecognized interval {name}")

def is_noteset(cur, notes):
    return any(note % 12 == cur % 12 for note in notes)


def genfretboard(tonic, notes, minfret, maxfret, tuning):
    for fret in range(maxfret, minfret-1, -1):
        x = fret % 12;
        if fret and fret % 12 in [0,3,5,7,9]:
            name = f"{fret}"
        else:
            name = ""
        print(f" {name:2s}", end="")
    print()

    for idx, string_name in enumerate(tuning):
        string = note(string_name)
        print("-", end="");
        for fret in range(maxfret, minfret-1, -1):
            x = is_noteset(string + fret, notes)
            if fret == 0:
                sym = 'o' if x else ' '
                print(f"|{sym}", end="")
            else:
                sym = 'o' if x else '-'
                print(f"{sym}-|", end="")
        print(f" {idx+1}={string_name}")

def main():
    p = argparse.ArgumentParser(prog=sys.argv[0], description="print a fretboard",
        epilog="tonic note is specified as a note, flat or sharp\nintervals are specified as maj, min, aug, dim or p <num>")
    p.add_argument("-t", "--tonic", default="A")
    p.add_argument("-f", "--minfret", type=int, default=0)
    p.add_argument("-F", "--maxfret", type=int, default=12)
    p.add_argument("-T", "--tuning", default="E A D G B E")
    p.add_argument("notes", nargs="*")
    opt = p.parse_args()

    tonic = note(opt.tonic)
    tuning = opt.tuning.split(' ')
    for n in tuning:
        note(n)
    notes = [tonic + interval(arg) for arg in opt.notes]
    genfretboard(tonic, notes, opt.minfret, opt.maxfret, tuning=tuning)

if __name__ == '__main__':
    main()
