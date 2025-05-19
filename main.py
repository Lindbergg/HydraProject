import pandas as pd
import random
import math
import os


from Player import Player
from Hydra import Hydra
from Head import Head
from Cycle import Cycle



class HydraSimulator:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.players = []
        self.hydras = []

    def read_csv(self):
        try:
            return pd.read_csv(self.csv_path, sep=',', engine='python')
        except Exception as e:
            print(f"[ERROR] Failed to read CSV file: {e}")
            return None

    def load_data(self):
        df = self.read_csv()
        if df is None:
            return False

        self.players.clear()
        for index, row in df.iloc[:-1].iterrows():  # skip last row (heads health)
            damage_data = row[1:].to_frame().T
            damage_data.columns = df.columns[1:]
            self.players.append(Player(row['Name'], damage_data))

        self.hydras.clear()
        hydra_map = {}
        health_row = df.iloc[-1, 1:]

        for column in df.columns[1:]:
            try:
                head_name, hydra_name = column.split(" - ")
            except ValueError:
                print(f"[WARN] Skipping malformed column header: {column}")
                continue

            hydra = hydra_map.setdefault(hydra_name, Hydra(hydra_name, []))
            if hydra not in self.hydras:
                self.hydras.append(hydra)

            try:
                health = int(str(health_row[column]).replace(",", ""))
            except ValueError:
                print(f"[WARN] Invalid health value in column '{column}': {health_row[column]}")
                continue

            head = Head(head_name, hydra)
            head.startHealth = health
            head.health = health
            hydra.heads.append(head)

        # Save the order of target columns (exclude first column like 'Name')
        self.target_order = list(df.columns[1:])

        return True

    def initialize_random_assignment(self):
        assignment = {}
        for player in self.players:
            attacks = []
            for _ in range(3):
                valid_hydras = [h for h in self.hydras if h.is_alive() and any(head.is_alive() for head in h.heads)]
                if not valid_hydras:
                    break
                hydra = random.choice(valid_hydras)
                head = random.choice([head for head in hydra.heads if head.is_alive()])
                attacks.append((hydra.name, head.name))
            assignment[player.name] = attacks
        return assignment

    def reset_battle_state(self):
        for hydra in self.hydras:
            hydra.reset()
        for player in self.players:
            player.attacks_left = 3

    def mutate_assignment(self, assignment):
        new_assignment = {p: a[:] for p, a in assignment.items()}
        mutations = 2 if random.random() < 0.2 else 1

        retry_limit = 5
        for _ in range(mutations):
            retry_count = 0
            while retry_count < retry_limit:
                player_name = random.choice(self.players).name
                attack_idx = random.randint(0, 2)
                valid_hydras = [h for h in self.hydras if h.is_alive() and any(head.is_alive() for head in h.heads)]
                if not valid_hydras:
                    break
                hydra = random.choice(valid_hydras)
                valid_heads = [head for head in hydra.heads if head.is_alive()]
                if not valid_heads:
                    retry_count += 1
                    continue
                head = random.choice(valid_heads)

                if new_assignment[player_name][attack_idx] != (hydra.name, head.name):
                    new_assignment[player_name][attack_idx] = (hydra.name, head.name)
                    break
                else:
                    retry_count += 1
            # If retries exhausted, just skip this mutation

        return new_assignment

    def simulated_annealing(self, cycle, max_iter=20000, initial_temp=1000, cooling_rate=0.995):
        temperature = initial_temp
        best_score = 0
        no_improve_counter = 0
        patience = 5000

        self.reset_battle_state()
        assignment = self.initialize_random_assignment()
        current_score = cycle.apply_assignment(assignment)
        best_assignment = {p: a[:] for p, a in assignment.items()}

        for i in range(max_iter):
            if temperature < 1e-5:
                #print("[INFO] Temperature too low, stopping.")
                break

            if i > 0 and i % 2000 == 0:
                temperature = initial_temp  # reheat
                #print(f"[INFO] Reheating temperature at iteration {i}")

            self.reset_battle_state()
            new_assignment = self.mutate_assignment(assignment)
            new_score = cycle.apply_assignment(new_assignment)
            delta = new_score - current_score

            if delta > 0 or random.random() < math.exp(delta / temperature):
                assignment = new_assignment
                current_score = new_score

                if new_score > best_score:
                    best_score = new_score
                    best_assignment = {p: a[:] for p, a in new_assignment.items()}
                    no_improve_counter = 0
                    #print(f"[INFO] Iter {i} | New Best Score: {best_score} | Temp: {temperature:.4f}")
                else:
                    no_improve_counter += 1
            else:
                no_improve_counter += 1

            # Optional early stopping if stuck
            if no_improve_counter > patience:
                #print(f"[INFO] No improvement for {patience} iterations, stopping early.")
                break

            temperature *= cooling_rate

        return best_assignment, best_score

    def run_simulation(self):
        if not self.players or not self.hydras:
            print("[ERROR] Players or Hydras not initialized. Aborting simulation.")
            return None, None, None

        #print("[INFO] Starting simulation round...")
        cycle = Cycle(self.players, self.hydras)
        best_assignment, score = self.simulated_annealing(cycle)

        
        #print(f"[RESULT] Best assignment found | Total Score: {score}")
        #print("-" * 50)
        #print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")

        #for player, attacks in best_assignment.items():
        #    if player in ("raf41983", "Freya"):
        #        for hydra_name, head_name in attacks:
        #            print(f"{player:<25} {hydra_name:<15} {head_name:<15}")

        #print("-" * 50)
        return best_assignment, score

    def runBruteforce(self):
        if not self.players or not self.hydras:
            print("[ERROR] Players or Hydras not initialized. Aborting simulation.")
            return None, None, None

        print("[INFO] Starting brute force simulation round...")
        cycle = Cycle(self.players, self.hydras)
        raw_assignment, score = cycle.brute_force(max_attempts=10000)

        # Convert from attack_log list to expected dict format
        assignment_dict = {}
        for player_name, hydra_name, head_name, damage, worth in raw_assignment:
            assignment_dict.setdefault(player_name, []).append((hydra_name, head_name))

        return assignment_dict, score
    
    def print_assignment_summary(self, assignment, score):
        from collections import defaultdict

        summary = defaultdict(list)

        # Build summary dictionary
        for player in self.players:
            if player.name not in assignment:
                continue
            for hydra_name, head_name in assignment[player.name]:
                key = f"{head_name} - {hydra_name}"  # format must match CSV header exactly
                hydra = next((h for h in self.hydras if h.name == hydra_name), None)
                if not hydra:
                    continue
                head = next((hd for hd in hydra.heads if hd.name == head_name), None)
                if not head:
                    continue
                damage = player.DamageToHead(hydra, head)
                summary[key].append((player.name, damage))

        print("\n[DETAILED TARGET BREAKDOWN]")
        print("-" * 50)

        # Print by original CSV order
        for target in self.target_order:
            if target not in summary:
                continue
            print(f"\n{target}:")
            total = 0
            for player_name, damage in summary[target]:
                total += damage
                print(f"  {player_name:<20} {damage:>12,}")
            print(f"{'TOTAL':<22} {total:>12,}")

        print("-" * 50)

        # Count total heads killed (health <= 0)
        heads_killed = 0
        total_heads = 0
        for hydra in self.hydras:
            for head in hydra.heads:
                total_heads += 1
                if head.health <= 0:
                    heads_killed += 1

        # Print final summary
        print("\n[FINAL SUMMARY]")
        print(f"Total heads killed: {heads_killed} / {total_heads}")
        print(f"Total score: {score:,}")

import concurrent.futures

def run_single_simulation(csv_path):
    sim = HydraSimulator(csv_path)
    if not sim.load_data():
        return None, 0
    return sim.run_simulation()  # returns assignment, score

def run_parallel_simulations(csv_path, n_simulations=100, max_workers=os.cpu_count() - 1, print_every=10):
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_single_simulation, csv_path) for _ in range(n_simulations)]

        completed = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                assignment, score = future.result()
                if assignment is not None:
                    results.append((assignment, score))
            except Exception as e:
                print(f"[ERROR] Simulation failed: {e}")

            completed += 1
            # Print progress every `print_every` simulations or at the end
            if completed % print_every == 0 or completed == n_simulations:
                best_assignment, best_score = max(results, key=lambda x: x[1]) if results else (None, 0)
                print(f"\n[INFO] Completed {completed} / {n_simulations} simulations. Current best score: {best_score}")

    if not results:
        return None, 0

    best_assignment, best_score = max(results, key=lambda x: x[1])
    return best_assignment, best_score



   
        

if __name__ == "__main__":
    simulator = HydraSimulator(r'.\Hero Wars - Brasil - HydraHelperSheet.csv')
    input_string = input("press SA to start simulated annealing, P for Parallel runs, otherwise press any for brute force: ")
    

    if simulator.load_data():
        best_assignment = {}
        highest_score = 0

        if input_string == "SA":
            for i in range(1, 100):
                print(f"\n--- Running Simulation {i} ---")
                assignment, score = simulator.run_simulation()

                if score > highest_score:
                    best_assignment = assignment
                    highest_score = score

                print(f"[SUMMARY] Simulation {i} complete. Best So Far | Score: {highest_score}")
                print("-" * 60)

            print("\n[FINAL RESULT] Best assignment across all simulations:")
            print("-" * 50)
            print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")
            for player, attacks in best_assignment.items():
                for hydra_name, head_name in attacks:
                    print(f"{player:<25} {hydra_name:<15} {head_name:<15}")
            print("-" * 50)
            
        if input_string == "P":
            try:
                n_sim = int(input("Enter number of simulations to run: "))
            except ValueError:
                n_sim = 100  # default fallback
            print("[INFO] Running parallel simulations...")
            best_assignment, highest_score = run_parallel_simulations(simulator.csv_path, n_simulations=n_sim, max_workers=8)
            print(f"\n[FINAL RESULT] Best assignment from parallel runs with score: {highest_score}")
            print("-" * 50)
            print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")
            for player, attacks in best_assignment.items():
                for hydra_name, head_name in attacks:
                    print(f"{player:<25} {hydra_name:<15} {head_name:<15}")
            print("-" * 50)

        
            
        else:
            print("[INFO] Running brute force simulation...")
            best_assignment, score = simulator.runBruteforce()
            #print assignment
            print(f"[RESULT] Best assignment found | Total Score: {score}")
            print("-" * 50)
            for best in best_assignment:
                print(f"{best}")
            print("-" * 50)

        # For use in print_assignment_summary
        # Reset hydras and players so healths and attacks_left are fresh
        simulator.reset_battle_state()

        # Apply the best assignment to update heads' health properly
        cycle = Cycle(simulator.players, simulator.hydras)
        cycle.apply_assignment(best_assignment)

        # Now print the summary with correct health states
        simulator.print_assignment_summary(best_assignment, highest_score)
    
