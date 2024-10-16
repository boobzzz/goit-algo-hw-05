def binary_search(numbers, target):
    low = 0
    high = len(numbers) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if numbers[mid] < target:
            low = mid + 1
        elif numbers[mid] > target:
            high = mid - 1
        else:
            return iterations, numbers[mid]

    return iterations, numbers[low] if low < len(numbers) else None


arr = [0.1, 0.2, 0.5, 0.7, 1.2, 1.5, 2.3]
n = 0.6
result = binary_search(arr, n)
print(result)
