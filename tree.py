#!/usr/bin/python3
# Usage: tree_query.py
# Authors: Ann Lee, David Ugalde, Jenny Zhang, Nadia Fayed
# Created on: November 1st, 2022
# Description: Make an interactive program with nyc tree data.
# Version: 1
# **************************************************************

# Import modules needed for program
import sys
import pandas as pd
import numpy as np
from collections import Counter

# Check if there is only one argument given:
if len(sys.argv) != 2:
    print('Usage: include only the tree.csv')
    sys.exit()

# Try to create a data frame with Pandas:
try:
    # Create a data frame from the input csv file:
    data = pd.read_csv(sys.argv[1])
    # Give data frame columns names:
    data.columns = ["Serial", "N/A", "Condition", "Tree", "Zip Code", "Borough", "Neighborhood", "X coor", "Y coor"]
    # Create temporary list with all trees:
    temp_tree = data["Tree"].values.tolist()
    # Use loop to get unique list of trees:
    tree_list = []
    for tree in temp_tree:
        if tree not in tree_list:
            tree_list.append(tree)
    # Sort list alphabetically:
    tree_list.sort()
    # Create a dictionary with every tree name as keys for their own dictionary:
    trees = {}
    # Create a numpy arr to get a count of trees total:
    arr = np.array(data['Tree'])

    for tree in tree_list:
        trees[tree] = {}
        # From array get a total of times the tree appears in array:
        trees[tree]['Total'] = np.count_nonzero(arr == tree)
        # Use pandas loc function to access multiple columns values and format them into list:
        zip_list = data.loc[data['Tree'] == tree, 'Zip Code'].tolist()
        # Now we add these Zip Codes to our dictionary:
        trees[tree]['Zip Code'] = list(dict.fromkeys(zip_list))
        # For Borough, we repeat but also add functionality to get the max value and its count:
        bor_list = data.loc[data['Tree'] == tree, 'Borough'].tolist()
        # Use max function to get the borough that appears the most:
        trees[tree]['Borough'] = max(set(bor_list), key=bor_list.count)
        # Now get the actual count from bor list with count functions:
        trees[tree]['Borough Count'] = bor_list.count(trees[tree]['Borough'])
        # We do the same for both x and y coordinates and set them together as tuple:
        x_list = data.loc[data['Tree'] == tree, 'X coor'].tolist()
        y_list = data.loc[data['Tree'] == tree, 'Y coor'].tolist()
        # We obtain list of tuples through zip and list function:
        trees[tree]['Coordinates'] = list(zip(x_list, y_list))
    # Use dictionary comprehension to convert keys to lower case:
    trees_final = {k.lower(): v for k, v in trees.items()}

    # Define function to print tree info:
    def tree_info(tree):
        print(f"Total number of such trees: {trees_final[tree]['Total']}")
        # Limit the number of zip codes to 5 for better visualization with list splicing:
        print(f"Zip codes in which this tree is found: {trees_final[tree]['Zip Code'][:5]} and more.")
        print(f"Borough containing the largest number of trees: {trees_final[tree]['Borough']}, with {trees[tree]['Borough Count']}")

    def most_common():
        # Use list comprehension to create list of trees all lower values to prevent inconsistent data portrayal:
        tree_list_lower = [tree.lower() for tree in temp_tree]
        tree_count = Counter(tree_list_lower)
        most_common = tree_count.most_common(20)
        # Set number variable to add manual counter for better visualization:
        num = 1
        for tree in most_common:
            print(f"{num}. {tree[0]}")
            num +=1

# Catch exception if file passed doesn't exist:
except FileNotFoundError:
    print("The file passed does not exist")
    sys.exit()
# Catch exception if there isn't reading permission for file:
except PermissionError:
    print("You don't have the appropriate permission to read this file")
    sys.exit()





