# 指令：生成 n=1000/2000/4000/8000 的随机整数数组各一份；分别用"冒泡排序(自己实现)"和"合并排序(Step1的)"计时，用 timeit 每档跑3次取均值；输出对照表：n、冒泡耗时、合并耗时、倍数关系
# 现在帮我检查一下n 翻倍时，冒泡耗时≈×4，合并耗时≈×2；n=8000 时合并比冒泡快一个数量级以上。如果有错误，可以修改上面的程序
# 输出对照表：n、冒泡耗时、合并耗时、倍数关系
# 现在帮我检查一下n 翻倍时，冒泡耗时≈×4，合并耗时≈×2；n=8000 时合并比冒泡快一个数量级以上。如果有错误，可以修改上面的程序
# 把 benchmark 扩展到 Python 内置 sorted()，对比”轮子 vs 自造” 15

import random
import timeit

# 设置随机种子以保证可复现性
random.seed(42)

# 测试的数组大小列表
ARRAY_SIZES = [1000, 2000, 4000, 8000]
# 随机整数的范围
RANDOM_RANGE = (0, 100000)
# 每档跑的次数（取均值）
REPEAT = 3

def generate_random_array(n: int) -> list:
    """生成大小为n的随机整数数组"""
    return [random.randint(*RANDOM_RANGE) for _ in range(n)]

def bubble_sort(arr: list) -> list:
    """冒泡排序（自己实现）"""
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def merge_sort(arr: list) -> list:
    """合并排序（Step1的）"""
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: list, right: list) -> list:
    """合并两个有序数组"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def benchmark_sort(arr: list, sort_func, repeat: int = 3) -> float:
    """使用 timeit 对排序函数计时，跑 repeat 次取平均耗时（秒）"""
    def wrapper():
        sort_func(arr)

    times = timeit.repeat(wrapper, repeat=repeat, number=1)
    return sum(times) / len(times)



def verify_results(sort_results: list) -> bool:
    """检查增长规律：n 翻倍时冒泡耗时≈×4、合并耗时≈×2；n=8000 时合并比冒泡快一个数量级以上"""
    print()
    print("=" * 60)
    print("增长规律检查")
    print("=" * 60)

    all_ok = True

    # 逐档检查 n 翻倍时的耗时倍数
    for i in range(1, len(sort_results)):
        prev, curr = sort_results[i - 1], sort_results[i]
        bubble_ratio = curr['bubble_time'] / prev['bubble_time']
        merge_ratio = curr['merge_time'] / prev['merge_time']
        sorted_ratio = curr['sorted_time'] / prev['sorted_time']

        # 容差区间：冒泡期望≈4 取 [3, 5.5]，合并/sorted 期望≈2 取 [1.5, 3]
        bubble_ok = 3.0 <= bubble_ratio <= 5.5
        merge_ok = 1.5 <= merge_ratio <= 3.0
        sorted_ok = 1.5 <= sorted_ratio <= 3.0
        if not (bubble_ok and merge_ok and sorted_ok):
            all_ok = False

        bubble_word = "符合" if bubble_ok else "不符"
        merge_word = "符合" if merge_ok else "不符"
        sorted_word = "符合" if sorted_ok else "不符"
        print(f"n {prev['n']} -> {curr['n']}: 冒泡 ×{bubble_ratio:.2f} (期望≈4, {bubble_word}) | 合并 ×{merge_ratio:.2f} (期望≈2, {merge_word}) | sorted ×{sorted_ratio:.2f} (期望≈2, {sorted_word})")

    # 检查 n=8000 时合并是否比冒泡快一个数量级以上
    last = sort_results[-1]
    speedup = last['bubble_time'] / last['merge_time'] if last['merge_time'] > 0 else float('inf')
    speedup_ok = speedup >= 10
    if not speedup_ok:
        all_ok = False
    print(f"\nn={last['n']}: 合并比冒泡快 {speedup:.1f} 倍 (要求≥10倍, {'符合' if speedup_ok else '不符'})")

    print("\n结论: " + ("全部符合预期" if all_ok else "存在不符项（可能是计时噪声，可把 REPEAT 调大重跑）"))
    return all_ok


def main():
    print("Benchmark 开始\n")

    # 存储各数组大小对应的排序耗时结果
    sort_results = []

    for n in ARRAY_SIZES:
        print(f"=== 数组大小 n={n} ===")

        # 生成随机整数数组（每档一份）
        arr = generate_random_array(n)

        # 正确性抽查：自造合并排序结果必须与轮子 sorted() 完全一致
        assert merge_sort(arr) == sorted(arr), "自造合并排序结果与 sorted() 不一致！"

        # 冒泡排序：timeit 跑3次取均值
        bubble_time = benchmark_sort(arr, bubble_sort, repeat=REPEAT)
        print(f"  冒泡排序平均耗时 ({REPEAT}次): {bubble_time:.6f} 秒")

        # 合并排序：timeit 跑3次取均值
        merge_time = benchmark_sort(arr, merge_sort, repeat=REPEAT)
        print(f"  合并排序平均耗时 ({REPEAT}次): {merge_time:.6f} 秒")

        # 内置 sorted()：timeit 跑3次取均值（轮子）
        sorted_time = benchmark_sort(arr, sorted, repeat=REPEAT)
        print(f"  内置 sorted 平均耗时 ({REPEAT}次): {sorted_time:.6f} 秒")

        sort_results.append({
            'n': n,
            'bubble_time': bubble_time,
            'merge_time': merge_time,
            'sorted_time': sorted_time,
        })
        print()

    
    print("=" * 72)
    print("排序性能对照表")
    print("=" * 72)
    header = f"{'数组大小n':<8} | {'冒泡耗时(秒)':<12} | {'合并耗时(秒)':<12} | {'sorted耗时(秒)':<12} | {'冒泡/合并':<8} | {'合并/sorted':<8}"
    print(header)
    print("-" * len(header))
    for r in sort_results:
        # 避免除以0，计算倍数
        ratio = r['bubble_time'] / r['merge_time'] if r['merge_time'] > 0 else float('inf')
        vs_sorted = r['merge_time'] / r['sorted_time'] if r['sorted_time'] > 0 else float('inf')
        print(f"{r['n']:<8} | {r['bubble_time']:<12.6f} | {r['merge_time']:<12.6f} | {r['sorted_time']:<12.6f} | {ratio:<8.2f} | {vs_sorted:<8.1f}")
    print("=" * 72)

    # 检查增长规律是否符合预期
    verify_results(sort_results)

    print("\nBenchmark 完成")

if __name__ == "__main__":
    main()



