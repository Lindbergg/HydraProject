# import .csv from path in the below method #
import pandas as pd
import os
import numpy as np

from Players import Player



# Function to read CSV file from a given path
def read_csv_file(path):
    #DataFrame from 1 csv file
    pand = pd.DataFrame()

    # read the csv file in the given path
    with open (path, 'r') as file:
        # Read the CSV file into a DataFrame
        pand = pd.read_csv(file)

        
    return pand

def main():
    # Path to the file containing CSV file
    path = 'C:\Python\Hero Wars - Brasil - HydraHelperSheet.csv'
    
    # Read CSV file
    DamageMatrix = read_csv_file(path)


   
if __name__ == "__main__":
    main()
