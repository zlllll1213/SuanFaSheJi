from kiwisolver import Solver


N = 15
K = 12
data = [[3,0,4,7,68] , [2,1,5,72] ,[ 4,2,3,8,11,59],
        [1,6,81] , [2,9,10,63] , [3,0,2,5,77], 
        [2,7,11,66] , [1,4,70] , [3,1,6,9,85],
        [2,3,10,61] , [1,8,74] , [2,5,11,69],
        [3,2,7,9,73] , [2,0,11,88] , [2,10,11,76]]
target = (1<<12) - 1
suppliers = []
for id, row in enumerate(data):
    count = row[0]
    types = row[1:-1]
    cost = row[-1]
    mask = 0
    for i in types:
        mask |=(1<<i)
    suppliers.append({
        'id': id,
        'type': types,
        'cost': cost,
        'mask': mask
    })

class Force:
    def __init__(self):
        self.min_cost = float('inf')
        self.best_combo = []
        self.total_checked = 0
    
    def solve(self):
        self._generate_combinations(0,[])
        return self.min_cost,self.best_combo

    def _generate_combinations(self, start_index, current_combo):
        if len(current_combo) == K:
            self.total_checked += 1
            self._check_validity(current_combo)
            return
        
        if (N - start_index) < (K - len(current_combo)):
            return
        
        for i in range(start_index, N):
            current_combo.append(suppliers[i])
            self._generate_combinations(i+1, current_combo)
            current_combo.pop()

    def _check_validity(self, combo):
        current_mask = 0
        current_cost = 0
        for s in combo:
            current_mask |= s['mask']
            current_cost += s['cost']
        
        if current_mask ==target:
            if current_cost < self.min_cost:
                self.min_cost = current_cost
                self.best_combo = [s['id'] for s in combo]

solver = Force()
min_cost, best_id = solver.solve()

print(f"检查组合总数:{solver.total_checked}")
print(f"最小碳足迹：{min_cost}")
print(f"最佳供应商组合:{best_id}")

class SolverDFS:
    def __init__(self):
        self.min_cost = float('inf')
        self.best_path = []
        self.iterations = 0
    
    def solve(self):
        self._dfs(0,0,0,0,[])
        return self.min_cost, self.best_path
    
    def _dfs(self, id, count, current_mask, current_cost, path):
        self.iterations += 1

        if current_cost >= self.min_cost:
            return
        
        if count == K:
            if current_mask == target:
                if current_cost < self.min_cost:
                    self.min_cost = current_cost
                    self.best_path = list(path)
            return
        if count + (N-id) < K:
            return 
        
        for i in range(id , N):
            s = suppliers[i]

            self._dfs(i+1,
                      count+1,
                      current_mask | s['mask'],
                      current_cost + s['cost'],
                      path + [s['id']])
            
dfs_solver = SolverDFS()
cost_dfs, path_dfs = dfs_solver.solve()
print(f"{'回溯法':<15}{'最小碳足迹:'}{cost_dfs:<10}")
def solve_dp():
    dp = [[float('inf')] * (target + 1) for _ in range(K + 1)]
    dp[0][0] = 0
    for s in  suppliers:
        s_cost = s['cost']
        s_mask = s['mask']

        for j in range(K - 1, -1, -1):
            for mask in range(target + 1):
                if dp[j][mask] == float('inf'):
                    continue

                new_mask = mask | s_mask
                new_cost = dp[j][mask] + s_cost
                
                if new_cost < dp[j+1][new_mask]:
                    dp[j+1][new_mask] = new_cost
    return dp[K][target]
    
cost_dp = solve_dp()
print(f"{'动态规划':<15}{'最少碳足迹:'}{cost_dp:<10}")