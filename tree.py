import pandas as pd
import numpy as np
from collections import Counter

# print("Welcome to the treequery program.")
# print("To begin, try typing 'help' for the list of valid commands.")
# command = input("Enter a command: ").lower()
# if command == 'help':
#     print("The list of available commands are: "
#           "1. 'help' for a help page about each valid program command."
#           "2. 'listtrees' for an alphabetical list of full tree species common names."
#           "3. 'treeinfo <tree_species_names>' for information about a species of tree, including total number of such trees, zip codes in which this tree is found, the borough containing the largest number of such trees, and the average diameter of trees of this type."
#           "4. 'nearby <latitude> <longitude> <distance>' for a list of full species common names and frequencies of all trees within the specified distance (km) from the given GPS point (latitude and longitude, both being fixed-point decimal numbers)."
#           "5. 'quit' to quit the application.")

pd.set_option('display.max_rows', None)
data = pd.read_csv('/Users/davidugalde/Downloads/Tree_Data.csv')
# print(data)

# print(data['spc_common'].nunique())

trees_list = []
for tree in data['spc_common']:
    if tree not in trees_list:
        trees_list.append(tree)
print(trees_list)

tree_list_final = [str(x).lower() for x in trees_list]
print(tree_list_final)

trees = {

}

arr = np.array(data['spc_common'])
print(arr)
arr = arr.astype(str)
np.char.lower(arr)
print(arr)

for tree in tree_list_final:
    trees[tree] = {}

print(trees)

for tree in tree_list_final:
    trees[tree]['Total'] = np.count_nonzero(arr == tree)
    # trees[tree]['Zip Code'] = data.query(f'spc_common=={tree}')['postcode']
    l = data.loc[data['spc_common'] == tree, 'postcode'].tolist()
    trees[tree]['Zip Code'] = list(dict.fromkeys(l))
    b = data.loc[data['spc_common'] == tree, 'borough'].tolist()
    try:
        trees[tree]['Borough'] = max(set(b), key=b.count)
        trees[tree]['Borough Count'] = b.count(trees[tree]['Borough'])
    except ValueError:
        pass
    d = data.loc[data['spc_common'] == tree, 'tree_dbh'].tolist()
    try:
        mean = sum(d) / len(d)
        trees[tree]['Average diameter'] = round(mean, 2)
    except ZeroDivisionError:
        pass

print(trees)
print(trees['white oak'])


def tree_info(tree):

    print(f"Total number of such trees: {trees[tree]['Total']}")
    print(f"Zip codes in which this tree is found: {trees[tree]['Zip Code'][:5]}")
    print(
        f"Borough containing the largest number of such trees: {trees[tree]['Borough']}, with {trees[tree]['Borough Count']}")
    print(f"Average diameter: {trees[tree]['Average diameter']}")

def most_common():
    data['total'] = data['spc_common']
    common = data.pipe(lambda x: x.div(x['total'], axis='index')).applymap('{:.0%}'.format)
    print(common)


print(arr)
# is_on = True
# while is_on:
#     tree = input("Enter tree: ").lower()
#     if tree == "q":
#         is_on = False
#     if tree in trees:
#         tree_info(tree)


