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

    def read_file_csv(self):
        try:
            df = pd.read_csv(self.csv_path, sep=',', engine='python')
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    def load_data(self):
        DamageMatrix = self.read_file_csv()
        if DamageMatrix is None:
            return False
        
        self.players = []
        for index, row in DamageMatrix.iterrows():
            if index == DamageMatrix.shape[0] - 1:
                continue  # skip last row (heads health)
            damage_data = DamageMatrix.iloc[index, 1:].to_frame().T
            damage_data.columns = DamageMatrix.columns[1:]
            player = Player(row['Name'], damage_data)
            self.players.append(player)

        self.hydras = []
        hydra_dict = {}
        bottom_row = DamageMatrix.iloc[-1, 1:]

        for column in DamageMatrix.columns[1:]:
            try:
                head_name, hydra_name = column.split(" - ")
            except ValueError:
                print(f"Skipping malformed column header: {column}")
                continue

            if hydra_name == "Dreadful":
                continue  # skip Dreadful hydras

            if hydra_name not in hydra_dict:
                hydra = Hydra(hydra_name, [])
                hydra_dict[hydra_name] = hydra
                self.hydras.append(hydra)
            else:
                hydra = hydra_dict[hydra_name]

            health_str = bottom_row[column]
            try:
                health_val = int(str(health_str).replace(",", ""))
            except ValueError:
                print(f"Invalid health value for {column}: {health_str}")
                continue

            head = Head(head_name, hydra)
            head.startHealth = health_val
            head.health = health_val
            hydra.heads.append(head)

        return True

    def simulated_annealing(self, cycle, max_iter=100000, initial_temp=1000, cooling_rate=0.995):
        temperature = initial_temp
        highest_value = 0

        # Reset hydras and players
        for hydra in self.hydras:
            hydra.reset()
        for player in self.players:
            player.attacks_left = 3

        # Initialize random assignment
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

        current_score, current_value = cycle.apply_assignment(assignment)
        best_assignment = {p: a[:] for p, a in assignment.items()}
        hydras_health_left = current_score

        for i in range(max_iter):
            if temperature < 1:
                break

            # Reheat every 10,000 iterations
            if i > 0 and i % 10000 == 0:
                temperature = initial_temp

            # Reset hydras and players before applying new assignment
            for hydra in self.hydras:
                hydra.reset()
            for player in self.players:
                player.attacks_left = 3

            new_assignment = {p: a[:] for p, a in assignment.items()}

            # 10% chance mutate 2 attacks, else 1
            mutations = 2 if random.random() < 0.1 else 1
            for _ in range(mutations):
                player_name = random.choice(self.players).name
                attack_idx = random.randint(0, 2)
                valid_hydras = [h for h in self.hydras if h.is_alive() and any(head.is_alive() for head in h.heads)]
                if not valid_hydras:
                    print("No valid hydras with alive heads!")
                    break
                hydra = random.choice(valid_hydras)
                valid_heads = [head for head in hydra.heads if head.is_alive()]
                if not valid_heads:
                    continue
                head = random.choice(valid_heads)
                new_assignment[player_name][attack_idx] = (hydra.name, head.name)

            new_total_health_left, current_value = cycle.apply_assignment(new_assignment)
            delta = current_score - new_total_health_left

            if delta > 0 or random.random() < math.exp(delta / temperature):
                assignment = new_assignment
                current_score = new_total_health_left

                if current_value > highest_value:
                    highest_value = current_value
                    hydras_health_left = new_total_health_left
                    best_assignment = {p: a[:] for p, a in new_assignment.items()}
                    print(f"Iteration {i} | Hydras health left: {hydras_health_left} | Current Value: {current_value} | Highest: {highest_value} | Temp: {temperature:.2f}")
                else:
                    if new_total_health_left < hydras_health_left:
                        print(f"Iteration {i} | Score: {new_total_health_left} | Current Value: {current_value} | Highest: {highest_value} | Temp: {temperature:.2f}")

            temperature *= cooling_rate

        return best_assignment, hydras_health_left, highest_value

    def run_simulation(self):
        if not self.players or not self.hydras:
            print("Players or Hydras data missing, cannot simulate.")
            return

        print("Starting simulation...")
        cycle = Cycle(self.players, self.hydras)
        best_assignment, best_score, highest_value = self.simulated_annealing(cycle)

        print(f"Best total health left found: {best_score} | Current Value: {highest_value}")
        print("Sample from best assignment:")
        print("-" * 50)
        print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")

        for player, attack_list in best_assignment.items():
            for hydra_name, head_name in attack_list:
                # Only print for these two players as in original
                if player == "raf41983" or player == "Freya":
                    print(f"{player:<25} {hydra_name:<15} {head_name:<15}")
                else:
                    break
        print("-" * 50)

        return best_assignment, best_score, highest_value


if __name__ == "__main__":
    simulator = HydraSimulator(r'.\Hero Wars - Brasil - HydraHelperSheet.csv')
    if simulator.load_data():
        best_assignment = {}
        best_score = 0
        highest_value = 0
        for i in range(1, 25):
            hold, health_left, score = simulator.run_simulation()
            if(score > highest_value):
                best_assignment = hold
                best_score = health_left
                highest_value = score

            print(f"Simulation {i} completed.")
            print("-" * 50)
            print(f"top scores amongts 10 randomly seeded simulations total health left of hydras: {best_score} | Current Value: {highest_value}")
            print("-" * 50)

        print("Best assignment across all simulations:")
        print("-" * 50)
        print(f"{'Player':<25} {'Hydra':<15} {'Head':<15}")
        for player, attack_list in best_assignment.items():
            for hydra_name, head_name in attack_list:
                # Only print for these two players as in original
                print(f"{player:<25} {hydra_name:<15} {head_name:<15}")
                
            



