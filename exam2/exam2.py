D = 8
data = [
    42, 44, 41, 43, 45, 40, 46, 42, 44, 43, 47, 45, 46, 48, 49, 50,
    52, 85, 53, 54, 55, 57, 56, 58, 59, 60, 62, 61, 63, 64, 65, 67,
    66, 68, 69, 70, 72, 71, 73, 74, 75, 77, 76, 78, 99, 99, 82, 81,
    83, 84, 85, 87, 86, 88, 89, 90, 92, 91, 93, 94, 95, 97, 96, 98,
    99, 100, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85,
    84, 83, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68,
    67, 66, 65, 64
]
#贪心算法
def solve_greedy(soc_data,Max_diff):
    if not soc_data:
        return 0, []
    segements = []
    current_segment = [soc_data[0]]
    current_min = soc_data[0]
    current_max = soc_data[0]
    for x in data[1:]:
        new_min = min(current_min,x)
        new_max = max(current_max,x)
        if new_max - new_min <= Max_diff:
            current_segment.append(x)
            current_min = new_min
            current_max = new_max
        else:
            segements.append(current_segment)
            current_segment = [x]
            current_min = x
            current_max = x
    segements.append(current_segment)
    return len(segements), segements

count, result = solve_greedy(data,D)
print(f"————贪心算法分段结果———")
print(f"最少分段数为：{count}")
print(f"分段结果为：{result[3:7]}")
#动态规划算法

def solve_dp(soc_data,Max_diff):
    n = len(soc_data)
    count = 0
    dp = [float('inf')]*(n+1)
    dp[0] = 0

    for i in range(1,n+1):
        current_min = soc_data[i-1]
        current_max = soc_data[i-1]
        for j in range(i-1,-1,-1):
            current_min = min(current_min,soc_data[j])
            current_max = max(current_max,soc_data[j])
            if current_max - current_min >= Max_diff:
                break
            if dp[i] + 1<=dp[j]:
                dp[i] = dp[j]


