# 给你下面这段代码，帮我看看有什么问题，如果有，请指出来，否则请说没有问题，并且请说明问题所在的位置和原因，以及如何修复
# 给 merge_sort 加”递归深度打印”，观察 8000 元素的递归树深度，是否符合预期？

# 递归深度统计（模块级变量）
MAX_DEPTH = 0
CALL_COUNT = 0

def merge_sort(nums, depth=0):
    """合并排序：分治三步的完整样板（depth=当前递归深度，顶层调用为 0）"""
    global MAX_DEPTH, CALL_COUNT
    CALL_COUNT += 1
    # 只在刷新历史最大深度时打印，避免 n=8000 时输出上万行
    if depth > MAX_DEPTH:
        MAX_DEPTH = depth
        print(f"  [递归深度] depth={depth:>2}, 子数组长度={len(nums)}")

    # 基准情形：长度 0 或 1 的数组天然有序
    if len(nums) <= 1:
        return nums

    # ---- 分解（Divide）：从中间切成两半 ----
    mid = len(nums) // 2
    left, right = nums[:mid], nums[mid:]

    # ---- 解决（Conquer）：递归排序两个小段（深度 +1）----
    left_sorted = merge_sort(left, depth + 1)
    right_sorted = merge_sort(right, depth + 1)

    # ---- 合并（Combine）：两个有序段拼成一个有序段 ----
    return merge(left_sorted, right_sorted)

def merge(a, b):
    """双指针合并两个有序数组"""
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:              # 取较小者入结果
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])              # 残段必有序，直接接上
    result.extend(b[j:])
    return result

if __name__ == "__main__":
    import math
    import random

    # 小例子：先直观看到递归如何逐层展开
    print(merge_sort([8, 3, 5, 1, 9, 2]))  # [1, 2, 3, 5, 8, 9]

    # ---- 观察 8000 元素的递归树深度 ----
    random.seed(42)
    data = [random.randint(0, 100000) for _ in range(8000)]

    MAX_DEPTH, CALL_COUNT = 0, 0  # 重置统计，只观察本次大测试
    print("\n--- n=8000 递归深度观察 ---")
    merge_sort(data)

    expected = math.ceil(math.log2(8000))
    print(f"实测最大递归深度: {MAX_DEPTH}（顶层调用记为 0）")
    print(f"总递归调用次数: {CALL_COUNT}（理论值 2n-1 = {2 * 8000 - 1}）")
    print(f"理论深度 ceil(log2(8000)) = {expected}（2^12=4096 < 8000 ≤ 2^13=8192）")
    print(f"结论: {'符合' if MAX_DEPTH == expected else '不符合'} O(log n) 预期")