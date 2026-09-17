# ============================================================
# Runner — read test cases then run all solvers
# Authors: S. El Alaoui and ChatGPT 5
# ============================================================

import math
import json
import time

from solvers import *
from the3jugs import * 

"""
Runs all four algorithms on a test case 
and returns the results as a dictionary.

    ** Modify ** it to track the:
        execution time
    for each algorithm and add it to their respective 
    dictionaries (bt_res, bti_res, bfs_res and dfs_res)

"""
def run_case(case):
    capacities = case["capacities"]
    goal = case["goal"]

    problem = NJugsProblem(capacities=capacities, goal=goal)

    # Backtracking
    try:
        start_time = time.perf_counter()

        bt = BacktrackingSearch(problem)
        bt_res = bt.solve()

        end_time = time.perf_counter()
        bt_res["execution_time"] = end_time - start_time

    except RecursionError as e:
        print(f"Caught a RecursionError: {e}")

        bt_res = dict(
            best_cost=math.nan,
            best_path=[],
            found=False,
            expanded=0,
            execution_time=math.nan,
        )

    # Iterative Backtracking
    start_time = time.perf_counter()

    bti = BacktrackingSearchIterative(problem)
    bti_res = bti.solve()

    end_time = time.perf_counter()
    bti_res["execution_time"] = end_time - start_time

    # BFS
    start_time = time.perf_counter()

    bfs = BFSSearch(problem)
    bfs_res = bfs.solve()

    end_time = time.perf_counter()
    bfs_res["execution_time"] = end_time - start_time

    # DFS
    start_time = time.perf_counter()

    dfs = DFSSearch(problem)
    dfs_res = dfs.solve()

    end_time = time.perf_counter()
    dfs_res["execution_time"] = end_time - start_time

    return {
        "name": case.get("name", ""),
        "capacities": capacities,
        "start": [0, 0, 0],
        "goal": goal,
        "backtracking": bt_res,
        "backtrackingIter": bti_res,
        "bfs": bfs_res,
        "dfs": dfs_res,
    }

"""
Reads the results stored in ``res`` and prints them.

You MAY MODIFY it to also include:
    Execution time
    Branching factor (b)
    Maximum depth (D)
    Depth of shallowest solution (d)

Follow the same output formatting.
"""
def pretty_print_result(res, show_paths=False):
    print("=" * 70)
    print(f"Case: {res['name']}")
    print(f" Capacities: {res['capacities']}")
    print(f" Start:      {tuple(res['start'])}")
    print(f" Goal:       {tuple(res['goal'])}")

    for alg in ["backtracking", "backtrackingIter", "bfs", "dfs"]:
    # for alg in ["bfs"]:
        r = res[alg]
        status = "FOUND" if r["found"] else "NO SOLUTION"
        print(
            f"  [{alg.upper()}] {status} "
            f"| cost={r['best_cost']} "
            f"| expanded={r['expanded']} "
            f"| b={r.get('branching_factor', 'N/A')} "
            f"| D={r.get('max_depth', 'N/A')} "
            f"| d={r.get('solution_depth', 'N/A')}"
            f"| time={r.get('execution_time', 'N/A')}"
        )
        if show_paths and r["found"]:
            print(f"   Path length: {len(r['best_path'])-1}")
            print("   Path states:")
            for s in r["best_path"]:
                print(f"     {tuple(s)}")

"""
DO NOT MODIFY 

Reads test cases from the file: path 

Expected JSON structure:
[
  {"name":"case1","capacities":[...],"start":[...],"goal":[...]},
  ...
]

To add more test cases, edit ``test_cases.json`` and follow the correct formatting (valid JSON, no trailing commas).
"""
def read_cases_from_json(path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Basic validation
    cleaned = []
    for idx, case in enumerate(data, start=1):
        name = case.get("name", f"case_{idx}")
        caps = list(case["capacities"])
        goal = list(case["goal"])
        cleaned.append(dict(name=name, capacities=caps, goal=goal))
    return cleaned

"""
DO NOT MODIFY 

Reads test cases from a file, runs all configured search algorithms, and prints the results.

To add more test cases, edit ``test_cases.json`` and follow the correct formatting (valid JSON, no trailing commas).
"""
def main():
    
    tc_file = "test_cases.json"
    cases = read_cases_from_json(tc_file)
    
    results = []
    for case in cases:
        res = run_case(case)
        results.append(res)
        pretty_print_result(res)

    # Also write results to a JSON for programmatic grading if desired
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nWrote detailed results to results.json")

if __name__ == "__main__":
    main()
