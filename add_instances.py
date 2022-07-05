import pandas as pd
cases = ['s000.kp', 's001.kp', 's002.kp']
for case in cases: 
    vals = pd.read_csv(f'values({case}).csv')
    wes = pd.read_csv(f'weights({case}).csv')
    ops = pd.read_csv(f'optimals({case}).csv')
    ins_col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    vals.insert(loc=0, column='Instances', value=ins_col)
    wes.insert(loc=0, column='Instances', value=ins_col)
    ops.insert(loc=0, column='Instances', value=ins_col)
    vals.to_csv(f'values({case}).csv', index = False)
    wes.to_csv(f'weights({case}).csv', index = False)
    ops.to_csv(f'optimals({case}).csv', index = False)