def find_dup_str(s, n):
    for i in range(len(s) - n + 1):
        substring = s[i:i+n]
        rest = s[i+n:]
        if substring in rest:
            return substring
    return ""


s = input("Enter a string: ")
n = int(input("Enter a substring length: "))
print(find_dup_str(s, n))


def find_max_dup(s):
    for n in range(len(s), 0, -1):
        result = find_dup_str(s, n)
        if result != "":
            return result
    return ""