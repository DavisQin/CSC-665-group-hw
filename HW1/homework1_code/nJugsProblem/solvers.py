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
        # Initialize the BFS search
        #self.problem is for NjugsProblem, which is a subclass of SearchProblem
        self.problem = problem
        #looking for minimum cost path and minium path, so we initialize best_cost to infinity and best_path to None
        self.best_cost = math.inf
        self.best_path = None
        self.frontier = deque()
        self.explored = set()
    def solve(self):
        # Initialize the BFS search
        start = self.problem.start_state()
        self.frontier.append((start, [], 0))
        self.explored.add(str(start))

        while self.frontier:
            #pop/explore the first element from the queue
            state, path, cost = self.frontier.popleft()

            # Goal check
            if self.problem.is_end(state):
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_path = path[:]  # copy
                continue

            # Expand
            for action in self.problem.actions(state):
                next_state = self.problem.succ(state, action)
                key = str(next_state)
                if key not in self.explored:
                    self.explored.add(key)
                    next_cost = cost + self.problem.cost(state, action)
                    self.frontier.append((next_state, path + [next_state], next_cost))

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
        self.first_cost = math.inf
        self.first_path = None
        self.frontier = []
        self.explored = set()

    def solve(self):
        start = self.problem.start_state()
        self.frontier.append((start, [], 0))
        self.explored.add(str(start))

        while self.frontier:
            #pop/explore the last element from the stack
            state, path, cost = self.frontier.pop()

            if self.problem.is_end(state):
                if cost < self.first_cost:
                    self.first_cost = cost
                    self.first_path = [self.problem.start_state()] + path
                return dict(
                    best_cost=self.first_cost,
                    best_path=self.first_path,
                    found=True,
                    expanded=len(self.explored),
                )

            for action in self.problem.actions(state):
                next_state = self.problem.succ(state, action)
                key = str(next_state)
                if key not in self.explored:
                    self.explored.add(key)
                    next_cost = cost + self.problem.cost(state, action)
                    self.frontier.append((next_state, path + [next_state], next_cost))



