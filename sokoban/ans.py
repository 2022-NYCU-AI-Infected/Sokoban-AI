from concurrent.futures import thread
import sokobanAPI, solver
from time import perf_counter as timer
import threading



def solve(methodN, level):
    start = timer()
    s = solver.solver()
    s.refresh()
    methods = {"bfs": s.bfs, "dfs": s.dfs, "astar": s.astar, "ucs": s.ucs}
    method = methods[methodN]

    g = sokobanAPI.API(i)
    # g.start()
    g.loadLevel()
    ans = method(g.getMatrix())
    end = timer()
    print(f"{methodN}({level}) {end - start} \n {ans}")
    # g.playSeq(ans[0], delay=0.1)

    

names = ["bfs", "ucs", "astar"]
for i in range(8, 10):
    # threads = []

    # for name in names:
    #     t = threading.Thread(target=solve, args=(name, i))
    #     threads.append(t)

    # for t in threads:
    #     t.start()

    # for t in threads:
    #     t.join()

    for methodN in names:
        solve(methodN, i)