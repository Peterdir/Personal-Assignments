# ======================
# Import
# ======================
from queue import Queue, PriorityQueue
from tkinter import *
import os
import math
import numpy as np
from Algorithm import *
from PIL import Image, ImageTk

# ======================
# Khởi tạo Tkinter
# ======================
root = Tk()
root.geometry("1300x820+10+10")
root.title("Cờ vua")

top_frame = Frame(root, bg="white")
top_frame.pack(side=TOP, fill="both", expand=False, padx=10, pady=(10,5))

C1 = Canvas(top_frame, bg="white", height=540, width=540)
C1.pack(side=LEFT, padx=(50,10), pady=10)

C2 = Canvas(top_frame, bg="white", height=540, width=540)
C2.pack(side=LEFT, padx=(10,50), pady=10)

btn_frame = Frame(root, bg="white")
btn_frame.pack(side=TOP, pady=10, fill="x", padx=10)

# ======================
# Biến toàn cục
# ======================
size = 62.5
N = 8
offset = 30
size_col = 10
current_path = []
current_index = 0
cost_map = {}  # Lưu chi phí
is_running = False
current_algo = None

# Thời gian giữa các bước chạy trên C!
step_delay = 1
dfs_gen = None 
bfs_gen = None
ucs_gen = None
dls_gen = None
ids_gen = None
andor_gen = None
gbfs_gen = None
astar_gen = None
Hill_gen = None
sa_gen = None
localBeam_gen = None
genetic_gen = None
sensorless_gen = None
partial_obs_gen = None

# ======================
# Hàm vẽ bàn cờ & tiện ích
# ======================
def clear_queens():
    global current_path, current_index, is_running, cost_map, current_algo
    is_running = False
    current_path = []
    current_index = 0
    cost_map = {}
    current_algo = None

    C1.delete("all")
    draw_labels(C1)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C1.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    cost_label.config(text="")

    C2.delete("all")
    draw_labels(C2)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C2.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    cost_label.config(text="")

def draw_labels(canvas):
    cols = ['1','2','3','4','5','6','7','8']
    rows = ['A','B','C','D','E','F','G','H']
    for i in range(N):
        y = size * i + size / 2
        canvas.create_text(size_col, y, text=cols[i], font=("Arial", 12, "bold"))
    for i in range(N):
        x = size * i + offset + size / 2
        canvas.create_text(x, N * size + 15, text=rows[i], font=("Arial", 12, "bold"))

def table_initial():
    C1.delete("all")
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C1.create_rectangle(x1, y1, x2, y2, fill=color)


def table_operator():
    C2.delete("all")
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C2.create_rectangle(x1, y1, x2, y2, fill=color)



# ======================
# Generator
# ======================
def dfs_generator(N):
    stack = [[]]  # bắt đầu từ trạng thái rỗng
    parent = {tuple([]): None}
    while stack:
        state = stack.pop()
        yield ("visit", state)  # báo là đang thăm trạng thái này
        if len(state) == N:  # nếu tìm thấy lời giải
            yield ("found", tuple(state), parent)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = (state)
                    stack.append(new_state)
                    yield ("push", new_state)  # báo là thêm trạng thái mới vào stack

def bfs_generator(N):
    q = Queue()
    q.put([])
    parent = {tuple([]): None}
    while not q.empty():
        state = q.get()
        yield ("visit", state)
        if len(state) == N:
            yield ("found", tuple(state), parent)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = (state)
                    q.put(new_state)
                    yield ("push", new_state)

def ucs_generator(N):
    pq = PriorityQueue()
    pq.put((0, []))

    parent = {tuple([]): None}
    cost_map = {tuple([]): 0}

    while not pq.empty():
        cost, state = pq.get()
        yield ("visit", state, cost)
        if len(state) == N:
            yield ("found", state, parent, cost_map)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                new_cost = cost_of_state(new_state)
                t_new_state = tuple(new_state)
                if t_new_state not in cost_map or new_cost < cost_map[t_new_state]:
                    parent[t_new_state] = tuple(state)
                    cost_map[t_new_state] = new_cost
                    pq.put((new_cost, new_state))
                    yield ("push", new_state, new_cost)

def dls_generator(N, limit):
    stack = [([], 0)]
    parent = {tuple([]): None}

    while stack:
        state, depth = stack.pop()
        yield("visit", state)
        if len(state) == N:
            yield("found", tuple(state), parent)
            return
        
        if depth < limit:
            for col in range(N):
                if check_queens(state, col):
                    new_state = state + [col]
                    if tuple(new_state) not in parent:
                        parent[tuple(new_state)] = tuple(state)
                        stack.append((new_state, depth + 1))
                        yield("push", new_state)

def ids_generator(N):
    for limit in range(1, N+1):
        stack = [([], 0)]
        parent = {tuple([]): None}  # khởi tạo lại cho mỗi depth
        while stack:
            state, depth = stack.pop()
            yield ("visit", state)
            if len(state) == N:
                yield ("found", tuple(state), parent)
                return
            if depth < limit:
                for col in range(N):
                    if check_queens(state, col):
                        new_state = state + [col]
                        t_new_state = tuple(new_state)
                        if t_new_state not in parent:
                            parent[t_new_state] = tuple(state)
                            stack.append((new_state, depth + 1))
                            yield ("push", new_state)

def andor_generator(N):
    parent = {tuple([]): None}

    def or_search(state, path):
        yield ("visit", state)
        if state == GOAL_STATE:
            yield ("found", tuple(state), parent)
            return True

        if tuple(state) in path:
            return False

        for action in actions(state):
            new_state = result(state, action)
            tnew = tuple(new_state)
            if tnew not in parent:
                parent[tnew] = tuple(state)
                yield ("push", new_state)
                ok = yield from and_search([new_state], path + [tuple(state)])
                if ok:
                    return True
        return False

    def and_search(states, path):
        for s in states:
            ok = yield from or_search(s, path)
            if not ok:
                return False
        return True

    yield from or_search([], [])

def gbfs_generator(N):
    pq = PriorityQueue()
    start = []
    pq.put((heuristic(start), start))
    parent = {tuple([]): None}

    while not pq.empty():
        h_val, state = pq.get()
        yield ("visit", state, h_val)  # đang thăm
        if len(state) == N:
            yield ("found", state, parent)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                t_new_state = tuple(new_state)
                if t_new_state not in parent:
                    parent[t_new_state] = tuple(state)
                    pq.put((heuristic(new_state), new_state))
                    yield ("push", new_state, heuristic(new_state))

def astar_generator(N):
    pq = PriorityQueue()
    start = []
    pq.put((heuristic(start), 0, start))
    parent = {tuple([]): None}
    cost_map = {tuple([]): 0}

    while not pq.empty():
        f_val, g_val, state = pq.get()
        yield ("visit", state, g_val, f_val)
        if len(state) == N:
            yield ("found", state, parent, cost_map)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                g_new = g_val + cost_of_state(new_state)
                f_new = g_new + heuristic(new_state)
                t_new_state = tuple(new_state)
                if t_new_state not in cost_map or g_new < cost_map[t_new_state]:
                    parent[t_new_state] = tuple(state)
                    cost_map[t_new_state] = g_new
                    pq.put((f_new, g_new, new_state))
                    yield ("push", new_state, g_new, f_new)

def hill_generator(N):
    state = np.random.permutation(N).tolist()  
    yield ("visit", state)
    
    while True:
        neighbors = []
        for i in range(N):
            for j in range(N):
                if j != state[i]:
                    new_state = state.copy()
                    new_state[i] = j
                    neighbors.append(new_state)
        
        current_cost = heuristic(state)
        neighbors.sort(key=lambda x: heuristic(x))
        best_neighbor = neighbors[0]
        best_cost = heuristic(best_neighbor)
        
        if best_cost >= current_cost: 
            yield ("found", state, best_cost)
            return
        
        state = best_neighbor
        yield ("visit", state)

def sa_generator(N, T_init=1000, alpha=0.95, steps=1000):
    state = np.random.permutation(N).tolist()
    T = T_init
    yield ("visit", state, heuristic(state))
    
    for _ in range(steps):
        if heuristic(state) == 0:
            yield ("found", state, 0)
            return
        
        i, j = np.random.randint(0, N, 2)
        while j == state[i]:
            j = np.random.randint(0, N)
        new_state = state.copy()
        new_state[i] = j
        
        delta = heuristic(new_state) - heuristic(state)
        if delta < 0 or np.random.rand() < np.exp(-delta / T):
            state = new_state
            yield ("visit", state, heuristic(state))
        
        T *= alpha
    
    yield ("found", state, heuristic(state))

def local_beam_generator(N, k=3, max_iters=1000):
    beam = [np.random.randint(0, N, N).tolist() for _ in range(k)]
    
    for _ in range(max_iters):
        for state in beam:
            if heuristic(state) == 0:
                yield ("found", state)
                return
        
        yield ("visit", beam.copy()) 
        
        successors = []
        for state in beam:
            for i in range(N):
                for j in range(N):
                    if j != state[i]:
                        new_state = state.copy()
                        new_state[i] = j
                        successors.append(new_state)
        
        if not successors:
            break
        
        successors.sort(key=heuristic)
        beam = successors[:k]
    
    best_state = min(beam, key=heuristic)
    yield ("found", best_state)

def genetic_generator(N, pop_size=20, max_generations=1000, mutation_rate=0.1):
    population = generate_population(pop_size)
    
    best_state = None
    best_fit = float('inf')
    
    for gen in range(max_generations):
        fitnesses = [heuristic_conflict(ind) for ind in population]

        min_idx = fitnesses.index(min(fitnesses))
        yield ("visit", population[min_idx], fitnesses[min_idx])

        if 0 in fitnesses:
            best_index = fitnesses.index(0)
            yield ("found", population[best_index], 0)
            return

        new_population = []
        while len(new_population) < pop_size:
            p1, p2 = select_parents(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        min_fit = min(fitnesses)
        if min_fit < best_fit:
            best_fit = min_fit
            best_state = population[fitnesses.index(min_fit)]
    
    yield ("found", best_state, best_fit)

def sensorless_generator(N=8):
    start_belief = tuple([()])  
    frontier = Queue()
    frontier.put(start_belief)

    parent = {start_belief: None}
    action_parent = {start_belief: None}

    def isGoal(state, N):
        return len(state) == N

    while not frontier.empty():
        belief = frontier.get()
        yield ("visit", belief)  

        if all(isGoal(s, N) for s in belief):
            path = []
            b = belief
            while b is not None:
                a = action_parent[b]
                if a is not None:
                    path.append(a)
                b = parent[b]
            yield ("found", path[::-1], belief)
            return

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
                    yield ("push", new_belief, col)  

    yield ("notfound", [], ())

def partial_observation_generator(N=8):
    initial_state=[4]
    start_belief = tuple([tuple(initial_state)])  
    frontier = Queue()
    frontier.put(start_belief)

    parent = {start_belief: None}
    action_parent = {start_belief: None}

    def isGoal(state, N):
        return len(state) == N

    while not frontier.empty():
        belief = frontier.get()
        yield ("visit", belief)

        if all(isGoal(s, N) for s in belief):
            path = []
            b = belief
            while b is not None:
                a = action_parent[b]
                if a is not None:
                    path.append(a)
                b = parent[b]
            yield ("found", path[::-1], belief)
            return

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
                    yield ("push", new_belief, col)

    yield ("notfound", [], ())

def backtracking_generator(N):
    def backtrack(state):
        yield state  

        if len(state) == N:
            return  

        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                yield from backtrack(new_state)

    return backtrack([])

def forward_checking_generator(N):
    def fc(state, domains):
        yield ("visit", state)
        
        if len(state) == N:
            yield ("found", tuple(state))
            return
        
        row = len(state)
        for col in range(N):
            if col in domains[row]:
                new_domains = [d.copy() for d in domains]
                
                new_state = state + [col]
                
                consistent = True
                for r in range(row + 1, N):
                    new_domains[r] -= {col, col + (r - row), col - (r - row)}
                    if not new_domains[r]:
                        consistent = False
                        break
                
                if consistent:
                    yield from fc(new_state, new_domains)
    
    domains = [set(range(N)) for _ in range(N)]
    yield from fc([], domains)

# ======================
# Hiển thị trạng thái
# ======================
def draw_state(state):
    # vẽ final state lên C2
    if current_algo == "UCS":
        tstate = tuple(state)
        cost = cost_map.get(tstate, cost_of_state(state))
        draw_state_on_canvas(C2, state, show_mobility=True, show_cost=cost)
        cost_label.config(text=f"Cost: {cost}")
    else:
        draw_state_on_canvas(C2, state, show_mobility=False, show_cost=None)
        cost_label.config(text="")

def draw_state_on_canvas(canvas, state, show_mobility=False, show_cost=None):
    canvas.delete("all")
    draw_labels(canvas)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    
    # vẽ hậu & mobility (nếu yêu cầu)
    for row, col in enumerate(state):
        x1 = size*col+offset
        y1 = size*row
        x2, y2 = x1+size, y1+size
        try:
            canvas.create_image((x1+x2)/2, (y1+y2)/2, image=queen_img)
        except:
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Q', font=("Arial", 24, "bold"))
        if show_mobility:
            mob = mobility_of_queen(state, row, col)
            canvas.create_text(x1+8, y1+10, text=str(mob), anchor="nw",
                               font=("Arial", 10, "bold"), fill="white")
        
    # Nếu yêu cầu hiển thị cost (dùng cho C2 khi UCS)
    if show_cost is not None:
        canvas.create_text(250, 560, text=f"Cost: {show_cost}", font=("Arial", 14, "bold"), fill="blue")
        


# ======================
# Auto-run
# ======================
after_id = None
def reset_before_run():
    global is_running, current_path, current_index, current_algo, after_id
    is_running = False
    current_path = []
    current_index = 0
    current_algo = None

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

def show_next_state():
    global current_index
    if current_index < len(current_path):
        draw_state_on_canvas(C1, current_path[current_index], show_mobility=True, show_cost=None)
        current_index += 1

def resume_run():
    global is_running
    is_running = True

    if current_algo == "DFS":
        try:
            run_dfs_step()
        except NameError:
            pass
    elif current_algo == "BFS":
        try:
            run_bfs_step()
        except NameError:
            pass
    else:
        run_next_state()

def stop_run():
    global is_running
    is_running = False

def run_next_state():
    global current_index, is_running
    if is_running and current_index < len(current_path):
        show_next_state()
        root.after(step_delay, run_next_state)

def run_dfs_auto():
    reset_before_run()
    global dfs_gen, current_algo, is_running
    solutions = dfs_queens(N)
    if solutions:
        final_solution = solutions[0][-1] 
        draw_state_on_canvas(C2, final_solution, show_mobility=False)
    
    dfs_gen = dfs_generator(N)
    current_algo = "DFS"
    is_running = True
    run_dfs_step()

def run_bfs_auto():
    reset_before_run()
    global bfs_gen, current_algo, is_running
    solutions = bfs_queens(N)
    if solutions:
        final_solution = solutions[0][-1]
        draw_state_on_canvas(C2, final_solution, show_mobility=False)

    bfs_gen = bfs_generator(N)
    current_algo = "BFS"
    is_running = True
    run_bfs_step()

def run_ucs_auto():
    reset_before_run()
    global ucs_gen, current_algo, is_running
    solution, cost = uniform_cost_search(N)
    if solution:
        final_solution = solution[0][-1]
        draw_state_on_canvas(C2, final_solution, show_mobility=True)

    ucs_gen = ucs_generator(N)
    current_algo = "UCS"
    is_running = True
    run_ucs_step()

def run_dls_auto():
    reset_before_run()
    global dls_gen, current_algo, is_running
    solutions = depth_limited_search(N, 8)
    if solutions:
        final_solution = solutions[0][-1]
        draw_state_on_canvas(C2, final_solution)

    dls_gen = dls_generator(N, 8) # Giới hạn độ sâu là 8
    current_algo = "DLS"
    is_running = True
    run_dls_step()

def run_ids_auto():
    reset_before_run()
    global ids_gen, current_algo, is_running
    solutions = iterative_deepening_search(N)
    if solutions:
        final_solution = solutions[0][-1]
        draw_state_on_canvas(C2, final_solution)

    ids_gen = ids_generator(N)
    current_algo = "IDS"
    is_running = True
    run_ids_step()

def run_gbfs_auto():
    reset_before_run()
    global gbfs_gen, current_path, current_index, is_running, current_algo
    gbfs_gen = gbfs_generator(N)
    current_algo = "GBFS"
    current_path = []  # lưu path nếu cần
    current_index = 0
    is_running = True
    run_gbfs_step()

def run_astar_auto():
    reset_before_run()
    global astar_gen, current_algo, is_running, current_path, current_index, cost_map
    astar_gen = astar_generator(N)
    path, cmap = astar_search(N)
    cost_map = cmap
    if path:
        final_state = path[-1]
        draw_state_on_canvas(C2, final_state, show_mobility=True, show_cost=cost_map[tuple(final_state)])

    current_algo = "A*"
    current_path = []
    current_index = 0
    is_running = True
    run_astar_step()

def run_hill_auto():
    global Hill_gen, current_algo, is_running
    reset_before_run()
    Hill_gen = hill_generator(N)
    final_solution, final_cost = hillClimbing_search()
    if final_solution is not None and len(final_solution) > 0:
        draw_state_on_canvas(C2, final_solution, show_cost=final_cost)

    current_algo = "Hill Climbing"
    is_running = True
    run_hill_step()

def run_sa_auto():
    global sa_gen, current_algo, current_path, current_index, is_running
    reset_before_run()
    sa_gen = sa_generator(N)
    final_solution, final_cost = simulated_annealing()
    if final_solution is not None:
        draw_state_on_canvas(C2, final_solution, show_cost=final_cost)
    
    current_algo = "Simulated Annealing"
    current_path = []
    current_index = 0
    is_running = True
    run_sa_step()

def run_localBeam_auto():
    global localBeam_gen, current_path, current_index, is_running, current_algo
    reset_before_run()
    
    localBeam_gen = local_beam_generator(N, k=3)
    current_algo = "Local Beam"
    current_path = []
    current_index = 0
    is_running = True
    run_localBeam_step()

def run_Genetic_auto():
    global genetic_gen, current_path, current_index, is_running, current_algo
    reset_before_run()
    best_solution, best_hval = None, None
    for event in genetic_generator(N):
        if event[0] == "found":
            best_solution, best_hval = event[1], event[2]
            break
    
    if best_solution is not None:
        draw_state_on_canvas(C2, best_solution, show_cost=best_hval)
    genetic_gen = genetic_generator(N)
    current_algo = "Genetic Algorithm"
    current_path = []
    current_index = 0
    is_running = True
    run_Genetic_step()

def run_andor_auto():
    reset_before_run()
    global andor_gen, current_algo, is_running
    solution_goal, solution_path = AND_OR_SEARCH([], GOAL_STATE)
    if solution_path:
       draw_state_on_canvas(C2, solution_path[-1], show_mobility=False)
    andor_gen = andor_generator(N)
    current_algo = "AND-OR (gen)"
    is_running = True
    run_andor_step()

def run_sensorless_auto():
    global sensorless_gen, current_algo, is_running
    reset_before_run()
    path, final_belief = sensorless_search_queens()

    if path:
        draw_state_on_canvas(C2, final_belief[0], show_mobility=False)

    sensorless_gen = sensorless_generator(N)  
    current_algo = "Sensorless Search"
    is_running = True
    run_sensorless_step()

def run_partialObs_auto():
    global partial_obs_gen, current_algo, is_running
    reset_before_run()
    path, final_belief = partial_observable_search_queens()

    if path:
        draw_state_on_canvas(C2, final_belief[0], show_mobility=False)

    partial_obs_gen = partial_observation_generator(N)
    current_algo = "Partial Observation Search"
    is_running = True
    run_partialObs_step()

def run_backtracking_auto():
    global backtracking_gen, current_algo, is_running
    reset_before_run()
    
    solution = backtracking_search(N)
    
    if solution:
        draw_state_on_canvas(C2, solution[0][-1], show_mobility=False)

    backtracking_gen = backtracking_generator(N)
    current_algo = "Backtracking Search"
    is_running = True
    run_backtracking_step()

def run_forward_checking_auto():
    global forward_gen, current_algo, is_running
    reset_before_run()
    solution = forward_checking_search(N)

    if solution:
        draw_state_on_canvas(C2, solution[-1])

    forward_gen = forward_checking_generator(N)
    current_algo = "Forward Checking"
    is_running = True
    run_forward_checking_step()

# ======================
# Step-by-step
# ======================
def run_dfs_step():
    global dfs_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(dfs_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_dfs_step)
    except StopIteration:
        is_running = False

def run_bfs_step():
    global bfs_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(bfs_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_bfs_step)
    except StopIteration:
        is_running = False

def run_ucs_step():
    global ucs_gen, is_running, after_id
    if not is_running:  
        return
    try:
        event = next(ucs_gen)
        if event[0] in ("visit", "push"):
            state, cost = event[1], event[2]
            draw_state_on_canvas(C1, state, show_mobility=True, show_cost=cost)
        elif event[0] == "found":
            final_state, cost_map = list(event[1]), event[3]
            draw_state_on_canvas(C2, final_state, show_mobility=True,
                                 show_cost=cost_map[tuple(final_state)])
            is_running = False
            return
        after_id = root.after(step_delay, run_ucs_step)
    except StopIteration:
        is_running = False

def run_dls_step():
    global dls_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(dls_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            draw_state_on_canvas(C1, state)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state)
            is_running = False
            return
        after_id = root.after(step_delay, run_dls_step)
    except StopIteration:
        is_running = False

def run_andor_step():
    global andor_gen, is_running, after_id
    if not is_running or andor_gen is None:
        return
    try:
        event = next(andor_gen)
        if event[0] == "visit":
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "push":
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            parent = event[2]
            # vẽ final lên C2
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_andor_step)
    except StopIteration:
        is_running = False

def run_ids_step():
    global ids_gen, is_running, after_id
    if not is_running or ids_gen is None:
        return
    try:
        event = next(ids_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_ids_step)
    except StopIteration:
        is_running = False

def run_gbfs_step():
    global gbfs_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(gbfs_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            h_val = event[2]
            draw_state_on_canvas(C1, state, show_mobility=False, show_cost=h_val)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_gbfs_step)
    except StopIteration:
        is_running = False

def run_astar_step():
    global astar_gen, is_running, after_id, cost_map
    if not is_running or astar_gen is None:
        return
    try:
        event = next(astar_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            g_val = event[2]
            f_val = event[3]
            draw_state_on_canvas(C1, state, show_mobility=True, show_cost=f_val)
        elif event[0] == "found":
            final_state = list(event[1])
            parent = event[2]
            cost_map = event[3]
            draw_state_on_canvas(C2, final_state, show_mobility=True,
                                 show_cost=cost_map[tuple(final_state)])
            is_running = False
            return
        after_id = root.after(step_delay, run_astar_step)
    except StopIteration:
        is_running = False

def run_hill_step():
    global Hill_gen, is_running, after_id
    if not is_running or Hill_gen is None:
        return
    try:
        event = next(Hill_gen)
        if event[0] == "visit":
            state = event[1]
            draw_state_on_canvas(C1, state)
        elif event[0] == "found":
            state, cost = event[1], event[2]
            draw_state_on_canvas(C2, state, show_cost=cost)
            is_running = False
            return
        after_id = root.after(step_delay, run_hill_step)
    except StopIteration:
        is_running = False

def run_sa_step():
    global sa_gen, current_index, current_path, is_running, after_id
    if not is_running or sa_gen is None:
        return
    try:
        event = next(sa_gen)
        if event[0] == "visit":
            state, h_val = event[1], event[2]
            current_path.append(state)
            current_index += 1
            draw_state_on_canvas(C1, state, show_cost=h_val)
        elif event[0] == "found":
            state, h_val = event[1], event[2]
            draw_state_on_canvas(C2, state, show_cost=h_val)
            is_running = False
            return
        after_id = root.after(step_delay, run_sa_step)
    except StopIteration:
        is_running = False

def run_localBeam_step():
    global localBeam_gen, current_index, current_path, is_running, after_id
    if not is_running or localBeam_gen is None:
        return
    try:
        event = next(localBeam_gen)
        if event[0] == "visit":
            beam_states = event[1]
            draw_state_on_canvas(C1, beam_states[0])
        elif event[0] == "found":
            final_state = event[1]
            draw_state_on_canvas(C2, final_state)
            is_running = False
            return
        after_id = root.after(step_delay, run_localBeam_step)
    except StopIteration:
        is_running = False

def run_Genetic_step():
    global genetic_gen, is_running, after_id
    if not is_running or genetic_gen is None:
        return
    try:
        event = next(genetic_gen)
        if event[0] == "visit":
            state, h_val = event[1], event[2]
            draw_state_on_canvas(C1, state, show_cost=h_val)
        elif event[0] == "found":
            state, h_val = event[1], event[2]
            draw_state_on_canvas(C2, state, show_cost=h_val)
            is_running = False
            return
        after_id = root.after(step_delay, run_Genetic_step)
    except StopIteration:
        is_running = False

def run_sensorless_step():
    global sensorless_gen, is_running, after_id
    if not is_running or sensorless_gen is None:
        return
    try:
        event = next(sensorless_gen)
        if event[0] == "visit":
            belief = event[1]
            for state in belief:
                draw_state_on_canvas(C1, state, show_mobility=False)

        elif event[0] == "push":
            new_belief = event[1]
            for state in new_belief:
                draw_state_on_canvas(C1, state, show_mobility=False)

        elif event[0] == "found":
            path, belief = event[1], event[2]
            for state in belief:
                draw_state_on_canvas(C2, state, show_mobility=False)
            is_running = False
            return

        elif event[0] == "notfound":
            is_running = False
            return

        after_id = root.after(step_delay, run_sensorless_step)
    except StopIteration:
        is_running = False

def run_partialObs_step():
    global partial_obs_gen, is_running, after_id
    if not is_running or partial_obs_gen is None:
        return
    try:
        event = next(partial_obs_gen)
        if event[0] == "visit":
            belief = event[1]
            if belief:  
                draw_state_on_canvas(C1, belief[0], show_mobility=False)
        elif event[0] == "push":
            belief, col = event[1], event[2]
            if belief:
                draw_state_on_canvas(C1, belief[0], show_mobility=False)
        elif event[0] == "found":
            path, final_belief = event[1], event[2]
            if final_belief:
                draw_state_on_canvas(C2, final_belief[0], show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_partialObs_step)
    except StopIteration:
        is_running = False

def run_backtracking_step():
    global backtracking_gen, is_running, after_id
    if not is_running or backtracking_gen is None:
        return
    try:
        state = next(backtracking_gen)
        draw_state_on_canvas(C1, state, show_mobility=False)

        if len(state) == N:
            draw_state_on_canvas(C2, state, show_mobility=False)
            is_running = False
            return

        after_id = root.after(step_delay, run_backtracking_step)
    except StopIteration:
        is_running = False

def run_forward_checking_step():
    global forward_gen, is_running, after_id
    if not is_running or forward_gen is None:
        return
    try:
        event = next(forward_gen)
        if event[0] == "visit":
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_forward_checking_step)
    except StopIteration:
        is_running = False

# ======================
# Load ảnh hậu
# ======================
current_dir = os.path.dirname(os.path.abspath(__file__))
queen_path = os.path.join(current_dir, "wq.png")
try:
    try:
        resample = Image.Resampling.LANCZOS
    except:
        resample = Image.LANCZOS
    img = Image.open(queen_path).resize((int(size), int(size)), resample)
    queen_img = ImageTk.PhotoImage(img)
except:
    queen_img = PhotoImage(width=int(size), height=int(size))

# ======================
# Giao diện nút
# ======================
table_initial()
table_operator()
draw_labels(C1)
draw_labels(C2)

btn_frame = Frame(root, bg="white")
btn_frame.pack(side=BOTTOM, pady=5, fill="x")

# Hàng 1: classical search
Button(btn_frame, text="BFS", font=("Arial",14,"bold"),
       bg="#009688", fg="white", command=run_bfs_auto).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="DFS", font=("Arial",14,"bold"),
       bg="#795548", fg="white", command=run_dfs_auto).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="UCS", font=("Arial",14,"bold"),
       bg="#3F51B5", fg="white", command=run_ucs_auto).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="DLS", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", command=run_dls_auto).grid(row=0, column=3, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="IDS", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", command=run_ids_auto).grid(row=0, column=4, padx=5, pady=5, sticky="ew")

# Hàng 2: heuristic search
Button(btn_frame, text="Greedy Best-First", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", command=run_gbfs_auto).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="A* Search", font=("Arial",14,"bold"),
       bg="#FF9800", fg="white", command=run_astar_auto).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Hill Climbing", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", command=run_hill_auto).grid(row=1, column=2, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Simulated Annealing", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", command=run_sa_auto).grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# Hàng 3: Local & Advanced
Button(btn_frame, text="Local Beam", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", command=run_localBeam_auto).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Genetic Algorithm", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", command=run_Genetic_auto).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="AND-OR", font=("Arial",14,"bold"),
       bg="#FF5722", fg="white", command=run_andor_auto).grid(row=2, column=2, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Sensorless Search", font=("Arial",14,"bold"),
       bg="#673AB7", fg="white", command=run_sensorless_auto).grid(row=2, column=3, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Partial Obs Search", font=("Arial",14,"bold"),
       bg="#9C27B0", fg="white", command=run_partialObs_auto).grid(row=2, column=4, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Backtracking", font=("Arial",14,"bold"),
       bg="#4E342E", fg="white", command=run_backtracking_auto).grid(row=2, column=5, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="Forward Checking", font=("Arial",14,"bold"),
       bg="#FF5722", fg="white", command=run_forward_checking_auto).grid(row=2, column=6, padx=5, pady=5, sticky="ew")

# Hàng 4: Control
Button(btn_frame, text="⏯ Resume", font=("Arial",14,"bold"),
       bg="#4CAF50", fg="white", command=resume_run).grid(row=1, column=4, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="⏸ Stop", font=("Arial",14,"bold"),
       bg="#F44336", fg="white", command=stop_run).grid(row=1, column=5, padx=5, pady=5, sticky="ew")
Button(btn_frame, text="🧹 Clear", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", command=clear_queens).grid(row=1, column=6, padx=5, pady=5, sticky="ew")

# Cấu hình cột để các nút chia đều
for i in range(7):
    btn_frame.grid_columnconfigure(i, weight=1)

# Nhãn hiển thị kết quả / cost
cost_label = Label(root, text="", font=("Arial",14), fg="blue")
cost_label.pack(pady=5)

root.mainloop()
