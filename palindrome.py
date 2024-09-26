def manacher(text):
    # Implement the Manacher's algorithm for finding the longest palindromic substring
    # Transform the input text to avoid even-length issues
    T = '#'.join(f'^{text}$')
    n = len(T)
    P = [0] * n
    center = right = 0
    for i in range(1, n - 1):
        if i < right:
            P[i] = min(right - i, P[2 * center - i])
        while T[i + P[i] + 1] == T[i - P[i] - 1]:
            P[i] += 1
        if i + P[i] > right:
            center, right = i, i + P[i]
    max_len = max(P)
    center_index = P.index(max_len)
    start = (center_index - max_len) // 2
    return text[start:start + max_len]


