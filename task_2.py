def binary_search(arr, x):
    iter = 0
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
        iter += 1
        mid = (high + low) // 2
 
        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1
 
        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1
 
        # інакше x присутній на позиції і повертаємо його
        else:
            if mid < len(arr) - 1:
                return (iter, arr[mid+1])
            else:
                return (iter, 'відсутня "верхня межа"')
 
    # якщо елемент не знайдений
    return -1

arr = [1/40, 1/10, 1/4, 1/3, 1/2]
x = 1/3
result = binary_search(arr, x)
if result != -1:
    print(f"Element is present at index {result}")
else:
    print("Element is not present in array")