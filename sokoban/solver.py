from collections import deque
from queue import PriorityQueue
import numpy as np
from hungarian import Hungarian
import math

def hungarianDistance(method):
    def calc(state, cache):
        if 'hungarian' not in cache:
            cache['hungarian'] = {}
        player = state.getPlayerPosition()
        boxes = state.getBoxes()
        targets = state.getTargets()
        key = (",".join([str(x[0]) + "-" + str(x[1]) for x in boxes]),
               ",".join([str(x[0]) + "-" + str(x[1]) for x in targets]))
        total = 0
        if key in cache['hungarian']:
            total = cache['hungarian'][key]
        else :
            distance_list = []
            for b in boxes:
                distance_list.append([method(b, t) for t in targets])
            if len(distance_list) == 0:
                return 1
            array = np.array(distance_list, dtype='float64')
            hungarian = Hungarian(array)
            hungarian.calculate()
            total = hungarian.get_total_potential()
            cache['hungarian'][key] = total
        total += sum([method(player, b) for b in boxes] or [0])
        return total
    return calc

def distance(method):
    def calc(state, cache):
        if 'min_distance' not in cache:
            cache['min_distance'] = {}
        player = state.getPlayerPosition()
        boxes = state.getBoxes()
        targets = state.getTargets()
        total = 0
        key = (",".join([str(x[0]) + "-" + str(x[1]) for x in boxes]),
                ",".join([str(x[0]) + "-" + str(x[1]) for x in targets]))
        if key in cache['min_distance']:
            total = cache['min_distance'][key]
        else:
            for b in boxes:
                total += min([method(b, t) for t in targets] or [0])
            cache['min_distance'][key] = total
        total += sum([method(player, b) for b in boxes] or [0])
        return total
    return calc

def costDefault(key, cache):
    if key == 'Move':
        return 1
    elif key == 'Push':
        return 2
    elif key == 'PushOut':
        return 10

def cost2(key, cache):
    if key == 'Move':
        return 2
    elif key == 'Push':
        return 1
    elif key == 'PushOut':
        return 2

class solver:
    def __init__(self):
        self.cache = {}
        self.costs = {"none": lambda key, cache: 1,
                        "default": costDefault,
                        "cost2": cost2
        }
        self.heuristic = {"none": lambda x, y: 0,
                            "hungarian": hungarianDistance(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),
                            "manhattan": distance(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),
                            "euclidean": distance(lambda a, b: math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)),
                            "hungarian_euclidean": hungarianDistance(lambda a, b: math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))
        }
    
    def refresh(self):
        self.cache = {}

    def dfs(self, startState, maxDepth=150, cache={}):
        stack = deque([(startState, "")])
        while len(stack) > 0:
            state, action = stack.pop()
            cache[state.getHash()] = len(action)
            if state.isSuccess():
                return (action, len(cache))
            if state.isFailure():
                continue
            if len(action) >= maxDepth:
                break
            for (act, _) in state.getPossibleActions():
                nextState = state.successor(act)
                if nextState.getHash() in cache and cache[nextState.getHash()] <= len(action) + 1:
                    continue
                stack.append((nextState, action + act))
        return ("", 0)

    def bfs(self, startState, maxDepth=float('inf'), cache={}):
        return self.ucs(startState=startState, cache=cache, cost="none")
    
    def ucs(self, startState, cache={}, cost="default", maxCost=500):
        return self.astar(startState=startState, cache=cache, cost=cost, maxCost=maxCost, heuristic="none")

    def astar(self, startState, cache={}, cost="default", maxCost=1000, heuristic="hungarian"):
        h = self.heuristic[heuristic]
        costCalc = self.costs[cost]
        queue = PQ()
        action_map = {}

        startState.h = h(startState, self.cache)
        queue.update(startState, startState.h)
        action_map[startState.getHash()] = ""
        while not queue.empty():
            state, cost = queue.pop()
            actions = action_map[state.getHash()]
            cache[state.getHash()] = len(actions)
            if state.isSuccess():
                return (actions, len(cache))
            if state.isFailure():
                continue
            if cost >= maxCost:
                continue
            for (act, costDelta) in state.getPossibleActions():
                nextState = state.successor(act)
                if nextState.getHash() in cache:
                    continue
                old = action_map.get(nextState.getHash(), None)
                if not old or len(old) > len(actions) + 1:
                    action_map[nextState.getHash()] = actions + act
                nextState.h = h(nextState, self.cache)
                queue.update(nextState, nextState.h + costCalc(costDelta, self.cache) + cost - state.h)
        return ("", 0)
                
        

        
class PQ:
    def __init__(self):
        self.queue = PriorityQueue()
        self.map = {}
    
    def update(self, state, cost):
        oldCost = self.map.get(state)
        if oldCost == None or cost < oldCost:
            self.map[state] = cost
            self.queue.put((cost, state))

    def pop(self):
        while not self.queue.empty():
            cost, state = self.queue.get()
            if self.map[state] == -100000:
                continue
            self.map[state] = -100000
            return (state, cost)
        return (None, None)
    
    def empty(self):
        return self.queue.empty()

    
    