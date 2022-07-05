from ortools.algorithms import pywrapknapsack_solver
import os
import time
import pandas as pd
import csv

def store_direction(case):
    pathfiles = []
    root_path = 'kplib'
    instances = os.listdir(root_path)
    NumbersOfValues = ['n00050', 'n00100', 'n00200', 'n00500', 'n01000']
    for files in instances:
        for NumOfVal in NumbersOfValues:
            pathfiles.append(f"{root_path}\{files}\{NumOfVal}\R01000\{case}")
    return pathfiles
def get_info(path):
    with open(path, 'r') as fi:
        content = fi.read()
        content = content.split('\n')
        problem_size = int(content[1])
        capicity = [int(content[2])]
        values = []
        weights = [[]]
        for item in content[4:-1]:
            value, weight = item.split(" ")
            values.append(int(value))
            weights[0].append(int(weight))
    return problem_size, capicity, values, weights

def main():
    cases = ['s000.kp', 's001.kp', 's002.kp']
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    TIME_LIMIT = 60
    for case in cases: 
        ListOfPathFiles = store_direction(case)
        list_weight = []
        list_values = []
        list_optimal = []
        number_values = [50,100,200,500,1000]
        for file in ListOfPathFiles:
            n, capacities, values, weights = get_info(file)
            solver.Init(values, weights, capacities)
            solver.set_time_limit(TIME_LIMIT)
            t_0 = time.time()
            computed_value = solver.Solve()
            t_1 = time.time() - t_0
            packed_items = []
            packed_weights = []
            total_weight = 0
            print('Total value =', computed_value)
            list_values.append(computed_value)
            for i in range(len(values)):
                if solver.BestSolutionContains(i):
                    packed_items.append(i)
                    packed_weights.append(weights[0][i])
                    total_weight += weights[0][i]
            print(f'Solution for {file}: ')
            print('Total weight:', total_weight)
            list_weight.append(total_weight)
            print('Packed items:', packed_items)
            print('Packed_weights:', packed_weights)
            if t_1 > TIME_LIMIT:
                list_optimal.append('_')
            else:
                list_optimal.append('Optimal')
            print(f'Optimal or not:{list_optimal[-1]}')
        #Data processing
        values_file = []
        weight_file = []
        Optimal_file = []
        count = 1
        for index in list_values:
            if count % 5 == 0:
                features = list_values[count-5:count]
                values_file.append(features)
            count += 1
        with open(f'values({case}).csv', 'w+') as fov:
            write = csv.writer(fov)
            write.writerow(number_values)
            write.writerows(values_file)
        count = 1
        for index in list_weight:
            if count % 5 == 0:
                features = list_weight[count-5:count]
                weight_file.append(features)
            count += 1
        with open(f'weights({case}).csv', 'w+') as fow:
            write = csv.writer(fow)
            write.writerow(number_values)
            write.writerows(weight_file)
        count = 1
        for index in list_optimal:
            if count % 5 == 0:
                features = list_optimal[count-5:count]
                Optimal_file.append(features)
            count += 1
        with open(f'optimals({case}).csv', 'w+') as foo:
            write = csv.writer(foo)
            write.writerow(number_values)
            write.writerows(Optimal_file)

if __name__ == '__main__':
    main()