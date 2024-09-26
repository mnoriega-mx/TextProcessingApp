def KMP_search(text, pattern):
    # Implement the KMP algorithm
    lps = [0] * len(pattern)
    j = 0  # index for pattern
    i = 0  # index for text
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            yield i - j  # found pattern at index i - j
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

