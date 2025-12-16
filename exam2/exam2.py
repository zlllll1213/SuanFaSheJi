import matplotlib.pyplot as plt
import numpy as np

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


# 贪心算法
def solve_greedy(soc_data, Max_diff):
    # 如果数据为空，返回0段和空列表
    if not soc_data:
        return 0, []
    segments = []
    current_segment = [soc_data[0]]
    current_min = soc_data[0]
    current_max = soc_data[0]
    # 遍历数据中的每个元素
    for x in data[1:]:
        new_min = min(current_min, x)
        new_max = max(current_max, x)
        # 如果当前段的最大值与最小值之差不超过最大允许差值，则将元素加入当前段
        if new_max - new_min <= Max_diff:
            current_segment.append(x)
            current_min = new_min
            current_max = new_max
        # 否则开始新的段
        else:
            segments.append(current_segment)
            current_segment = [x]
            current_min = x
            current_max = x
    # 将最后一段添加到结果中
    segments.append(current_segment)
    return len(segments), segments


count, result = solve_greedy(data, D)
print(f"————贪心算法分段结果———")
print(f"最少分段数为：{count}")
print(f"分段结果为：{result[3:7]}")


# 动态规划算法
def solve_dp(soc_data, Max_diff):
    n = len(soc_data)
    # 初始化dp数组，dp[i]表示前i个元素的最少分段数
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    # 对于每个位置i
    for i in range(1, n + 1):
        current_min = soc_data[i - 1]
        current_max = soc_data[i - 1]
        # 从当前位置向前查找可能的分段点
        for j in range(i - 1, -1, -1):
            current_min = min(current_min, soc_data[j])
            current_max = max(current_max, soc_data[j])
            # 如果当前段超过了最大差值限制，则停止
            if current_max - current_min > Max_diff:
                break
            # 更新最优解
            if dp[j] + 1 <= dp[i]:
                dp[i] = dp[j] + 1
    return dp[n]


count = solve_dp(data, D)
print(f"----dp 算法----")
print(f"最少段数为：{count}")


def plot_greedy_result(ax, soc_data, segments, title):
    x_values = list(range(len(soc_data)))

    # 绘制所有数据点
    ax.plot(x_values, soc_data, 'bo-', markersize=4, linewidth=1)

    # 为每段使用不同颜色
    colors = plt.cm.Set3(np.linspace(0, 1, len(segments)))

    start_idx = 0
    for i, segment in enumerate(segments):
        end_idx = start_idx + len(segment)
        ax.plot(x_values[start_idx:end_idx],
                soc_data[start_idx:end_idx],
                color=colors[i],
                linewidth=2,
                marker='o',
                markersize=5)

        # 标记段边界
        if i < len(segments) - 1:
            ax.axvline(x=end_idx - 1, color='red', linestyle='--', alpha=0.7)

        start_idx = end_idx

    ax.set_title(f'{title}\n(Number of segments: {len(segments)})')
    ax.set_xlabel('Index')  # X轴标签改为英文
    ax.set_ylabel('Value')  # Y轴标签改为英文
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')


def plot_dp_result(ax, soc_data, max_diff, title):
    # 由于DP算法不存储段信息，我们显示数据并标记可能的分割点
    x_values = list(range(len(soc_data)))

    ax.plot(x_values, soc_data, 'go-', markersize=4, linewidth=1)

    # 基于最大差值约束标记可能的分割点
    current_min = soc_data[0]
    current_max = soc_data[0]
    split_points = [0]

    for i in range(1, len(soc_data)):
        current_min = min(current_min, soc_data[i])
        current_max = max(current_max, soc_data[i])

        if current_max - current_min > max_diff:
            split_points.append(i)
            current_min = soc_data[i]
            current_max = soc_data[i]

    split_points.append(len(soc_data))

    # 为各段着色
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(split_points) - 1))

    for i in range(len(split_points) - 1):
        start = split_points[i]
        end = split_points[i + 1]
        ax.plot(x_values[start:end],
                soc_data[start:end],
                color=colors[i],
                linewidth=2,
                marker='o',
                markersize=5)

        # 标记段边界
        if i < len(split_points) - 2:
            ax.axvline(x=end - 1, color='red', linestyle='--', alpha=0.7)

    ax.set_title(f'{title}\n(Minimum number of segments: {len(split_points) - 1})')
    ax.set_xlabel('Index')  # X轴标签改为英文
    ax.set_ylabel('Value')  # Y轴标签改为英文
    ax.grid(True, alpha=0.3)


# 生成可视化图表
if __name__ == "__main__":
    # 获取贪心算法的分段结果
    _, greedy_segments = solve_greedy(data, D)

    # 创建包含两个子图的图形
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # 绘制贪心算法结果
    plot_greedy_result(ax1, data, greedy_segments, "Greedy Algorithm Segmentation")

    # 绘制动态规划算法结果（模拟）
    plot_dp_result(ax2, data, D, "Dynamic Programming Approach (Simulated Segments)")

    plt.tight_layout()
    plt.show()
