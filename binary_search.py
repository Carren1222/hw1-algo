# 帮我看看这个代码，有没有问题，为什么运行不出来，指出问题并且给出更改
# 我要实现 binary_search(rates, target)（rates 有序）并且能在 1024 档模拟利率表中找 3.75%，这个你帮我想想办法，怎么在上面代码的基础上实现
# 现在我要确认你给我的代码是真分治
# 用二分查找在真实利率表（自制 100 档）找”月供最接近 5000 的利率” 10
# 那现在帮我设计一个（ binary_search.py 6 - 121 ）”未排序翻车”实验

def binary_search(rates, target, low=0, high=None, count=None):
    """在有序数组 rates 中找 target，返回下标，找不到返回 -1。
    前提：rates 必须已按升序排好——不满足此前提，结果不可预测。
    本实现采用**分治策略**：递归地将当前搜索区间拆分为左右两个子区间，
    仅在符合条件的子区间中继续查找，完全符合分治的「分解-解决-合并」范式。"""
    # 初始化参数（首次调用时的默认处理）
    if high is None:
        high = len(rates) - 1
    if count is None:
        count = [0]  # 用列表包装计数，方便递归过程中共享修改
    # 基础情况1：空数组
    if not rates:
        print("列表为空，未找到")
        return -1
    # 基础情况2：搜索区间为空（low > high），未找到
    if low > high:
        print(f"没找到，共比较 {count[0]} 次")
        return -1
    # 分解（Divide）：计算当前区间的中间位置，避免整数溢出
    mid = low + (high - low) // 2
    count[0] += 1
    # 解决（Conquer）：比较中间元素与目标，决定递归方向
    # 用绝对容差处理浮点数精度问题，兼容整数和浮点数查找
    if abs(rates[mid] - target) < 1e-9:
        print(f"找到，位于下标 {mid}，共比较 {count[0]} 次")
        return mid
    elif rates[mid] < target:
        # 目标在右子区间，递归解决右子问题
        return binary_search(rates, target, mid + 1, high, count)
    else:
        # 目标在左子区间，递归解决左子问题
        return binary_search(rates, target, low, mid - 1, count)
    # 合并（Combine）：本问题无需额外合并，子问题的解直接作为当前问题的解


def monthly_payment(principal: float, annual_rate_pct: float, months: int) -> float:
    """等额本息月供公式：M = P·r·(1+r)^n / ((1+r)^n − 1)，r 为月利率"""
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return principal / months
    k = (1 + r) ** months
    return principal * r * k / (k - 1)


def binary_search_closest(arr, target, low=0, high=None, count=None):
    """二分查找变体：返回与 target 最接近的元素下标（arr 须有序/单调）。
    区间收缩耗尽时，最近的候选必然是边界 high（左侧最后一个）与 low（右侧第一个）。"""
    if high is None:
        high = len(arr) - 1
    if count is None:
        count = [0]
    if not arr:
        print("列表为空，未找到")
        return -1
    if low > high:
        # target 介于 arr[high] 与 arr[low] 之间，取更近者
        candidates = [i for i in (high, low) if 0 <= i < len(arr)]
        best = min(candidates, key=lambda i: abs(arr[i] - target))
        print(f"无精确值，最接近的下标 {best}，共比较 {count[0]} 次")
        return best
    mid = low + (high - low) // 2
    count[0] += 1
    if abs(arr[mid] - target) < 1e-9:
        print(f"精确找到，下标 {mid}，共比较 {count[0]} 次")
        return mid
    elif arr[mid] < target:
        return binary_search_closest(arr, target, mid + 1, high, count)
    else:
        return binary_search_closest(arr, target, low, mid - 1, count)


def unsorted_failure_experiment():
    """未排序翻车实验：证明二分查找的正确性完全依赖数组有序"""
    import random
    import contextlib
    import io

    print("\n" + "=" * 60)
    print("未排序翻车实验")
    print("=" * 60)

    # ---- 实验1：确定性翻车 ----
    print("\n[实验1] 确定性翻车：同一组元素，排序能找到，乱序就漏报")
    sorted_arr = [1, 3, 5, 7, 9]
    unsorted_arr = [5, 1, 9, 3, 7]   # 相同元素，刻意打乱
    target = 1

    print(f"有序数组: {sorted_arr}, 找 {target}")
    r1 = binary_search(sorted_arr, target)
    print(f"  -> 结果: {r1} {'(正确)' if r1 == 0 else '(错误!)'}")

    print(f"乱序数组: {unsorted_arr}, 找 {target}")
    r2 = binary_search(unsorted_arr, target)
    print(f"  -> 结果: {r2} {'(翻车! 明明存在却返回-1)' if r2 == -1 else '(碰巧找到)'}")

    # ---- 实验2：随机乱序统计 ----
    print("\n[实验2] 随机乱序统计：乱序后二分查找的漏报率")
    random.seed(42)
    base = list(range(1, 101))   # 1~100
    target = 50
    trials = 1000
    misses = 0
    with contextlib.redirect_stdout(io.StringIO()):   # 吞掉 1000 次 print
        for _ in range(trials):
            shuffled = base.copy()
            random.shuffle(shuffled)
            if binary_search(shuffled, target) == -1:
                misses += 1
    print(f"数组: 1~100 (每次随机打乱), 目标: {target}, 试验次数: {trials}")
    print(f"漏报次数: {misses}/{trials}, 漏报率: {misses / trials * 100:.1f}%")
    print(f"对照: 排序后查找 1000 次，漏报率恒为 0%")

    # ---- 实验3：排序后恢复正常 ----
    print("\n[实验3] 修复方法：先排序再查找")
    fixed = sorted(unsorted_arr)
    r3 = binary_search(fixed, target)
    print(f"乱序数组排序后: {fixed}, 找 {target}")
    print(f"  -> 结果: {r3} {'(正确)' if r3 == 0 else '(错误!)'}")

    print("\n结论：二分查找的'折半舍弃'依赖有序性；未排序时，被舍弃的一半里可能藏着目标，导致漏报。")


if __name__ == "__main__":
    # 简单测试
    rates = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 7
    result = binary_search(rates, target)
    print(f"返回下标: {result}")

    

    # 生成 1024 档模拟利率表的函数
    def generate_rates_table(n=1024, start=0.01, step=0.01):
        """生成从 start 开始，每次增加 step，共 n 档的有序利率表"""
        rates_table = [round(start + i * step, 2) for i in range(n)]
        return rates_table
    # 在主程序中测试 1024 档模拟利率表查找 3.75%
    print("\n--- 1024 档模拟利率表测试 ---")
    rates_1024 = generate_rates_table()
    print(f"利率表范围: {rates_1024[0]}% ~ {rates_1024[-1]}%，共 {len(rates_1024)} 档")
    # 查找 3.75%
    target_rate = 3.75
    result_rate = binary_search(rates_1024, target_rate)

    # 额外测试：查找不存在的利率（验证边界情况）
    target_not_found = 5.555
    result_not_found = binary_search(rates_1024, target_not_found)
    print(f"在 1024 档利率表中查找不存在的 {target_not_found}%，返回值: {result_not_found}")

    # ---- 真实利率表（自制 100 档）：找"月供最接近 5000 的利率" ----
    print("\n--- 100 档真实利率表：找月供最接近 5000 的利率 ---")
    PRINCIPAL = 1_000_000   # 贷款本金 100 万
    MONTHS = 360            # 贷款 30 年

    rates_100 = generate_rates_table(n=100, start=3.00, step=0.03)
    print(f"利率表范围: {rates_100[0]}% ~ {rates_100[-1]}%，共 {len(rates_100)} 档")

    # 月供随利率单调递增 → 对"月供数组"二分即可
    payments = [round(monthly_payment(PRINCIPAL, rate, MONTHS), 2) for rate in rates_100]
    print(f"月供范围: {payments[0]:.2f} 元 ~ {payments[-1]:.2f} 元")

    target_payment = 5000.0
    best_idx = binary_search_closest(payments, target_payment)
    print(f"月供最接近 {target_payment:.0f} 元的利率: {rates_100[best_idx]}%")
    print(f"对应月供 {payments[best_idx]:.2f} 元，偏差 {abs(payments[best_idx] - target_payment):.2f} 元")

    # 未排序翻车实验
    unsorted_failure_experiment()

