def is_palindrome(s):
    clean_s = ''.join(c for c in s.lower() if c.isalnum())
    return clean_s == clean_s[::-1]

string = "A man, a plan, a canal: Panama"
print(is_palindrome(string)) 