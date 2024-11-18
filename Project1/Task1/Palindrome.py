def is_palindrome(s):
    s = s.lower()
    clean_s = ''
    for char in s:
        if char.isalpha() or char.isdigit():
            clean_s += char
    return clean_s == clean_s[::-1]

string = "A man, a plan, a canal: Panama"
print(is_palindrome(string)) 