def LCS(text1, text2):
    m = len(text1)
    n = len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Variable to track the length of the longest common substring
    longest_length = 0
    longest_end_pos = 0  # Track the end position of the longest substring in text1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                # Update the longest length and end position
                if dp[i][j] > longest_length:
                    longest_length = dp[i][j]
                    longest_end_pos = i  # end position of the current longest substring
            else:
                dp[i][j] = 0  # Reset since it's not a common substring

    # Extract the longest common substring
    lcs_str = text1[longest_end_pos - longest_length: longest_end_pos]

    return lcs_str
