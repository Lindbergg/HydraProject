# import .csv from path in the below method #
import pandas as pd
import os
import numpy as np
import random
import math

from Player import Player
from Hydra import Hydra
from Head import Head
from Cycle import Cycle

# sample data in multline commet
"""
Name                   , Darkness - Dreadful, Water - Dreadful, Earth - Dreadful, Light - Dreadful, Wind - Dreadful, Fire - Dreadful, Darkness - Ancient, Water - Ancient, Earth - Ancient, Light - Ancient, Wind - Ancient, Fire - Ancient, Darkness - Elder, Water - Elder, Earth - Elder, Light - Elder, Wind - Elder, Fire - Elder, Darkness - Common, Water - Common, Earth - Common, Light - Common, Wind - Common, Fire - Common
raf41983               , "60,295,650"       , 0               , 0               , "65,497,757"    , 0              , "106,981,939"  , "54,533,157"      , "39,451,447"   , "36,133,447"   , "54,533,157"   , "34,528,524"  , "54,533,157"  , 0               , 0            , 0            , 0            , "17,699,730", 0           , 0                , 0             , 0             , 0             , 0            , 0
Virus                  , 0                  , 0               , 0               , 0               , 0              , 0              , "1,606,936"       , "9,686,171"    , "1,518,712"    , "7,581,136"    , "1,176,017"   , "15,675,659"  , "12,838,616"    , "12,240,813" , "5,462,147"  , "7,547,913"  , "11,780,448", "15,546,713", 0                , 0             , 0             , 0             , 0            , "5,946,906"
wojownik               , 0                  , 0               , 0               , 0               , 0              , 0              , 0                 , "6,859,851"    , "2,591,022"    , 0              , "3,740,388"   , "15,064,513"  , "13,489,869"    , "9,861,676"  , "7,050,947"  , "8,635,407"  , 0           , "13,780,247", 0                , 0             , 0             , 0             , 0            , 0
.++ Japanese Characters, 0                  , 0               , 0               , 0               , 0              , 0              , "692,165"         , "6,256,132"    , "808,046"      , "5,425,548"    , "641,439"     , "11,704,959"  , "13,122,459"    , "11,030,479" , "9,743,833"  , "9,467,052"  , "12,947,519", "14,668,240", "5,946,906"      , "5,946,906"   , "5,234,295"   , "5,946,906"   , 0            , 0
xIIHOBBITIIx           , 0                  , 0               , 0               , 0               , 0              , "577,795"      , "7,129,459"       , "5,861,338"    , "2,015,873"    , 0              , "539,619"     , "15,648,435"  , "12,896,488"    , "12,691,457" , "4,908,820"  , "5,421,476"  , 0           , "13,988,022", "5,946,906"      , "5,946,906"   , 0             , 0             , 0            , "5,946,906"
"""

def read_file_csv(path):
    df = pd.read_csv(path, sep=',', engine='python')
    return df


def simulated_annealing(cycle, players, hydras, max_iter=10000, initial_temp=100000, cooling_rate=0.999):
    # Initialize random assignment: Each player attacks 3 random hydra heads
    assignment = {}
    for player in players:
        attacks = []
        for _ in range(3):
            valid_hydras = [h for h in hydras if h.is_alive()]
            if not valid_hydras:
                # No hydras alive, handle gracefully - e.g. break loop or return
                break  # or raise Exception, or return some result

            hydra = random.choice(valid_hydras)
            head = random.choice(hydra.heads)
            attacks.append((hydra.name, head.name))
        assignment[player.name] = attacks

    for hydra in hydras:
        hydra.reset()
    for player in players:
        player.attacks_left = 3  # Reset players' attacks left
    current_score = cycle.apply_assignment(assignment)
    best_assignment = assignment.copy()
    best_score = current_score
    temperature = initial_temp

    for i in range(max_iter):
        # Create a neighbor assignment by randomly changing one attack
        new_assignment = {p: a[:] for p, a in assignment.items()}  # deep copy of lists

        # Randomly pick a player and attack index to mutate
        p = random.choice(players).name
        attack_idx = random.randint(0, 2)

        hydra = random.choice(hydras)
        valid_hydras = [h for h in hydras if h.is_alive() and len(h.heads) > 0]
        if not valid_hydras:
            print("No valid hydras with heads!")
            break
        hydra = random.choice(valid_hydras)
        head = random.choice(hydra.heads)
        new_assignment[p][attack_idx] = (hydra.name, head.name)

        # Reset hydras
        for h in hydras:
            h.reset()

        for player in players:
            player.attacks_left = 3  # Reset players' attacks left
        new_score = cycle.apply_assignment(new_assignment)
        
        delta = new_score - current_score

        # Accept new assignment if better or with probability (simulated annealing)
        if delta > 0 or random.random() < math.exp(delta / temperature):
            assignment = new_assignment
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_assignment = new_assignment

        # Cool down temperature
        temperature *= cooling_rate
        if temperature < 1e-3:
            break
        
        # Optionally print progress every 1000 iterations (avoid too much spam)
        if i % 1000 == 0:
            hydras_alive = [h for h in hydras if len(h.heads) > 0]
            heads_alive = sum(len(h.heads) for h in hydras_alive)
            print(f"Iteration {i}: Current score = {current_score}, Best score = {best_score}, Heads alive = {heads_alive}, Temp = {temperature:.2f}")
            
            # Optionally, you can print the current assignment players on what head
            for player, attacks in assignment.items():
                pass
                #print(f"  {player}: {attacks}")
        

    return best_assignment, best_score


def initialize_hydras_and_heads(DamageMatrix):
    hydras = []
    hydra_dict = {}
    bottom_row = DamageMatrix.iloc[-1, 1:]

    for column in DamageMatrix.columns[1:]:
        parts = column.split(" - ")
        if len(parts) != 2:
            print(f"Skipping malformed column: {column}")
            continue
        head_name, hydra_name = parts
        
        hydra = hydra_dict.setdefault(hydra_name, Hydra(hydra_name, []))
        if hydra not in hydras:
            hydras.append(hydra)

        health_str = bottom_row[column]
        try:
            health_val = int(str(health_str).replace(",", ""))
        except Exception as e:
            print(f"Invalid health value for column '{column}': {health_str}")
            continue
        
        head = Head(head_name, hydra)
        head.startHealth = health_val
        head.health = health_val
        hydra.heads.append(head)
    
    return hydras

def main():
    # Path to CSV file
    path = r'.\Hero Wars - Brasil - HydraHelperSheet.csv'
    
    # Read CSV file
    DamageMatrix = read_file_csv(path)

    # Create players from rows (except last row)
    players = []
    for index, row in DamageMatrix.iterrows():
        if index == DamageMatrix.shape[0] - 1:
            # Skip last row, which contains health info for heads
            continue
        
        # Create a DataFrame with the damage columns for this player (1 row, all columns except Name)
        dataframeRowWithHeaders = DamageMatrix.iloc[index, 1:].to_frame().T
        dataframeRowWithHeaders.columns = DamageMatrix.columns[1:]
        
        player = Player(row['Name'], dataframeRowWithHeaders)
        players.append(player)
    
    # Create hydras and heads from column headers
    hydras = []
    hydra_dict = {}

    # Last row contains heads health per column
    bottomRow = DamageMatrix.iloc[DamageMatrix.shape[0] - 1, 1:]
    
    for column in DamageMatrix.columns[1:]:
        head_name, hydra_name = column.split(" - ")

        if hydra_name == "Dreadful":
            # Skip Dreadful hydras
            continue

        if hydra_name not in hydra_dict:
            hydra = Hydra(hydra_name, [])
            hydra_dict[hydra_name] = hydra
            hydras.append(hydra)
        else:
            hydra = hydra_dict[hydra_name]

        head = Head(head_name, hydra)
        health_str = bottomRow[column]
        head.startHealth = int(health_str.replace(",", ""))
        head.health = head.startHealth

        hydra.heads.append(head)

    return players, hydras
       

def GameSim(players, hydras):
    print("Starting simulation...")
    cycle = Cycle(players, hydras)

    best_assignment, best_score = simulated_annealing(cycle, players, hydras)

    print(f"Best total worth found: {best_score}")

    # Optionally apply best_assignment again to display final results
    cycle.apply_assignment(best_assignment)
    


if __name__ == "__main__":
    # Call the main function
    players, hydras = main()
    
    GameSim(players, hydras)
    