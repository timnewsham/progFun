#!/usr/bin/env python3
"""
Parse, filter, process, print data from DLNR's shark incident page.
"""

import re
import time
from bs4 import BeautifulSoup

# wget -O shark-index.html https://dlnr.hawaii.gov/sharks/shark-incidents/incidents-list/
FN = 'shark-index.html'

# columns
DATETIME=0
LOCATION=1
ACTIVITY=2
WATERCLARITY=3
WATERDEPTH=4
VICTIM=5
DESCR=6
SHARK=7

def read_db():
    soup = BeautifulSoup(open(FN), "html.parser")
    rows = []
    for row in soup.find_all('tr'):
        r = [col.get_text() for col in row.find_all('td')]
        if r:
            rows.append(r)
    return rows

get_location = lambda r : r[LOCATION]
get_activity = lambda r : r[ACTIVITY]
get_descr = lambda r : r[DESCR]
get_shark = lambda r : r[SHARK]

def get_time(r):
    dt = r[DATETIME]
    dt = dt.replace('before ', '').replace('est. ', '').replace('approx ', '').replace('noon', 'pm').replace("p.m.", "pm").strip()

    #'1999/07/21, 10:25 am'
    t = time.strptime(dt, '%Y/%m/%d, %I:%M %p')
    return t

get_year = lambda r : get_time(r).tm_year
#get_mon = lambda r : get_time(r).tm_mon
get_mon = lambda r : time.strftime("%b", get_time(r))
get_mday = lambda r : get_time(r).tm_mday
#get_wday = lambda r : get_time(r).tm_wday
get_wday = lambda r : time.strftime("%a", get_time(r))
get_hour = lambda r : get_time(r).tm_hour

def get_sorted_wday(r):
    tm = get_time(r)
    name = time.strftime("%a", get_time(r))
    return f"{tm.tm_wday}_{name}"

def get_sorted_mon(r):
    tm = get_time(r)
    name = time.strftime("%b", get_time(r))
    return f"{tm.tm_mon:02d}_{name}"

def get_island(r):
    return r[LOCATION].split(', ')[0].replace("O‘ahu", "Oʻahu")

def get_town(r):
    t = r[LOCATION].split(', ')[1]
    if ';' in t:
        t = t.split(';')[0]
    t = t.replace('Makaha Beach', 'Mākaha Beach').replace('Hale‘iwa', 'Haleʻiwa')
    t = t.replace('Honokowai','Honokōwai')
    t = t.replace('Kanaha', 'Kanahā')
    t = t.replace('Pā‘ia Bay', 'Pāʻia Bay')
    t = t.replace('Kāʻanapali', 'Kā‘anapali')
    return t

def histo(db, f):
    ks = dict()
    for r in db:
        k = f(r)
        ks[k] = ks.get(k, 0) + 1
    return ks

def histoSorted(db, name, f):
    vs = [(n, k) for k,n in histo(db, f).items()]
    tot = sum(n for n,k in vs)
    vs.sort(reverse=True)
    print(name)
    for n,k in vs:
        perc = 100.0 * n / tot
        print(f"{n} {perc:.0f}%:\t{k}")
    print()

def histoByKey(db, name, f):
    ks = histo(db, f)
    tot = sum(ks.values())
    print(name)
    for k in sorted(ks):
        n = ks[k]
        perc = 100.0 * n / tot
        g = '*' * n
        kstr = str(k)
        print(f"{kstr:12s} {n:3d} {perc:2.0f}% {g}")
        #print(f"{k}\t{n:3d} {g}")
    print()

def times(db):
    for r in db:
        tm = get_time(r)
        t = time.mktime(tm)
        print(time.ctime(t))

def show(r):
    tm = get_time(r)
    t = time.mktime(tm)
    print(time.ctime(t), r[ACTIVITY], r[LOCATION], "depth", r[WATERDEPTH])

def oddTime(r):
    tm = get_time(r)
    return not (6 <= tm.tm_hour and tm.tm_hour <= 19)

def all(db):
    for r in db:
        show(r)
    print()

def filt(db, func):
    return list(filter(func, db))

def eq(select, targ):
    return lambda r : select(r) == targ

def like(select, pat):
    return lambda r : re.search(pat, select(r)) is not None

db = read_db()

#db = filt(db, eq(get_island, "Oʻahu"))
#db = filt(db, like(get_activity, "with sharks"))
#db = filt(db, eq(get_wday, "Wed"))
#db = filt(db, eq(get_mon, "Oct"))

all(db)

#histoSorted(db, "year", get_year)
#histoSorted(db, "month", get_sorted_mon)
#histoSorted(db, "mday", get_mday)
#histoSorted(db, "wday", get_sorted_wday)
#histoSorted(db, "hour", get_hour)
#histoSorted(db, "island", get_island)

histoByKey(db, "year", get_year)
histoByKey(db, "month", get_sorted_mon)
histoByKey(db, "mday", get_mday)
histoByKey(db, "wday", get_sorted_wday)
histoByKey(db, "hour", get_hour)
histoByKey(db, "island", get_island)
#histoByKey(db, "town", get_town)

