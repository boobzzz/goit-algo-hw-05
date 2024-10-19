import timeit


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


def knuth_morris_pratt(pattern, text):
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore(pattern, text):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


def rabin_karp(pattern, text, q=101):
    m = len(pattern)
    n = len(text)
    d = 256
    h = 1
    p = 0
    t = 0

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1


search_entries = [
    {
        'article': 'стаття 1.txt',
        'exists': 'алгоритм',
        'not_exists': 'неіснуюче слово'
    },
    {
        'article': 'стаття 2.txt',
        'exists': 'рекомендаційної',
        'not_exists': 'видумане слово'
    }
]
search_methods = {
    'КМП': knuth_morris_pratt,
    'Боєр-Мур': boyer_moore,
    'Рабін-Карп': rabin_karp
}


def process_search_data():
    for entry in search_entries:
        text = open(entry['article'], encoding='utf8').read()

        print(f'\nSearch results for {entry['article']}:')
        get_data_per_pattern(entry['exists'], text, True)
        get_data_per_pattern(entry['not_exists'], text, False)


def get_data_per_pattern(pattern, text, is_in_text):
    is_pattern_in_text = 'present' if is_in_text else 'non present'
    print(f'{' ' * 4}Pattern is {is_pattern_in_text} in text:')
    for key in search_methods.keys():
        time = timeit.timeit(lambda: search_methods[key](pattern, text), number=10)
        print(f'{' ' * 6}Час {key}: {time}')


process_search_data()
