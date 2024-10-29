def filter_strings(lambda_func, string_array):
    filtered_array = list(filter(lambda_func, string_array))
    return filtered_array


strings = ["apple", "banana", "apricot", "pear", "grape", "avacado", "a", "alpha", "  orange "]
filtered = filter_strings(lambda s: " " not in s and not s.startswith("a") and len(s) >= 5, strings)
print(filtered)