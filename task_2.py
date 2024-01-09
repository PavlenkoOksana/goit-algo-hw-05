def binary_search(arr, x):
    iter = 0
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:
        iter += 1
        mid = (high + low) // 2

        if arr[mid] == x:
            return (iter, arr[mid])
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    if low < len(arr):
        return (iter, arr[low])
    else:
        return (iter, arr[-1])


arr = [1/40, 1/10, 1/4, 1/3, 1/2]
x = 1/6
result = binary_search(arr, x)
print(result)