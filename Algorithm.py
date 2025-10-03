from queue import Queue, PriorityQueue
from tkinter import *
import numpy as np
import random

N = 8

# ======================
# Thuật toán chung
# ======================
def check_queens(state, col):
    row = len(state)
    for r in range(row):
        c = state[r]
        if c == col or abs(r - row) == abs(c - col):
            return False
    return True

def reconstruct_path(parent, state_tuple):
    path = []
    s = state_tuple
    while s is not None:
        path.append(list(s))
        s = parent.get(s)
    return path[::-1]

# ======================
# Mobility / cost functions
# ======================
def occupied_positions(state):
    return {(r, c) for r, c in enumerate(state)}

DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

def mobility_of_queen(state, row, col):
    occ = occupied_positions(state)
    count = 0
    for dr, dc in DIRECTIONS:
        r, c = row+dr, col+dc
        while 0 <= r < N and 0 <= c < N:
            if (r, c) in occ:
                break
            count += 1
            r += dr
            c += dc
    return count

def cost_of_state(state):
    total = 0
    for r, c in enumerate(state):
        total += mobility_of_queen(state, r, c)
    return total

# ======================
# Cost function for Informed (Heuristic) Search Strategies
# ====================== 
GOAL_STATE = [1, 3, 5, 7, 2, 0, 6, 4]
def is_goal(state):
    global GOAL_STATE
    return state == GOAL_STATE

def heuristic(state):
    total = 0
    for row in range(len(state)):
        total += abs(state[row] - GOAL_STATE[row])
    
    return total

# ======================
# Greedy best first search
# ======================
def greedy_best_first_search():
    global N
    start = []
    frontier = PriorityQueue()
    frontier.put((heuristic(start), start))
    parent = {tuple(start): None}

    while not frontier.empty():
        h_val, state = frontier.get()

        if is_goal(state):
            return reconstruct_path(parent, tuple(state))
        
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = tuple(state)
                    frontier.put((heuristic(new_state), new_state))

    return []

# ======================
# DLS (Depth - limited search) and Iterative deepening search
# ======================
def iterative_deepening_search(N):
    for depth in range(N + 1):
        result = depth_limited_search(N, depth)
        if result != "cutoff":
            return result

def depth_limited_search(N, limit):
    start = []
    parent = {tuple(start): None}
    return recursive_DLS(start, parent, N, limit)

def recursive_DLS(state, parent, N, limit):
    if len(state) == N:
        return [reconstruct_path(parent, tuple(state))]
    elif limit == 0:
        return "cutoff"
    else:
        cutoff_occurred = False
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = tuple(state)
                result = recursive_DLS(new_state, parent, N, limit - 1)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result != "failure":
                    return result 
        if cutoff_occurred:
            return "cutoff"
        else:
            return "failure"

# ======================
# UCS (Uniform - cost search)
# ======================
def uniform_cost_search(N):
    start = []
    frontier = PriorityQueue()
    frontier.put((cost_of_state(start), start))
    parent = {tuple(start): None}
    cost_so_far = {tuple(start): cost_of_state(start)}

    while not frontier.empty():
        path_cost, state = frontier.get()
        tstate = tuple(state)
        if cost_so_far.get(tstate) != path_cost:
            continue
        if len(state) == N:
            return [reconstruct_path(parent, tstate)], cost_so_far
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                new_cost = cost_of_state(new_state)
                tnew = tuple(new_state)
                if tnew not in cost_so_far or new_cost < cost_so_far[tnew]:
                    cost_so_far[tnew] = new_cost
                    parent[tnew] = tstate
                    frontier.put((new_cost, new_state))
    return [], cost_so_far

# ======================
# DFS / BFS
# ======================
def dfs_queens(N):
    stack = [[]]
    parent = {tuple([]): None}
    while stack:
        state = stack.pop()
        tstate = tuple(state)
        if len(state) == N:
            return [reconstruct_path(parent, tstate)]
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                if tnew not in parent:
                    parent[tnew] = tstate
                    stack.append(new_state)
    return []

def bfs_queens(N):
    def actions(state): return [col for col in range(N) if check_queens(state, col)]
    def child_node(state, action): return state + [action]
    node = []
    frontier = Queue()
    frontier.put(node)
    parent = {tuple(node): None}
    while not frontier.empty():
        state = frontier.get()
        for action in actions(state):
            child = child_node(state, action)
            tchild = tuple(child)
            if tchild not in parent:
                parent[tchild] = tuple(state)
                if len(child) == N:
                    return [reconstruct_path(parent, tchild)]
                frontier.put(child)
    return []

# ======================
# A* Search
# ======================
def astar_search(N):
    start = []
    frontier = PriorityQueue()
    g_start = cost_of_state(start)
    f_start = g_start + heuristic(start)
    frontier.put((f_start, g_start, start))
    parent = {tuple(start): None}
    cost_so_far = {tuple(start): g_start}

    while not frontier.empty():
        f_val, g_val, state = frontier.get()
        tstate = tuple(state)
        if cost_so_far.get(tstate, None) != g_val:
            continue

        if len(state) == N:
            return reconstruct_path(parent, tstate), cost_so_far

        # Expand
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                new_g = cost_of_state(new_state)
                if tnew not in cost_so_far or new_g < cost_so_far[tnew]:
                    cost_so_far[tnew] = new_g
                    parent[tnew] = tstate
                    new_f = new_g + heuristic(new_state)
                    frontier.put((new_f, new_g, new_state))

    return [], cost_so_far

# ======================
# Hill-climbing search
# ======================
def heuristic_conflict(state):
    n = len(state)
    result = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                result += 1
    return result

def generator_state(state):
    successors = []
    
    for r in range(N):
        for c in range(N):
            if state[r] != c:
                new_state = state.copy()
                new_state[r] = c
                successors.append(new_state)

    return successors

def hillClimbing_search():
    current_state = np.random.choice(np.arange(0, N), size=N, replace=False)
    current_heuristic = heuristic_conflict(current_state)

    while True:
        successors = generator_state(current_state)
        best_state = min(successors, key=heuristic_conflict)
        best_heuristic = heuristic_conflict(best_state)

        if best_heuristic >= current_heuristic:
            break

        current_state = best_state
        current_heuristic = best_heuristic
        if current_heuristic == 0:
            break
    
    return current_state, current_heuristic


# ======================
# Simulated Annealing
# ======================
def simulated_annealing():
    T = 1
    cooling = 0.95
    current_state = np.random.choice(np.arange(0, N), size=N, replace=False).tolist()
    current_heuristic = heuristic_conflict(current_state)

    while T > 1e-6:
        if current_heuristic == 0:
            return current_state, current_heuristic
        
        successors = generator_state(current_state)

        next_state = random.choice(successors)
        next_heuristic = heuristic_conflict(next_state)

        deltaE = next_heuristic - current_heuristic

        if deltaE < 0:
            current_state, current_heuristic = next_state, next_heuristic
        else:
            p = np.exp(-deltaE / T)
            if random.random() < p:
                current_state, current_heuristic = next_state, next_heuristic

        T *= cooling

    return current_state, current_heuristic

# ======================
# Local Beam Search
# ======================
def local_beam_search(max_iters=1000):
    k = 8
    beam = []
    
    for _ in range(k):
        state = np.random.choice(np.arange(0, N), size=N, replace=False)
        beam.append(state)

    best_overall = None
    best_h = float('inf')

    for _ in range(max_iters):
        new_beam = []

        for state in beam:
            successors = generator_state(state)
            if not successors:
                continue
            best_child = min(successors, key=heuristic_conflict)
            h = heuristic_conflict(best_child)

            if h == 0:
                return best_child, 0

            new_beam.append(best_child)
            if h < best_h:
                best_h = h
                best_overall = best_child.copy()

        if len(new_beam) >= k:
            beam = new_beam[:k]
            continue

        candidates = []
        for state in beam:
            candidates.extend(generator_state(state))

        candidates = [c for c in candidates if c not in new_beam]

        candidates.sort(key=lambda st: heuristic_conflict(st))
        need = k - len(new_beam)
        new_beam.extend(candidates[:need])

        beam = new_beam

    return best_overall, best_h

# ======================
# Genetic Algorithm
# ======================
def generate_population(size):
    population = []
    for _ in range(size):
        state = np.random.choice(range(N), size=N, replace=False)
        population.append(state)
    return population

def select_parents(population, fitnesses):
    probs = [1/(1 + f) for f in fitnesses]
    parents = random.choices(population, weights=probs, k=2)
    return parents

def crossover(parent1, parent2):
    parent1 = parent1.tolist() if isinstance(parent1, np.ndarray) else parent1
    parent2 = parent2.tolist() if isinstance(parent2, np.ndarray) else parent2
    point = random.randint(1, N-1)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(state, mutation_rate=0.1):
    new_state = state.copy()
    for i in range(N):
        if random.random() < mutation_rate:
            new_state[i] = random.randint(0, N-1)
    return new_state

def genetic_algorithm(pop_size=20, max_generations=1000):
    population = generate_population(pop_size)
    
    best_state = None
    best_fit = float('inf')

    for gen in range(max_generations):
        fitnesses = [heuristic_conflict(ind) for ind in population]

        if min(fitnesses) == 0:
            best_index = fitnesses.index(0)
            return population[best_index], 0

        new_population = []

        while len(new_population) < pop_size:
            p1, p2 = select_parents(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate=0.1)
            new_population.append(child)

        population = new_population

        min_fit = min(fitnesses)
        if min_fit < best_fit:
            best_fit = min_fit
            best_state = population[fitnesses.index(min_fit)]

    return best_state, best_fit


# ======================
# AND OR SEARCH
# ======================
def actions(state):
    return [col for col in range(N) if check_queens(state, col)]

def result(state, col):
    return state + [col]

def AND_OR_SEARCH(start, goal):
    return OR_SEARCH(start, goal, path=[])

def OR_SEARCH(state, goal, path):
    if state == goal:
        return state, [state] 
    if state in path:
        return "failure", []

    for action in actions(state):
        result_state = result(state, action)
        solution, subpath = AND_SEARCH([result_state], goal, path + [state])
        if solution != "failure":
            return solution, [state] + subpath
    return "failure", []

def AND_SEARCH(states, goal, path):
    plans = []
    for s in states:
        solution, subpath = OR_SEARCH(s, goal, path)
        if solution == "failure":
            return "failure", []
        plans.extend(subpath)  
    return solution, plans

# ======================
# Searching with No Observation
# ======================
def sensorless_search_queens():
    start_belief = tuple([()])  
    frontier = Queue()
    frontier.put(start_belief)

    parent = {start_belief: None}
    action_parent = {start_belief: None}

    N = 8
    def isGoal(state, N):
        return len(state) == N

    while not frontier.empty():
        belief = frontier.get()

        if all(isGoal(s, N) for s in belief):
            path = []
            b = belief
            while b is not None:
                a = action_parent[b]
                if a is not None:
                    path.append(a)
                b = parent[b]
            return path[::-1], belief

        for col in range(N):
            new_belief = []
            for s in belief:
                if check_queens(s, col):
                    new_belief.append(s + (col,))
            if new_belief:
                new_belief = tuple(new_belief)
                if new_belief not in parent:
                    parent[new_belief] = belief
                    action_parent[new_belief] = col
                    frontier.put(new_belief)

    return [], ()

# ======================
# Searching with partial Observation
# ======================
def partial_observable_search_queens():
    initial_state = [4]

    start_belief = tuple([tuple(initial_state)]) 
    frontier = Queue()
    frontier.put(start_belief)

    parent = {start_belief: None}
    action_parent = {start_belief: None}

    def isGoal(state):
        return len(state) == N

    while not frontier.empty():
        belief = frontier.get()

        if all(isGoal(s) for s in belief):
            b = belief
            path = []
            while b is not None:
                path.append(list(b))
                b = parent[b]
            return path[::-1], belief  

        for col in range(N):
            new_belief = []
            for s in belief:
                if len(s) < N and check_queens(s, col):
                    candidate = s + (col,)
                    new_belief.append(candidate)

            if new_belief:
                new_belief = tuple(new_belief)
                if new_belief not in parent:
                    parent[new_belief] = belief
                    action_parent[new_belief] = col
                    frontier.put(new_belief)

    return [], () 

# ======================
# Backtracking Search
# ======================
def backtracking_search(N):
    def backtrack(state, parent):
        if len(state) == N:
            return [reconstruct_path(parent, tuple(state))]

        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                if tnew not in parent:
                    parent[tnew] = tuple(state)
                result = backtrack(new_state, parent)
                if result is not None:  
                    return result
        return None 

    start = []
    parent = {tuple(start): None}
    return backtrack(start, parent)

# ======================
# Forward Checking Search
# ======================
def forward_checking_search(N):
    def forward_check(state, domains, parent):
        if len(state) == N:
            return reconstruct_path(parent, tuple(state))

        row = len(state)
        for col in domains[row]:
            new_state = state + [col]

            new_domains = [d.copy() for d in domains]

            consistent = True
            for r in range(row + 1, N):
                new_domains[r] -= {col, col + (r - row), col - (r - row)}
                if not new_domains[r]:
                    consistent = False
                    break

            if consistent:
                tnew = tuple(new_state)
                if tnew not in parent:
                    parent[tnew] = tuple(state)
                result = forward_check(new_state, new_domains, parent)
                if result is not None:
                    return result

        return None

    domains = [set(range(N)) for _ in range(N)]
    start = []
    parent = {tuple(start): None}
    return forward_check(start, domains, parent)