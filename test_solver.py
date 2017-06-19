#!/usr/bin/env python


from copy import deepcopy
import heapq
import pytest


set1 = {
    "n_slots": 8,
    "sats": [
        {"hwid": "1000", "ra": 4.1, "slot": 0},
        {"hwid": "1001", "ra": 4.5, "slot": 0},
        {"hwid": "1002", "ra": 4.9, "slot": 0},
        {"hwid": "1003", "ra": 5.1, "slot": 0},
        {"hwid": "1004", "ra": 6.1, "slot": 0}
    ]
}
set1soln = {
    "n_slots": 8,
    "sats": [
        {"hwid": "1000", "ra": 4.1, "slot": 3},
        {"hwid": "1001", "ra": 4.5, "slot": 4},
        {"hwid": "1002", "ra": 4.9, "slot": 5},
        {"hwid": "1003", "ra": 5.1, "slot": 6},
        {"hwid": "1004", "ra": 6.1, "slot": 7}
    ]
}

set2 = {
    "n_slots": 15,
    "sats": [
        {"hwid": "1000", "ra": 0.5, "slot": 0},
        {"hwid": "1001", "ra": 1.1, "slot": 0},
        {"hwid": "1002", "ra": 2.10, "slot": 0},
        {"hwid": "1003", "ra": 2.11, "slot": 0},
        {"hwid": "1004", "ra": 2.12, "slot": 0},
        {"hwid": "1005", "ra": 14.9, "slot": 0}
    ]
}

testdata = [
    (set1,set1soln)
]




def closest(a, b):
    return a["slot"] - a["ra"] < b["slot"] - b["ra"]


def update_slots(pset):
    slots = [[] for _ in range(0, pset["n_slots"])]

    n_sats = len(pset["sats"])

    for sat in sorted(pset["sats"], closest):
        slots[sat["slot"]].append(sat)

    pset["slots"] = slots


def print_assignment(pset):
    score = sum([1 for strip in pset["slots"] if strip])
    pset = deepcopy(pset)
    seen_sats = 0
    sum_err = 0.0
    while seen_sats < len(pset["sats"]):
        for slot in pset["slots"]:
            if slot:
                sat = slot.pop()
                sum_err += sat_err(sat, pset["n_slots"])
                print "| {hwid}".format(hwid=sat["hwid"]),
                seen_sats += 1
            else:
                print "| ----",
        print "|"
    print "sum_err:", sum_err
    print "strips:", score


def sat_err(sat, n_slots):
    return min(
        abs(sat["slot"] - sat["ra"]),
        abs(sat["slot"] - (n_slots - sat["ra"]))
    )


def sum_err(pset, n_slots):
    return sum([sat_err(sat, n_slots) for sat in pset["sats"]])

def print_angles(pset):
    pset = deepcopy(pset)
    seen_sats = 0
    while seen_sats < len(pset["sats"]):
        for slot in pset["slots"]:
            if slot:
                sat = slot.pop()
                print "| {angle}".format(angle=round(sat["ra"],2)),
                seen_sats += 1
            else:
                print "| ----",
        print "|"


def print_errors(pset):
    pset = deepcopy(pset)
    seen_sats = 0
    while seen_sats < len(pset["sats"]):
        for slot in pset["slots"]:
            if slot:
                sat = slot.pop()
                print "| {err}".format(err=sat_err(sat, pset["n_slots"])),
                seen_sats += 1
            else:
                print "| ----",
        print "|"


def first_assign(pset):
    for sat in pset["sats"]:
        sat["slot"] = int(round(sat["ra"])) % pset["n_slots"]

def assign_simple(pset):
    n_slots = pset["n_slots"]
    slots = [[] for _ in range(0, n_slots)]
    depth = [0 for _ in range(0, n_slots)]

    n_sats = len(pset["sats"])

    first_assign(pset)

    heap = []
    for sat in pset["sats"]:
        heapq.heappush(
            heap,
            min(
                (abs(sat["slot"] - sat["ra"]), sat),
                (abs(sat["slot"] - (n_slots - sat["ra"])), sat)
            )
        )

    last_err = 0
    while True:
        try:
            closest = heapq.heappop(heap)
            print closest
            distance, sat = closest
            slot = sat["slot"]
            if not slots[slot]:
                slots[slot].append(sat)
            else:
                next_slot = slot + 1 % n_slots
                prev_slot = (slot + n_slots - 1) % n_slots

                if sat["ra"] > slots[slot][0]["ra"]:
                    sat["slot"] = next_slot
                    sat["ra"] += 0.001
                elif sat["ra"] < slots[slot][0]["ra"]:
                    sat["slot"] = prev_slot
                    sat["ra"] -= 0.001
                else:
                    continue
                    sat["slot"] = next_slot
                    sat["ra"] += 0.001
                heapq.heappush(heap, (sat_err(sat, n_slots), sat))

        except IndexError:
            break
        update_slots(pset)
        print_assignment(pset)


def siman_solver(pset):
    pass


def linear_programming_solver(pset):
    pass


def sat_dist(sat, slot, n_slots):
    return min(
        abs(slot - sat["ra"]),
        abs(slot - (n_slots - sat["ra"]))
    )


def rank_solver(pset):
    # set up data structures
    n_slots = pset["n_slots"]
    slots = [[] for _ in range(0, n_slots)]

    # populate each slot with heap sorted by distance from slot
    for i, slot in enumerate(slots):
        for sat in sats:
            distance = sat_dist(sat, slot, n_slots)
            if distance < 2:
                # meets constraint
                heapq.heappush(slot, (distance, sat))

    # sort satellites by worst global ranking, and start assignment
    sat_rank = {}
    for sat in sats:
       # 
    


def slots(pset):
    return {sat["hwid"]: sat["slot"] for sat in pset["sats"]}


@pytest.mark.parametrize("problem,solution", testdata)
def test_rounding_solver(problem, solution):
    first_assign(problem)
    assert slots(problem) == slots(solution)



#tset = set1
#
#update_slots(tset)
#print_assignment(tset)
#
#print "*"*80
#assign_simple(tset)
#print "*"*80
#
#print_assignment(tset)
#print_angles(tset)
#print_errors(tset)
#
