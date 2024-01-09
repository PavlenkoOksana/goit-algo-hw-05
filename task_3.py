import timeit
from pathlib import Path

# -------------   Боєра-Мура ------------
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1
# End of -------------   Боєра-Мура ------------


# -----------------  Кнута-Морріса-Пратта (КМП) -----------------------
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# end of ---------- Кнута-Морріса-Пратта (КМП) -----------------------


# -----------------  Рабіна-Карпа -----------------------
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1
# end of ---------- Рабіна-Карпа -----------------------


def test_sorting_algorithm(algorithm, text, pattern):
    def sort_data():
        return algorithm(text, pattern)

    return timeit.timeit(sort_data, number=1)


def main():
    file_path = Path('C:/Users/kompik/Downloads/стаття 1.txt')  
    pattern = "АЛГОРИТМІВ У БІБЛІОТЕКАХ МОВ ПРОГРАМУВАННЯ"  
    file_path_1 = Path('C:/Users/kompik/Downloads/стаття 2.txt')  
    pattern_1 = "Міхав В.В., Мелешко Є.В., Шимко С.В."  
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            # Вимірювання часу виконання для кожного алгоритму
            boyer_moore_search_time = test_sorting_algorithm(boyer_moore_search, file_content, pattern)
            kmp_search_time = test_sorting_algorithm(kmp_search, file_content, pattern)
            rabin_karp_search_time = test_sorting_algorithm(rabin_karp_search, file_content, pattern)
            print('Порівняльний аналіз 3-х алгоритмів за часом пошуку підрядка "pattern" у файлі "стаття 1.txt",:\n')
            print(f"Алгоритм Боєра-Мура: {boyer_moore_search_time} сек.")
            print(f"Алгоритм Кнута-Морріса-Пратта: {kmp_search_time} сек.")
            print(f"Алгоритм Рабіна-Карпа: {rabin_karp_search_time} сек.")
            print("----------------------------------------\n")
            
            boyer_moore_search_time = test_sorting_algorithm(boyer_moore_search, file_content, pattern_1)
            kmp_search_time = test_sorting_algorithm(kmp_search, file_content, pattern_1)
            rabin_karp_search_time = test_sorting_algorithm(rabin_karp_search, file_content, pattern_1)
            print('Порівняльний аналіз 3-х алгоритмів за часом пошуку підрядка "pattern_1" у файлі "стаття 1.txt",:\n')
            print(f"Алгоритм Боєра-Мура: {boyer_moore_search_time} сек.")
            print(f"Алгоритм Кнута-Морріса-Пратта: {kmp_search_time} сек.")
            print(f"Алгоритм Рабіна-Карпа: {rabin_karp_search_time} сек.")
            print("----------------------------------------\n")
    except FileNotFoundError:
      print(f"File '{file_path}' not found")
    except Exception as e:
      print(f"An error occurred: {e}")

    try:
        with open(file_path_1, 'r') as file:
            file_content_1 = file.read()
            # Вимірювання часу виконання для кожного алгоритму
            boyer_moore_search_time = test_sorting_algorithm(boyer_moore_search, file_content_1, pattern_1)
            kmp_search_time = test_sorting_algorithm(kmp_search, file_content_1, pattern_1)
            rabin_karp_search_time = test_sorting_algorithm(rabin_karp_search, file_content_1, pattern_1)
            print('Порівняльний аналіз 3-х алгоритмів за часом пошуку підрядка "pattern_1" у файлі "стаття 2.txt",:\n')
            print(f"Алгоритм Боєра-Мура: {boyer_moore_search_time} сек.")
            print(f"Алгоритм Кнута-Морріса-Пратта: {kmp_search_time} сек.")
            print(f"Алгоритм Рабіна-Карпа: {rabin_karp_search_time} сек.")
            print("----------------------------------------\n")
            
            boyer_moore_search_time = test_sorting_algorithm(boyer_moore_search, file_content_1, pattern)
            kmp_search_time = test_sorting_algorithm(kmp_search, file_content_1, pattern)
            rabin_karp_search_time = test_sorting_algorithm(rabin_karp_search, file_content_1, pattern)
            print('Порівняльний аналіз 3-х алгоритмів за часом пошуку підрядка "pattern" у файлі "стаття 2.txt",:\n')
            print(f"Алгоритм Боєра-Мура: {boyer_moore_search_time} сек.")
            print(f"Алгоритм Кнута-Морріса-Пратта: {kmp_search_time} сек.")
            print(f"Алгоритм Рабіна-Карпа: {rabin_karp_search_time} сек.")
            print("----------------------------------------\n")
    except FileNotFoundError:
      print(f"File '{file_path}' not found")
    except Exception as e:
      print(f"An error occurred: {e}")  



if __name__ == "__main__":
    main()