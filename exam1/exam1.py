data = [
    -1.2, -0.8, 0.5 , 1.0, -0.3, 0.2,
    0.6, 1.4, 2.1, -0.9, 0.8, 1.6, 
    -0.7, 0.9, 1.3, -0.4, 0.2, 1.5,
    1.8, 1.2, -0.6, 0.7, -0.2, 0.4
]

##暴力枚举法
def solve_brute_force(arr):
    max_profict=float('-inf')
    max_start = 0
    max_end =0
    n = len(arr)
    for i in range(n):
        current_num=0
        for j in range(i,n):
            current_num += arr[j]
            if current_num>max_profict:
                max_profict=current_num
                max_start=i
                max_end=j
    
    return max_profict,max_start,max_end

max1,start1,end1=solve_brute_force(data)
print(f"最大净收益的放电区间为{start1}:00 到 {end1+1}：00")
print(f"最大收益为{max1:.1f}")


##分治法
def find_max_crossing(arr,low, mid, high):
    #左半部分最大值
    max_left =float('-inf')
    current_sum=0
    max_mid_left =mid
    for i in range(mid,low-1, -1):
        current_sum +=arr[i]
        if current_sum > max_left:
            max_left = current_sum
            max_mid_left = i

    #右半部分最大值
    max_right = float('-inf')
    current_sum = 0
    max_mid_right = mid+1
    for j in range(mid+1,high+1):
        current_sum += arr[j]
        if current_sum > max_right:
            max_right = current_sum
            max_mid_right = j

    return (max_left + max_right), max_mid_left, max_mid_right

def solve_divide_and_conquer(arr, low, high):
    if low == high:
        return arr[low], low, high
    
    mid=(low+high)//2

    left_sum,left_low,left_high = solve_divide_and_conquer(arr,low,mid)

    right_sum,right_low,right_high = solve_divide_and_conquer(arr,mid+1,high)

    cross_sum,cross_low,cross_high = find_max_crossing(arr,low,mid,high)

    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_sum,left_low,left_high
    
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_sum,right_low,right_high
    
    else:
        return cross_sum,cross_low,cross_high
    
max2,start2,end2=solve_divide_and_conquer(data,0,len(data)-1)
print(f"最大净收益的放电区间为{start2}:00 到 {end2+1}:00")
print(f"最大收益为{max2:.1f}")

##dp（动态规划）法
def solve_kadane(arr):
    max_so_far=float('-inf')
    current_sum=0
    max_start=0
    max_end=0
    temp=0

    for i in range(len(arr)):
        current_sum += arr[i]

        if current_sum > max_so_far:
            max_so_far = current_sum
            max_start = temp
            max_end = i

        if current_sum < 0:
            current_sum = 0
            temp = i+1

    return max_so_far, max_start, max_end

max3,start3,end3= solve_kadane(data)
print(f"最大净收益的区间为{start3}:00 到 {end3 +1}:00")
print(f"最大净收益为{max3:.1f}")
