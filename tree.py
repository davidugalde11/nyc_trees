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
import re
from math import asin, sin, cos, radians, sqrt

# Check if there is only one argument given:
if len(sys.argv) != 2:
    print('Usage: include only the tree.csv')
    sys.exit()
# Check if the file given is in csv format:
if not sys.argv[1].endswith('.csv'):
    print("The file may not be in the correct format or be corrupted.")
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
    # Create a new key value that contains the 'key' of tree:
    for tree in trees_final.keys():
        # Accomplish with re module that allows numerous delimiters, done for each tree:
        trees_final[tree]["Keys"] = re.split("-| ", tree)

    # Define function to print tree info:
    def tree_info(query):
        # Remove the first element which corresponds to command "treeinfo":
        query.remove(query[0])
        # Define matches variable as an empty list:
        matches = []
        for tree in trees_final.keys():
            if trees_final[tree]["Keys"] == query:
                print(f"Total number of such trees: {trees_final[tree]['Total']}")
                # Limit the number of zip codes to 5 for better visualization with list splicing:
                print(f"Zip codes in which this tree is found: {trees_final[tree]['Zip Code'][:5]} and more.")
                print(f"Borough containing the largest number of trees: {trees_final[tree]['Borough']}, with {trees[tree]['Borough Count']}")
                return
        for key in query:
            for tree in trees_final.keys():
                if key in trees_final[tree]["Keys"]:
                    matches.append(tree)
        print("All matching species:")
        for match in matches:
            print(match + "\n")



    # Define the most common function:
    def most_common():
        # Use list comprehension to create list of trees all lower values to prevent inconsistent data portrayal:
        tree_list_lower = [tree.lower() for tree in temp_tree]
        tree_count = Counter(tree_list_lower)
        most_common = tree_count.most_common(20)
        # Set number variable to add manual counter for better visualization:
        num = 1
        # Print a caption for values:
        print("Here are the twenty most popular trees in NYC:")
        for tree in most_common:
            print(f"{num}. {tree[0]}")
            num +=1

    # Define the get help function:
    def get_help():
        print("These are the available commands in the treequery program:")
        print("1. help")
        print("2. listtrees")
        print("3. treeinfo (with at least one input argument")
        print("4. nearby (with some input arguments")
        print("5. most_common")
        print("6. quit")

    # Define the list trees function:
    def list_trees():
        # Create temp list to modify without interfering with other functions:
        temp_tree_list = [tree.lower() for tree in tree_list]
        temp_tree_list.sort()
        for tree in temp_tree_list:
            print(tree)
            
            
            
    # Define the Haversine formula function:
    def haversine(lat1, lon1, lat2, lon2): # Compute the distance between two points defined by decimal latitude and longitude
        r = 6367.5 # Radius of Earth in km
        # Convert decimal latitude and longitude to radians
        d_lat = radians(lat2 - lat1)
        d_lon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        b = sin(d_lat/2)**2 + cos(lat1)*cos(lat2)*sin(d_lon/2)**2
        a = 2*asin(sqrt(b))
        return r * a #  The complete Haversine formula

    # Get center_point x and y coordinates (lat1 and lon1) as decimal arguments from user
    # Loop function over all x and y coordinates (lat2 and lon2) for all trees
        # lat1 = 
        # lon1 = 
        # lat2 = 
        # lon2 = 
        # radius = number in km
        # a = haversine(lat1, lon1, lat2, lon2)
        # if a <= radius:
            # add tree to a running total of trees of that same species/with that same name that are within the user-specified radius (in km)
            # add tree to running total of ALL trees that are within the user-specified radius a <= radius
        # In alphabetical order print tree's common name: <frequency of tree as a percentage relative to all other trees that are within the user-specified radius> aka number_of_unique_tree / number_of_all_trees_in_area as a %
        # if running total of all trees for a <= radius is == 0, print that there are no trees within that radius
        
        
    
    # Set interactive loop so user can keep asking questions until program ends:
    # Set a variable to true that can be changed to false when the loop is over:
    is_on = True
    # Welcome message:
    print("Welcome to the treequery program")
    print("To begin, try typing 'help' for the list of valid commands.")
    while is_on:
        # Get user input and reformat it to lowercase:
        command = input("Enter a command: ").lower()
        # Turn command into a list using re.split to also account for trees with "-" in their name.
        command = re.split("-| ", command)
        # Call appropriate function or response based on user input:
        if command[0] == 'help':
            get_help()
        elif command[0] == 'listtrees':
            list_trees()
        # Input the list we made as the parameter for tree_info():
        elif command[0] == 'treeinfo':
            tree_info(command)
        elif command[0] == 'nearby':
            pass
        elif command[0] == 'quit':
            print("Thank you for using treequery program!")
            is_on = False
            sys.exit()
        elif command[0] == 'commontrees':
            most_common()
        # Anything else the program can't account for is invalid:
        else:
            print("Invalid command. Type 'help' for the list of valid commands")


# Catch exception if file passed doesn't exist:
except FileNotFoundError:
    print("The file passed does not exist")
    sys.exit()
# Catch exception if there isn't reading permission for file:
except PermissionError:
    print("You don't have the appropriate permission to read this file")
    sys.exit()







