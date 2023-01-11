import sys
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

delta = 30 
alpha = [[0, 110, 48, 94],
        [110, 0, 118, 48],
        [48, 118, 0, 110],
        [94, 48, 110, 0]]

def matrix_match(char):
    if char == 'A':
        return 0
    elif char == 'C':
        return 1
    elif char == 'G':
        return 2
    elif char == 'T':
        return 3

def check_cost(x_in, y_in):

    cost = 0 

    for i in range(len(x_in)):
        x = x_in[i]
        y = y_in[i]

        if x == '_' or y == '_':
            cost += delta 
        elif x != y: 
            cost += alpha[matrix_match(x)][matrix_match(y)]  

    return cost

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

def checker_with_no_solution_file(file_basic, file_efficient):
    basic_file = open(file_basic).read().splitlines()
    efficient_file = open(file_efficient).read().splitlines()

    basic_output_x = basic_file[1]
    basic_output_y = basic_file[2]

    efficient_output_x = efficient_file[1]
    efficient_output_y = efficient_file[2]

    length_check = False
    char_check = False
    costs_check = False

    # check lengths are all the same
    if(len(basic_output_x) == len(efficient_output_x)):
        length_check = True

    # check same characters are present
    if(basic_output_x.translate(str.maketrans('', '', '_')) == efficient_output_x.translate(str.maketrans('', '', '_')) ):
        if(basic_output_y.translate(str.maketrans('', '', '_')) == efficient_output_y.translate(str.maketrans('', '', '_'))):
            char_check = True

    # check costs match between basic and efficient in output files and in internal check
    basic_cost = check_cost(basic_output_x, basic_output_y)
    efficient_cost = check_cost(efficient_output_x, efficient_output_y)

    if(basic_cost == int(float(basic_file[0])) == efficient_cost == int(float(efficient_file[0]))):
        costs_check = True

    char_check_color = bcolors.OKGREEN if char_check else bcolors.FAIL
    length_check_color = bcolors.OKGREEN if length_check else bcolors.FAIL
    costs_check_color = bcolors.OKGREEN if costs_check else bcolors.FAIL

    print("Length check: " + length_check_color + str(length_check) + bcolors.ENDC)
    print('Char check: ' + char_check_color + str(char_check) + bcolors.ENDC)
    print('Cost check: ' + costs_check_color + str(costs_check) + bcolors.ENDC)
    print('     Basic cost: ' + str(basic_cost))
    print('     Efficient cost: ' + str(efficient_cost))

def checker(file_basic, file_efficient, file_solution):
    basic_file = open(file_basic).read().splitlines()
    efficient_file = open(file_efficient).read().splitlines()
    solution_file = open(file_solution).read().splitlines()

    basic_output_x = basic_file[1]
    basic_output_y = basic_file[2]

    efficient_output_x = efficient_file[1]
    efficient_output_y = efficient_file[2]

    solution_output_x = solution_file[1]
    solution_output_y = solution_file[2]

    length_check = False
    char_check = False
    costs_check = False

    # check lengths are all the same
    if(len(basic_output_x) == len(efficient_output_x) == len(solution_output_x)):
        length_check = True

    # check same characters are present
    if(basic_output_x.translate(str.maketrans('', '', '_')) == efficient_output_x.translate(str.maketrans('', '', '_')) == solution_output_x.translate(str.maketrans('', '', '_'))):
        if(basic_output_y.translate(str.maketrans('', '', '_')) == efficient_output_y.translate(str.maketrans('', '', '_')) == solution_output_y.translate(str.maketrans('', '', '_'))):
            char_check = True

    # check costs match the solution in output files and in internal checks
    basic_cost = check_cost(basic_output_x, basic_output_y)
    efficient_cost = check_cost(efficient_output_x, efficient_output_y)
    solution_cost = check_cost(solution_output_x, solution_output_y)

    if(basic_cost == int(float(basic_file[0])) == efficient_cost == int(float(efficient_file[0])) == solution_cost == int(float(solution_file[0]))):
        costs_check = True

    char_check_color = bcolors.OKGREEN if char_check else bcolors.FAIL
    length_check_color = bcolors.OKGREEN if length_check else bcolors.FAIL
    costs_check_color = bcolors.OKGREEN if costs_check else bcolors.FAIL

    print("Length check: " + length_check_color + str(length_check) + bcolors.ENDC)
    print('Char check: ' + char_check_color + str(char_check) + bcolors.ENDC)
    print('Cost check: ' + costs_check_color + str(costs_check) + bcolors.ENDC)
    print('     Basic cost: ' + str(basic_cost))
    print('     Efficient cost: ' + str(efficient_cost))
    print('     Solution cost: ' + str(solution_cost))

    return

if __name__ == "__main__":
    file_basic = sys.argv[1]
    file_efficient = sys.argv[2]

    # ex: python3 checker.py output_basic.txt output_efficient.txt output_solution.txt
    if len(sys.argv) == 4:
        file_solution = sys.argv[3]
        checker(file_basic, file_efficient, file_solution)

    # ex: python3 checker.py output_basic.txt output_efficient.txt
    elif len(sys.argv) == 3:
        checker_with_no_solution_file(file_basic, file_efficient)