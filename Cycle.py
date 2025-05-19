import random
import copy

class Cycle:
    def __init__(self, players, hydras):
        self.players = players
        self.hydras = hydras
        self.current_value = 0

        # Cache for quick lookup
        self.hydra_dict = {h.name: h for h in hydras}
        for hydra in hydras:
            hydra.head_dict = {head.name: head for head in hydra.heads}

    def apply_assignment(self, assignment):
        self.current_value = 0

        # Reset hydras and players
        for hydra in self.hydras:
            hydra.reset()
        for player in self.players:
            player.attacks_left = 3

        for player in self.players:
            attacks = assignment.get(player.name, [])
            for hydra_name, head_name in attacks:
                if player.attacks_left <= 0:
                    break

                hydra = self.hydra_dict.get(hydra_name)
                if not hydra:
                    continue

                head = hydra.head_dict.get(head_name)
                if not head or head.health <= 0:
                    continue

                damage = player.DamageToHead(hydra, head)
                if damage <= 0:
                    continue

                actual_damage = min(damage, head.health)
                head.health -= actual_damage
                player.attacks_left -= 1

                if head.health <= 0:
                    head.health = 0
                    self.current_value += head.worth
                    hydra.on_head_killed()

        return self.current_value

    def brute_force(self, max_attempts=10000):
        best_assignment = None
        best_value = 0

        for attempt in range(max_attempts):
            # Clone all hydras and reset state
            hydras = [copy.deepcopy(hydra) for hydra in self.hydras]
            players = [copy.deepcopy(player) for player in self.players]
            
            # Shuffle initial state
            random.shuffle(players)
            random.shuffle(hydras)
            for hydra in hydras:
                random.shuffle(hydra.heads)

            total_value = 0
            attack_log = []

            for player in players:
                for _ in range(3):  # 3 attacks per player
                    # Get all alive heads across all hydras
                    possible_targets = [
                        (hydra, head)
                        for hydra in hydras
                        for head in hydra.heads
                        if head.is_alive()
                    ]
                    if not possible_targets:
                        break

                    # Shuffle targets for extra randomness before picking the first
                    random.shuffle(possible_targets)
                    hydra, head = possible_targets[0]

                    damage = player.DamageToHead(hydra, head)
                    damage = damage if damage else 0

                    head.health -= damage
                    if head.health <= 0 and head.alive:
                        head.alive = False
                        hydra.on_head_killed()
                        total_value += head.worth

                    attack_log.append((player.name, hydra.name, head.name, damage, head.worth))

            if total_value > best_value:
                best_value = total_value
                best_assignment = attack_log

        return best_assignment, best_value
