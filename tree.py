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
from math import radians, cos, sin, asin, sqrt

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
    data.columns = ["Serial", "N/A", "Condition", "Tree", "Zip Code", "Borough", "Neighborhood", "Latitude", "Longitude"]
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
        # For part 4 get the count associated for each borough:
        trees[tree]["Brooklyn"] = bor_list.count("Brooklyn")
        trees[tree]["Bronx"] = bor_list.count("Bronx")
        trees[tree]["Queens"] = bor_list.count("Queens")
        trees[tree]["Manhattan"] = bor_list.count("Manhattan")
        trees[tree]["Staten Island"] = bor_list.count("Staten Island")
        # We do the same for both x and y coordinates and set them together as tuple:
        lan_list = data.loc[data['Tree'] == tree, 'Latitude'].tolist()
        lon_list = data.loc[data['Tree'] == tree, 'Longitude'].tolist()
        # We obtain list of tuples through zip and list function:
        trees[tree]['Coordinates'] = list(zip(lan_list, lon_list))
    # Use dictionary comprehension to convert keys to lower case:
    trees_final = {k.lower(): v for k, v in trees.items()}
    # Create a new key value that contains the 'key' of tree:
    for tree in trees_final.keys():
        # Accomplish with re module that allows numerous delimiters, done for each tree:
        trees_final[tree]["Keys"] = re.split("-| ", tree)
    # Get the total number of threes in the csv file give through len from arr created with every tree name:
    nyc_trees = len(arr)
    # Create a new numpy array so we are able to access each borough's sum with Counter:
    np_boroughs = np.array(data["Borough"])
    # Use the Counter Method to get the sum of each borough in the form of the dictionary created:
    borough_count = Counter(np_boroughs)
    # For each borough access their respective value from np_boroughs dictionary:
    brooklyn_count = borough_count["Brooklyn"]
    bronx_count = borough_count["Bronx"]
    manhattan_count = borough_count["Manhattan"]
    queens_count = borough_count["Queens"]
    staten_island_count = borough_count["Staten Island"]

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
        print("\nAll matching species:\n")
        # Define variables needed for percentage with 0 to add onto during loop:
        match_nyc = 0
        match_manhattan = 0
        match_bronx = 0
        match_brooklyn = 0
        match_queens = 0
        match_staten_island = 0
        for match in matches:
            print(match + "\n")
            # For every match in the matches dictionary add on to respective value for percentage calculation:
            match_nyc += trees_final[match]["Total"]
            match_manhattan += trees_final[match]["Manhattan"]
            match_bronx += trees_final[match]["Bronx"]
            match_brooklyn += trees_final[match]["Brooklyn"]
            match_queens += trees_final[match]["Queens"]
            match_staten_island += trees_final[match]["Staten Island"]
        # Print output using round  function, formatting tools and tab special character:
        print("\nPopularity in the city:\n")
        print(f"NYC:  \t\t\t\t{match_nyc :5} ({nyc_trees :5}){round(((match_nyc/nyc_trees) * 100), 2) :5}%")
        print(f"Manhattan:   \t\t\t{match_manhattan :5} ({manhattan_count :5}) {round(((match_manhattan / manhattan_count) * 100), 2) :5}%")
        print(f"Bronx:    \t\t\t{match_bronx :5} ({bronx_count :5}) {round(((match_bronx / bronx_count) * 100), 2) :5}%")
        print(f"Brooklyn: \t\t\t{match_brooklyn :5} ({brooklyn_count :5}){round(((match_brooklyn / brooklyn_count) * 100), 2) :5}%")
        print(f"Queens: \t\t\t{match_queens :5} ({queens_count :5}){round(((match_queens / queens_count) * 100), 2) :5}%")
        print(f"Staten Island: \t\t\t{match_staten_island :5} ({staten_island_count :5}){round(((match_staten_island / staten_island_count) * 100), 2) :5}%")

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
        print("5. common")
        print("6. quit")

    # Define the list trees function:
    def list_trees():
        # Create temp list to modify without interfering with other functions:
        temp_tree_list = [tree.lower() for tree in tree_list]
        # Use sort function to alphabetize list of trees:
        temp_tree_list.sort()
        for tree in temp_tree_list:
            print(tree)

    # Define the nearby tree function:
    def nearby(query):
        # There can't be more or less than three arguments and this if statement will catch that possible error:
        if len(query) != 4:
            print("Too many or missing arguments. Please provide latitude, longitude, and distance(km) only.")
            return
        # Remove function name from list:
        query.remove(query[0])
        # Create a dictionary that will input the trees as keys and their total as values:
        matches = {}
        # Radius of earth in km for the Harversine formula:
        R = 6371
        # Use radians from math to get the correct format for Harvesine formula:
        # Convert string into float values:
        lat1 = radians(float(query[0]))
        lon1 = radians(float(query[1]))
        distance1 = float(query[2])
        # Loop through every tree to check for matches:
        for tree in trees_final.keys():
            # assign key and a value of 0 we can add onto if there's a match:
            matches[tree] = 0
            # access coordinates we defined at the  beginning of our program:
            for coordinate in trees_final[tree]["Coordinates"]:
                # Access their lat and lon values through indexing the coordinate tuple:
                lat2 = radians(float(coordinate[0]))
                lon2 = radians(float(coordinate[1]))
                # Set variable of delta latitude and delta longitude for simplicity when computing Harverine formula:
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                # Use the sin, cos, asin and square root functions we imported from math:
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                distance2 = c * R
                # If the distance is less than the specified distance we have a match:
                if distance2 <= distance1:
                    matches[tree] += 1
        # Get match total by adding all values of dictionary with sum function:
        total_match = sum(matches.values())
        # Catch if there aren't any matches, let the user know, and leave function:
        if total_match == 0:
            print("No trees are present within this distance.")
            return
        # Loop through every tree in matches:
        for tree in matches.keys():
            # Use continue to not output any match of 0.0%
            if matches[tree] == 0:
                continue
            # Print all the tree matches and their value represented as a percentage:
            print(f"{tree:8}: {round(((matches[tree] / total_match) * 100), 2) :8}%")


    # Set interactive loop so user can keep asking questions until program ends:
    # Set a variable to true that can be changed to false when the loop is over:
    is_on = True
    # Welcome message:
    print("Welcome to the treequery program")
    print("To begin, try typing 'help' for the list of valid commands.")
    while is_on:
        # Get user input and reformat it to lowercase:
        user_input = input("Enter a command: ").lower()
        command = user_input.split()
        # Call appropriate function or response based on user input:
        if command[0] == 'help':
            get_help()
        elif command[0] == 'listtrees':
            list_trees()
        # Input the list we made as the parameter for tree_info():
        elif command[0] == 'treeinfo':
            # Turn command into a list using re.split to also account for trees with "-" in their name.
            command = re.split("-| ", user_input)
            tree_info(command)
        elif command[0] == 'nearby':
            nearby(command)
        elif command[0] == 'quit':
            print("Thank you for using treequery program!")
            is_on = False
            sys.exit()
        elif command[0] == 'common':
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









