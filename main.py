import pandas as pd
import random
import math

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
        mutations = 2 if random.random() < 0.1 else 1

        for _ in range(mutations):
            player_name = random.choice(self.players).name
            attack_idx = random.randint(0, 2)
            valid_hydras = [h for h in self.hydras if h.is_alive() and any(head.is_alive() for head in h.heads)]
            if not valid_hydras:
                break
            hydra = random.choice(valid_hydras)
            valid_heads = [head for head in hydra.heads if head.is_alive()]
            if not valid_heads:
                continue
            head = random.choice(valid_heads)
            new_assignment[player_name][attack_idx] = (hydra.name, head.name)

        return new_assignment

    def simulated_annealing(self, cycle, max_iter=10000, initial_temp=1000, cooling_rate=0.995):
        temperature = initial_temp
        best_score = 0

        self.reset_battle_state()
        assignment = self.initialize_random_assignment()

        health_left, current_score = cycle.apply_assignment(assignment)
        best_assignment = {p: a[:] for p, a in assignment.items()}

        for i in range(max_iter):
            if temperature < 1:
                break
            if i > 0 and i % 10000 == 0:
                temperature = initial_temp  # reheat

            self.reset_battle_state()
            new_assignment = self.mutate_assignment(assignment)
            new_health_left, new_score = cycle.apply_assignment(new_assignment)
            delta = health_left - new_health_left

            if delta > 0 or random.random() < math.exp(delta / temperature):
                assignment = new_assignment
                health_left = new_health_left

                if new_score > best_score:
                    best_score = new_score
                    best_assignment = {p: a[:] for p, a in new_assignment.items()}
                    print(f"[INFO] Iter {i} | New Best Score: {best_score} | Remaining Health: {health_left} | Temp: {temperature:.2f}")
                elif new_health_left < health_left:
                    print(f"[DEBUG] Iter {i} | Improved Health Left: {new_health_left} | Score: {new_score} | Temp: {temperature:.2f}")

            temperature *= cooling_rate

        return best_assignment, health_left, best_score

    def run_simulation(self):
        if not self.players or not self.hydras:
            print("[ERROR] Players or Hydras not initialized. Aborting simulation.")
            return None, None, None

        print("[INFO] Starting simulation round...")
        cycle = Cycle(self.players, self.hydras)
        best_assignment, health_left, score = self.simulated_annealing(cycle)

        print(f"[RESULT] Best assignment found | Remaining Hydra Health: {health_left} | Total Score: {score}")
        print("-" * 50)
        print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")

        for player, attacks in best_assignment.items():
            if player in ("raf41983", "Freya"):
                for hydra_name, head_name in attacks:
                    print(f"{player:<25} {hydra_name:<15} {head_name:<15}")

        print("-" * 50)
        return best_assignment, health_left, score


if __name__ == "__main__":
    simulator = HydraSimulator(r'.\Hero Wars - Brasil - HydraHelperSheet.csv')

    if simulator.load_data():
        best_assignment = {}
        best_health_left = float('inf')
        highest_score = 0

        for i in range(1, 25):
            print(f"\n--- Running Simulation {i} ---")
            assignment, health_left, score = simulator.run_simulation()

            if score > highest_score:
                best_assignment = assignment
                best_health_left = health_left
                highest_score = score

            print(f"[SUMMARY] Simulation {i} complete. Best So Far | Health Left: {best_health_left} | Score: {highest_score}")
            print("-" * 60)

        print("\n[FINAL RESULT] Best assignment across all simulations:")
        print("-" * 50)
        print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")
        for player, attacks in best_assignment.items():
            for hydra_name, head_name in attacks:
                print(f"{player:<25} {hydra_name:<15} {head_name:<15}")
        print("-" * 50)
