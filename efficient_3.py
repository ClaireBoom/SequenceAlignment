import time
import numpy as np
import math
import psutil
import sys

mismatch_penalties = np.array([
    [  0, 110,  48,  94],
    [110,   0, 118,  48],
    [ 48, 118,   0, 110],
    [ 94,  48, 110,   0]
])

gap_penalty = 30

def input_string_generator(input_file):
    f = open(input_file)

    final_strings = ["",""]
    string_lengths = [0,0]
    current_string_index = 0

    line = f.readline()

    while line:
        line = line.replace("\n", "")
        current_string = final_strings[current_string_index]

        if line[:1].isalpha():
            if final_strings[current_string_index]:
                current_string_index += 1

            string_lengths[current_string_index] = len(line)
            current_string = line
        else:
            line = int(line)
            string_lengths[current_string_index] *= 2
            current_string = current_string[:line+1] + current_string + current_string[line+1:]

        final_strings[current_string_index] = current_string

        line = f.readline()

    f.close()
    return final_strings

def convert_base_to_index(base_letter):
    if base_letter == 'A':
        return 0
    elif base_letter == 'C':
        return 1
    elif base_letter == 'G':
        return 2
    elif base_letter == 'T':
        return 3

def get_mismatch_penalty(i, j, x, y):
    # subtract by 1 on i and j since our dp array goes from s_1...s_length
    # where row 0 and column 0 are the base cases

    x_i = convert_base_to_index(x[i-1])
    y_j = convert_base_to_index(y[j-1])

    return mismatch_penalties[x_i,y_j]


def recurrence(dp, i, j, x, y):
    mismatch = get_mismatch_penalty(i, j, x, y)

    dp[i,j] = min(
        mismatch + dp[i-1,j-1],
        gap_penalty + dp[i-1,j],
        gap_penalty + dp[i,j-1]
    )

def get_optimal_alignments(dp, i, j, x, y):
    result_string_x = '';
    result_string_y = '';

    while i > 0 or j > 0:
        if dp[i][j] == dp[i-1][j] + gap_penalty:
            result_string_x += x[i-1]
            result_string_y += '_'
            i -= 1
        elif dp[i][j] == dp[i][j-1] + gap_penalty:
            result_string_x += '_'
            result_string_y += y[j-1]
            j -= 1
        else:
            result_string_x += x[i-1]
            result_string_y += y[j-1]               
            i -= 1
            j -= 1

    result_string_x = result_string_x[::-1]
    result_string_y = result_string_y[::-1]

    return [result_string_x, result_string_y]

def basic_alignment(dp, x, y):
    m = len(x)
    n = len(y)

    # base cases
    dp[0] = [i*gap_penalty for i in range(n+1)]
    dp[:, 0] = [i*gap_penalty for i in range(m+1)]

    # fill out dp matrix using recurrence
    for i in range(1, m+1):
        for j in range(1, n+1):
            recurrence(dp, i, j, x, y)

    # concatenate list of results
    return get_optimal_alignments(dp, m, n, x, y) + [round(dp[m,n])]

def efficient_recurrence(dp, i, j, x, y):
    mismatch = get_mismatch_penalty(i,j,x,y)

    dp[1,j] = min(
        mismatch + dp[0,j-1],
        gap_penalty + dp[0,j],
        gap_penalty + dp[1,j-1]
    )

def efficient_dp(x, y):
    m = len(x)
    n = len(y)

    # compute optimal alignments between x and left half of y
    # we only need to return the last row
    dp = np.zeros((2, n+1))
    # base cases
    dp[0] = [i*gap_penalty for i in range(n+1)]

    for i in range(1, m+1):
        dp[1,0] = i*gap_penalty
        for j in range(1, n+1):
            efficient_recurrence(dp,i,j,x,y)
        
        dp[0] = dp[1]

    return dp[1]


min_cost = 0

def efficient_alignment(x, y):

    global min_cost

    m = len(x)
    n = len(y)

    # first split x in half and find the optimal alignments with
    # x_l and y and x_r and y
    i = m//2
    x_l = x[:i]
    x_r = x[i:]

    # base cases
    if(m <= 2 or n <= 2):
        dp = np.zeros((m+1, n+1))
        result = basic_alignment(dp, x, y)
        min_cost = min_cost + result[2]

        return result
    else:
        opt_l = efficient_dp(x_l, y)

        x_r_reverse = x_r[::-1]
        y_reverse = y[::-1]

        opt_r = efficient_dp(x_r_reverse, y_reverse)

        # add value of kth row from opt_l to n-kth row from opt_r for each k to find the min
        best_cost = math.inf
        best_k = 0
        for k in range(0,n+1):
            cost = opt_l[k] + opt_r[n-k]
            if(cost <= best_cost):
                best_cost = cost
                best_k = k

        l_alignment = efficient_alignment(x_l, y[:best_k])
        r_alignment = efficient_alignment(x_r, y[best_k:])

        return [l_alignment[0] + r_alignment[0], l_alignment[1] + r_alignment[1]]

def calculate_efficient(input_file, output_file):

    input_strings = input_string_generator(input_file)
    x_string = input_strings[0]
    y_string = input_strings[1]

    start_time = time.time()

    sequence = efficient_alignment(x_string, y_string)

    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)

    end_time = time.time()
    time_taken = (end_time - start_time)*1000

    f = open(output_file, "w+")
    f.write(str(int(min_cost)) + "\n")
    f.write(sequence[0]  + "\n")
    f.write(sequence[1] + "\n")
    f.write(str(time_taken) + "\n")
    f.write(str(memory_consumed) + "\n")
    f.close()

if __name__ == "__main__":
    input_arg = sys.argv[1]
    output_arg = sys.argv[2]

    calculate_efficient(input_arg, output_arg)
