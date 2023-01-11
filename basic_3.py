import time
import psutil
import sys
import numpy as np

delta = 30 
alpha = [[0, 110, 48, 94],
        [110, 0, 118, 48],
        [48, 118, 0, 110],
        [94, 48, 110, 0]]

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

def basic_alignment(input_file, output_file):

    start_time = time.time()

    input_strings = input_string_generator(input_file)
    x_string = input_strings[0]
    y_string = input_strings[1]
    m = len(x_string)
    n = len(y_string)

    opt = np.zeros((m+1, n+1))

    for i in range(m+1):
        opt[i][0] = delta*i

    for i in range(n+1):
        opt[0][i] = delta*i

    for i in range(1,m+1):
        for j in range(1,n+1):
            x = x_string[i-1]
            y = y_string[j-1]

            alpha_cost = alpha[matrix_match(x)][matrix_match(y)]

            opt[i][j] = min(alpha_cost + opt[i-1][j-1], delta + opt[i-1][j], delta + opt[i][j-1])

    i = m
    j = n

    result_string_x = '';
    result_string_y = '';

    while i > 0 or j > 0:
        if opt[i][j] == opt[i-1][j] + delta:
            result_string_x += x_string[i-1]
            result_string_y += '_'
            i -= 1
        elif opt[i][j] == opt[i][j-1] + delta:
            result_string_x += '_'
            result_string_y += y_string[j-1]
            j -= 1
        else:
            result_string_x += x_string[i-1]
            result_string_y += y_string[j-1]               
            i -= 1
            j -= 1

    result_string_x = result_string_x[::-1]
    result_string_y = result_string_y[::-1]  

    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)

    end_time = time.time()
    time_taken = (end_time - start_time)*1000

    f = open(output_file, "w+")
    f.write(str(int(opt[m][n])) + "\n")
    f.write(result_string_x  + "\n")
    f.write(result_string_y + "\n")
    f.write(str(time_taken) + "\n")
    f.write(str(memory_consumed) + "\n")
    f.close()

def matrix_match(char):
    if char == 'A':
        return 0
    elif char == 'C':
        return 1
    elif char == 'G':
        return 2
    elif char == 'T':
        return 3

def check_cost(x, y):

    cost = 0 

    for i in range(len(x)):
        x = x[i]
        y = y[i]

        if x == '_' or y == '_':
            cost += delta 
        elif x != y: 
            cost += alpha[matrix_match(x)][matrix_match(y)]  

    return cost

if __name__ == "__main__":
    input_arg = sys.argv[1]
    output_arg = sys.argv[2]

    basic_alignment(input_arg, output_arg)