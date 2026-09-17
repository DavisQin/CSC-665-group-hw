# ============================================================
# Solvers — Backtracking (two different implementations)
#           Placeholder for BFS, DFS
# Authors: S. El Alaoui and ChatGPT 5
# ============================================================

import math
from collections import deque
import time

from the3jugs import *

"""
Depth-first backtracking with simple 'explored' pruning.
Stores the best (lowest-cost) path of states encountered to any goal.
This is a recursive implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored 
        
"""
class BacktrackingSearch:
    def __init__(self, problem: SearchProblem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def recurse(self, state, path, cost: int):
        if self.problem.is_end(state):
       
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_path = path[:]  # copy
                # print(self.best_cost)
            return

        for action in self.problem.actions(state):
            next_state = self.problem.succ(state, action)
            key = str(next_state)
            # key = next_state
            if key not in self.explored:
                
                self.explored.add(key)
                
                self.recurse(next_state, path + [next_state], cost + self.problem.cost(state, action))

    def solve(self):
        start = self.problem.start_state()
        self.explored.add(str(start))
        self.recurse(start, [], 0)
        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
        )

"""
Depth-first backtracking with simple 'explored' pruning (iterative).
Stores the best (lowest-cost) path of states encountered to any goal.
This is an iterative implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored

"""
class BacktrackingSearchIterative:
    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        start_key = str(start)
        self.explored.add(start_key)

        # Stack holds tuples: (state, path_from_after_start, cost_so_far)
        stack = [(start, [], 0)]

        while stack:
            state, path, cost = stack.pop()

            # Goal check
            if self.problem.is_end(state):
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_path = path[:]  # copy
                continue

            # Expand
            actions = list(self.problem.actions(state))
            # To match recursive DFS order, push in reverse so first action is explored first.
            for action in reversed(actions):
                next_state = self.problem.succ(state, action)
                key = str(next_state)
                if key not in self.explored:
                    self.explored.add(key)
                    next_cost = cost + self.problem.cost(state, action)
                    stack.append((next_state, path + [next_state], next_cost))

        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
        )


"""
Add an iterative implementation of DFS.
BFS explores nodes level by leveland is guaranteed to find a goal at minimum depth (the fewest steps).

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""
class BFSSearch:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()

        queue = deque()
        queue.append((start, [start], 0))

        explored = set()
        explored.add(start)

        total_children = 0
        expanded_nodes = 0
        max_depth = 0

        while queue:
            state, path, cost = queue.popleft()

            depth = len(path) - 1

            expanded_nodes += 1
            max_depth = max(max_depth, depth)

            # Goal check
            if self.problem.is_end(state):
                branching_factor = (
                    total_children / expanded_nodes
                    if expanded_nodes > 0
                    else 0
                )

                return {
                    "best_cost": cost,
                    "best_path": path,
                    "found": True,
                    "expanded": len(explored),
                    "branching_factor": branching_factor,
                    "max_depth": max_depth,
                    "solution_depth": depth
                }

            # Get all valid actions from this state
            actions = list(self.problem.actions(state))

            # Count all generated children for branching factor
            total_children += len(actions)

            for action in actions:
                next_state = self.problem.succ(state, action)

                if next_state not in explored:
                    explored.add(next_state)

                    queue.append((
                        next_state,
                        path + [next_state],
                        cost + self.problem.cost(state, action)
                    ))

        branching_factor = (
            total_children / expanded_nodes
            if expanded_nodes > 0
            else 0
        )

        return {
            "best_cost": math.inf,
            "best_path": [],
            "found": False,
            "expanded": len(explored),
            "branching_factor": branching_factor,
            "max_depth": max_depth,
            "solution_depth": None
        }

"""
Add an iterative implementation of DFS.
DFS explores along a path as deep as possible before backtracking 
and returns the first solution found, which may not be the shortest.

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""
class DFSSearch:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()

        stack = []
        stack.append((start, [start], 0))

        explored = set()
        explored.add(start)

        total_children = 0
        expanded_nodes = 0
        max_depth = 0

        # Keep track of solutions
        first_solution_path = None
        first_solution_cost = math.inf
        shallowest_solution_depth = math.inf

        while stack:
            state, path, cost = stack.pop()

            depth = len(path) - 1

            expanded_nodes += 1
            max_depth = max(max_depth, depth)

            # If this state is a goal
            if self.problem.is_end(state):

                # Save the first solution DFS finds
                if first_solution_path is None:
                    first_solution_path = path
                    first_solution_cost = cost

                # Track the shallowest goal encountered
                shallowest_solution_depth = min(
                    shallowest_solution_depth,
                    depth
                )

                # Do NOT return yet.
                # Continue searching to calculate D and d.
                continue

            actions = list(self.problem.actions(state))

            total_children += len(actions)

            for action in reversed(actions):
                next_state = self.problem.succ(state, action)

                if next_state not in explored:
                    explored.add(next_state)

                    stack.append((
                        next_state,
                        path + [next_state],
                        cost + self.problem.cost(state, action)
                    ))

        branching_factor = (
            total_children / expanded_nodes
            if expanded_nodes > 0
            else 0
        )

        if first_solution_path is not None:
            return {
                "best_cost": first_solution_cost,
                "best_path": first_solution_path,
                "found": True,
                "expanded": len(explored),
                "branching_factor": branching_factor,
                "max_depth": max_depth,
                "solution_depth": shallowest_solution_depth
            }

        return {
            "best_cost": math.inf,
            "best_path": [],
            "found": False,
            "expanded": len(explored),
            "branching_factor": branching_factor,
            "max_depth": max_depth,
            "solution_depth": None
        }



