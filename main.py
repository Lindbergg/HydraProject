# import .csv from path in the below method #
import pandas as pd
import os
import numpy as np

from Player import Player

# sample data in multline commet
"""
Name                   , Darkness - Dreadful, Water - Dreadful, Earth - Dreadful, Light - Dreadful, Wind - Dreadful, Fire - Dreadful, Darkness - Ancient, Water - Ancient, Earth - Ancient, Light - Ancient, Wind - Ancient, Fire - Ancient, Darkness - Elder, Water - Elder, Earth - Elder, Light - Elder, Wind - Elder, Fire - Elder, Darkness - Common, Water - Common, Earth - Common, Light - Common, Wind - Common, Fire - Common
raf41983               , "60,295,650"       , 0               , 0               , "65,497,757"    , 0              , "106,981,939"  , "54,533,157"      , "39,451,447"   , "36,133,447"   , "54,533,157"   , "34,528,524"  , "54,533,157"  , 0               , 0            , 0            , 0            , "17,699,730", 0           , 0                , 0             , 0             , 0             , 0            , 0
Virus                  , 0                  , 0               , 0               , 0               , 0              , 0              , "1,606,936"       , "9,686,171"    , "1,518,712"    , "7,581,136"    , "1,176,017"   , "15,675,659"  , "12,838,616"    , "12,240,813" , "5,462,147"  , "7,547,913"  , "11,780,448", "15,546,713", 0                , 0             , 0             , 0             , 0            , "5,946,906"
wojownik               , 0                  , 0               , 0               , 0               , 0              , 0              , 0                 , "6,859,851"    , "2,591,022"    , 0              , "3,740,388"   , "15,064,513"  , "13,489,869"    , "9,861,676"  , "7,050,947"  , "8,635,407"  , 0           , "13,780,247", 0                , 0             , 0             , 0             , 0            , 0
.++ Japanese Characters, 0                  , 0               , 0               , 0               , 0              , 0              , "692,165"         , "6,256,132"    , "808,046"      , "5,425,548"    , "641,439"     , "11,704,959"  , "13,122,459"    , "11,030,479" , "9,743,833"  , "9,467,052"  , "12,947,519", "14,668,240", "5,946,906"      , "5,946,906"   , "5,234,295"   , "5,946,906"   , 0            , 0
xIIHOBBITIIx           , 0                  , 0               , 0               , 0               , 0              , "577,795"      , "7,129,459"       , "5,861,338"    , "2,015,873"    , 0              , "539,619"     , "15,648,435"  , "12,896,488"    , "12,691,457" , "4,908,820"  , "5,421,476"  , 0           , "13,988,022", "5,946,906"      , "5,946,906"   , 0             , 0             , 0            , "5,946,906"
"""

# Function to read CSV file from a given path
def read_file_csv(path):
    #DataFrame from 1 csv file
    pand = pd.DataFrame()

    # read the csv file in the given path
    with open (path, 'r') as file:
        # Read the CSV file into a DataFrame
        pand = pd.read_csv(file, sep=',')
    return pand

def main():
    # Path to the file containing CSV file
    path = '.\Hero Wars - Brasil - HydraHelperSheet.csv'
    
    # Read CSV file
    DamageMatrix = read_file_csv(path)

    

    # print column header names
    print(DamageMatrix.columns)

    # create a list of players
    players = []
    # iterate through the rows of the DataFrame
    for index, row in DamageMatrix.iterrows():
        if(index == DamageMatrix.shape[0] - 1):
            continue
        
        # create a Player object for each row
        player = Player(row['Name'], row[1:])
        # append the Player object to the list
        players.append(player)
    
    #print the players
    for player in players:
        print(f"Player Name: {player.name}")
        print(f"All Targets: {player.allTargets}")
        print()
    
        


   
if __name__ == "__main__":
    main()
    
